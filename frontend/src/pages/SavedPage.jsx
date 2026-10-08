import React from 'react';
import { Bookmark, MessageSquare, ArrowRight } from 'lucide-react';
import Button from '../components/common/Button';
import { DEMO_SAVED_ITEMS } from '../services/mockData';

export default function SavedPage({ onOpenSession }) {
  return (
    <div
      style={{
        flex: 1,
        padding: 'var(--space-8) var(--space-6)',
        overflowY: 'auto',
        maxWidth: '820px',
        margin: '0 auto',
        width: '100%',
      }}
    >
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: 'var(--text-xl)', fontWeight: 600, marginBottom: '4px' }}>
          Saved Items
        </h1>
        <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)' }}>
          Bookmarked code solutions and theoretical explanations from your workspace.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {DEMO_SAVED_ITEMS.map((item) => (
          <div
            key={item.id}
            style={{
              padding: '16px',
              backgroundColor: 'var(--bg-surface)',
              border: '1px solid var(--border-color)',
              borderRadius: 'var(--radius-sm)',
              boxShadow: 'var(--shadow-xs)',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: 'var(--text-base)', fontWeight: 600, color: 'var(--text-primary)' }}>
                {item.title}
              </span>
              <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)' }}>
                {item.date}
              </span>
            </div>

            <div
              style={{
                fontFamily: 'var(--font-mono)',
                fontSize: 'var(--text-xs)',
                backgroundColor: 'var(--bg-subtle)',
                padding: '8px 10px',
                borderRadius: 'var(--radius-xs)',
                color: 'var(--text-secondary)',
                overflowX: 'auto',
              }}
            >
              {item.snippet}
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '4px' }}>
              <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <MessageSquare size={12} />
                <span>Session: {item.sessionTitle}</span>
              </span>

              <Button
                variant="ghost"
                size="sm"
                onClick={() => onOpenSession && onOpenSession('session-1')}
              >
                <span>Open in Chat</span>
                <ArrowRight size={12} />
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
