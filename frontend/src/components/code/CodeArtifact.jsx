import React, { useState, useEffect, useRef } from 'react';
import CodeToolbar from './CodeToolbar';
import ValidationStatus from './ValidationStatus';
import ExecutionResult from '../response/ExecutionResult';
import { Terminal, AlertCircle, ChevronDown, ChevronRight } from 'lucide-react';
import { validateCode, runCode } from '../../services/api';

/**
 * Parse structured diagnostic message into line, column, severity, and text.
 */
function parseDiagnostic(diag) {
  if (typeof diag !== 'string') return { text: String(diag), line: null, col: null, severity: 'ERROR' };
  const lineColMatch = diag.match(/\(line\s+(\d+)(?:,\s*col(?:umn)?\s*(\d+))?\)/i);
  const line = lineColMatch ? lineColMatch[1] : null;
  const col = lineColMatch && lineColMatch[2] ? lineColMatch[2] : null;
  const sevMatch = diag.match(/^\[(ERROR|WARNING|INFO)\]/i);
  const severity = sevMatch ? sevMatch[1].toUpperCase() : 'ERROR';
  const cleanMsg = diag.replace(/^\[(ERROR|WARNING|INFO)\]\s*/i, '').replace(/\(line\s+\d+.*?\)/i, '').trim();
  return { text: cleanMsg || diag, line, col, severity };
}

/**
 * CodeArtifact
 * The primary code display, inline editor, validation, and sandbox runner workspace component.
 * Features T24:
 * - Current editor content as source of truth
 * - Monotonic code revision tracking
 * - Debounced (750ms) real-time syntax validation
 * - Stale-result protection & revision-matched diagnostics
 * - Safe Run action gated by T18 validation
 * - Standard input (stdin) support
 * - Tab / Shift-Tab indentation in editor
 */
