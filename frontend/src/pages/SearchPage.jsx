import React, { useState } from 'react';
import { Search as SearchIcon, MessageSquare, FileText, ArrowRight } from 'lucide-react';
import { INITIAL_SESSIONS, DEMO_NOTES, DEMO_SAVED_ITEMS } from '../services/mockData';
import Button from '../components/common/Button';

export default function SearchPage({ onSelectSession }) {
  const [query, setQuery] = useState('');

  const filterText = (text) => text.toLowerCase().includes(query.toLowerCase());

  const matchedSessions = query ? INITIAL_SESSIONS.filter((s) => filterText(s.title)) : INITIAL_SESSIONS;
  const matchedNotes = query ? DEMO_NOTES.filter((n) => filterText(n.title) || filterText(n.content)) : DEMO_NOTES;

  return (
    <div
      style={{
        flex: 1,
        padding: 'var(--space-8) var(--space-6)',
        overflowY: 'auto',
        maxWidth: '720px',
        margin: '0 auto',
        width: '100%',
      }}
    >
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: 'var(--text-xl)', fontWeight: 600, marginBottom: '12px' }}>
          Search Workspace
        </h1>

        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            padding: '10px 14px',
            backgroundColor: 'var(--bg-surface)',
            border: '1px solid var(--border-color)',
            borderRadius: 'var(--radius-sm)',
            boxShadow: 'var(--shadow-xs)',
          }}
        >
          <SearchIcon size={16} color="var(--text-muted)" />
          <input
            type="text"
            placeholder="Search sessions, messages and notes..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
            style={{
              flex: 1,
              border: 'none',
              outline: 'none',
              fontSize: 'var(--text-base)',
              backgroundColor: 'transparent',
              color: 'var(--text-primary)',
            }}
          />
        </div>
      </div>

      {/* Sessions Match */}
      <div style={{ marginBottom: '28px' }}>
        <h2 style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px' }}>
          Sessions ({matchedSessions.length})
        </h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
          {matchedSessions.map((s) => (
            <button
              key={s.id}
              type="button"
              onClick={() => onSelectSession && onSelectSession(s.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '10px 14px',
                backgroundColor: 'var(--bg-surface)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                textAlign: 'left',
                cursor: 'pointer',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <MessageSquare size={14} color="var(--accent-primary)" />
                <span style={{ fontWeight: 500, color: 'var(--text-primary)' }}>{s.title}</span>
              </div>
              <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)' }}>{s.lastUpdated}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Notes Match */}
      <div>
        <h2 style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px' }}>
          Notes ({matchedNotes.length})
        </h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
          {matchedNotes.map((n) => (
            <div
              key={n.id}
              style={{
                padding: '12px 14px',
                backgroundColor: 'var(--bg-surface)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                <FileText size={14} color="var(--text-muted)" />
                <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{n.title}</span>
              </div>
              <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
                {n.content}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
