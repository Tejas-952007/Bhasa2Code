import React from 'react';

export default function UserMessage({ message }) {
  return (
    <div
      style={{
        padding: 'var(--space-4) 0',
        borderBottom: '1px solid var(--border-subtle)',
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          marginBottom: 'var(--space-1)',
        }}
      >
        <span
          style={{
            fontSize: 'var(--text-xs)',
            fontWeight: 600,
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            color: 'var(--text-muted)',
          }}
        >
          You
        </span>
        {message.language && (
          <span
            style={{
              fontSize: '0.65rem',
              color: 'var(--text-muted)',
              backgroundColor: 'var(--bg-subtle)',
              padding: '1px 5px',
              borderRadius: 'var(--radius-xs)',
            }}
          >
            {message.language}
          </span>
        )}
      </div>

      <div
        style={{
          fontSize: 'var(--text-base)',
          color: 'var(--text-primary)',
          lineHeight: 'var(--leading-relaxed)',
          whiteSpace: 'pre-wrap',
        }}
      >
        {message.content}
      </div>
    </div>
  );
}
