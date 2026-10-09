import React, { useState, useRef, useEffect } from 'react';
import { ArrowUp, Square } from 'lucide-react';

export default function Composer({
  onSend,
  onStop = null,
  disabled = false,
  isStreaming = false,
  placeholder = "Ask anything about coding...",
}) {
  const [text, setText] = useState('');
  const textareaRef = useRef(null);
  const isSubmittingRef = useRef(false);

  // Auto-resize textarea height up to a max
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const scrollHeight = textareaRef.current.scrollHeight;
      textareaRef.current.style.height = `${Math.min(scrollHeight, 140)}px`;
    }
  }, [text]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent?.isComposing && !e.repeat) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleSubmit = () => {
    if (isStreaming) {
      if (onStop) onStop();
      return;
    }

    const trimmed = text.trim();
    if (!trimmed || disabled || isSubmittingRef.current) return;

    isSubmittingRef.current = true;
    if (onSend) {
      onSend(trimmed);
    }
    setText('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }

    setTimeout(() => {
      isSubmittingRef.current = false;
    }, 400);
  };

  const hasContent = text.trim().length > 0;

  return (
    <div
      style={{
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-lg)',
        backgroundColor: 'var(--bg-surface)',
        boxShadow: '0 4px 18px rgba(15, 23, 42, 0.06)',
        transition: 'border-color var(--transition-fast), box-shadow var(--transition-fast)',
        padding: '10px 14px',
        display: 'flex',
        alignItems: 'flex-end',
        gap: '10px',
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
        disabled={disabled && !isStreaming}
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

      {isStreaming ? (
        <button
          type="button"
          onClick={onStop}
          title="Stop generation"
          aria-label="Stop generation"
          style={{
            padding: '4px 10px',
            height: '28px',
            borderRadius: 'var(--radius-sm)',
            backgroundColor: '#1e293b',
            color: '#f8fafc',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: 'var(--text-xs)',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'all var(--transition-fast)',
            border: '1px solid #334155',
            flexShrink: 0,
            marginBottom: '3px',
          }}
        >
          <Square size={11} fill="currentColor" />
          <span>Stop</span>
        </button>
      ) : (
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
            cursor: hasContent && !disabled ? 'pointer' : 'default',
            transition: 'all var(--transition-fast)',
            border: 'none',
            flexShrink: 0,
            marginBottom: '3px',
          }}
        >
          <ArrowUp size={16} strokeWidth={2.5} />
        </button>
      )}
    </div>
  );
}
