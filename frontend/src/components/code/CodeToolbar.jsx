import React, { useState } from 'react';
import { Copy, Check, Edit3, ShieldCheck, Play, Save, X, Loader2, ArrowDownToLine } from 'lucide-react';

/**
 * CodeToolbar
 * Primary action bar for CodeArtifact:
 * - Normal mode: Copy, Edit, Validate, Run, Stdin
 * - Edit mode: Save, Cancel, Validate, Run, Stdin
 */
export default function CodeToolbar({
  onCopy,
  onStartEdit,
  onSave,
  onCancel,
  onValidate,
  onRun,
  onToggleStdin = null,
  showStdin = false,
  isEditing = false,
  isRunning = false,
  isValidating = false,
}) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (onCopy) onCopy();
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const btnStyle = {
    padding: '4px 10px',
    borderRadius: 'var(--radius-xs)',
    fontSize: 'var(--text-xs)',
    display: 'inline-flex',
    alignItems: 'center',
    gap: '5px',
    color: '#cbd5e1',
    backgroundColor: '#262d3d',
    border: '1px solid #333c4d',
    cursor: 'pointer',
    transition: 'all 120ms ease',
    fontWeight: 500,
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap' }}>
      {isEditing ? (
        <>
          <button
            type="button"
            onClick={onSave}
            title="Save code changes"
            style={{
              ...btnStyle,
              backgroundColor: '#15803d',
              color: '#ffffff',
              borderColor: '#16a34a',
              fontWeight: 600,
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#166534')}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#15803d')}
          >
            <Save size={13} />
            <span>Save</span>
          </button>

          <button
            type="button"
            onClick={onCancel}
            title="Cancel editing without saving"
            style={{
              ...btnStyle,
              backgroundColor: '#374151',
              color: '#e5e7eb',
              borderColor: '#4b5563',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#4b5563')}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#374151')}
          >
            <X size={13} />
            <span>Cancel</span>
          </button>
        </>
      ) : (
        <>
          <button
            type="button"
            style={btnStyle}
            onClick={handleCopy}
            title="Copy code to clipboard"
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#333c4d')}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#262d3d')}
          >
            {copied ? <Check size={13} color="#34d399" /> : <Copy size={13} />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>

          <button
            type="button"
            style={btnStyle}
            onClick={onStartEdit}
            title="Edit code inline"
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#333c4d')}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#262d3d')}
          >
            <Edit3 size={13} />
            <span>Edit</span>
          </button>
        </>
      )}

      {/* Validate Button */}
      <button
        type="button"
        disabled={isValidating}
        style={{
          ...btnStyle,
          opacity: isValidating ? 0.75 : 1,
          cursor: isValidating ? 'wait' : 'pointer',
        }}
        onClick={onValidate}
        title="Validate code syntax"
        onMouseEnter={(e) => {
          if (!isValidating) e.currentTarget.style.backgroundColor = '#333c4d';
        }}
        onMouseLeave={(e) => {
          if (!isValidating) e.currentTarget.style.backgroundColor = '#262d3d';
        }}
      >
        {isValidating ? (
          <Loader2 size={13} className="spin" color="#60a5fa" />
        ) : (
          <ShieldCheck size={13} color="#60a5fa" />
        )}
        <span>{isValidating ? 'Validating...' : 'Validate'}</span>
      </button>

      {/* Run Button */}
      <button
        type="button"
        disabled={isRunning}
        onClick={onRun}
        title="Run code in secure sandbox"
        style={{
          ...btnStyle,
          backgroundColor: '#2563eb',
          color: '#ffffff',
          border: '1px solid #3b82f6',
          fontWeight: 600,
          boxShadow: '0 1px 3px rgba(37, 99, 235, 0.3)',
          opacity: isRunning ? 0.8 : 1,
          cursor: isRunning ? 'wait' : 'pointer',
        }}
        onMouseEnter={(e) => {
          if (!isRunning) e.currentTarget.style.backgroundColor = '#1d4ed8';
        }}
        onMouseLeave={(e) => {
          if (!isRunning) e.currentTarget.style.backgroundColor = '#2563eb';
        }}
      >
        {isRunning ? (
          <Loader2 size={13} className="spin" />
        ) : (
          <Play size={13} fill="currentColor" />
        )}
        <span>{isRunning ? 'Running...' : 'Run'}</span>
      </button>

      {/* Stdin Toggle Button */}
      {onToggleStdin && (
        <button
          type="button"
          onClick={onToggleStdin}
          title="Toggle Program Input (stdin)"
          style={{
            ...btnStyle,
            backgroundColor: showStdin ? '#1e293b' : '#262d3d',
            borderColor: showStdin ? '#3b82f6' : '#333c4d',
            color: showStdin ? '#93c5fd' : '#cbd5e1',
          }}
          onMouseEnter={(e) => {
            if (!showStdin) e.currentTarget.style.backgroundColor = '#333c4d';
          }}
          onMouseLeave={(e) => {
            if (!showStdin) e.currentTarget.style.backgroundColor = '#262d3d';
          }}
        >
          <ArrowDownToLine size={12} />
          <span>stdin</span>
        </button>
      )}
    </div>
  );
}
