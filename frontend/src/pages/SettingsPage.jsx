import React, { useState, useEffect } from 'react';
import { X, Check, Sun, Moon, Trash2, Download, AlertCircle } from 'lucide-react';
import Button from '../components/common/Button';
import { DEMO_NOTES } from '../services/mockData';

export default function SettingsPage({
  onClose,
  theme = 'light',
  onThemeChange,
  editorFontSize = '14px',
  onEditorFontSizeChange,
  codingModel = 'qwen2.5-coder:1.5b',
  onCodingModelChange,
  onClearAllSessions,
  sessionsCount = 0,
}) {
  const [selectedTheme, setSelectedTheme] = useState(theme);
  const [selectedFontSize, setSelectedFontSize] = useState(editorFontSize);
  const [selectedModel, setSelectedModel] = useState(codingModel);

  const [confirmClear, setConfirmClear] = useState(false);
  const [isClearing, setIsClearing] = useState(false);
  const [statusMessage, setStatusMessage] = useState(null);

  useEffect(() => {
    setSelectedTheme(theme);
  }, [theme]);

  useEffect(() => {
    setSelectedFontSize(editorFontSize);
  }, [editorFontSize]);

  useEffect(() => {
    setSelectedModel(codingModel);
  }, [codingModel]);

  const handleThemeSelect = (t) => {
    setSelectedTheme(t);
    if (onThemeChange) {
      onThemeChange(t);
    } else {
      document.documentElement.setAttribute('data-theme', t);
      try {
        localStorage.setItem('b2c_theme', t);
      } catch {}
    }
    showToast(`Switched to ${t === 'dark' ? 'Dark' : 'Light'} theme`);
  };

  const handleFontSizeSelect = (sz) => {
    setSelectedFontSize(sz);
    if (onEditorFontSizeChange) {
      onEditorFontSizeChange(sz);
    } else {
      document.documentElement.style.setProperty('--editor-font-size', sz);
      try {
        localStorage.setItem('b2c_editor_font_size', sz);
      } catch {}
    }
    showToast(`Editor font size set to ${sz}`);
  };

  const handleModelChange = (m) => {
    setSelectedModel(m);
    if (onCodingModelChange) {
      onCodingModelChange(m);
    } else {
      try {
        localStorage.setItem('b2c_coding_model', m);
      } catch {}
    }
    showToast(`Coding model set to ${m}`);
  };

  const showToast = (msg, type = 'success') => {
    setStatusMessage({ text: msg, type });
    setTimeout(() => {
      setStatusMessage(null);
    }, 3000);
  };

  const handleConfirmClearChat = async () => {
    setIsClearing(true);
    try {
      if (onClearAllSessions) {
        await onClearAllSessions();
      }
      setConfirmClear(false);
      showToast('All conversation history cleared successfully');
    } catch (err) {
      showToast('Failed to clear conversation history', 'error');
    } finally {
      setIsClearing(false);
    }
  };

  const handleExportNotes = () => {
    try {
      let notes = [];
      try {
        const saved = localStorage.getItem('b2c_notes');
        notes = saved ? JSON.parse(saved) : DEMO_NOTES;
      } catch {
        notes = DEMO_NOTES;
      }

      const dateStr = new Date().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });

      let md = `# Bhasha2Code Workspace Notes Export\n`;
      md += `*Exported on: ${dateStr}*\n\n`;
      md += `---\n\n`;

      if (notes.length === 0) {
        md += `*No notes currently saved in workspace.*\n`;
      } else {
        notes.forEach((note, idx) => {
          md += `### ${idx + 1}. ${note.title || 'Untitled Note'}\n`;
          md += `*Date: ${note.date || 'N/A'}*\n\n`;
          md += `${note.content || ''}\n\n`;
          md += `---\n\n`;
        });
      }

      const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `bhasha2code-workspace-notes-${new Date().toISOString().slice(0, 10)}.md`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      showToast('Workspace notes exported as Markdown');
    } catch (err) {
      showToast('Failed to export notes', 'error');
    }
  };

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.45)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 100,
        padding: '16px',
        backdropFilter: 'blur(2px)',
      }}
      onClick={onClose}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '480px',
          backgroundColor: 'var(--bg-surface)',
          color: 'var(--text-primary)',
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
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h2 style={{ fontSize: 'var(--text-md)', fontWeight: 600 }}>Workspace Settings</h2>
            {statusMessage && (
              <span
                style={{
                  fontSize: '0.72rem',
                  padding: '2px 8px',
                  borderRadius: 'var(--radius-xs)',
                  backgroundColor:
                    statusMessage.type === 'error'
                      ? 'var(--status-error-bg)'
                      : 'var(--status-success-bg)',
                  color:
                    statusMessage.type === 'error'
                      ? 'var(--status-error)'
                      : 'var(--status-success)',
                  border: `1px solid ${
                    statusMessage.type === 'error'
                      ? 'var(--status-error-border)'
                      : 'var(--status-success-border)'
                  }`,
                  fontWeight: 500,
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px',
                }}
              >
                <Check size={11} /> {statusMessage.text}
              </span>
            )}
          </div>
          <Button variant="ghost" size="sm" onClick={onClose} ariaLabel="Close settings">
            <X size={16} />
          </Button>
        </div>

        {/* Settings Body */}
        <div style={{ padding: '20px 18px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* 1. Appearance */}
          <div>
            <label
              style={{
                fontSize: 'var(--text-xs)',
                fontWeight: 600,
                textTransform: 'uppercase',
                color: 'var(--text-muted)',
                display: 'block',
                marginBottom: '8px',
                letterSpacing: '0.04em',
              }}
            >
              Appearance
            </label>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                type="button"
                onClick={() => handleThemeSelect('light')}
                style={{
                  flex: 1,
                  padding: '9px 12px',
                  borderRadius: 'var(--radius-sm)',
                  border:
                    selectedTheme === 'light'
                      ? '2px solid var(--accent-primary)'
                      : '1px solid var(--border-color)',
                  backgroundColor:
                    selectedTheme === 'light'
                      ? 'var(--accent-subtle)'
                      : 'var(--bg-surface)',
                  color:
                    selectedTheme === 'light'
                      ? 'var(--accent-text)'
                      : 'var(--text-primary)',
                  fontWeight: selectedTheme === 'light' ? 600 : 500,
                  fontSize: 'var(--text-sm)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  cursor: 'pointer',
                  transition: 'all var(--transition-fast)',
                }}
              >
                <Sun size={15} />
                <span>Light (Default)</span>
              </button>

              <button
                type="button"
                onClick={() => handleThemeSelect('dark')}
                style={{
                  flex: 1,
                  padding: '9px 12px',
                  borderRadius: 'var(--radius-sm)',
                  border:
                    selectedTheme === 'dark'
                      ? '2px solid var(--accent-primary)'
                      : '1px solid var(--border-color)',
                  backgroundColor:
                    selectedTheme === 'dark'
                      ? 'var(--accent-subtle)'
                      : 'var(--bg-surface)',
                  color:
                    selectedTheme === 'dark'
                      ? 'var(--accent-text)'
                      : 'var(--text-primary)',
                  fontWeight: selectedTheme === 'dark' ? 600 : 500,
                  fontSize: 'var(--text-sm)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  cursor: 'pointer',
                  transition: 'all var(--transition-fast)',
                }}
              >
                <Moon size={15} />
                <span>Dark Pro</span>
              </button>
            </div>
          </div>

          {/* 2. Coding Model Selection */}
          <div>
            <label
              style={{
                fontSize: 'var(--text-xs)',
                fontWeight: 600,
                textTransform: 'uppercase',
                color: 'var(--text-muted)',
                display: 'block',
                marginBottom: '8px',
                letterSpacing: '0.04em',
              }}
            >
              Coding Model
            </label>
            <select
              value={selectedModel}
              onChange={(e) => handleModelChange(e.target.value)}
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
              <option value="qwen2.5-coder:1.5b">
                Qwen 2.5 Coder 1.5B (Active Local · Fast &amp; Light)
              </option>
              <option value="qwen2.5-coder:3b">
                Qwen 2.5 Coder 3B (Fast &amp; Recommended)
              </option>
              <option value="qwen2.5-coder:7b">
                Qwen 2.5 Coder 7B (High Accuracy)
              </option>
              <option value="qwen2.5-coder:32b">
                Qwen 2.5 Coder 32B (Maximum Accuracy)
              </option>
              <option value="deepseek-coder:1.3b-instruct-q4_K_M">
                DeepSeek Coder 1.3B (Instruct)
              </option>
            </select>
          </div>

          {/* 3. Code Editor Font Size */}
          <div>
            <label
              style={{
                fontSize: 'var(--text-xs)',
                fontWeight: 600,
                textTransform: 'uppercase',
                color: 'var(--text-muted)',
                display: 'block',
                marginBottom: '8px',
                letterSpacing: '0.04em',
              }}
            >
              Editor Font Size
            </label>
            <div style={{ display: 'flex', gap: '8px' }}>
              {[
                { label: 'Small (13px)', value: '13px' },
                { label: 'Default (14px)', value: '14px' },
                { label: 'Large (16px)', value: '16px' },
              ].map((opt) => {
                const isActive = selectedFontSize === opt.value;
                return (
                  <button
                    key={opt.value}
                    type="button"
                    onClick={() => handleFontSizeSelect(opt.value)}
                    style={{
                      flex: 1,
                      padding: '8px 10px',
                      borderRadius: 'var(--radius-sm)',
                      border: isActive
                        ? '2px solid var(--accent-primary)'
                        : '1px solid var(--border-color)',
                      backgroundColor: isActive
                        ? 'var(--accent-subtle)'
                        : 'var(--bg-surface)',
                      color: isActive ? 'var(--accent-text)' : 'var(--text-primary)',
                      fontWeight: isActive ? 600 : 400,
                      fontSize: 'var(--text-xs)',
                      cursor: 'pointer',
                      transition: 'all var(--transition-fast)',
                    }}
                  >
                    {opt.label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* 4. Workspace Data Management */}
          <div>
            <label
              style={{
                fontSize: 'var(--text-xs)',
                fontWeight: 600,
                textTransform: 'uppercase',
                color: 'var(--text-muted)',
                display: 'block',
                marginBottom: '8px',
                letterSpacing: '0.04em',
              }}
            >
              Workspace Data
            </label>
            <div
              style={{
                padding: '14px',
                backgroundColor: 'var(--bg-subtle)',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-color)',
                display: 'flex',
                flexDirection: 'column',
                gap: '10px',
              }}
            >
              <p
                style={{
                  fontSize: 'var(--text-xs)',
                  color: 'var(--text-secondary)',
                  lineHeight: '1.45',
                  margin: 0,
                }}
              >
                Manage your local session history ({sessionsCount} active chat
                {sessionsCount === 1 ? '' : 's'}) and saved study notes.
              </p>

              {confirmClear ? (
                <div
                  style={{
                    padding: '10px 12px',
                    borderRadius: 'var(--radius-xs)',
                    backgroundColor: 'var(--status-error-bg)',
                    border: '1px solid var(--status-error-border)',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '8px',
                  }}
                >
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px',
                      color: 'var(--status-error)',
                      fontSize: 'var(--text-xs)',
                      fontWeight: 600,
                    }}
                  >
                    <AlertCircle size={14} />
                    <span>Clear all {sessionsCount} chat sessions permanently?</span>
                  </div>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button
                      type="button"
                      disabled={isClearing}
                      onClick={handleConfirmClearChat}
                      style={{
                        padding: '5px 12px',
                        backgroundColor: 'var(--status-error)',
                        color: '#ffffff',
                        border: 'none',
                        borderRadius: 'var(--radius-xs)',
                        fontSize: 'var(--text-xs)',
                        fontWeight: 600,
                        cursor: isClearing ? 'not-allowed' : 'pointer',
                      }}
                    >
                      {isClearing ? 'Clearing...' : 'Yes, Delete All'}
                    </button>
                    <button
                      type="button"
                      disabled={isClearing}
                      onClick={() => setConfirmClear(false)}
                      style={{
                        padding: '5px 12px',
                        backgroundColor: 'transparent',
                        color: 'var(--text-secondary)',
                        border: '1px solid var(--border-color)',
                        borderRadius: 'var(--radius-xs)',
                        fontSize: 'var(--text-xs)',
                        cursor: 'pointer',
                      }}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => setConfirmClear(true)}
                    style={{ fontSize: 'var(--text-xs)', display: 'inline-flex', gap: '6px' }}
                  >
                    <Trash2 size={13} style={{ opacity: 0.7 }} />
                    <span>Clear Chat History</span>
                  </Button>
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={handleExportNotes}
                    style={{ fontSize: 'var(--text-xs)', display: 'inline-flex', gap: '6px' }}
                  >
                    <Download size={13} style={{ opacity: 0.7 }} />
                    <span>Export Workspace Notes</span>
                  </Button>
                </div>
              )}
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
