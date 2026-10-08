import React, { useState } from 'react';
import CodeToolbar from './CodeToolbar';
import ValidationStatus from './ValidationStatus';
import { Terminal } from 'lucide-react';

export default function CodeArtifact({
  initialCode = '',
  filename = 'main.py',
  language = 'python',
  initialValidation = 'VALID',
  initialExecution = 'SUCCESS',
  initialOutput = '',
  durationMs = 152.4,
}) {
  const [code, setCode] = useState(initialCode);
  const [isEditing, setIsEditing] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [showOutput, setShowOutput] = useState(true);
  const [output, setOutput] = useState(initialOutput);
  const [executionStatus, setExecutionStatus] = useState(initialExecution);
  const [validationStatus, setValidationStatus] = useState(initialValidation);

  const lines = code.split('\n');

  const handleCopy = () => {
    navigator.clipboard?.writeText(code);
  };

  const handleValidate = () => {
    // Demo validation feedback
    setValidationStatus('VALID');
  };

  const handleRun = () => {
    setIsRunning(true);
    setTimeout(() => {
      setIsRunning(false);
      setShowOutput(true);
      setExecutionStatus('SUCCESS');
      if (!output) {
        setOutput("Program executed successfully.\nResult: 15.0\n(Demo sandbox result)");
      }
    }, 600);
  };

  return (
    <div
      style={{
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-md)',
        backgroundColor: 'var(--bg-code)',
        overflow: 'hidden',
        margin: 'var(--space-3) 0',
        boxShadow: 'var(--shadow-xs)',
      }}
    >
      {/* Code Header Bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '6px 12px',
          backgroundColor: 'var(--bg-code-header)',
          borderBottom: '1px solid var(--border-color)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: 'var(--text-xs)',
              fontWeight: 600,
              color: 'var(--text-primary)',
            }}
          >
            {filename}
          </span>
          <span
            style={{
              fontSize: '0.7rem',
              textTransform: 'uppercase',
              color: 'var(--text-muted)',
              backgroundColor: 'var(--bg-surface)',
              padding: '1px 5px',
              borderRadius: 'var(--radius-xs)',
              border: '1px solid var(--border-color)',
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
              durationMs={durationMs}
            />
          )}
        </div>
      </div>

      {/* Code Body */}
      <div style={{ position: 'relative', overflowX: 'auto' }}>
        {isEditing ? (
          <div style={{ display: 'flex' }}>
            {/* Line numbers column */}
            <div
              style={{
                padding: '12px 8px',
                textAlign: 'right',
                userSelect: 'none',
                color: 'var(--text-muted)',
                fontFamily: 'var(--font-mono)',
                fontSize: 'var(--text-xs)',
                lineHeight: '1.5',
                borderRight: '1px solid var(--border-subtle)',
                backgroundColor: 'rgba(0, 0, 0, 0.01)',
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
                padding: '12px',
                fontFamily: 'var(--font-mono)',
                fontSize: 'var(--text-xs)',
                lineHeight: '1.5',
                backgroundColor: 'transparent',
                border: 'none',
                outline: 'none',
                resize: 'none',
                minHeight: `${Math.max(lines.length * 20, 160)}px`,
                color: 'var(--text-primary)',
                whiteSpace: 'pre',
              }}
            />
          </div>
        ) : (
          <div
            style={{
              display: 'flex',
              padding: '10px 0',
              fontFamily: 'var(--font-mono)',
              fontSize: 'var(--text-xs)',
              lineHeight: '1.5',
            }}
          >
            {/* Line Numbers */}
            <div
              style={{
                padding: '0 12px',
                textAlign: 'right',
                userSelect: 'none',
                color: 'var(--text-muted)',
                borderRight: '1px solid var(--border-subtle)',
                minWidth: '40px',
              }}
            >
              {lines.map((_, i) => (
                <div key={i}>{i + 1}</div>
              ))}
            </div>

            {/* Code Lines */}
            <div style={{ padding: '0 12px', flex: 1, overflowX: 'auto' }}>
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
          padding: '6px 12px',
          borderTop: '1px solid var(--border-color)',
          backgroundColor: 'var(--bg-surface)',
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
              color: 'var(--text-secondary)',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              padding: '2px 6px',
            }}
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
