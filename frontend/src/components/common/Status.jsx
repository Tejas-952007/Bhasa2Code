import React from 'react';

export default function Status({ state = 'ready', label, className = '' }) {
  const configs = {
    ready: {
      color: 'var(--status-success)',
      defaultText: 'Local · Ready',
      bgColor: 'transparent',
    },
    loading: {
      color: 'var(--status-warning)',
      defaultText: 'Local model starting...',
      bgColor: 'transparent',
    },
    busy: {
      color: 'var(--accent-primary)',
      defaultText: 'Processing...',
      bgColor: 'transparent',
    },
    unavailable: {
      color: 'var(--status-error)',
      defaultText: 'Ollama offline',
      bgColor: 'transparent',
    },
    error: {
      color: 'var(--status-error)',
      defaultText: 'Runtime error',
      bgColor: 'transparent',
    },
  };

  const cfg = configs[state] || configs.ready;
  const displayText = label || cfg.defaultText;

  return (
    <div
      className={`b2c-status-indicator ${className}`}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '6px',
        fontSize: 'var(--text-xs)',
        color: 'var(--text-secondary)',
        userSelect: 'none',
      }}
      title={`Model Status: ${displayText}`}
    >
      <span
        style={{
          width: '7px',
          height: '7px',
          borderRadius: '50%',
          backgroundColor: cfg.color,
          display: 'inline-block',
          boxShadow: `0 0 0 2px ${cfg.color}20`,
        }}
        aria-hidden="true"
      />
      <span>{displayText}</span>
    </div>
  );
}
