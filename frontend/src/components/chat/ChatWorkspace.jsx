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
          <Composer onSend={onSendMessage} />
        </div>
      </div>
    </div>
  );
}
