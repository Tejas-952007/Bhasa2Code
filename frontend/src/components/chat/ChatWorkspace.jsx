import React, { useRef, useEffect } from 'react';
import UserMessage from './UserMessage';
import AssistantMessage from './AssistantMessage';
import Composer from './Composer';
import EmptyState from '../common/EmptyState';
import { Terminal } from 'lucide-react';

export default function ChatWorkspace({
  messages = [],
  isStudyMode = false,
  onSendMessage,
  activeSessionTitle = 'Python Calculator',
  contextHint = 'Using current session context',
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isStudyMode]);

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
          padding: 'var(--space-4) var(--space-6)',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <div
          style={{
            maxWidth: '820px',
            width: '100%',
            margin: '0 auto',
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
              <div ref={bottomRef} style={{ height: '16px' }} />
            </div>
          )}
        </div>
      </div>

      {/* Bottom Composer Bar */}
      <div
        style={{
          padding: '12px 20px 16px',
          backgroundColor: 'var(--bg-app)',
          borderTop: '1px solid var(--border-subtle)',
        }}
      >
        <div
          style={{
            maxWidth: '820px',
            margin: '0 auto',
            width: '100%',
          }}
        >
          <Composer onSend={onSendMessage} />
        </div>
      </div>
    </div>
  );
}
