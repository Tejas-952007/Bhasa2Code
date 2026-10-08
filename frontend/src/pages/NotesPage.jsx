import React, { useState } from 'react';
import { Plus, Trash2, Edit2 } from 'lucide-react';
import Button from '../components/common/Button';
import { DEMO_NOTES } from '../services/mockData';

export default function NotesPage({ onBackToChat }) {
  const [notes, setNotes] = useState(DEMO_NOTES);
  const [selectedNoteId, setSelectedNoteId] = useState(notes[0]?.id);
  const [isCreating, setIsCreating] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newContent, setNewContent] = useState('');

  const activeNote = notes.find((n) => n.id === selectedNoteId) || notes[0];

  const handleCreateNote = () => {
    if (!newTitle.trim()) return;
    const note = {
      id: `note-${Date.now()}`,
      title: newTitle.trim(),
      date: 'Today',
      content: newContent.trim() || 'No content yet.',
    };
    setNotes([note, ...notes]);
    setSelectedNoteId(note.id);
    setIsCreating(false);
    setNewTitle('');
    setNewContent('');
  };

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
      {/* Left List of Notes */}
      <div
        style={{
          width: '280px',
          borderRight: '1px solid var(--border-color)',
          backgroundColor: 'var(--bg-surface)',
          display: 'flex',
          flexDirection: 'column',
          flexShrink: 0,
        }}
      >
        <div
          style={{
            padding: '16px',
            borderBottom: '1px solid var(--border-subtle)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <h2 style={{ fontSize: 'var(--text-lg)', fontWeight: 600 }}>Notes</h2>
          <Button
            variant="secondary"
            size="sm"
            icon={Plus}
            onClick={() => setIsCreating(true)}
          >
            New
          </Button>
        </div>

        <div style={{ flex: 1, overflowY: 'auto', padding: '8px' }}>
          {notes.map((note) => {
            const isSelected = note.id === selectedNoteId && !isCreating;
            return (
              <button
                key={note.id}
                type="button"
                onClick={() => {
                  setSelectedNoteId(note.id);
                  setIsCreating(false);
                }}
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  width: '100%',
                  textAlign: 'left',
                  padding: '10px 12px',
                  borderRadius: 'var(--radius-sm)',
                  backgroundColor: isSelected ? 'var(--bg-subtle)' : 'transparent',
                  borderLeft: isSelected ? '3px solid var(--accent-primary)' : '3px solid transparent',
                  marginBottom: '4px',
                }}
              >
                <span
                  style={{
                    fontSize: 'var(--text-sm)',
                    fontWeight: isSelected ? 600 : 500,
                    color: 'var(--text-primary)',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                  }}
                >
                  {note.title}
                </span>
                <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', marginTop: '2px' }}>
                  {note.date}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Right Note Detail / Editor */}
      <div
        style={{
          flex: 1,
          padding: 'var(--space-8)',
          overflowY: 'auto',
          maxWidth: '720px',
          margin: '0 auto',
          width: '100%',
        }}
      >
        {isCreating ? (
          <div>
            <h3 style={{ marginBottom: '16px' }}>Create New Note</h3>
            <input
              type="text"
              placeholder="Note title..."
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 12px',
                fontSize: 'var(--text-md)',
                fontWeight: 600,
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                marginBottom: '12px',
                outline: 'none',
              }}
            />
            <textarea
              rows={12}
              placeholder="Note content..."
              value={newContent}
              onChange={(e) => setNewContent(e.target.value)}
              style={{
                width: '100%',
                padding: '12px',
                fontSize: 'var(--text-sm)',
                fontFamily: 'var(--font-sans)',
                lineHeight: 'var(--leading-relaxed)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                marginBottom: '16px',
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
        ) : activeNote ? (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <h1 style={{ fontSize: 'var(--text-2xl)', fontWeight: 600 }}>{activeNote.title}</h1>
            </div>
            <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', marginBottom: '24px' }}>
              Last updated: {activeNote.date}
            </div>
            <div
              style={{
                fontSize: 'var(--text-base)',
                color: 'var(--text-primary)',
                lineHeight: 'var(--leading-relaxed)',
                whiteSpace: 'pre-wrap',
              }}
            >
              {activeNote.content}
            </div>
          </div>
        ) : (
          <div style={{ color: 'var(--text-muted)' }}>Select or create a note.</div>
        )}
      </div>
    </div>
  );
}
