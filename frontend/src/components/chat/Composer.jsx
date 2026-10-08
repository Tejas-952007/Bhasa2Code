import React, { useState, useRef, useEffect } from 'react';
import { ArrowUp } from 'lucide-react';

export default function Composer({ onSend, disabled = false, placeholder = "Ask anything about coding..." }) {
  const [text, setText] = useState('');
  const textareaRef = useRef(null);

  // Auto-resize textarea height up to a max
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const scrollHeight = textareaRef.current.scrollHeight;
      textareaRef.current.style.height = `${Math.min(scrollHeight, 140)}px`;
    }
  }, [text]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleSubmit = () => {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    if (onSend) {
      onSend(trimmed);
    }
    setText('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const hasContent = text.trim().length > 0;

  return (
    <div
      style={{
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-md)',
        backgroundColor: 'var(--bg-surface)',
        boxShadow: 'var(--shadow-xs)',
        transition: 'border-color var(--transition-fast), box-shadow var(--transition-fast)',
        padding: '6px 10px',
        display: 'flex',
        alignItems: 'flex-end',
        gap: '8px',
      }}
      className="b2c-composer-container"
    >
      <textarea
        ref={textareaRef}
        rows={1}
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        style={{
          flex: 1,
          border: 'none',
          outline: 'none',
          backgroundColor: 'transparent',
          resize: 'none',
          fontSize: 'var(--text-base)',
          color: 'var(--text-primary)',
          fontFamily: 'var(--font-sans)',
          lineHeight: 'var(--leading-normal)',
          padding: '6px 4px',
          maxHeight: '140px',
        }}
      />

      <button
        type="button"
        onClick={handleSubmit}
        disabled={!hasContent || disabled}
        title="Send message (Enter)"
        aria-label="Send message"
        style={{
          width: '28px',
          height: '28px',
          borderRadius: 'var(--radius-sm)',
          backgroundColor: hasContent ? 'var(--accent-primary)' : 'var(--bg-subtle)',
          color: hasContent ? '#ffffff' : 'var(--text-muted)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: hasContent ? 'pointer' : 'default',
          transition: 'all var(--transition-fast)',
          border: 'none',
          flexShrink: 0,
          marginBottom: '3px',
        }}
      >
        <ArrowUp size={16} strokeWidth={2.5} />
      </button>
    </div>
  );
}
