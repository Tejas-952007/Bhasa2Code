import React, { useRef, useEffect } from 'react';
import UserMessage from './UserMessage';
import AssistantMessage from './AssistantMessage';
import Composer from './Composer';
import EmptyState from '../common/EmptyState';
import { Terminal } from 'lucide-react';

export default function ChatWorkspace({
  messages = [],
  isStudyMode = false,
  isLoading = false,
  errorMessage = null,
  onRetry = null,
  onSendMessage,
  activeSessionTitle = 'Python Calculator',
  contextHint = 'Using current session context',
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isStudyMode, isLoading, errorMessage]);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        width: '100%',
        backgroundColor: 'var(--bg-app)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Context Banner (quiet, subtle inline indicator) */}
      {messages.length > 0 && (
        <div
          style={{
            padding: '6px 20px',
            backgroundColor: 'var(--bg-surface)',
            borderBottom: '1px solid var(--border-subtle)',
            fontSize: 'var(--text-xs)',
            color: 'var(--text-muted)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            userSelect: 'none',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>
              {activeSessionTitle}
            </span>
            <span>·</span>
            <span>{contextHint}</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Terminal size={11} />
            <span>Python 3.12 sandbox</span>
          </div>
        </div>
      )}

      {/* Main Scrollable Messages Container */}
      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '20px 24px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <div
          style={{
            maxWidth: '880px',
            width: '100%',
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          {messages.length === 0 ? (
            <EmptyState onSelectPrompt={(p) => onSendMessage && onSendMessage(p)} />
          ) : (
            <div>
              {messages.map((msg) =>
                msg.role === 'user' ? (
                  <UserMessage key={msg.id} message={msg} />
                ) : (
                  <AssistantMessage
                    key={msg.id}
                    message={msg}
                    isStudyMode={isStudyMode}
                  />
                )
              )}

              {/* Generating response loading state */}
              {isLoading && (
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    padding: '14px 18px',
                    margin: '14px 0',
                    backgroundColor: 'var(--bg-surface)',
                    border: '1px solid var(--border-color)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--text-secondary)',
                    fontSize: 'var(--text-sm)',
                    boxShadow: 'var(--shadow-sm)',
                  }}
                >
                  <div
                    style={{
                      width: '8px',
                      height: '8px',
                      borderRadius: '50%',
                      backgroundColor: 'var(--accent-primary)',
                      boxShadow: '0 0 8px var(--accent-primary)',
                    }}
                  />
                  <span style={{ fontWeight: 500 }}>Generating response...</span>
                </div>
              )}

              {/* Error State */}
              {errorMessage && (
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '12px 18px',
                    margin: '14px 0',
                    backgroundColor: 'var(--status-error-bg, #fef2f2)',
                    border: '1px solid var(--status-error-border, #fecaca)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--status-error, #b91c1c)',
                    fontSize: 'var(--text-sm)',
                  }}
                >
                  <span>{errorMessage}</span>
                  {onRetry && (
                    <button
                      type="button"
                      onClick={onRetry}
                      style={{
                        padding: '4px 10px',
                        backgroundColor: 'transparent',
                        border: '1px solid var(--status-error, #b91c1c)',
                        color: 'var(--status-error, #b91c1c)',
                        borderRadius: 'var(--radius-xs)',
                        fontSize: 'var(--text-xs)',
                        fontWeight: 600,
                        cursor: 'pointer',
                      }}
                    >
                      Retry
                    </button>
                  )}
                </div>
              )}

              <div ref={bottomRef} style={{ height: '20px' }} />
            </div>
          )}
        </div>
      </div>

      {/* Bottom Composer Bar */}
      <div
        style={{
          padding: '12px 24px 18px',
          backgroundColor: 'var(--bg-app)',
          borderTop: '1px solid var(--border-color)',
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <div
          style={{
            maxWidth: '880px',
            width: '100%',
          }}
        >
          <Composer onSend={onSendMessage} disabled={isLoading} />
        </div>
      </div>
    </div>
  );
}
