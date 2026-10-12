import React, { useState } from 'react';
import {
  Search as SearchIcon,
  MessageSquare,
  FileText,
  Bookmark,
  ArrowRight,
  X,
  Code2,
  Calendar,
} from 'lucide-react';
import Button from '../components/common/Button';
import { DEMO_NOTES, DEMO_SAVED_ITEMS } from '../services/mockData';

export default function SearchPage({
  sessions = [],
  onSelectSession,
  onSelectView,
}) {
  const [query, setQuery] = useState('');
  const [activeTab, setActiveTab] = useState('all'); // 'all' | 'sessions' | 'notes' | 'saved'

  // Retrieve user notes
  const [notes, setNotes] = useState(() => {
    try {
      const stored = localStorage.getItem('b2c_notes');
      return stored ? JSON.parse(stored) : DEMO_NOTES;
    } catch {
      return DEMO_NOTES;
    }
  });

  // Retrieve user saved snippets
  const [savedItems, setSavedItems] = useState(() => {
    try {
      const stored = localStorage.getItem('b2c_saved_items');
      return stored ? JSON.parse(stored) : DEMO_SAVED_ITEMS;
    } catch {
      return DEMO_SAVED_ITEMS;
    }
  });

  // Reload notes & saved snippets whenever page mounts or gains focus
  React.useEffect(() => {
    try {
      const storedNotes = localStorage.getItem('b2c_notes');
      if (storedNotes) setNotes(JSON.parse(storedNotes));
      const storedSaved = localStorage.getItem('b2c_saved_items');
      if (storedSaved) setSavedItems(JSON.parse(storedSaved));
    } catch {}
  }, []);

  const filterText = (text) => {
    if (!text) return false;
    return text.toLowerCase().includes(query.trim().toLowerCase());
  };

  const isQueryActive = query.trim().length > 0;

  // Filtered lists
  const matchedSessions = isQueryActive
    ? sessions.filter(
        (s) =>
          filterText(s.title) ||
          filterText(s.programming_language) ||
          filterText(s.current_language)
      )
    : sessions;

  const matchedNotes = isQueryActive
    ? notes.filter((n) => filterText(n.title) || filterText(n.content))
    : notes;

  const matchedSaved = isQueryActive
    ? savedItems.filter(
        (item) =>
          filterText(item.title) ||
          filterText(item.snippet) ||
          filterText(item.sessionTitle)
      )
    : savedItems;

  const totalMatches =
    matchedSessions.length + matchedNotes.length + matchedSaved.length;

  const tabButtonStyle = (tabKey) => {
    const isActive = activeTab === tabKey;
    return {
      padding: '6px 14px',
      borderRadius: 'var(--radius-sm)',
      fontSize: 'var(--text-xs)',
      fontWeight: isActive ? 600 : 500,
      backgroundColor: isActive ? 'var(--accent-subtle)' : 'var(--bg-surface)',
      color: isActive ? 'var(--accent-text)' : 'var(--text-secondary)',
      border: isActive ? '1px solid var(--accent-primary)' : '1px solid var(--border-color)',
      cursor: 'pointer',
      display: 'inline-flex',
      alignItems: 'center',
      gap: '6px',
      transition: 'all var(--transition-fast)',
    };
  };

  return (
    <div
      style={{
        flex: 1,
        padding: '28px 24px',
        overflowY: 'auto',
        maxWidth: '820px',
        margin: '0 auto',
        width: '100%',
      }}
    >
      {/* Header & Search Input */}
      <div style={{ marginBottom: '24px' }}>
        <h1
          style={{
            fontSize: 'var(--text-xl)',
            fontWeight: 700,
            marginBottom: '6px',
            color: 'var(--text-primary)',
          }}
        >
          Search Workspace
        </h1>
        <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)', marginBottom: '16px' }}>
          Instantly find conversations, generated code snippets, algorithms, and study notes across your workspace.
        </p>

        {/* Big Search Input */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            padding: '12px 16px',
            backgroundColor: 'var(--bg-surface)',
            border: '1px solid var(--border-color)',
            borderRadius: 'var(--radius-md)',
            boxShadow: 'var(--shadow-sm)',
            transition: 'border-color var(--transition-fast)',
          }}
        >
          <SearchIcon size={18} color="var(--accent-primary)" style={{ flexShrink: 0 }} />
          <input
            type="text"
            placeholder="Type keywords (e.g. Binary Search, recursion, Python, Logistic Regression)..."
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
          {query && (
            <button
              type="button"
              onClick={() => setQuery('')}
              title="Clear search"
              style={{
                padding: '4px',
                color: 'var(--text-muted)',
                borderRadius: 'var(--radius-xs)',
                cursor: 'pointer',
              }}
            >
              <X size={16} />
            </button>
          )}
        </div>

        {/* Filter Tabs */}
        <div style={{ display: 'flex', gap: '8px', marginTop: '14px', flexWrap: 'wrap' }}>
          <button
            type="button"
            onClick={() => setActiveTab('all')}
            style={tabButtonStyle('all')}
          >
            All Results ({totalMatches})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('sessions')}
            style={tabButtonStyle('sessions')}
          >
            <MessageSquare size={13} />
            Sessions ({matchedSessions.length})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('notes')}
            style={tabButtonStyle('notes')}
          >
            <FileText size={13} />
            Notes ({matchedNotes.length})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('saved')}
            style={tabButtonStyle('saved')}
          >
            <Bookmark size={13} />
            Saved ({matchedSaved.length})
          </button>
        </div>
      </div>

      {/* No Results Fallback */}
      {totalMatches === 0 && (
        <div
          style={{
            padding: '48px 24px',
            textAlign: 'center',
            backgroundColor: 'var(--bg-surface)',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border-color)',
          }}
        >
          <SearchIcon size={32} color="var(--text-muted)" style={{ margin: '0 auto 12px' }} />
          <h3 style={{ fontSize: 'var(--text-md)', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '4px' }}>
            No matches found for "{query}"
          </h3>
          <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)' }}>
            Try searching with broader terms or check spelling.
          </p>
        </div>
      )}

      {/* 1. Matched Sessions */}
      {(activeTab === 'all' || activeTab === 'sessions') && matchedSessions.length > 0 && (
        <div style={{ marginBottom: '28px' }}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '10px',
            }}
          >
            <h2
              style={{
                fontSize: 'var(--text-xs)',
                fontWeight: 600,
                color: 'var(--text-muted)',
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
              }}
            >
              <MessageSquare size={13} />
              <span>Chat Sessions ({matchedSessions.length})</span>
            </h2>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {matchedSessions.map((s) => (
              <div
                key={s.id}
                onClick={() => onSelectSession && onSelectSession(s.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px 16px',
                  backgroundColor: 'var(--bg-surface)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  boxShadow: 'var(--shadow-xs)',
                  cursor: 'pointer',
                  transition: 'border-color var(--transition-fast), transform var(--transition-fast)',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = 'var(--accent-primary)';
                  e.currentTarget.style.transform = 'translateY(-1px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = 'var(--border-color)';
                  e.currentTarget.style.transform = 'translateY(0)';
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', overflow: 'hidden' }}>
                  <div
                    style={{
                      width: '28px',
                      height: '28px',
                      borderRadius: 'var(--radius-xs)',
                      backgroundColor: 'var(--accent-subtle)',
                      color: 'var(--accent-primary)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0,
                    }}
                  >
                    <MessageSquare size={15} />
                  </div>
                  <div style={{ overflow: 'hidden' }}>
                    <div
                      style={{
                        fontWeight: 600,
                        fontSize: 'var(--text-sm)',
                        color: 'var(--text-primary)',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {s.title}
                    </div>
                    <span style={{ fontSize: '0.70rem', color: 'var(--text-muted)' }}>
                      Language: {s.programming_language || 'python'} · Active
                    </span>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
                  <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)' }}>
                    {s.created_at ? new Date(s.created_at).toLocaleDateString() : 'Recent'}
                  </span>
                  <ArrowRight size={14} color="var(--text-muted)" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 2. Matched Notes */}
      {(activeTab === 'all' || activeTab === 'notes') && matchedNotes.length > 0 && (
        <div style={{ marginBottom: '28px' }}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '10px',
            }}
          >
            <h2
              style={{
                fontSize: 'var(--text-xs)',
                fontWeight: 600,
                color: 'var(--text-muted)',
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
              }}
            >
              <FileText size={13} />
              <span>Workspace Notes ({matchedNotes.length})</span>
            </h2>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {matchedNotes.map((n) => (
              <div
                key={n.id}
                onClick={() => onSelectView && onSelectView('notes', { noteId: n.id })}
                style={{
                  padding: '14px 16px',
                  backgroundColor: 'var(--bg-surface)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  boxShadow: 'var(--shadow-xs)',
                  cursor: 'pointer',
                  transition: 'border-color var(--transition-fast)',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.borderColor = 'var(--accent-primary)')}
                onMouseLeave={(e) => (e.currentTarget.style.borderColor = 'var(--border-color)')}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <FileText size={15} color="var(--accent-primary)" />
                    <span style={{ fontWeight: 600, fontSize: 'var(--text-sm)', color: 'var(--text-primary)' }}>
                      {n.title}
                    </span>
                  </div>
                  <span style={{ fontSize: '0.70rem', color: 'var(--text-muted)' }}>
                    {n.date}
                  </span>
                </div>
                <p
                  style={{
                    fontSize: 'var(--text-xs)',
                    color: 'var(--text-secondary)',
                    lineHeight: '1.5',
                    margin: 0,
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden',
                  }}
                >
                  {n.content}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 3. Matched Saved Items */}
      {(activeTab === 'all' || activeTab === 'saved') && matchedSaved.length > 0 && (
        <div style={{ marginBottom: '28px' }}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '10px',
            }}
          >
            <h2
              style={{
                fontSize: 'var(--text-xs)',
                fontWeight: 600,
                color: 'var(--text-muted)',
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
              }}
            >
              <Bookmark size={13} />
              <span>Saved Snippets ({matchedSaved.length})</span>
            </h2>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {matchedSaved.map((item) => (
              <div
                key={item.id}
                onClick={() => onSelectView && onSelectView('saved')}
                style={{
                  padding: '14px 16px',
                  backgroundColor: 'var(--bg-surface)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  boxShadow: 'var(--shadow-xs)',
                  cursor: 'pointer',
                  transition: 'border-color var(--transition-fast)',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.borderColor = 'var(--accent-primary)')}
                onMouseLeave={(e) => (e.currentTarget.style.borderColor = 'var(--border-color)')}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Bookmark size={15} color="var(--accent-primary)" />
                    <span style={{ fontWeight: 600, fontSize: 'var(--text-sm)', color: 'var(--text-primary)' }}>
                      {item.title}
                    </span>
                  </div>
                  <span style={{ fontSize: '0.70rem', color: 'var(--text-muted)' }}>
                    {item.date}
                  </span>
                </div>

                <div
                  style={{
                    fontFamily: 'var(--font-mono)',
                    fontSize: 'var(--text-xs)',
                    backgroundColor: 'var(--bg-subtle)',
                    padding: '6px 10px',
                    borderRadius: 'var(--radius-xs)',
                    color: 'var(--text-secondary)',
                    overflow: 'hidden',
                    whiteSpace: 'nowrap',
                    textOverflow: 'ellipsis',
                  }}
                >
                  {item.snippet}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
