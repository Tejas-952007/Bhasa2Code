import React, { useState, useEffect, useCallback } from 'react';
import AppShell from './components/layout/AppShell';
import ChatWorkspace from './components/chat/ChatWorkspace';
import NotesPage from './pages/NotesPage';
import SavedPage from './pages/SavedPage';
import SearchPage from './pages/SearchPage';
import {
  health,
  listSessions,
  createSession,
  getSession,
  renameSession,
  deleteSession,
  sendMessage,
  adaptBackendMessage,
  adaptChatResponse,
} from './services/api';

export default function App() {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [activeView, setActiveView] = useState('chat');
  const [isStudyMode, setIsStudyMode] = useState(false);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [lastFailedPrompt, setLastFailedPrompt] = useState(null);
  const [serverStatus, setServerStatus] = useState({
    state: 'loading',
    label: 'Connecting...',
  });

  // Check health and initialize sessions
  const checkHealthAndLoad = useCallback(async () => {
    try {
      const h = await health();
      if (h.status === 'healthy') {
        setServerStatus({
          state: 'ready',
          label: `Local · ${h.model || 'Ready'}`,
        });
      } else if (h.status === 'degraded' || h.ollama === 'unavailable') {
        setServerStatus({
          state: 'unavailable',
          label: 'Ollama offline',
        });
      } else {
        setServerStatus({
          state: 'ready',
          label: 'Local · Ready',
        });
      }
    } catch {
      setServerStatus({
        state: 'unavailable',
        label: 'Backend offline',
      });
    }

    try {
      const userSessions = await listSessions();
      setSessions(userSessions);
      if (userSessions.length > 0) {
        const first = userSessions[0];
        setActiveSessionId(first.id);
        const detail = await getSession(first.id);
        const adapted = (detail.messages || []).map(adaptBackendMessage);
        setMessages(adapted);
      } else {
        setActiveSessionId(null);
        setMessages([]);
      }
    } catch (err) {
      console.warn('Could not load sessions:', err);
    }
  }, []);

  useEffect(() => {
    checkHealthAndLoad();
  }, [checkHealthAndLoad]);

  // Select existing session
  const handleSelectSession = async (sessionId) => {
    setActiveSessionId(sessionId);
    setActiveView('chat');
    setErrorMessage(null);
    try {
      const detail = await getSession(sessionId);
      const adapted = (detail.messages || []).map(adaptBackendMessage);
      setMessages(adapted);
    } catch (err) {
      setErrorMessage(err.message || 'Failed to load conversation history.');
      setMessages([]);
    }
  };

  // + New Chat
  const handleNewChat = async () => {
    try {
      const created = await createSession('New Chat');
      setSessions((prev) => [created, ...prev]);
      setActiveSessionId(created.id);
      setMessages([]);
      setActiveView('chat');
      setErrorMessage(null);
    } catch (err) {
      setErrorMessage(err.message || 'Could not create new session.');
    }
  };

  // Rename Session
  const handleRenameSession = async (sessionId, newTitle) => {
    try {
      const updated = await renameSession(sessionId, newTitle);
      setSessions((prev) =>
        prev.map((s) => (s.id === sessionId ? { ...s, title: updated.title } : s))
      );
    } catch (err) {
      setErrorMessage(err.message || 'Failed to rename session.');
    }
  };

  // Delete Session
  const handleDeleteSession = async (sessionId) => {
    try {
      await deleteSession(sessionId);
      const remaining = sessions.filter((s) => s.id !== sessionId);
      setSessions(remaining);

      if (activeSessionId === sessionId) {
        if (remaining.length > 0) {
          handleSelectSession(remaining[0].id);
        } else {
          setActiveSessionId(null);
          setMessages([]);
        }
      }
    } catch (err) {
      setErrorMessage(err.message || 'Failed to delete session.');
    }
  };

  // Send Message
  const handleSendMessage = async (text) => {
    if (!text || !text.trim() || isLoading) return;

    const trimmed = text.trim();
    setErrorMessage(null);
    setLastFailedPrompt(null);

    // Optimistic user message
    const tempUserMsg = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: trimmed,
    };
    setMessages((prev) => [...prev, tempUserMsg]);
    setIsLoading(true);

    try {
      const resp = await sendMessage({
        sessionId: activeSessionId,
        message: trimmed,
        studyMode: isStudyMode,
      });

      const { sessionId, userMessage, assistantMessage } = adaptChatResponse(resp);

      // Replace optimistic message with confirmed and append assistant message
      setMessages((prev) => {
        const withoutTemp = prev.filter((m) => m.id !== tempUserMsg.id);
        return [...withoutTemp, userMessage, assistantMessage];
      });

      // If this was a new session without an explicit active ID, update it
      if (!activeSessionId || activeSessionId !== sessionId) {
        setActiveSessionId(sessionId);
        // Refresh session list
        const updatedSessions = await listSessions();
        setSessions(updatedSessions);
      } else {
        // Update title if it was "New Chat"
        setSessions((prev) =>
          prev.map((s) => {
            if (s.id === sessionId && (s.title === 'New Chat' || s.title === 'Untitled Chat')) {
              const snippet = trimmed.slice(0, 24) + (trimmed.length > 24 ? '...' : '');
              return { ...s, title: snippet };
            }
            return s;
          })
        );
      }
    } catch (err) {
      setErrorMessage(err.message || 'Failed to generate response. Please try again.');
      setLastFailedPrompt(trimmed);
      // Remove failed optimistic message or leave it
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectView = (view) => {
    if (view === 'study') {
      setIsStudyMode(true);
      setActiveView('chat');
    } else {
      setActiveView(view);
    }
  };

  const currentSession = sessions.find((s) => s.id === activeSessionId);

  return (
    <AppShell
      sessions={sessions}
      activeSessionId={activeSessionId}
      onSelectSession={handleSelectSession}
      onNewChat={handleNewChat}
      onRenameSession={handleRenameSession}
      onDeleteSession={handleDeleteSession}
      serverStatus={serverStatus}
      activeView={activeView}
      onSelectView={handleSelectView}
      isStudyMode={isStudyMode}
      onToggleStudyMode={setIsStudyMode}
    >
      {activeView === 'chat' && (
        <ChatWorkspace
          messages={messages}
          isStudyMode={isStudyMode}
          isLoading={isLoading}
          errorMessage={errorMessage}
          onRetry={lastFailedPrompt ? () => handleSendMessage(lastFailedPrompt) : null}
          onSendMessage={handleSendMessage}
          activeSessionTitle={currentSession ? currentSession.title : 'Workspace'}
        />
      )}

      {activeView === 'notes' && (
        <NotesPage onBackToChat={() => setActiveView('chat')} />
      )}

      {activeView === 'saved' && (
        <SavedPage onOpenSession={handleSelectSession} />
      )}

      {activeView === 'search' && (
        <SearchPage onSelectSession={handleSelectSession} />
      )}
    </AppShell>
  );
}
