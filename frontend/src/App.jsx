import React, { useState, useEffect, useCallback, useRef } from 'react';
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
  streamMessage,
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

  // T23: Prevent duplicate requests — only one stream can be in-flight at a time.
  const inflightRef = useRef(false);
  // T23: AbortController ref for cancelling in-progress streams.
  const abortControllerRef = useRef(null);
  // T23: Ref to track active session during async streaming (avoids stale closure).
  const activeSessionIdRef = useRef(activeSessionId);
  useEffect(() => { activeSessionIdRef.current = activeSessionId; }, [activeSessionId]);


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

  // Send Message (streaming)
  const handleSendMessage = async (text) => {
    if (!text || !text.trim()) return;

    // T23: Hard deduplication — block concurrent requests
    if (inflightRef.current) {
      console.warn('Bhasha2Code: request already in-flight, ignoring duplicate submission.');
      return;
    }

    const trimmed = text.trim();
    setErrorMessage(null);
    setLastFailedPrompt(null);
    inflightRef.current = true;

    // Create a new AbortController for this stream
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    const controller = new AbortController();
    abortControllerRef.current = controller;

    // T23: Optimistic user message
    const tempUserMsgId = `temp-user-${Date.now()}`;
    const tempUserMsg = { id: tempUserMsgId, role: 'user', content: trimmed };

    // T23: Streaming placeholder (accumulates tokens live)
    const tempStreamId = `temp-stream-${Date.now()}`;
    const tempStreamMsg = {
      id: tempStreamId,
      role: 'assistant',
      content: '',
      _streaming: true,
    };

    setMessages((prev) => [...prev, tempUserMsg, tempStreamMsg]);
    setIsLoading(true);

    // T23: Unique turn identifier for backend deduplication and idempotency
    const clientTurnId = `turn-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;

    // Resolve current session ID at call time (not from stale closure)
    const currentSessionId = activeSessionIdRef.current;
    let resolvedSessionId = currentSessionId;
    let confirmedUserMsgId = null;

    try {
      for await (const event of streamMessage({
        sessionId: currentSessionId,
        message: trimmed,
        studyMode: isStudyMode,
        clientTurnId,
        signal: controller.signal,
      })) {
        if (event.type === 'start') {
          resolvedSessionId = event.session_id;
          confirmedUserMsgId = event.user_message_id;
          // Update session if it's new
          if (!currentSessionId || currentSessionId !== resolvedSessionId) {
            setActiveSessionId(resolvedSessionId);
            activeSessionIdRef.current = resolvedSessionId;
          }
        } else if (event.type === 'token') {
          // Append token to streaming message
          setMessages((prev) =>
            prev.map((m) =>
              m.id === tempStreamId
                ? { ...m, content: m.content + event.token }
                : m
            )
          );
        } else if (event.type === 'complete') {
          // Build proper adapted messages from the complete payload
          const adapted = adaptChatResponse(event);

          setMessages((prev) => {
            // Remove both temp messages, insert real ones
            const without = prev.filter(
              (m) => m.id !== tempUserMsgId && m.id !== tempStreamId
            );
            return [...without, adapted.userMessage, adapted.assistantMessage];
          });

          // Session list refresh
          try {
            const updatedSessions = await listSessions();
            setSessions(updatedSessions);
          } catch { /* non-fatal */ }

        } else if (event.type === 'error') {
          setErrorMessage(event.message || 'Generation failed. Please try again.');
          setLastFailedPrompt(trimmed);
          // Remove streaming placeholder, keep user message for retry context
          setMessages((prev) => prev.filter((m) => m.id !== tempStreamId));
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        setErrorMessage(err.message || 'Failed to generate response. Please try again.');
        setLastFailedPrompt(trimmed);
        setMessages((prev) =>
          prev.filter((m) => m.id !== tempStreamId)
        );
      }
    } finally {
      inflightRef.current = false;
      setIsLoading(false);
    }
  };

  // T23: Handle user request cancellation (Stop button)
  const handleStopGeneration = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    inflightRef.current = false;
    setIsLoading(false);
    setMessages((prev) =>
      prev.map((m) =>
        m._streaming
          ? {
              ...m,
              _streaming: false,
              content: m.content ? m.content + '\n\n*[Generation stopped]*' : '*[Generation stopped]*',
            }
          : m
      )
    );
  };

  const handleUpdateMessageCode = (messageId, newCode) => {
    setMessages((prev) =>
      prev.map((m) => {
        if (m.id === messageId && m.codeBlock) {
          return {
            ...m,
            codeBlock: {
              ...m.codeBlock,
              code: newCode,
            },
          };
        }
        return m;
      })
    );
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
          isStreaming={isLoading}
          errorMessage={errorMessage}
          onRetry={lastFailedPrompt ? () => handleSendMessage(lastFailedPrompt) : null}
          onSendMessage={handleSendMessage}
          onStopGeneration={handleStopGeneration}
          onUpdateMessageCode={handleUpdateMessageCode}
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
