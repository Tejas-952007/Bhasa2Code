import React, { useState, useEffect } from 'react';
import {
  Plus,
  Trash2,
  Edit2,
  Check,
  X,
  Download,
  ArrowLeft,
  FileText,
  Search,
  Calendar,
} from 'lucide-react';
import Button from '../components/common/Button';
import { DEMO_NOTES } from '../services/mockData';

export default function NotesPage({ initialNoteId = null, onBackToChat }) {
  const [notes, setNotes] = useState(() => {
    try {
      const saved = localStorage.getItem('b2c_notes');
      return saved ? JSON.parse(saved) : DEMO_NOTES;
    } catch {
      return DEMO_NOTES;
    }
  });

  const [selectedNoteId, setSelectedNoteId] = useState(() => {
    if (initialNoteId) return initialNoteId;
    try {
      const saved = localStorage.getItem('b2c_notes');
      const list = saved ? JSON.parse(saved) : DEMO_NOTES;
      return list[0]?.id || null;
    } catch {
      return DEMO_NOTES[0]?.id || null;
    }
  });

  useEffect(() => {
    if (initialNoteId) {
      setSelectedNoteId(initialNoteId);
    }
  }, [initialNoteId]);

  const [searchQuery, setSearchQuery] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newContent, setNewContent] = useState('');
  const [editTitle, setEditTitle] = useState('');
  const [editContent, setEditContent] = useState('');
  const [confirmDeleteId, setConfirmDeleteId] = useState(null);

  // Sync to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('b2c_notes', JSON.stringify(notes));
    } catch {}
  }, [notes]);

  const activeNote = notes.find((n) => n.id === selectedNoteId) || notes[0];

  const handleStartCreate = () => {
    setIsCreating(true);
    setIsEditing(false);
    setNewTitle('');
    setNewContent('');
  };

  const handleCreateNote = () => {
    if (!newTitle.trim()) return;
    const now = new Date();
    const dateFormatted = now.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });

    const newNote = {
      id: `note-${Date.now()}`,
      title: newTitle.trim(),
      date: dateFormatted,
      content: newContent.trim() || 'No content added.',
    };

    const updated = [newNote, ...notes];
    setNotes(updated);
    setSelectedNoteId(newNote.id);
    setIsCreating(false);
    setNewTitle('');
    setNewContent('');
  };

  const handleStartEdit = () => {
    if (!activeNote) return;
    setIsEditing(true);
    setIsCreating(false);
    setEditTitle(activeNote.title);
    setEditContent(activeNote.content);
  };

  const handleSaveEdit = () => {
    if (!editTitle.trim() || !activeNote) return;
    const now = new Date();
    const dateFormatted = now.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });

    const updated = notes.map((n) =>
      n.id === activeNote.id
        ? {
            ...n,
            title: editTitle.trim(),
            content: editContent.trim(),
            date: dateFormatted,
          }
        : n
    );
    setNotes(updated);
    setIsEditing(false);
  };

  const handleDeleteNote = (noteId) => {
    const remaining = notes.filter((n) => n.id !== noteId);
    setNotes(remaining);
    setConfirmDeleteId(null);
    if (selectedNoteId === noteId) {
      setSelectedNoteId(remaining[0]?.id || null);
    }
  };

  const handleExportSingleNote = (note) => {
    if (!note) return;
    const md = `# ${note.title}\n*Last updated: ${note.date}*\n\n${note.content}\n`;
    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${note.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.md`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const filteredNotes = notes.filter((n) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return n.title.toLowerCase().includes(q) || (n.content && n.content.toLowerCase().includes(q));
  });

  return (
    <div
      style={{
        display: 'flex',
        height: '100%',
        width: '100%',
        backgroundColor: 'var(--bg-app)',
        overflow: 'hidden',
      }}
    >
      {/* Left Column: Notes List */}
      <div
        style={{
          width: '300px',
          borderRight: '1px solid var(--border-color)',
          backgroundColor: 'var(--bg-surface)',
          display: 'flex',
          flexDirection: 'column',
          flexShrink: 0,
        }}
      >
        {/* Header */}
        <div
          style={{
            padding: '14px 16px',
            borderBottom: '1px solid var(--border-color)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {onBackToChat && (
              <button
                type="button"
                onClick={onBackToChat}
                title="Back to Chat"
                style={{
                  padding: '4px',
                  borderRadius: 'var(--radius-xs)',
                  color: 'var(--text-muted)',
                  cursor: 'pointer',
                }}
              >
                <ArrowLeft size={16} />
              </button>
            )}
            <h2 style={{ fontSize: 'var(--text-md)', fontWeight: 600, color: 'var(--text-primary)' }}>
              Workspace Notes
            </h2>
          </div>

          <Button
            variant="primary"
            size="sm"
            onClick={handleStartCreate}
            style={{ fontSize: 'var(--text-xs)', padding: '5px 10px' }}
          >
            <Plus size={14} />
            <span>New Note</span>
          </Button>
        </div>

        {/* Search Notes Filter */}
        <div style={{ padding: '8px 12px', borderBottom: '1px solid var(--border-subtle)' }}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 10px',
              backgroundColor: 'var(--bg-subtle)',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-color)',
            }}
          >
            <Search size={13} style={{ color: 'var(--text-muted)', flexShrink: 0 }} />
            <input
              type="text"
              placeholder="Search notes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                border: 'none',
                outline: 'none',
                backgroundColor: 'transparent',
                fontSize: 'var(--text-xs)',
                color: 'var(--text-primary)',
              }}
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                style={{ color: 'var(--text-muted)', padding: '0 2px' }}
              >
                <X size={12} />
              </button>
            )}
          </div>
        </div>

        {/* Scrollable Notes List */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '8px' }}>
          {filteredNotes.length === 0 ? (
            <div
              style={{
                padding: '24px 12px',
                textAlign: 'center',
                color: 'var(--text-muted)',
                fontSize: 'var(--text-xs)',
              }}
            >
              {searchQuery ? 'No matching notes found.' : 'No notes yet. Click "+ New Note" to start.'}
            </div>
          ) : (
            filteredNotes.map((note) => {
              const isSelected = note.id === selectedNoteId && !isCreating;
              return (
                <div
                  key={note.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    borderRadius: 'var(--radius-sm)',
                    backgroundColor: isSelected ? 'var(--accent-subtle)' : 'transparent',
                    borderLeft: isSelected
                      ? '3px solid var(--accent-primary)'
                      : '3px solid transparent',
                    marginBottom: '4px',
                    transition: 'all var(--transition-fast)',
                  }}
                >
                  <button
                    type="button"
                    onClick={() => {
                      setSelectedNoteId(note.id);
                      setIsCreating(false);
                      setIsEditing(false);
                    }}
                    style={{
                      flex: 1,
                      display: 'flex',
                      flexDirection: 'column',
                      textAlign: 'left',
                      padding: '10px 12px',
                      border: 'none',
                      backgroundColor: 'transparent',
                      cursor: 'pointer',
                      overflow: 'hidden',
                    }}
                  >
                    <span
                      style={{
                        fontSize: 'var(--text-sm)',
                        fontWeight: isSelected ? 600 : 500,
                        color: isSelected ? 'var(--accent-text)' : 'var(--text-primary)',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                        width: '100%',
                      }}
                    >
                      {note.title}
                    </span>
                    <span
                      style={{
                        fontSize: '0.70rem',
                        color: 'var(--text-muted)',
                        marginTop: '3px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px',
                      }}
                    >
                      <Calendar size={10} />
                      {note.date}
                    </span>
                  </button>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Right Column: Note Content / Editor */}
      <div
        style={{
          flex: 1,
          padding: '28px 36px',
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <div style={{ maxWidth: '780px', width: '100%' }}>
          {isCreating ? (
            /* Creating Form */
            <div
              style={{
                backgroundColor: 'var(--bg-surface)',
                padding: '24px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-color)',
                boxShadow: 'var(--shadow-xs)',
              }}
            >
              <h3 style={{ fontSize: 'var(--text-lg)', fontWeight: 600, marginBottom: '16px', color: 'var(--text-primary)' }}>
                Create New Note
              </h3>
              <input
                type="text"
                placeholder="Enter note title..."
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                autoFocus
                style={{
                  width: '100%',
                  padding: '10px 14px',
                  fontSize: 'var(--text-base)',
                  fontWeight: 600,
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  marginBottom: '14px',
                  backgroundColor: 'var(--bg-app)',
                  color: 'var(--text-primary)',
                  outline: 'none',
                }}
              />
              <textarea
                rows={14}
                placeholder="Write your study notes, insights, algorithms or reference code here..."
                value={newContent}
                onChange={(e) => setNewContent(e.target.value)}
                style={{
                  width: '100%',
                  padding: '14px',
                  fontSize: 'var(--text-sm)',
                  fontFamily: 'var(--font-sans)',
                  lineHeight: 'var(--leading-relaxed)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  marginBottom: '16px',
                  backgroundColor: 'var(--bg-app)',
                  color: 'var(--text-primary)',
                  outline: 'none',
                  resize: 'vertical',
                }}
              />
              <div style={{ display: 'flex', gap: '8px' }}>
                <Button variant="primary" onClick={handleCreateNote}>
                  Save Note
                </Button>
                <Button variant="ghost" onClick={() => setIsCreating(false)}>
                  Cancel
                </Button>
              </div>
            </div>
          ) : isEditing ? (
            /* Editing Form */
            <div
              style={{
                backgroundColor: 'var(--bg-surface)',
                padding: '24px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-color)',
                boxShadow: 'var(--shadow-xs)',
              }}
            >
              <h3 style={{ fontSize: 'var(--text-lg)', fontWeight: 600, marginBottom: '16px', color: 'var(--text-primary)' }}>
                Edit Note
              </h3>
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                autoFocus
                style={{
                  width: '100%',
                  padding: '10px 14px',
                  fontSize: 'var(--text-base)',
                  fontWeight: 600,
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  marginBottom: '14px',
                  backgroundColor: 'var(--bg-app)',
                  color: 'var(--text-primary)',
                  outline: 'none',
                }}
              />
              <textarea
                rows={14}
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                style={{
                  width: '100%',
                  padding: '14px',
                  fontSize: 'var(--text-sm)',
                  fontFamily: 'var(--font-sans)',
                  lineHeight: 'var(--leading-relaxed)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  marginBottom: '16px',
                  backgroundColor: 'var(--bg-app)',
                  color: 'var(--text-primary)',
                  outline: 'none',
                  resize: 'vertical',
                }}
              />
              <div style={{ display: 'flex', gap: '8px' }}>
                <Button variant="primary" onClick={handleSaveEdit}>
                  Save Changes
                </Button>
                <Button variant="ghost" onClick={() => setIsEditing(false)}>
                  Cancel
                </Button>
              </div>
            </div>
          ) : activeNote ? (
            /* Display Active Note */
            <div
              style={{
                backgroundColor: 'var(--bg-surface)',
                padding: '28px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-color)',
                boxShadow: 'var(--shadow-xs)',
              }}
            >
              {/* Note Header & Action Buttons */}
              <div
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  justifyContent: 'space-between',
                  gap: '16px',
                  paddingBottom: '14px',
                  borderBottom: '1px solid var(--border-subtle)',
                  marginBottom: '18px',
                }}
              >
                <div>
                  <h1 style={{ fontSize: 'var(--text-2xl)', fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.3 }}>
                    {activeNote.title}
                  </h1>
                  <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', display: 'inline-flex', alignItems: 'center', gap: '4px', marginTop: '6px' }}>
                    <Calendar size={12} />
                    Last updated: {activeNote.date}
                  </span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleStartEdit}
                    title="Edit Note"
                    style={{ padding: '6px 10px', fontSize: 'var(--text-xs)' }}
                  >
                    <Edit2 size={13} />
                    <span>Edit</span>
                  </Button>

                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleExportSingleNote(activeNote)}
                    title="Export Note as Markdown"
                    style={{ padding: '6px 10px', fontSize: 'var(--text-xs)' }}
                  >
                    <Download size={13} />
                    <span>Export</span>
                  </Button>

                  {confirmDeleteId === activeNote.id ? (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <button
                        type="button"
                        onClick={() => handleDeleteNote(activeNote.id)}
                        style={{
                          padding: '4px 8px',
                          backgroundColor: 'var(--status-error)',
                          color: '#ffffff',
                          borderRadius: 'var(--radius-xs)',
                          fontSize: 'var(--text-xs)',
                          fontWeight: 600,
                          cursor: 'pointer',
                        }}
                      >
                        Delete?
                      </button>
                      <button
                        type="button"
                        onClick={() => setConfirmDeleteId(null)}
                        style={{
                          padding: '4px 8px',
                          color: 'var(--text-muted)',
                          fontSize: 'var(--text-xs)',
                          cursor: 'pointer',
                        }}
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setConfirmDeleteId(activeNote.id)}
                      title="Delete Note"
                      style={{ padding: '6px 10px', color: 'var(--status-error)' }}
                    >
                      <Trash2 size={13} />
                    </Button>
                  )}
                </div>
              </div>

              {/* Note Content Body */}
              <div
                style={{
                  fontSize: 'var(--text-base)',
                  color: 'var(--text-primary)',
                  lineHeight: 'var(--leading-relaxed)',
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word',
                }}
              >
                {activeNote.content}
              </div>
            </div>
          ) : (
            <div
              style={{
                padding: '48px',
                textAlign: 'center',
                backgroundColor: 'var(--bg-surface)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-color)',
              }}
            >
              <FileText size={36} color="var(--text-muted)" style={{ margin: '0 auto 12px' }} />
              <h3 style={{ fontSize: 'var(--text-md)', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '4px' }}>
                No note selected
              </h3>
              <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)', marginBottom: '16px' }}>
                Select an existing note from the sidebar or create a new one.
              </p>
              <Button variant="primary" size="sm" onClick={handleStartCreate}>
                <Plus size={14} /> Create Note
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
