import React, { useState } from 'react';
import CodeToolbar from './CodeToolbar';
import ValidationStatus from './ValidationStatus';
import ExecutionResult from '../response/ExecutionResult';
import { Terminal } from 'lucide-react';
import { validateCode, runCode } from '../../services/api';

/**
 * CodeArtifact
 * The primary code display, inline editor, validation, and sandbox runner workspace component.
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
        }
      : null
  );

  const lines = (isEditing ? draftCode : code).split('\n');

  const handleCopy = () => {
    navigator.clipboard?.writeText(code);
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
  };

  const handleCancel = () => {
    setDraftCode(code);
    setIsEditing(false);
  };

  const handleValidate = async () => {
    setIsValidating(true);
    try {
      const res = await validateCode({ language, code });
      setIsValidating(false);
      setValidationStatus(res.is_valid ? 'VALID' : 'INVALID');
      setValidationDiagnostics(res.diagnostics || []);
      if (!res.is_valid) {
        setExecutionResult({
          status: 'VALIDATION_FAILED',
          stdout: '',
          stderr: '',
          exitCode: 1,
          durationMs: 0,
          diagnostics: res.diagnostics || ['Syntax validation failed.'],
        });
        setShowConsole(true);
      }
    } catch (err) {
      setIsValidating(false);
      setValidationStatus('INVALID');
      setValidationDiagnostics([err.message || 'Validation request failed.']);
      setExecutionResult({
        status: 'VALIDATION_FAILED',
        stdout: '',
        stderr: '',
        exitCode: 1,
        durationMs: 0,
        diagnostics: [err.message || 'Validation request failed.'],
      });
      setShowConsole(true);
    }
  };

  const handleRun = async () => {
    setIsRunning(true);
    setShowConsole(true);
    setExecutionResult({
      status: 'RUNNING',
      stdout: 'Running secure sandbox...',
      stderr: '',
      exitCode: 0,
      durationMs: 0,
      diagnostics: [],
    });

    try {
      const res = await runCode({ language, code });
      setIsRunning(false);

      if (res.status === 'VALIDATION_FAILED') {
        setValidationStatus('INVALID');
      }

      setExecutionResult({
        status: res.status,
        stdout: res.stdout || '',
        stderr: res.stderr || '',
        exitCode: res.exit_code ?? 0,
        durationMs: res.duration_ms ?? 0,
        diagnostics: res.diagnostics || [],
      });
    } catch (err) {
      setIsRunning(false);
      setExecutionResult({
        status: 'SANDBOX_ERROR',
        stdout: '',
        stderr: '',
        exitCode: 1,
        durationMs: 0,
        diagnostics: [err.message || 'Failed to execute code in sandbox.'],
      });
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
              value={draftCode}
              onChange={(e) => setDraftCode(e.target.value)}
              spellCheck={false}
              autoFocus
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
          onValidate={handleValidate}
          onRun={handleRun}
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
              color: '#94a3b8',
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
            onMouseLeave={(e) => (e.currentTarget.style.color = '#94a3b8')}
          >
            <Terminal size={12} />
            <span>{showConsole ? 'Hide Console' : 'View Console'}</span>
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
          onClose={() => setShowConsole(false)}
        />
      )}
    </div>
  );
}
