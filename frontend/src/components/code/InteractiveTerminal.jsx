import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Square, RotateCw, Trash2, X, ArrowUp, AlertCircle, CheckCircle2 } from 'lucide-react';
import { getInteractiveRunWsUrl } from '../../services/api';

/**
 * InteractiveTerminal
 * Live bidirectional execution terminal for Bhasha2Code sandbox programs.
 * Connects directly via WebSocket to /api/v1/code/interactive-run.
 * Streams stdout/stderr as generated, displays prompts without newlines,
 * accepts user keyboard input in real-time, and supports clean termination.
 */
export default function InteractiveTerminal({
  language = 'python',
  code = '',
  isStale = false,
  onClose = null,
  onStatusChange = null,
  onValidationFailure = null,
  autoStart = true,
}) {
  const [entries, setEntries] = useState([]);
  const [status, setStatus] = useState('IDLE'); // IDLE, STARTING, RUNNING, WAITING_FOR_INPUT, COMPLETED, RUNTIME_ERROR, TIMEOUT, RESOURCE_LIMIT, VALIDATION_FAILED, CANCELLED
  const [exitCode, setExitCode] = useState(null);
  const [durationMs, setDurationMs] = useState(0);
  const [diagnostics, setDiagnostics] = useState([]);
  const [inputText, setInputText] = useState('');
  const [history, setHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);

  const wsRef = useRef(null);
  const sessionIdRef = useRef(0);
  const terminalEndRef = useRef(null);
  const screenRef = useRef(null);
  const inputRef = useRef(null);
  const codeRef = useRef(code);
  codeRef.current = code;

  const updateStatus = (newStatus) => {
    setStatus(newStatus);
    if (onStatusChange) {
      onStatusChange(newStatus);
    }
  };

  const startSession = () => {
    // Invalidate and aggressively detach any existing socket
    const currentSessionId = ++sessionIdRef.current;
    if (wsRef.current) {
      const oldWs = wsRef.current;
      oldWs.onopen = null;
      oldWs.onmessage = null;
      oldWs.onerror = null;
      oldWs.onclose = null;
      try {
        if (oldWs.readyState === WebSocket.OPEN) {
          oldWs.send(JSON.stringify({ type: 'terminate' }));
        }
        oldWs.close();
      } catch {}
      wsRef.current = null;
    }

    setEntries([]);
    setDiagnostics([]);
    setExitCode(null);
    setDurationMs(0);
    updateStatus('STARTING');

    const wsUrl = getInteractiveRunWsUrl();
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      // Abort if another session was started or component unmounted
      if (sessionIdRef.current !== currentSessionId) {
        try {
          ws.close();
        } catch {}
        return;
      }
      // Send initial start handshake with current code
      ws.send(
        JSON.stringify({
          type: 'start',
          language,
          code: codeRef.current,
        })
      );
    };

    ws.onmessage = (event) => {
      // Ignore messages from obsolete sessions
      if (sessionIdRef.current !== currentSessionId) {
        try {
          ws.close();
        } catch {}
        return;
      }

      try {
        const msg = JSON.parse(event.data);
        const { type } = msg;

        if (type === 'started') {
          updateStatus('RUNNING');
          // Focus input box immediately
          setTimeout(() => inputRef.current?.focus(), 50);
        } else if (type === 'stdout') {
          setEntries((prev) => {
            // Guard: deduplicate if identical initial prompt is received consecutively before input
            if (
              prev.length === 1 &&
              prev[0].type === 'stdout' &&
              prev[0].text === msg.data
            ) {
              return prev;
            }
            return [...prev, { type: 'stdout', text: msg.data }];
          });
          updateStatus('RUNNING');
        } else if (type === 'stderr') {
          setEntries((prev) => [...prev, { type: 'stderr', text: msg.data }]);
        } else if (type === 'completed') {
          const codeVal = msg.exit_code ?? 0;
          setExitCode(codeVal);
          setDurationMs(msg.duration_ms ?? 0);
          updateStatus(codeVal === 0 ? 'COMPLETED' : 'RUNTIME_ERROR');
          setEntries((prev) => {
            const hasStdout = prev.some((e) => e.type === 'stdout' && e.text && e.text.trim().length > 0);
            const notice = codeVal === 0 && !hasStdout
              ? `\nProcess completed · Exit code ${codeVal}\n(Note: No stdout or test assertions were executed. Defining functions without calling them produces no output and does not run tests.)`
              : `\nProcess completed · Exit code ${codeVal}`;
            return [
              ...prev,
              {
                type: 'system',
                text: notice,
                success: codeVal === 0,
              },
            ];
          });
        } else if (type === 'error') {
          const errType = msg.error_type || 'SANDBOX_ERROR';
          const errMsg = msg.message || 'Execution error';
          if (errType === 'VALIDATION_FAILED') {
            updateStatus('VALIDATION_FAILED');
            const diags = msg.diagnostics || [errMsg];
            setDiagnostics(diags);
            if (onValidationFailure) {
              onValidationFailure(diags);
            }
          } else {
            updateStatus('RUNTIME_ERROR');
          }
          setEntries((prev) => [
            ...prev,
            {
              type: 'system',
              text: `\n[Error]: ${errMsg}` + (msg.diagnostics ? `\n${msg.diagnostics.join('\n')}` : ''),
              success: false,
            },
          ]);
        } else if (type === 'timeout') {
          updateStatus('TIMEOUT');
          setEntries((prev) => [
            ...prev,
            { type: 'system', text: `\n[Timeout]: ${msg.message || 'Execution timed out.'}`, success: false },
          ]);
        } else if (type === 'resource_limit') {
          updateStatus('RESOURCE_LIMIT');
          setEntries((prev) => [
            ...prev,
            { type: 'system', text: `\n[Resource Limit]: ${msg.message || 'Resource limit exceeded.'}`, success: false },
          ]);
        }
      } catch (err) {
        console.error('Error parsing WebSocket message:', err);
      }
    };

    ws.onerror = (err) => {
      if (sessionIdRef.current !== currentSessionId) return;
      console.warn('Interactive terminal WebSocket error:', err);
      updateStatus('SANDBOX_ERROR');
      setEntries((prev) => [
        ...prev,
        { type: 'system', text: '\nFailed to connect to execution terminal service.', success: false },
      ]);
    };

    ws.onclose = () => {
      if (sessionIdRef.current !== currentSessionId) return;
      // If closed while running without explicit status
      setStatus((cur) => {
        if (cur === 'RUNNING' || cur === 'STARTING') {
          return 'COMPLETED';
        }
        return cur;
      });
    };
  };

  useEffect(() => {
    if (autoStart) {
      startSession();
    }
    return () => {
      // Invalidate session on unmount
      sessionIdRef.current += 1;
      if (wsRef.current) {
        const s = wsRef.current;
        s.onopen = null;
        s.onmessage = null;
        s.onerror = null;
        s.onclose = null;
        try {
          if (s.readyState === WebSocket.OPEN) {
            s.send(JSON.stringify({ type: 'terminate' }));
          }
          s.close();
        } catch {}
        wsRef.current = null;
      }
    };
  }, []);

  // Auto-scroll terminal when entries change
  useEffect(() => {
    if (screenRef.current) {
      screenRef.current.scrollTop = screenRef.current.scrollHeight;
    } else {
      terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [entries]);

  // Handle Stop / Terminate
  const handleStop = () => {
    if (wsRef.current && (status === 'RUNNING' || status === 'STARTING')) {
      try {
        wsRef.current.send(JSON.stringify({ type: 'terminate' }));
      } catch {}
      updateStatus('CANCELLED');
      setEntries((prev) => [
        ...prev,
        { type: 'system', text: '\nProcess terminated by user.', success: false },
      ]);
    }
  };

  // Submit stdin
  const handleSendInput = (e) => {
    if (e) e.preventDefault();
    if (!inputText.trim() && inputText !== '') {
      // allow empty enter
    }
    const submitted = inputText;
    if (wsRef.current && (status === 'RUNNING' || status === 'STARTING')) {
      // Display entered line in the terminal feed
      setEntries((prev) => [...prev, { type: 'stdin', text: submitted + '\n' }]);
      try {
        wsRef.current.send(JSON.stringify({ type: 'stdin', data: submitted + '\n' }));
      } catch (err) {
        console.warn('Failed to send stdin:', err);
      }
      setHistory((prev) => [...prev, submitted]);
      setHistoryIndex(-1);
      setInputText('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSendInput();
    } else if (e.key === 'ArrowUp') {
      if (history.length > 0) {
        e.preventDefault();
        const nextIdx = historyIndex === -1 ? history.length - 1 : Math.max(0, historyIndex - 1);
        setHistoryIndex(nextIdx);
        setInputText(history[nextIdx]);
      }
    } else if (e.key === 'ArrowDown') {
      if (historyIndex !== -1) {
        e.preventDefault();
        const nextIdx = historyIndex + 1;
        if (nextIdx >= history.length) {
          setHistoryIndex(-1);
          setInputText('');
        } else {
          setHistoryIndex(nextIdx);
          setInputText(history[nextIdx]);
        }
      }
    }
  };

  const isExecutionActive = status === 'RUNNING' || status === 'STARTING';

  const getStatusBadge = () => {
    switch (status) {
      case 'STARTING':
        return { label: 'Starting...', color: '#60a5fa', bg: 'rgba(59, 130, 246, 0.15)', border: '#2563eb' };
      case 'RUNNING':
        return { label: 'Running', color: '#34d399', bg: 'rgba(16, 185, 129, 0.15)', border: '#059669', pulse: true };
      case 'WAITING_FOR_INPUT':
        return { label: 'Waiting for Input', color: '#fbbf24', bg: 'rgba(245, 158, 11, 0.15)', border: '#d97706' };
      case 'COMPLETED':
        return { label: `Completed · ${durationMs}ms`, color: '#34d399', bg: 'rgba(16, 185, 129, 0.12)', border: '#059669' };
      case 'RUNTIME_ERROR':
        return { label: `Exit Code ${exitCode ?? 1}`, color: '#f87171', bg: 'rgba(239, 68, 68, 0.15)', border: '#dc2626' };
      case 'VALIDATION_FAILED':
        return { label: 'Validation Failed', color: '#f87171', bg: 'rgba(239, 68, 68, 0.15)', border: '#dc2626' };
      case 'TIMEOUT':
        return { label: 'Timed Out', color: '#fb923c', bg: 'rgba(249, 115, 22, 0.15)', border: '#ea580c' };
      case 'RESOURCE_LIMIT':
        return { label: 'Resource Limit', color: '#f87171', bg: 'rgba(239, 68, 68, 0.15)', border: '#dc2626' };
      case 'CANCELLED':
        return { label: 'Terminated', color: '#94a3b8', bg: 'rgba(148, 163, 184, 0.15)', border: '#64748b' };
      default:
        return { label: 'Idle', color: '#94a3b8', bg: 'rgba(148, 163, 184, 0.1)', border: '#475569' };
    }
  };

  const badge = getStatusBadge();

  return (
    <div
      data-testid="interactive-terminal"
      style={{
        borderTop: '1px solid var(--border-code)',
        backgroundColor: '#090d16',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Terminal Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '6px 12px',
          backgroundColor: '#0d131f',
          borderBottom: '1px solid #1e293b',
          fontSize: '0.72rem',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px', color: '#94a3b8', fontWeight: 600 }}>
            <Terminal size={13} color="#38bdf8" />
            <span>Terminal</span>
          </div>

          {/* Stale Badge */}
          {isStale && (
            <span
              style={{
                fontSize: '0.65rem',
                color: '#fbbf24',
                backgroundColor: 'rgba(245, 158, 11, 0.15)',
                border: '1px solid #d97706',
                padding: '1px 5px',
                borderRadius: 'var(--radius-xs)',
              }}
            >
              stale
            </span>
          )}

          {/* Status Badge */}
          <span
            data-testid="terminal-status-badge"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              color: badge.color,
              backgroundColor: badge.bg,
              border: `1px solid ${badge.border}`,
              padding: '1px 6px',
              borderRadius: 'var(--radius-xs)',
              fontSize: '0.65rem',
              fontWeight: 600,
            }}
          >
            {badge.pulse && (
              <span
                style={{
                  width: '5px',
                  height: '5px',
                  borderRadius: '50%',
                  backgroundColor: badge.color,
                  display: 'inline-block',
                }}
              />
            )}
            {badge.label}
          </span>
        </div>

        {/* Action Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
          {isExecutionActive ? (
            <button
              type="button"
              data-testid="terminal-stop"
              onClick={handleStop}
              title="Stop Execution"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
                padding: '2px 7px',
                backgroundColor: '#7f1d1d',
                border: '1px solid #ef4444',
                borderRadius: 'var(--radius-xs)',
                color: '#fecaca',
                fontSize: '0.68rem',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              <Square size={10} fill="#fecaca" />
              <span>Stop</span>
            </button>
          ) : (
            <button
              type="button"
              data-testid="terminal-rerun"
              onClick={startSession}
              title="Re-run in Terminal"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
                padding: '2px 7px',
                backgroundColor: '#1e293b',
                border: '1px solid #334155',
                borderRadius: 'var(--radius-xs)',
                color: '#93c5fd',
                fontSize: '0.68rem',
                fontWeight: 500,
                cursor: 'pointer',
              }}
            >
              <RotateCw size={10} />
              <span>Re-run</span>
            </button>
          )}

          <button
            type="button"
            onClick={() => setEntries([])}
            title="Clear Terminal Output"
            style={{
              padding: '2px 6px',
              backgroundColor: 'transparent',
              border: 'none',
              color: '#64748b',
              cursor: 'pointer',
              borderRadius: 'var(--radius-xs)',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.color = '#cbd5e1')}
            onMouseLeave={(e) => (e.currentTarget.style.color = '#64748b')}
          >
            <Trash2 size={11} />
          </button>

          {onClose && (
            <button
              type="button"
              onClick={onClose}
              title="Close Terminal"
              style={{
                padding: '2px 6px',
                backgroundColor: 'transparent',
                border: 'none',
                color: '#64748b',
                cursor: 'pointer',
                borderRadius: 'var(--radius-xs)',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.color = '#cbd5e1')}
              onMouseLeave={(e) => (e.currentTarget.style.color = '#64748b')}
            >
              <X size={12} />
            </button>
          )}
        </div>
      </div>

      {/* Terminal Screen / Output Body */}
      <div
        ref={screenRef}
        data-testid="terminal-screen"
        style={{
          padding: '10px 14px',
          minHeight: '120px',
          maxHeight: '260px',
          overflowY: 'auto',
          fontFamily: 'var(--font-mono)',
          fontSize: 'var(--text-xs)',
          lineHeight: '1.45',
          color: '#f1f5f9',
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
        }}
      >
        {status === 'STARTING' && entries.length === 0 && (
          <div style={{ color: '#64748b', fontStyle: 'italic' }}>
            Starting sandbox container...
          </div>
        )}

        {diagnostics.length > 0 && (
          <div style={{ marginBottom: '8px', color: '#f87171' }}>
            {diagnostics.map((diag, i) => (
              <div key={i}>{diag}</div>
            ))}
          </div>
        )}

        {entries.map((entry, idx) => {
          if (entry.type === 'stdout') {
            return (
              <span key={idx} style={{ color: '#f1f5f9' }}>
                {entry.text}
              </span>
            );
          }
          if (entry.type === 'stderr') {
            return (
              <span key={idx} style={{ color: '#f87171' }}>
                {entry.text}
              </span>
            );
          }
          if (entry.type === 'stdin') {
            return (
              <span key={idx} style={{ color: '#38bdf8', fontWeight: 600 }}>
                {entry.text}
              </span>
            );
          }
          if (entry.type === 'system') {
            return (
              <div
                key={idx}
                style={{
                  color: entry.success ? '#34d399' : '#94a3b8',
                  fontSize: '0.70rem',
                  marginTop: '4px',
                  fontWeight: 600,
                }}
              >
                {entry.text}
              </div>
            );
          }
          return null;
        })}
        <div ref={terminalEndRef} />
      </div>

      {/* Live Terminal Input Bar */}
      {isExecutionActive && (
        <form
          onSubmit={handleSendInput}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '6px 12px',
            backgroundColor: '#0a0f1a',
            borderTop: '1px solid #1e293b',
          }}
        >
          <span style={{ color: '#38bdf8', fontFamily: 'var(--font-mono)', fontWeight: 700, fontSize: '0.80rem' }}>
            &gt;
          </span>
          <input
            ref={inputRef}
            data-testid="terminal-input"
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type input and press Enter..."
            style={{
              flex: 1,
              backgroundColor: 'transparent',
              border: 'none',
              outline: 'none',
              color: '#f8fafc',
              fontFamily: 'var(--font-mono)',
              fontSize: 'var(--text-xs)',
            }}
          />
          <button
            type="submit"
            data-testid="terminal-submit"
            title="Submit Input (Enter)"
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '24px',
              height: '24px',
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: 'var(--radius-xs)',
              color: '#93c5fd',
              cursor: 'pointer',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#334155')}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#1e293b')}
          >
            <ArrowUp size={12} />
          </button>
        </form>
      )}
    </div>
  );
}
