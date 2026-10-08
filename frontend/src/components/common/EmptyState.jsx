import React from 'react';

export default function EmptyState({ onSelectPrompt }) {
  const examplePrompts = [
    "Python madhe calculator banav",
    "हा code Marathi madhe explain kar",
    "Why is my loop slow?"
  ];

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        padding: 'var(--space-8) var(--space-4)',
        maxWidth: '560px',
        margin: 'auto',
      }}
    >
      <h1
        style={{
          fontSize: 'var(--text-2xl)',
          fontWeight: 600,
          color: 'var(--text-primary)',
          letterSpacing: '-0.02em',
          marginBottom: 'var(--space-2)',
        }}
      >
        Bhasha2Code
      </h1>

      <p
        style={{
          fontSize: 'var(--text-base)',
          color: 'var(--text-secondary)',
          marginBottom: 'var(--space-3)',
          fontWeight: 500,
        }}
      >
        Your local coding workspace
      </p>

      <p
        style={{
          fontSize: 'var(--text-sm)',
          color: 'var(--text-muted)',
          lineHeight: 'var(--leading-relaxed)',
          marginBottom: 'var(--space-6)',
        }}
      >
        Ask a coding question in English, Hindi, Marathi, Hinglish or mixed language.
      </p>

      {/* Subtle Example Prompts */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 'var(--space-2)',
          width: '100%',
        }}
      >
        <span
          style={{
            fontSize: 'var(--text-xs)',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            color: 'var(--text-muted)',
            marginBottom: 'var(--space-1)',
            textAlign: 'left',
          }}
        >
          Suggested Prompts
        </span>

        {examplePrompts.map((prompt, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => onSelectPrompt && onSelectPrompt(prompt)}
            style={{
              padding: '8px 12px',
              backgroundColor: 'var(--bg-surface)',
              border: '1px solid var(--border-color)',
              borderRadius: 'var(--radius-sm)',
              color: 'var(--text-secondary)',
              fontSize: 'var(--text-sm)',
              textAlign: 'left',
              cursor: 'pointer',
              transition: 'all var(--transition-fast)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = 'var(--accent-primary)';
              e.currentTarget.style.color = 'var(--text-primary)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = 'var(--border-color)';
              e.currentTarget.style.color = 'var(--text-secondary)';
            }}
          >
            <span>{prompt}</span>
            <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)' }}>↗</span>
          </button>
        ))}
      </div>
    </div>
  );
}
