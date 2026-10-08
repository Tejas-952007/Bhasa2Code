import React from 'react';
import Status from '../common/Status';
import StudyToggle from '../study/StudyToggle';
import { Settings, Menu } from 'lucide-react';
import Button from '../common/Button';

export default function Header({
  isStudyMode = false,
  onToggleStudyMode,
  onOpenSettings,
  onToggleSidebar,
  sidebarCollapsed = false,
}) {
  return (
    <header
      style={{
        height: '48px',
        borderBottom: '1px solid var(--border-color)',
        backgroundColor: 'var(--bg-surface)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 16px',
        userSelect: 'none',
        flexShrink: 0,
        zIndex: 10,
      }}
    >
      {/* Left: Brand / Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <button
          type="button"
          onClick={onToggleSidebar}
          title="Toggle sidebar"
          style={{
            padding: '4px',
            color: 'var(--text-secondary)',
            borderRadius: 'var(--radius-xs)',
          }}
        >
          <Menu size={16} />
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span
            style={{
              fontWeight: 600,
              fontSize: 'var(--text-base)',
              letterSpacing: '-0.02em',
              color: 'var(--text-primary)',
            }}
          >
            Bhasha2Code
          </span>
          <span
            style={{
              fontSize: '0.65rem',
              color: 'var(--text-muted)',
              border: '1px solid var(--border-color)',
              padding: '1px 5px',
              borderRadius: 'var(--radius-xs)',
              fontWeight: 500,
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
        <Status state="ready" label="Local · Ready" />

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
