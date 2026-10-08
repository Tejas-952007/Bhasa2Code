import React, { useState } from 'react';
import { Terminal, Copy, Check, AlertCircle, Clock, ShieldAlert } from 'lucide-react';

/**
 * ExecutionResult
 * Console-style presentation for code runtime sandbox execution.
 * Formats success output, runtime errors, timeouts, and resource limits cleanly.
 */
export default function ExecutionResult({
  status = 'SUCCESS',
  stdout = '',
  stderr = '',
  exitCode = 0,
  durationMs = 0,
  diagnostics = [],
  rawOutput = '',
  onClose = null,
}) {
  const [copied, setCopied] = useState(false);

  const normalizedStatus = (status || 'SUCCESS').toUpperCase();

  const isSuccess = normalizedStatus === 'SUCCESS' || normalizedStatus === 'RAN_SUCCESSFULLY' || (exitCode === 0 && !stderr && normalizedStatus !== 'TIMEOUT' && normalizedStatus !== 'RESOURCE_LIMIT' && normalizedStatus !== 'SANDBOX_ERROR');
  const isTimeout = normalizedStatus === 'TIMEOUT' || normalizedStatus === 'TIMED_OUT';
  const isResourceLimit = normalizedStatus === 'RESOURCE_LIMIT';
  const isSandboxError = normalizedStatus === 'SANDBOX_ERROR' || normalizedStatus === 'UNAVAILABLE';
  const isValidationError = normalizedStatus === 'VALIDATION_FAILED';
  const isRuntimeError = !isSuccess && !isTimeout && !isResourceLimit && !isSandboxError && !isValidationError;

  let headerTitle = 'Output';
  let titleColor = '#cbd5e1';
  let statusIcon = Terminal;

  if (isTimeout) {
    headerTitle = 'Execution Timed Out';
    titleColor = '#f59e0b';
    statusIcon = Clock;
  } else if (isResourceLimit) {
    headerTitle = 'Resource Limit Exceeded';
    titleColor = '#ef4444';
    statusIcon = ShieldAlert;
  } else if (isSandboxError) {
    headerTitle = 'Sandbox Unavailable';
    titleColor = '#ef4444';
    statusIcon = AlertCircle;
  } else if (isValidationError) {
    headerTitle = 'Validation Failed';
    titleColor = '#ef4444';
    statusIcon = AlertCircle;
  } else if (isRuntimeError) {
    headerTitle = 'Runtime Error';
    titleColor = '#f87171';
    statusIcon = AlertCircle;
  }

  // Format content to display
  let content = '';
  if (isTimeout) {
    content = 'Execution timed out.\n\nThe program exceeded the allowed runtime.';
  } else if (isResourceLimit) {
    content = 'Execution stopped.\n\nThe program exceeded the sandbox resource limit.';
  } else if (isSandboxError) {
    content = 'The code could not be executed safely.\n\nSandbox unavailable: Docker runtime is not accessible.';
    if (diagnostics && diagnostics.length > 0) {
      content += `\n${diagnostics.join('\n')}`;
    }
  } else if (isValidationError) {
    content = diagnostics && diagnostics.length > 0
      ? `Validation failed prior to execution:\n${diagnostics.join('\n')}`
      : 'Validation failed prior to execution.';
  } else {
    // Standard execution output
    if (stdout && stderr) {
      content = `${stdout}\n\n[stderr]:\n${stderr}`;
    } else if (stdout) {
      content = stdout;
    } else if (stderr) {
      content = stderr;
    } else if (rawOutput) {
      content = rawOutput;
    } else if (diagnostics && diagnostics.length > 0) {
      content = diagnostics.join('\n');
    } else {
      content = exitCode === 0 ? '(Program produced no stdout output)' : `(Process exited with code ${exitCode})`;
    }
  }

  const handleCopy = () => {
    navigator.clipboard?.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const HeaderIcon = statusIcon;

  return (
    <div
      style={{
        borderTop: '1px solid var(--border-code)',
        backgroundColor: '#0f172a',
        color: '#f8fafc',
        fontFamily: 'var(--font-mono)',
        fontSize: 'var(--text-xs)',
        lineHeight: '1.5',
      }}
    >
      {/* Console Bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '8px 14px',
          backgroundColor: '#1e293b',
          borderBottom: '1px solid #334155',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <HeaderIcon size={13} color={titleColor} />
          <span
            style={{
              fontWeight: 600,
              fontSize: '0.72rem',
              color: titleColor,
              letterSpacing: '0.03em',
            }}
          >
            {headerTitle}
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {durationMs > 0 && (
            <span
              style={{
                color: '#94a3b8',
                fontSize: '0.70rem',
              }}
            >
              Completed · {Math.round(durationMs)} ms
            </span>
          )}

          <button
            type="button"
            onClick={handleCopy}
            title="Copy output"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              color: '#94a3b8',
              backgroundColor: 'transparent',
              border: 'none',
              cursor: 'pointer',
              padding: '2px 4px',
              borderRadius: 'var(--radius-xs)',
              fontSize: '0.70rem',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.color = '#f8fafc')}
            onMouseLeave={(e) => (e.currentTarget.style.color = '#94a3b8')}
          >
            {copied ? <Check size={11} color="#34d399" /> : <Copy size={11} />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>

          {onClose && (
            <button
              type="button"
              onClick={onClose}
              title="Close console"
              style={{
                color: '#94a3b8',
                backgroundColor: 'transparent',
                border: 'none',
                cursor: 'pointer',
                fontSize: '0.70rem',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.color = '#f8fafc')}
              onMouseLeave={(e) => (e.currentTarget.style.color = '#94a3b8')}
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Output Console Pre */}
      <pre
        style={{
          margin: 0,
          padding: '12px 16px',
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
          color: isRuntimeError || isTimeout || isResourceLimit || isSandboxError ? '#fca5a5' : '#f1f5f9',
          maxHeight: '260px',
          overflowY: 'auto',
          fontSize: 'var(--text-xs)',
        }}
      >
        {content}
      </pre>
    </div>
  );
}
