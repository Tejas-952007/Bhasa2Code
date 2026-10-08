import React from 'react';
import {
  Plus,
  Bookmark,
  FileText,
  BookOpen,
  Search,
  Settings,
  ChevronRight,
  MessageSquare,
} from 'lucide-react';
import Button from '../common/Button';

export default function Sidebar({
  sessions = [],
  activeSessionId,
  onSelectSession,
  onNewChat,
  activeView,
  onSelectView,
  collapsed = false,
  onOpenSettings,
}) {
  if (collapsed) {
    return null;
  }

  const sectionLabelStyle = {
    fontSize: '0.7rem',
    fontWeight: 600,
    textTransform: 'uppercase',
    letterSpacing: '0.06em',
    color: 'var(--text-muted)',
    padding: '0 10px',
    marginBottom: '6px',
  };

  const navItemStyle = (isActive) => ({
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    width: '100%',
    padding: '8px 12px',
    borderRadius: 'var(--radius-sm)',
    fontSize: 'var(--text-sm)',
    color: isActive ? 'var(--accent-text)' : 'var(--text-secondary)',
    backgroundColor: isActive ? 'var(--accent-subtle)' : 'transparent',
    fontWeight: isActive ? 600 : 500,
    textAlign: 'left',
    transition: 'all var(--transition-fast)',
    borderLeft: isActive ? '3px solid var(--accent-primary)' : '3px solid transparent',
  });

  return (
    <aside
      style={{
        width: '250px',
        height: '100%',
        backgroundColor: 'var(--bg-sidebar)',
        borderRight: '1px solid var(--border-color)',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        flexShrink: 0,
        userSelect: 'none',
      }}
    >
      {/* Top Half: New Chat & Recent Sessions */}
      <div style={{ padding: '14px 12px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {/* + New Chat Button */}
        <button
          type="button"
          onClick={onNewChat}
          style={{
            width: '100%',
            height: '40px',
            padding: '0 12px',
            borderRadius: 'var(--radius-md)',
            backgroundColor: 'var(--accent-primary)',
            color: '#ffffff',
            border: 'none',
            fontSize: 'var(--text-sm)',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            cursor: 'pointer',
            boxShadow: '0 2px 6px rgba(37, 99, 235, 0.25)',
            transition: 'all var(--transition-fast)',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--accent-hover)';
            e.currentTarget.style.transform = 'translateY(-1px)';
            e.currentTarget.style.boxShadow = '0 4px 12px rgba(37, 99, 235, 0.35)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--accent-primary)';
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 2px 6px rgba(37, 99, 235, 0.25)';
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Plus size={18} strokeWidth={2.5} />
            <span>New Chat</span>
          </div>
          <span
            style={{
              fontSize: '0.68rem',
              backgroundColor: 'rgba(255, 255, 255, 0.2)',
              padding: '2px 6px',
              borderRadius: 'var(--radius-xs)',
              letterSpacing: '0.02em',
              fontWeight: 500,
            }}
          >
            ⌘N
          </span>
        </button>

        {/* Recent Sessions */}
        <div>
          <div style={sectionLabelStyle}>Recent</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
            {sessions.map((session) => {
              const isActive = activeView === 'chat' && session.id === activeSessionId;
              return (
                <button
                  key={session.id}
                  type="button"
                  onClick={() => onSelectSession(session.id)}
                  style={navItemStyle(isActive)}
                  onMouseEnter={(e) => {
                    if (!isActive) e.currentTarget.style.backgroundColor = 'rgba(0, 0, 0, 0.03)';
                  }}
                  onMouseLeave={(e) => {
                    if (!isActive) e.currentTarget.style.backgroundColor = 'transparent';
                  }}
                >
                  <MessageSquare size={14} style={{ flexShrink: 0, opacity: 0.7 }} />
                  <span
                    style={{
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                      flex: 1,
                    }}
                  >
                    {session.title}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Bottom Half: Navigation Sections & Settings */}
      <div
        style={{
          padding: '12px 10px',
          borderTop: '1px solid var(--border-subtle)',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px',
        }}
      >
        {/* Workspace Tools */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
          <button
            type="button"
            onClick={() => onSelectView('saved')}
            style={navItemStyle(activeView === 'saved')}
          >
            <Bookmark size={14} style={{ opacity: 0.7 }} />
            <span>Saved</span>
          </button>

          <button
            type="button"
            onClick={() => onSelectView('notes')}
            style={navItemStyle(activeView === 'notes')}
          >
            <FileText size={14} style={{ opacity: 0.7 }} />
            <span>Notes</span>
          </button>

          <button
            type="button"
            onClick={() => onSelectView('study')}
            style={navItemStyle(activeView === 'study')}
          >
            <BookOpen size={14} style={{ opacity: 0.7 }} />
            <span>Study Mode</span>
          </button>

          <button
            type="button"
            onClick={() => onSelectView('search')}
            style={navItemStyle(activeView === 'search')}
          >
            <Search size={14} style={{ opacity: 0.7 }} />
            <span>Search</span>
          </button>
        </div>

        {/* Divider & Settings */}
        <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '8px' }}>
          <button
            type="button"
            onClick={onOpenSettings}
            style={navItemStyle(activeView === 'settings')}
          >
            <Settings size={14} style={{ opacity: 0.7 }} />
            <span>Settings</span>
          </button>
        </div>
      </div>
    </aside>
  );
}
