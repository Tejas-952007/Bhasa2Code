import React from 'react';
import Status from '../common/Status';
import StudyToggle from '../study/StudyToggle';
import { Settings, Menu, Code2 } from 'lucide-react';
import Button from '../common/Button';

export default function Header({
  isStudyMode = false,
  onToggleStudyMode,
  onOpenSettings,
  onToggleSidebar,
  sidebarCollapsed = false,
  serverStatus = { state: 'ready', label: 'Local · Ready' },
}) {
  return (
    <header
      style={{
        height: '52px',
        borderBottom: '1px solid var(--border-color)',
        backgroundColor: 'var(--bg-surface)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 18px',
        userSelect: 'none',
        flexShrink: 0,
        zIndex: 10,
        boxShadow: '0 1px 3px rgba(15, 23, 42, 0.03)',
      }}
    >
      {/* Left: Brand / Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <button
          type="button"
          onClick={onToggleSidebar}
          title="Toggle sidebar"
          style={{
            padding: '6px',
            color: 'var(--text-secondary)',
            borderRadius: 'var(--radius-sm)',
          }}
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = 'var(--bg-subtle)')}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
        >
          <Menu size={18} />
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div
            style={{
              width: '28px',
              height: '28px',
              borderRadius: 'var(--radius-sm)',
              background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
              color: '#ffffff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 2px 5px rgba(37, 99, 235, 0.3)',
            }}
          >
            <Code2 size={16} strokeWidth={2.5} />
          </div>
          <span
            style={{
              fontWeight: 700,
              fontSize: 'var(--text-base)',
              letterSpacing: '-0.02em',
              color: 'var(--text-primary)',
            }}
          >
            Bhasha2Code
          </span>
          <span
            style={{
              fontSize: '0.7rem',
              color: 'var(--accent-text)',
              backgroundColor: 'var(--accent-subtle)',
              border: '1px solid #bfdbfe',
              padding: '2px 7px',
              borderRadius: 'var(--radius-sm)',
              fontWeight: 600,
            }}
          >
            v1.0
          </span>
        </div>
      </div>

      {/* Center: Study Mode Toggle */}
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <StudyToggle isStudyMode={isStudyMode} onChange={onToggleStudyMode} />
      </div>

      {/* Right: Model Status & Settings */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <Status state={serverStatus?.state || 'ready'} label={serverStatus?.label || 'Local · Ready'} />

        <Button
          variant="ghost"
          size="sm"
          onClick={onOpenSettings}
          title="Settings"
          ariaLabel="Open settings"
        >
          <Settings size={15} />
        </Button>
      </div>
    </header>
  );
}
