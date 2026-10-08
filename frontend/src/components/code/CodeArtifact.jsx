import React, { useState } from 'react';
import CodeToolbar from './CodeToolbar';
import ValidationStatus from './ValidationStatus';
import { Terminal } from 'lucide-react';
import { validateCode, runCode } from '../../services/api';

export default function CodeArtifact({
  initialCode = '',
  filename = 'main.py',
  language = 'python',
  initialValidation = 'VALID',
  initialExecution = null,
  initialOutput = '',
  durationMs = 0,
}) {
  const [code, setCode] = useState(initialCode);
  const [isEditing, setIsEditing] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [showOutput, setShowOutput] = useState(Boolean(initialOutput));
  const [output, setOutput] = useState(initialOutput);
  const [executionStatus, setExecutionStatus] = useState(initialExecution);
  const [validationStatus, setValidationStatus] = useState(initialValidation);
  const [currentDurationMs, setCurrentDurationMs] = useState(durationMs);

  const lines = code.split('\n');

  const handleCopy = () => {
    navigator.clipboard?.writeText(code);
  };

  const handleValidate = async () => {
    try {
      const res = await validateCode({ language, code });
      setValidationStatus(res.is_valid ? 'VALID' : 'INVALID');
      if (!res.is_valid && res.diagnostics && res.diagnostics.length > 0) {
        setOutput(res.diagnostics.join('\n'));
        setShowOutput(true);
      }
    } catch (err) {
      setValidationStatus('INVALID');
      setOutput(err.message || 'Validation failed');
      setShowOutput(true);
    }
  };

  const handleRun = async () => {
    setIsRunning(true);
    setShowOutput(true);
    setOutput('Running secure sandbox...');
    try {
      const res = await runCode({ language, code });
      setIsRunning(false);
      setExecutionStatus(res.status);
      setCurrentDurationMs(res.duration_ms || 0);

      if (res.status === 'VALIDATION_FAILED') {
        setValidationStatus('INVALID');
        setOutput(
          res.diagnostics?.join('\n') || 'Validation failed prior to execution.'
        );
      } else if (res.status === 'SANDBOX_ERROR') {
        setOutput(
          res.diagnostics?.join('\n') || 'Sandbox unavailable: Docker runtime is not accessible.'
        );
      } else {
        const out = res.stdout || res.stderr || (res.diagnostics || []).join('\n');
        setOutput(out || `(Process finished with exit code ${res.exit_code})`);
      }
    } catch (err) {
      setIsRunning(false);
      setExecutionStatus('ERROR');
      setOutput(err.message || 'Failed to execute code in sandbox.');
    }
  };

  return (
    <div
      style={{
        border: '1px solid var(--border-code)',
        borderRadius: 'var(--radius-md)',
        backgroundColor: 'var(--bg-code)',
        overflow: 'hidden',
        margin: 'var(--space-3) 0',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
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
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <ValidationStatus type="validation" status={validationStatus} />
          {executionStatus && (
            <ValidationStatus
              type="execution"
              status={executionStatus}
              durationMs={currentDurationMs}
            />
          )}
        </div>
      </div>

      {/* Code Body */}
      <div style={{ position: 'relative', overflowX: 'auto', backgroundColor: 'var(--bg-code)' }}>
        {isEditing ? (
          <div style={{ display: 'flex' }}>
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
              value={code}
              onChange={(e) => setCode(e.target.value)}
              spellCheck={false}
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
            <div style={{ padding: '0 14px', flex: 1, overflowX: 'auto', color: '#e2e8f0' }}>
              {lines.map((line, i) => (
                <div key={i} style={{ whiteSpace: 'pre' }}>
                  {line || ' '}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Footer Toolbar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '8px 12px',
          borderTop: '1px solid var(--border-code)',
          backgroundColor: 'var(--bg-code-header)',
        }}
      >
        <CodeToolbar
          onCopy={handleCopy}
          onEdit={() => setIsEditing(!isEditing)}
          onValidate={handleValidate}
          onRun={handleRun}
          isEditing={isEditing}
          isRunning={isRunning}
        />

        {output && (
          <button
            type="button"
            onClick={() => setShowOutput(!showOutput)}
            style={{
              fontSize: 'var(--text-xs)',
              color: '#94a3b8',
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
              padding: '4px 8px',
              borderRadius: 'var(--radius-xs)',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.color = '#f1f5f9')}
            onMouseLeave={(e) => (e.currentTarget.style.color = '#94a3b8')}
          >
            <Terminal size={12} />
            <span>{showOutput ? 'Hide Output' : 'View Output'}</span>
          </button>
        )}
      </div>

      {/* Output Console (if executed) */}
      {showOutput && output && (
        <div
          style={{
            borderTop: '1px solid var(--border-color)',
            backgroundColor: '#181e29',
            color: '#e5e7eb',
            padding: '10px 14px',
            fontFamily: 'var(--font-mono)',
            fontSize: 'var(--text-xs)',
            lineHeight: '1.45',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '6px',
              paddingBottom: '4px',
              borderBottom: '1px solid #2d3748',
              color: '#9ca3af',
              fontSize: '0.7rem',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
            }}
          >
            <span>Sandbox Output (Demo)</span>
            <span>Duration: {durationMs}ms</span>
          </div>
          <pre style={{ margin: 0, whiteSpace: 'pre-wrap', color: '#f3f4f6' }}>
            {output}
          </pre>
        </div>
      )}
    </div>
  );
}
