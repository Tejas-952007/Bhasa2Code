import React, { useState } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import SettingsPage from '../../pages/SettingsPage';

export default function AppShell({
  children,
  sessions = [],
  activeSessionId,
  onSelectSession,
  onNewChat,
  onRenameSession,
  onDeleteSession,
  serverStatus,
  activeView = 'chat',
  onSelectView,
  isStudyMode = false,
  onToggleStudyMode,
  theme,
  onThemeChange,
  editorFontSize,
  onEditorFontSizeChange,
  codingModel,
  onCodingModelChange,
  onClearAllSessions,
}) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        width: '100vw',
        overflow: 'hidden',
        backgroundColor: 'var(--bg-app)',
      }}
    >
      {/* Top Header */}
      <Header
        isStudyMode={isStudyMode}
        onToggleStudyMode={onToggleStudyMode}
        onOpenSettings={() => setShowSettings(true)}
        onToggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)}
        sidebarCollapsed={sidebarCollapsed}
        serverStatus={serverStatus}
      />

      {/* Main Container: Sidebar + Content */}
      <div
        style={{
          display: 'flex',
          flex: 1,
          minHeight: 0,
          height: 'calc(100vh - 52px)',
          overflow: 'hidden',
          position: 'relative',
        }}
      >
        <Sidebar
          sessions={sessions}
          activeSessionId={activeSessionId}
          onSelectSession={onSelectSession}
          onNewChat={onNewChat}
          onRenameSession={onRenameSession}
          onDeleteSession={onDeleteSession}
          activeView={activeView}
          onSelectView={onSelectView}
          collapsed={sidebarCollapsed}
          onOpenSettings={() => setShowSettings(true)}
        />

        <main
          style={{
            flex: 1,
            height: '100%',
            minHeight: 0,
            overflow: 'hidden',
            display: 'flex',
            flexDirection: 'column',
            backgroundColor: 'var(--bg-app)',
          }}
        >
          {children}
        </main>
      </div>

      {/* Settings Modal */}
      {showSettings && (
        <SettingsPage
          onClose={() => setShowSettings(false)}
          theme={theme}
          onThemeChange={onThemeChange}
          editorFontSize={editorFontSize}
          onEditorFontSizeChange={onEditorFontSizeChange}
          codingModel={codingModel}
          onCodingModelChange={onCodingModelChange}
          onClearAllSessions={onClearAllSessions}
          sessionsCount={sessions.length}
        />
      )}
    </div>
  );
}
