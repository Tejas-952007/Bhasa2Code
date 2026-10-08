import React, { useState } from 'react';
import { Copy, Check, Edit3, ShieldCheck, Play } from 'lucide-react';
import Button from '../common/Button';

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

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--space-2)',
      }}
    >
      <Button
        variant="ghost"
        size="sm"
        onClick={handleCopy}
        title="Copy code to clipboard"
      >
        {copied ? <Check size={13} color="var(--status-success)" /> : <Copy size={13} />}
        <span>{copied ? 'Copied' : 'Copy'}</span>
      </Button>

      <Button
        variant={isEditing ? 'subtle' : 'ghost'}
        size="sm"
        onClick={onEdit}
        title={isEditing ? 'Done editing' : 'Edit code'}
      >
        <Edit3 size={13} />
        <span>{isEditing ? 'Done' : 'Edit'}</span>
      </Button>

      <Button
        variant="ghost"
        size="sm"
        onClick={onValidate}
        title="Validate syntax"
      >
        <ShieldCheck size={13} />
        <span>Validate</span>
      </Button>

      <Button
        variant="subtle"
        size="sm"
        onClick={onRun}
        disabled={isRunning}
        title="Run code in sandbox"
        style={{ color: 'var(--accent-primary)', fontWeight: 600 }}
      >
        <Play size={13} fill="currentColor" />
        <span>{isRunning ? 'Running...' : 'Run'}</span>
      </Button>
    </div>
  );
}
