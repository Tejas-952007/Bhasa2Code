import React, { useState, useEffect } from 'react';
import {
  Bookmark,
  MessageSquare,
  ArrowRight,
  Copy,
  Check,
  Trash2,
  Plus,
  Search,
  Code2,
  Calendar,
} from 'lucide-react';
import Button from '../components/common/Button';
import { DEMO_SAVED_ITEMS } from '../services/mockData';

export default function SavedPage({ onOpenSession }) {
  const [savedItems, setSavedItems] = useState(() => {
    try {
      const stored = localStorage.getItem('b2c_saved_items');
      return stored ? JSON.parse(stored) : DEMO_SAVED_ITEMS;
    } catch {
      return DEMO_SAVED_ITEMS;
    }
  });

  const [searchQuery, setSearchQuery] = useState('');
  const [copiedId, setCopiedId] = useState(null);
  const [isAdding, setIsAdding] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newSnippet, setNewSnippet] = useState('');
  const [newSessionTitle, setNewSessionTitle] = useState('Manual Bookmark');

  // Reload on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem('b2c_saved_items');
      if (stored) setSavedItems(JSON.parse(stored));
    } catch {}
  }, []);

  // Sync to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('b2c_saved_items', JSON.stringify(savedItems));
    } catch {}
  }, [savedItems]);

  const handleCopy = (id, text) => {
    navigator.clipboard?.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleDelete = (id) => {
    setSavedItems((prev) => prev.filter((item) => item.id !== id));
  };

  const handleAddSnippet = () => {
    if (!newTitle.trim() || !newSnippet.trim()) return;
    const now = new Date();
    const dateFormatted = now.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });

    const newItem = {
      id: `saved-${Date.now()}`,
      title: newTitle.trim(),
      sessionTitle: newSessionTitle.trim() || 'Custom Bookmark',
      sessionId: null,
      date: dateFormatted,
      snippet: newSnippet.trim(),
    };

    setSavedItems([newItem, ...savedItems]);
    setIsAdding(false);
    setNewTitle('');
    setNewSnippet('');
    setNewSessionTitle('Manual Bookmark');
  };

  const filteredItems = savedItems.filter((item) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      item.title.toLowerCase().includes(q) ||
      (item.snippet && item.snippet.toLowerCase().includes(q)) ||
      (item.sessionTitle && item.sessionTitle.toLowerCase().includes(q))
    );
  });

  return (
    <div
      style={{
        flex: 1,
        padding: '28px 24px',
        overflowY: 'auto',
        maxWidth: '860px',
        margin: '0 auto',
        width: '100%',
      }}
    >
      {/* Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'flex-start',
          justifyContent: 'space-between',
          gap: '16px',
          marginBottom: '20px',
        }}
      >
        <div>
          <h1
            style={{
              fontSize: 'var(--text-xl)',
              fontWeight: 700,
              color: 'var(--text-primary)',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
            }}
          >
            <Bookmark size={22} color="var(--accent-primary)" />
            <span>Saved Items &amp; Snippets</span>
          </h1>
          <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)', marginTop: '4px' }}>
            Bookmarked code solutions, reference algorithms, and notes from your workspace ({savedItems.length}).
          </p>
        </div>

        <Button
          variant="primary"
          size="sm"
          onClick={() => setIsAdding(!isAdding)}
          style={{ fontSize: 'var(--text-xs)', padding: '6px 12px' }}
        >
          <Plus size={14} />
          <span>{isAdding ? 'Cancel' : 'Save Snippet'}</span>
        </Button>
      </div>

      {/* Add New Snippet Form */}
      {isAdding && (
        <div
          style={{
            padding: '18px',
            backgroundColor: 'var(--bg-surface)',
            border: '1px solid var(--border-color)',
            borderRadius: 'var(--radius-md)',
            marginBottom: '20px',
            boxShadow: 'var(--shadow-sm)',
          }}
        >
          <h3
            style={{
              fontSize: 'var(--text-md)',
              fontWeight: 600,
              color: 'var(--text-primary)',
              marginBottom: '12px',
            }}
          >
            Add Custom Saved Snippet
          </h3>
          <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
            <input
              type="text"
              placeholder="Snippet title (e.g. Binary Search Loop)..."
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              style={{
                flex: 2,
                padding: '8px 12px',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                backgroundColor: 'var(--bg-app)',
                color: 'var(--text-primary)',
                fontSize: 'var(--text-sm)',
                outline: 'none',
              }}
            />
            <input
              type="text"
              placeholder="Origin / Tag (e.g. Python DAA)..."
              value={newSessionTitle}
              onChange={(e) => setNewSessionTitle(e.target.value)}
              style={{
                flex: 1,
                padding: '8px 12px',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                backgroundColor: 'var(--bg-app)',
                color: 'var(--text-primary)',
                fontSize: 'var(--text-sm)',
                outline: 'none',
              }}
            />
          </div>
          <textarea
            rows={5}
            placeholder="Paste code or reference text here..."
            value={newSnippet}
            onChange={(e) => setNewSnippet(e.target.value)}
            style={{
              width: '100%',
              padding: '10px 12px',
              fontFamily: 'var(--font-mono)',
              fontSize: 'var(--text-xs)',
              lineHeight: '1.5',
              border: '1px solid var(--border-color)',
              borderRadius: 'var(--radius-sm)',
              backgroundColor: 'var(--bg-app)',
              color: 'var(--text-primary)',
              outline: 'none',
              marginBottom: '12px',
            }}
          />
          <div style={{ display: 'flex', gap: '8px' }}>
            <Button variant="primary" size="sm" onClick={handleAddSnippet}>
              Save to Workspace
            </Button>
            <Button variant="ghost" size="sm" onClick={() => setIsAdding(false)}>
              Cancel
            </Button>
          </div>
        </div>
      )}

      {/* Search Filter Bar */}
      <div style={{ marginBottom: '16px' }}>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '8px 12px',
            backgroundColor: 'var(--bg-surface)',
            border: '1px solid var(--border-color)',
            borderRadius: 'var(--radius-sm)',
          }}
        >
          <Search size={15} color="var(--text-muted)" />
          <input
            type="text"
            placeholder="Filter saved snippets by title or code..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              flex: 1,
              border: 'none',
              outline: 'none',
              fontSize: 'var(--text-sm)',
              backgroundColor: 'transparent',
              color: 'var(--text-primary)',
            }}
          />
        </div>
      </div>

      {/* Saved Items List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        {filteredItems.length === 0 ? (
          <div
            style={{
              padding: '48px 24px',
              textAlign: 'center',
              backgroundColor: 'var(--bg-surface)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-color)',
            }}
          >
            <Bookmark size={32} color="var(--text-muted)" style={{ margin: '0 auto 10px' }} />
            <h3
              style={{
                fontSize: 'var(--text-md)',
                fontWeight: 600,
                color: 'var(--text-primary)',
                marginBottom: '4px',
              }}
            >
              No saved items found
            </h3>
            <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)' }}>
              {searchQuery
                ? 'Try a different search keyword.'
                : 'Bookmark solutions in chat or click "Save Snippet" above.'}
            </p>
          </div>
        ) : (
          filteredItems.map((item) => (
            <div
              key={item.id}
              style={{
                padding: '16px 18px',
                backgroundColor: 'var(--bg-surface)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-md)',
                boxShadow: 'var(--shadow-xs)',
                display: 'flex',
                flexDirection: 'column',
                gap: '10px',
                transition: 'border-color var(--transition-fast)',
              }}
            >
              {/* Card Header */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span
                  style={{
                    fontSize: 'var(--text-base)',
                    fontWeight: 600,
                    color: 'var(--text-primary)',
                  }}
                >
                  {item.title}
                </span>

                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span
                    style={{
                      fontSize: '0.70rem',
                      color: 'var(--text-muted)',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '4px',
                    }}
                  >
                    <Calendar size={11} />
                    {item.date}
                  </span>

                  <button
                    type="button"
                    onClick={() => handleDelete(item.id)}
                    title="Remove from saved"
                    style={{
                      padding: '4px',
                      color: 'var(--text-muted)',
                      cursor: 'pointer',
                      borderRadius: 'var(--radius-xs)',
                    }}
                    onMouseEnter={(e) => (e.currentTarget.style.color = 'var(--status-error)')}
                    onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--text-muted)')}
                  >
                    <Trash2 size={13} />
                  </button>
                </div>
              </div>

              {/* Code Snippet Box */}
              <div
                style={{
                  position: 'relative',
                  backgroundColor: 'var(--bg-code, #161a23)',
                  border: '1px solid var(--border-code, #2a3142)',
                  borderRadius: 'var(--radius-sm)',
                  overflow: 'hidden',
                }}
              >
                <div
                  style={{
                    position: 'absolute',
                    top: '6px',
                    right: '6px',
                    zIndex: 2,
                  }}
                >
                  <button
                    type="button"
                    onClick={() => handleCopy(item.id, item.snippet)}
                    title="Copy code snippet"
                    style={{
                      padding: '4px 8px',
                      fontSize: '0.68rem',
                      fontWeight: 500,
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                      color: '#f8fafc',
                      borderRadius: 'var(--radius-xs)',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '4px',
                      border: '1px solid rgba(255, 255, 255, 0.15)',
                    }}
                  >
                    {copiedId === item.id ? (
                      <>
                        <Check size={11} color="#34d399" />
                        <span>Copied</span>
                      </>
                    ) : (
                      <>
                        <Copy size={11} />
                        <span>Copy</span>
                      </>
                    )}
                  </button>
                </div>

                <pre
                  style={{
                    fontFamily: 'var(--font-mono)',
                    fontSize: 'var(--text-xs)',
                    color: 'var(--text-code, #e2e8f0)',
                    padding: '12px 14px',
                    margin: 0,
                    overflowX: 'auto',
                    lineHeight: '1.5',
                  }}
                >
                  <code>{item.snippet}</code>
                </pre>
              </div>

              {/* Card Footer: Origin Session + Open in Chat */}
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  paddingTop: '4px',
                }}
              >
                <span
                  style={{
                    fontSize: 'var(--text-xs)',
                    color: 'var(--text-secondary)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '5px',
                  }}
                >
                  <MessageSquare size={13} style={{ opacity: 0.7 }} />
                  <span>Session: {item.sessionTitle || 'Workspace'}</span>
                </span>

                {item.sessionId && onOpenSession ? (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => onOpenSession(item.sessionId)}
                    style={{ fontSize: 'var(--text-xs)', gap: '4px' }}
                  >
                    <span>Open in Chat</span>
                    <ArrowRight size={13} />
                  </Button>
                ) : (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => onOpenSession && onOpenSession(null)}
                    style={{ fontSize: 'var(--text-xs)', gap: '4px' }}
                  >
                    <span>Open Workspace</span>
                    <ArrowRight size={13} />
                  </Button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
