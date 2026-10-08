import React, { useState } from 'react';
import { Copy, Check, Edit3, ShieldCheck, Play } from 'lucide-react';

export default function CodeToolbar({
  onCopy,
  onEdit,
  onValidate,
  onRun,
  isEditing = false,
  isRunning = false,
}) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (onCopy) onCopy();
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const btnStyle = {
    padding: '4px 9px',
    borderRadius: 'var(--radius-xs)',
    fontSize: 'var(--text-xs)',
    display: 'inline-flex',
    alignItems: 'center',
    gap: '5px',
    color: '#cbd5e1',
    backgroundColor: '#262d3d',
    border: '1px solid #333c4d',
    cursor: 'pointer',
    transition: 'all 150ms ease',
  };

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '6px',
      }}
    >
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
        style={{
          ...btnStyle,
          backgroundColor: isEditing ? '#3b82f6' : '#262d3d',
          color: isEditing ? '#ffffff' : '#cbd5e1',
        }}
        onClick={onEdit}
        title={isEditing ? 'Done editing' : 'Edit code'}
      >
        <Edit3 size={13} />
        <span>{isEditing ? 'Done' : 'Edit'}</span>
      </button>

      <button
        type="button"
        style={btnStyle}
        onClick={onValidate}
        title="Validate syntax"
        onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#333c4d')}
        onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#262d3d')}
      >
        <ShieldCheck size={13} color="#60a5fa" />
        <span>Validate</span>
      </button>

      <button
        type="button"
        disabled={isRunning}
        onClick={onRun}
        title="Run code in sandbox"
        style={{
          ...btnStyle,
          backgroundColor: '#2563eb',
          color: '#ffffff',
          border: '1px solid #3b82f6',
          fontWeight: 600,
          boxShadow: '0 1px 3px rgba(37, 99, 235, 0.3)',
        }}
        onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#1d4ed8')}
        onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = '#2563eb')}
      >
        <Play size={13} fill="currentColor" />
        <span>{isRunning ? 'Running...' : 'Run'}</span>
      </button>
    </div>
  );
}
