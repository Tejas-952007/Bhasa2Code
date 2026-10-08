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
  activeView = 'chat',
  onSelectView,
  isStudyMode = false,
  onToggleStudyMode,
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
      />

      {/* Main Container: Sidebar + Content */}
      <div
        style={{
          display: 'flex',
          flex: 1,
          height: 'calc(100vh - 48px)',
          overflow: 'hidden',
          position: 'relative',
        }}
      >
        <Sidebar
          sessions={sessions}
          activeSessionId={activeSessionId}
          onSelectSession={onSelectSession}
          onNewChat={onNewChat}
          activeView={activeView}
          onSelectView={onSelectView}
          collapsed={sidebarCollapsed}
          onOpenSettings={() => setShowSettings(true)}
        />

        <main
          style={{
            flex: 1,
            height: '100%',
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
        <SettingsPage onClose={() => setShowSettings(false)} />
      )}
    </div>
  );
}
