import React, { useState } from 'react';
import { X, Check } from 'lucide-react';
import Button from '../components/common/Button';

export default function SettingsPage({ onClose }) {
  const [model, setModel] = useState('qwen2.5-coder:3b');
  const [theme, setTheme] = useState('light');
  const [sandboxEnabled, setSandboxEnabled] = useState(true);

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.35)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 100,
        padding: '16px',
      }}
      onClick={onClose}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '480px',
          backgroundColor: 'var(--bg-surface)',
          borderRadius: 'var(--radius-md)',
          boxShadow: 'var(--shadow-dropdown)',
          border: '1px solid var(--border-color)',
          overflow: 'hidden',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div
          style={{
            padding: '14px 18px',
            borderBottom: '1px solid var(--border-color)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <h2 style={{ fontSize: 'var(--text-md)', fontWeight: 600 }}>Workspace Settings</h2>
          <Button variant="ghost" size="sm" onClick={onClose} ariaLabel="Close settings">
            <X size={16} />
          </Button>
        </div>

        {/* Settings Body */}
        <div style={{ padding: '20px 18px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* 1. Appearance */}
          <div>
            <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, textTransform: 'uppercase', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
              Appearance
            </label>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                type="button"
                onClick={() => setTheme('light')}
                style={{
                  flex: 1,
                  padding: '8px',
                  borderRadius: 'var(--radius-sm)',
                  border: theme === 'light' ? '2px solid var(--accent-primary)' : '1px solid var(--border-color)',
                  backgroundColor: 'var(--bg-surface)',
                  fontWeight: 500,
                  fontSize: 'var(--text-sm)',
                  cursor: 'pointer',
                }}
              >
                Light (Default)
              </button>
              <button
                type="button"
                disabled
                title="Dark theme prepared architecturally"
                style={{
                  flex: 1,
                  padding: '8px',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-color)',
                  backgroundColor: 'var(--bg-subtle)',
                  color: 'var(--text-muted)',
                  fontSize: 'var(--text-sm)',
                  cursor: 'not-allowed',
                }}
              >
                Dark (Coming soon)
              </button>
            </div>
          </div>

          {/* 2. Coding Model Selection */}
          <div>
            <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, textTransform: 'uppercase', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
              Coding Model
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              style={{
                width: '100%',
                padding: '9px 12px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-color)',
                backgroundColor: 'var(--bg-surface)',
                color: 'var(--text-primary)',
                fontSize: 'var(--text-sm)',
                outline: 'none',
                cursor: 'pointer',
              }}
            >
              <option value="qwen2.5-coder:3b">Qwen 2.5 Coder 3B (Fast & Recommended)</option>
              <option value="qwen2.5-coder:7b">Qwen 2.5 Coder 7B (High Accuracy)</option>
              <option value="deepseek-coder:6.7b">DeepSeek Coder 6.7B (Advanced)</option>
            </select>
          </div>

          {/* 3. Code Editor Font Size */}
          <div>
            <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, textTransform: 'uppercase', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
              Editor Font Size
            </label>
            <div style={{ display: 'flex', gap: '8px' }}>
              {['Small (13px)', 'Default (14px)', 'Large (16px)'].map((sizeOpt, idx) => (
                <button
                  key={sizeOpt}
                  type="button"
                  style={{
                    flex: 1,
                    padding: '7px 8px',
                    borderRadius: 'var(--radius-sm)',
                    border: idx === 1 ? '2px solid var(--accent-primary)' : '1px solid var(--border-color)',
                    backgroundColor: idx === 1 ? 'var(--accent-subtle)' : 'var(--bg-surface)',
                    color: idx === 1 ? 'var(--accent-text)' : 'var(--text-primary)',
                    fontWeight: idx === 1 ? 600 : 400,
                    fontSize: 'var(--text-xs)',
                    cursor: 'pointer',
                  }}
                >
                  {sizeOpt}
                </button>
              ))}
            </div>
          </div>

          {/* 4. Workspace Data Management */}
          <div>
            <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, textTransform: 'uppercase', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
              Workspace Data
            </label>
            <div
              style={{
                padding: '12px 14px',
                backgroundColor: 'var(--bg-subtle)',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-color)',
                display: 'flex',
                flexDirection: 'column',
                gap: '8px',
              }}
            >
              <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', lineHeight: '1.45', margin: 0 }}>
                Manage your local session history, saved snippets, and generated study notes.
              </p>
              <div style={{ display: 'flex', gap: '8px', marginTop: '4px' }}>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => alert('Conversation history cleared')}
                  style={{ fontSize: 'var(--text-xs)' }}
                >
                  Clear Chat History
                </Button>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => alert('Workspace notes exported')}
                  style={{ fontSize: 'var(--text-xs)' }}
                >
                  Export Workspace Notes
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div
          style={{
            padding: '12px 18px',
            borderTop: '1px solid var(--border-color)',
            display: 'flex',
            justifyContent: 'flex-end',
            backgroundColor: 'var(--bg-app)',
          }}
        >
          <Button variant="primary" size="md" onClick={onClose}>
            Done
          </Button>
        </div>
      </div>
    </div>
  );
}
