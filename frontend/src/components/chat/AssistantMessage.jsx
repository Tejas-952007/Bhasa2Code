import React, { useState } from 'react';
import ResponseRenderer from '../response/ResponseRenderer';
import { Terminal, Copy, Check } from 'lucide-react';

/**
 * AssistantMessage
 * Professional assistant message wrapper.
 * Identity: Bhasha2Code (never "AI", "AI Assistant", or sparkles).
 */
export default function AssistantMessage({
  message,
  isStudyMode = false,
  onSelectSuggestion = null,
  onCodeChange = null,
}) {
  const [copied, setCopied] = useState(false);

  const handleCopyFull = () => {
    let fullText = message.content || '';
    if (message.codeBlock?.code) {
      fullText += `\n\n\`\`\`${message.codeBlock.language || 'text'}\n${message.codeBlock.code}\n\`\`\``;
    }
    if (message.explanation && message.explanation.length > 0) {
      fullText += `\n\nExplanation:\n${message.explanation.map((e) => `- ${e}`).join('\n')}`;
    }
    navigator.clipboard?.writeText(fullText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      style={{
        margin: '16px 0',
        padding: '18px 22px',
        backgroundColor: 'var(--bg-surface)',
        borderRadius: 'var(--radius-lg)',
        border: '1px solid var(--border-color)',
        boxShadow: 'var(--shadow-xs)',
      }}
    >
      {/* Assistant Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '14px',
          paddingBottom: '10px',
          borderBottom: '1px solid var(--border-subtle)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div
            style={{
              width: '22px',
              height: '22px',
              borderRadius: 'var(--radius-xs)',
              backgroundColor: '#1e293b',
              color: '#93c5fd',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Terminal size={12} strokeWidth={2.5} />
          </div>
          <span
            style={{
              fontSize: 'var(--text-sm)',
              fontWeight: 700,
              color: 'var(--text-primary)',
              letterSpacing: '-0.01em',
            }}
          >
            Bhasha2Code
          </span>
        </div>

        {/* Quiet Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <button
            type="button"
            onClick={handleCopyFull}
            title="Copy assistant response"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              fontSize: 'var(--text-xs)',
              color: 'var(--text-muted)',
              backgroundColor: 'transparent',
              border: 'none',
              cursor: 'pointer',
              padding: '3px 6px',
              borderRadius: 'var(--radius-xs)',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.color = 'var(--text-primary)')}
            onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--text-muted)')}
          >
            {copied ? <Check size={12} color="var(--status-success)" /> : <Copy size={12} />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
        </div>
      </div>

      {/* Response Renderer: Orchestrates text, sections, code artifacts, and study mode */}
      <ResponseRenderer
        message={message}
        isStudyMode={isStudyMode}
        onSelectSuggestion={onSelectSuggestion}
        onCodeChange={onCodeChange}
      />
    </div>
  );
}