export default function CodeArtifact({
  initialCode = '',
  filename = 'solution.py',
  language = 'python',
  initialValidation = 'VALID',
  initialExecution = null,
  initialOutput = '',
  durationMs = 0,
  onCodeChange = null,
}) {
  const [code, setCode] = useState(initialCode);
  const [draftCode, setDraftCode] = useState(initialCode);
  const [isEditing, setIsEditing] = useState(false);
  const [isValidating, setIsValidating] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [showConsole, setShowConsole] = useState(Boolean(initialOutput || initialExecution));

  // Stdin state
  const [stdin, setStdin] = useState('');
  const [showStdin, setShowStdin] = useState(false);

  // Diagnostic expansion
  const [showDiagnostics, setShowDiagnostics] = useState(true);

  // Monotonic Revision Tracking
  const revisionRef = useRef(1);
  const validatedRevisionRef = useRef(initialValidation === 'VALID' ? 1 : 0);
  const validatedCodeRef = useRef(initialCode);
  const executedRevisionRef = useRef(initialExecution ? 1 : null);
  const executedCodeRef = useRef(initialExecution ? initialCode : null);

  const [validationStatus, setValidationStatus] = useState(initialValidation);
  const [validationDiagnostics, setValidationDiagnostics] = useState([]);
  const [executionResult, setExecutionResult] = useState(
    initialOutput || initialExecution
      ? {
          status: initialExecution || 'SUCCESS',
          stdout: initialOutput || '',
          stderr: '',
          exitCode: 0,
          durationMs: durationMs,
          diagnostics: [],
          isStale: false,
        }
      : null
  );

  // Timers and cancellation
  const debounceTimerRef = useRef(null);
  const abortControllerRef = useRef(null);
  const textareaRef = useRef(null);

  // Synchronize when initialCode prop updates from upstream
  useEffect(() => {
    setCode(initialCode);
    setDraftCode(initialCode);
    revisionRef.current += 1;
    validatedRevisionRef.current = initialValidation === 'VALID' ? revisionRef.current : 0;
    validatedCodeRef.current = initialCode;
    setValidationStatus(initialValidation);
    setValidationDiagnostics([]);
    if (initialOutput || initialExecution) {
      setExecutionResult({
        status: initialExecution || 'SUCCESS',
        stdout: initialOutput || '',
        stderr: '',
        exitCode: 0,
        durationMs: durationMs,
        diagnostics: [],
        isStale: false,
      });
    }
  }, [initialCode, initialValidation]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
      if (abortControllerRef.current) abortControllerRef.current.abort();
    };
  }, []);

  const activeContent = isEditing ? draftCode : code;
  const lines = activeContent.split('\n');

  // Core validation function tied to target revision
  const triggerValidation = async (codeToValidate, targetRevision) => {
    if (!codeToValidate || !codeToValidate.trim()) {
      if (revisionRef.current === targetRevision) {
        setValidationStatus('NOT_VALIDATED');
        setValidationDiagnostics([]);
      }
      return;
    }

    setIsValidating(true);
    setValidationStatus('VALIDATING');

    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      const res = await validateCode({
        language,
        code: codeToValidate,
        signal: controller.signal,
      });

      // Stale-result protection: apply only if targetRevision matches the current revision
      if (revisionRef.current === targetRevision) {
        setIsValidating(false);
        const resolvedStatus = res.is_valid ? 'VALID' : (res.status || 'INVALID');
        setValidationStatus(resolvedStatus);
        setValidationDiagnostics(res.diagnostics || []);
        validatedRevisionRef.current = targetRevision;
        validatedCodeRef.current = codeToValidate;
      }
    } catch (err) {
      if (err.name === 'AbortError') return;
      if (revisionRef.current === targetRevision) {
        setIsValidating(false);
        setValidationStatus('ERROR');
        setValidationDiagnostics([err.message || 'Validation request failed.']);
      }
    }
  };

  // Handle code editing with debounced syntax validation
  const handleDraftChange = (newVal) => {
    setDraftCode(newVal);
    revisionRef.current += 1;
    const newRev = revisionRef.current;

    // Immediately mark validation as NOT_VALIDATED
    setValidationStatus('NOT_VALIDATED');
    setValidationDiagnostics([]);

    // Mark previous execution as stale
    setExecutionResult((prev) => (prev ? { ...prev, isStale: true } : null));

    // Reset debounce timer
    if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }

    // Schedule fresh debounced validation (750ms)
    debounceTimerRef.current = setTimeout(() => {
      triggerValidation(newVal, newRev);
    }, 750);
  };

  // Keyboard controls in textarea: Tab indentation, Enter shortcuts
  const handleKeyDown = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const target = e.target;
      const start = target.selectionStart;
      const end = target.selectionEnd;

      if (e.shiftKey) {
        // Shift+Tab: Unindent
        const before = draftCode.substring(0, start);
        if (before.endsWith('    ')) {
          const updated = draftCode.substring(0, start - 4) + draftCode.substring(start);
          handleDraftChange(updated);
          setTimeout(() => {
            target.selectionStart = target.selectionEnd = Math.max(0, start - 4);
          }, 0);
        }
      } else {
        // Tab: Insert 4 spaces
        const updated = draftCode.substring(0, start) + '    ' + draftCode.substring(end);
        handleDraftChange(updated);
        setTimeout(() => {
          target.selectionStart = target.selectionEnd = start + 4;
        }, 0);
      }
    } else if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleRun();
    } else if ((e.ctrlKey || e.metaKey) && e.key === 's') {
      e.preventDefault();
      handleSave();
    } else if (e.key === 'Escape') {
      handleCancel();
    }
  };

  const handleCopy = () => {
    navigator.clipboard?.writeText(activeContent);
  };

  const handleStartEdit = () => {
    setDraftCode(code);
    setIsEditing(true);
  };

  const handleSave = () => {
    setCode(draftCode);
    setIsEditing(false);
    if (onCodeChange) {
      onCodeChange(draftCode);
    }
    // If draft was not validated yet, trigger validation now
    if (validationStatus === 'NOT_VALIDATED' || validatedCodeRef.current !== draftCode) {
      triggerValidation(draftCode, revisionRef.current);
    }
  };

  const handleCancel = () => {
    setDraftCode(code);
    setIsEditing(false);
    if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    // Revert revision and trigger validation on restored saved code
    revisionRef.current += 1;
    triggerValidation(code, revisionRef.current);
  };

  // Explicit Validate Action
  const handleExplicitValidate = () => {
    if (isValidating) return;
    if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
    triggerValidation(activeContent, revisionRef.current);
  };

  // Run Action
  const handleRun = async () => {
    if (isRunning) return;

    // Check if the current revision was already validated and found INVALID
    if (validationStatus === 'INVALID' && validatedRevisionRef.current === revisionRef.current) {
      setShowConsole(true);
      setExecutionResult({
        status: 'VALIDATION_FAILED',
        stdout: '',
        stderr: '',
        exitCode: 1,
        durationMs: 0,
        diagnostics: validationDiagnostics.length > 0
          ? validationDiagnostics
          : ['Cannot execute: Code contains syntax or compilation errors.'],
        isStale: false,
      });
      return;
    }

    setIsRunning(true);
    setShowConsole(true);
    const runRev = revisionRef.current;
    const runCodeContent = activeContent;

    setExecutionResult({
      status: 'RUNNING',
      stdout: 'Running secure sandbox...',
      stderr: '',
      exitCode: 0,
      durationMs: 0,
      diagnostics: [],
      isStale: false,
    });

    try {
      const res = await runCode({
        language,
        code: runCodeContent,
        stdin: stdin || '',
      });

      setIsRunning(false);

      const isStale = revisionRef.current !== runRev;

      if (res.status === 'VALIDATION_FAILED') {
        setValidationStatus('INVALID');
        setValidationDiagnostics(res.diagnostics || ['Syntax validation failed prior to execution.']);
        validatedRevisionRef.current = runRev;
        validatedCodeRef.current = runCodeContent;
      }

      setExecutionResult({
        status: res.status,
        stdout: res.stdout || '',
        stderr: res.stderr || '',
        exitCode: res.exit_code ?? 0,
        durationMs: res.duration_ms ?? 0,
        diagnostics: res.diagnostics || [],
        isStale,
      });

      executedRevisionRef.current = runRev;
      executedCodeRef.current = runCodeContent;
    } catch (err) {
      setIsRunning(false);
      setExecutionResult({
        status: 'SANDBOX_ERROR',
        stdout: '',
        stderr: '',
        exitCode: 1,
        durationMs: 0,
        diagnostics: [err.message || 'Failed to execute code in sandbox.'],
        isStale: revisionRef.current !== runRev,
      });
    }
  };

  const hasDiagnostics = validationDiagnostics && validationDiagnostics.length > 0;

  return (
    <div
      style={{
        border: '1px solid var(--border-code)',
        borderRadius: 'var(--radius-md)',
        backgroundColor: 'var(--bg-code)',
        overflow: 'hidden',
        margin: 'var(--space-3) 0',
        boxShadow: 'var(--shadow-sm)',
      }}
    >
      {/* Code Header Bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '8px 14px',
          backgroundColor: 'var(--bg-code-header)',
          borderBottom: '1px solid var(--border-code)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: 'var(--text-xs)',
              fontWeight: 600,
              color: '#f1f5f9',
            }}
          >
            {filename}
          </span>
          <span
            style={{
              fontSize: '0.68rem',
              textTransform: 'uppercase',
              color: '#93c5fd',
              backgroundColor: '#1e293b',
              padding: '2px 6px',
              borderRadius: 'var(--radius-xs)',
              border: '1px solid #334155',
              fontWeight: 600,
            }}
          >
            {language}
          </span>
          {isEditing && (
            <span
              style={{
                fontSize: '0.65rem',
                color: '#34d399',
                backgroundColor: 'rgba(5, 150, 105, 0.15)',
                border: '1px solid #059669',
                borderRadius: 'var(--radius-xs)',
                padding: '1px 5px',
                fontWeight: 600,
                textTransform: 'uppercase',
              }}
            >
              Editing
            </span>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <ValidationStatus type="validation" status={isValidating ? 'VALIDATING' : validationStatus} />
          {executionResult && executionResult.status !== 'RUNNING' && (
            <ValidationStatus
              type="execution"
              status={executionResult.status}
              durationMs={executionResult.durationMs}
            />
          )}
        </div>
      </div>

      {/* Code Body */}
      <div
        style={{
          position: 'relative',
          overflowX: 'auto',
          backgroundColor: 'var(--bg-code)',
          maxHeight: '480px',
        }}
      >
        {isEditing ? (
          <div style={{ display: 'flex', minHeight: '160px' }}>
            {/* Line numbers column */}
            <div
              style={{
                padding: '12px 10px',
                textAlign: 'right',
                userSelect: 'none',
                color: '#64748b',
                fontFamily: 'var(--font-mono)',
                fontSize: 'var(--text-xs)',
                lineHeight: '1.55',
                borderRight: '1px solid var(--border-code)',
                backgroundColor: 'rgba(0, 0, 0, 0.25)',
                minWidth: '42px',
              }}
            >
              {lines.map((_, i) => (
                <div key={i}>{i + 1}</div>
              ))}
            </div>
            {/* Inline Editor Area */}
            <textarea
              ref={textareaRef}
              value={draftCode}
              onChange={(e) => handleDraftChange(e.target.value)}
              onKeyDown={handleKeyDown}
              spellCheck={false}
              autoFocus
              placeholder="Write or edit code here..."
              style={{
                flex: 1,
                padding: '12px 14px',
                fontFamily: 'var(--font-mono)',
                fontSize: 'var(--text-xs)',
                lineHeight: '1.55',
                backgroundColor: 'transparent',
                border: 'none',
                outline: 'none',
                resize: 'none',
                minHeight: `${Math.max(lines.length * 22, 160)}px`,
                color: '#f1f5f9',
                whiteSpace: 'pre',
              }}
            />
          </div>
        ) : (
          <div
            style={{
              display: 'flex',
              padding: '12px 0',
              fontFamily: 'var(--font-mono)',
              fontSize: 'var(--text-xs)',
              lineHeight: '1.55',
            }}
          >
            {/* Line Numbers */}
            <div
              style={{
                padding: '0 12px',
                textAlign: 'right',
                userSelect: 'none',
                color: '#64748b',
                borderRight: '1px solid var(--border-code)',
                minWidth: '42px',
              }}
            >
              {lines.map((_, i) => (
                <div key={i}>{i + 1}</div>
              ))}
            </div>

            {/* Code Lines */}
            <div
              style={{
                padding: '0 14px',
                flex: 1,
                overflowX: 'auto',
                color: '#e2e8f0',
              }}
            >
              {lines.map((line, i) => (
                <div key={i} style={{ whiteSpace: 'pre' }}>
                  {line || ' '}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Inline Validation Diagnostics Banner */}
      {(validationStatus === 'INVALID' || validationStatus === 'ERROR') && hasDiagnostics && (
        <div
          style={{
            padding: '8px 14px',
            backgroundColor: '#1e1b2e',
            borderTop: '1px solid #451a3a',
            fontSize: 'var(--text-xs)',
            fontFamily: 'var(--font-mono)',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: showDiagnostics ? '6px' : 0,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#f87171' }}>
              <AlertCircle size={13} color="#ef4444" />
              <span style={{ fontWeight: 600 }}>Validation Diagnostics</span>
              <span style={{ color: '#94a3b8', fontSize: '0.70rem' }}>
                ({validationDiagnostics.length} issue{validationDiagnostics.length > 1 ? 's' : ''})
              </span>
            </div>
            <button
              type="button"
              onClick={() => setShowDiagnostics(!showDiagnostics)}
              style={{
                backgroundColor: 'transparent',
                border: 'none',
                color: '#94a3b8',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                fontSize: '0.70rem',
              }}
            >
              {showDiagnostics ? <ChevronDown size={11} /> : <ChevronRight size={11} />}
              <span>{showDiagnostics ? 'Hide' : 'Show'}</span>
            </button>
          </div>

          {showDiagnostics && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {validationDiagnostics.map((diag, idx) => {
                const parsed = parseDiagnostic(diag);
                return (
                  <div
                    key={idx}
                    style={{
                      display: 'flex',
                      alignItems: 'baseline',
                      gap: '8px',
                      color: parsed.severity === 'WARNING' ? '#fde047' : '#fca5a5',
                      lineHeight: '1.4',
                    }}
                  >
                    {parsed.line && (
                      <span
                        style={{
                          backgroundColor: '#2e1065',
                          border: '1px solid #6b21a8',
                          color: '#d8b4fe',
                          padding: '0 4px',
                          borderRadius: '2px',
                          fontSize: '0.65rem',
                          fontWeight: 600,
                          flexShrink: 0,
                        }}
                      >
                        Line {parsed.line}{parsed.col ? `, Col ${parsed.col}` : ''}
                      </span>
                    )}
                    <span>{parsed.text}</span>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* Program Input (stdin) Drawer */}
      {showStdin && (
        <div
          style={{
            padding: '8px 14px',
            backgroundColor: '#090d16',
            borderTop: '1px solid var(--border-code)',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '4px',
              fontSize: '0.70rem',
              color: '#94a3b8',
            }}
          >
            <span style={{ fontWeight: 600, color: '#e2e8f0' }}>Program Input (stdin)</span>
            <span>Passed to input() / scanf() on Run</span>
          </div>
          <textarea
            value={stdin}
            onChange={(e) => setStdin(e.target.value)}
            placeholder="Enter input lines to pass to your program..."
            rows={2}
            style={{
              width: '100%',
              backgroundColor: '#0f172a',
              border: '1px solid #334155',
              borderRadius: 'var(--radius-xs)',
              color: '#f8fafc',
              fontFamily: 'var(--font-mono)',
              fontSize: 'var(--text-xs)',
              padding: '6px 8px',
              resize: 'vertical',
              outline: 'none',
            }}
          />
        </div>
      )}

      {/* Footer Toolbar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '8px 12px',
          borderTop: '1px solid var(--border-code)',
          backgroundColor: 'var(--bg-code-header)',
          flexWrap: 'wrap',
          gap: '6px',
        }}
      >
        <CodeToolbar
          onCopy={handleCopy}
          onStartEdit={handleStartEdit}
          onSave={handleSave}
          onCancel={handleCancel}
          onValidate={handleExplicitValidate}
          onRun={handleRun}
          onToggleStdin={() => setShowStdin(!showStdin)}
          showStdin={showStdin}
          isEditing={isEditing}
          isRunning={isRunning}
          isValidating={isValidating}
        />

        {executionResult && (
          <button
            type="button"
            onClick={() => setShowConsole(!showConsole)}
            style={{
              fontSize: 'var(--text-xs)',
              color: executionResult.isStale ? '#f59e0b' : '#94a3b8',
              backgroundColor: 'transparent',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
              padding: '4px 8px',
              borderRadius: 'var(--radius-xs)',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.color = '#f1f5f9')}
            onMouseLeave={(e) =>
              (e.currentTarget.style.color = executionResult.isStale ? '#f59e0b' : '#94a3b8')
            }
          >
            <Terminal size={12} />
            <span>
              {showConsole
                ? 'Hide Console'
                : executionResult.isStale
                ? 'View Console (stale)'
                : 'View Console'}
            </span>
          </button>
        )}
      </div>

      {/* Output Console via ExecutionResult */}
      {showConsole && executionResult && (
        <ExecutionResult
          status={executionResult.status}
          stdout={executionResult.stdout}
          stderr={executionResult.stderr}
          exitCode={executionResult.exitCode}
          durationMs={executionResult.durationMs}
          diagnostics={executionResult.diagnostics}
          isStale={executionResult.isStale}
          onClose={() => setShowConsole(false)}
        />
      )}
    </div>
  );
}
