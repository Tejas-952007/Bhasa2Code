import React from 'react';
import { User } from 'lucide-react';

export default function UserMessage({ message }) {
  return (
    <div
      style={{
        margin: '14px 0',
        padding: '14px 18px',
        backgroundColor: 'var(--bg-surface)',
        borderRadius: 'var(--radius-md)',
        border: '1px solid var(--border-color)',
        boxShadow: 'var(--shadow-xs)',
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          marginBottom: '6px',
        }}
      >
        <div
          style={{
            width: '20px',
            height: '20px',
            borderRadius: '50%',
            backgroundColor: 'var(--accent-subtle)',
            color: 'var(--accent-primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <User size={12} strokeWidth={2.5} />
        </div>
        <span
          style={{
            fontSize: 'var(--text-xs)',
            fontWeight: 600,
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            color: 'var(--text-secondary)',
          }}
        >
          You
        </span>
        {message.language && (
          <span
            style={{
              fontSize: '0.68rem',
              color: 'var(--accent-text)',
              backgroundColor: 'var(--accent-subtle)',
              border: '1px solid #bfdbfe',
              padding: '1px 6px',
              borderRadius: 'var(--radius-xs)',
              fontWeight: 600,
            }}
          >
            {message.language}
          </span>
        )}
      </div>

      <div
        style={{
          fontSize: 'var(--text-base)',
          fontWeight: 500,
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
