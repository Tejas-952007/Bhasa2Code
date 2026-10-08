import React from 'react';
import { ArrowUpRight } from 'lucide-react';

/**
 * SuggestionList
 * Displays 3-5 relevant follow-up suggestions provided by backend/context.
 */
export default function SuggestionList({ suggestions = [], onSelectSuggestion = null }) {
  if (!suggestions || suggestions.length === 0) return null;

  // Enforce max initial display of 3 to 5
  const visibleSuggestions = suggestions.slice(0, 5);

  return (
    <div style={{ marginTop: '14px', paddingTop: '10px', borderTop: '1px solid var(--border-subtle)' }}>
      <div
        style={{
          fontSize: 'var(--text-xs)',
          fontWeight: 700,
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: 'var(--text-muted)',
          marginBottom: '8px',
        }}
      >
        Suggestions
      </div>

      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '6px',
        }}
      >
        {visibleSuggestions.map((item, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => onSelectSuggestion && onSelectSuggestion(item)}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '5px 10px',
              borderRadius: 'var(--radius-sm)',
              fontSize: 'var(--text-xs)',
              fontWeight: 500,
              color: 'var(--text-primary)',
              backgroundColor: 'var(--bg-subtle)',
              border: '1px solid var(--border-color)',
              cursor: onSelectSuggestion ? 'pointer' : 'default',
              transition: 'all 120ms ease',
              textAlign: 'left',
            }}
            onMouseEnter={(e) => {
              if (onSelectSuggestion) {
                e.currentTarget.style.backgroundColor = 'var(--bg-surface)';
                e.currentTarget.style.borderColor = 'var(--accent-primary)';
                e.currentTarget.style.color = 'var(--accent-text)';
              }
            }}
            onMouseLeave={(e) => {
              if (onSelectSuggestion) {
                e.currentTarget.style.backgroundColor = 'var(--bg-subtle)';
                e.currentTarget.style.borderColor = 'var(--border-color)';
                e.currentTarget.style.color = 'var(--text-primary)';
              }
            }}
          >
            <span>{item}</span>
            {onSelectSuggestion && <ArrowUpRight size={11} color="var(--text-muted)" />}
          </button>
        ))}
      </div>
    </div>
  );
}
