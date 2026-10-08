import React from 'react';
import { BookOpen } from 'lucide-react';

export default function StudyToggle({ isStudyMode, onChange }) {
  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        backgroundColor: 'var(--bg-subtle)',
        padding: '2px',
        borderRadius: 'var(--radius-sm)',
        border: '1px solid var(--border-color)',
        userSelect: 'none',
      }}
    >
      <button
        type="button"
        onClick={() => onChange(false)}
        style={{
          padding: '3px 10px',
          fontSize: 'var(--text-xs)',
          fontWeight: !isStudyMode ? 600 : 400,
          color: !isStudyMode ? 'var(--text-primary)' : 'var(--text-secondary)',
          backgroundColor: !isStudyMode ? 'var(--bg-surface)' : 'transparent',
          borderRadius: 'var(--radius-xs)',
          boxShadow: !isStudyMode ? 'var(--shadow-xs)' : 'none',
          transition: 'all var(--transition-fast)',
        }}
      >
        Normal
      </button>

      <button
        type="button"
        onClick={() => onChange(true)}
        style={{
          padding: '3px 10px',
          fontSize: 'var(--text-xs)',
          fontWeight: isStudyMode ? 600 : 400,
          color: isStudyMode ? 'var(--accent-text)' : 'var(--text-secondary)',
          backgroundColor: isStudyMode ? 'var(--bg-surface)' : 'transparent',
          borderRadius: 'var(--radius-xs)',
          boxShadow: isStudyMode ? 'var(--shadow-xs)' : 'none',
          transition: 'all var(--transition-fast)',
          display: 'flex',
          alignItems: 'center',
          gap: '4px',
        }}
      >
        <BookOpen size={12} />
        <span>Study</span>
      </button>
    </div>
  );
}
