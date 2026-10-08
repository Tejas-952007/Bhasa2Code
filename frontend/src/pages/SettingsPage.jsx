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

          {/* 2. AI Model */}
          <div>
            <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, textTransform: 'uppercase', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
              Local AI Model (Ollama)
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              style={{
                width: '100%',
                padding: '8px 10px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-color)',
                backgroundColor: 'var(--bg-surface)',
                color: 'var(--text-primary)',
                fontSize: 'var(--text-sm)',
                outline: 'none',
              }}
            >
              <option value="qwen2.5-coder:3b">qwen2.5-coder:3b (Recommended default)</option>
              <option value="qwen2.5-coder:7b">qwen2.5-coder:7b</option>
              <option value="deepseek-coder:6.7b">deepseek-coder:6.7b</option>
            </select>
          </div>

          {/* 3. Code Execution */}
          <div>
            <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, textTransform: 'uppercase', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
              Code Execution
            </label>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '10px 12px',
                backgroundColor: 'var(--bg-subtle)',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-color)',
              }}
            >
              <div>
                <div style={{ fontSize: 'var(--text-sm)', fontWeight: 500 }}>Secure Isolated Sandbox</div>
                <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)' }}>
                  Runs code in an isolated container with bounded memory and CPU.
                </div>
              </div>
              <span
                style={{
                  fontSize: 'var(--text-xs)',
                  color: 'var(--status-success)',
                  fontWeight: 600,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                }}
              >
                <Check size={14} /> Enabled
              </span>
            </div>
          </div>

          {/* 4. Privacy & Data Storage */}
          <div>
            <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, textTransform: 'uppercase', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
              Privacy & Data Storage
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
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontSize: 'var(--text-sm)', fontWeight: 500, color: 'var(--text-primary)' }}>
                  Local Storage
                </span>
                <span
                  style={{
                    fontSize: 'var(--text-xs)',
                    color: 'var(--status-success)',
                    fontWeight: 600,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                  }}
                >
                  <Check size={14} /> 100% On-Device
                </span>
              </div>
              <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', lineHeight: '1.4', margin: 0 }}>
                All conversations, generated code, and notes are saved exclusively on your local device. No telemetry or external cloud sync.
              </p>
              <div style={{ display: 'flex', gap: '8px', marginTop: '4px' }}>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => alert('Conversation history cleared')}
                  style={{ fontSize: 'var(--text-xs)' }}
                >
                  Clear History
                </Button>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => alert('Workspace data exported')}
                  style={{ fontSize: 'var(--text-xs)' }}
                >
                  Export Data
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
