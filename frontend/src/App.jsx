import React, { useState } from 'react';
import AppShell from './components/layout/AppShell';
import ChatWorkspace from './components/chat/ChatWorkspace';
import NotesPage from './pages/NotesPage';
import SavedPage from './pages/SavedPage';
import SearchPage from './pages/SearchPage';
import { INITIAL_SESSIONS, DEMO_CONVERSATION } from './services/mockData';

export default function App() {
  const [sessions, setSessions] = useState(INITIAL_SESSIONS);
  const [activeSessionId, setActiveSessionId] = useState('session-1');
  const [activeView, setActiveView] = useState('chat');
  const [isStudyMode, setIsStudyMode] = useState(false);
  const [conversationMap, setConversationMap] = useState({
    'session-1': DEMO_CONVERSATION,
    'session-2': [],
    'session-3': [],
  });

  const activeMessages = conversationMap[activeSessionId] || [];
  const currentSession = sessions.find((s) => s.id === activeSessionId) || sessions[0];

  const handleNewChat = () => {
    const newId = `session-${Date.now()}`;
    const newSession = {
      id: newId,
      title: 'New Conversation',
      lastUpdated: 'Just now',
      language: 'python',
      active: true,
    };
    setSessions([newSession, ...sessions]);
    setActiveSessionId(newId);
    setConversationMap((prev) => ({ ...prev, [newId]: [] }));
    setActiveView('chat');
  };

  const handleSelectSession = (sessionId) => {
    setActiveSessionId(sessionId);
    setActiveView('chat');
  };

  const handleSendMessage = (text) => {
    const userMsg = {
      id: `msg-${Date.now()}`,
      role: 'user',
      timestamp: 'Now',
      content: text,
      language: 'MULTILINGUAL',
    };

    // Simulate prompt response in local demo state
    const assistantMsg = {
      id: `msg-resp-${Date.now()}`,
      role: 'assistant',
      timestamp: 'Now',
      content: `Here is a solution for your query: "${text}".`,
      codeBlock: {
        filename: 'solution.py',
        language: 'python',
        code: `# Solution for: ${text}\ndef process_request():\n    print("Executing query in isolated Python sandbox...")\n    return 42\n\nif __name__ == "__main__":\n    process_request()`,
        validationStatus: 'VALID',
        executionStatus: 'SUCCESS',
        output: 'Executing query in isolated Python sandbox...\n42\n(Demo sandbox result)',
        durationMs: 148.0,
      },
      explanation: [
        'Modular definition with direct execution block.',
        'Validated against syntax specifications.'
      ],
      example: 'Executed in Docker container with --network none and non-root execution.',
      study: {
        problemUnderstanding: `Solving query: ${text}`,
        algorithm: [
          '1. Parse problem inputs.',
          '2. Apply optimized algorithm.',
          '3. Return formatted answer.'
        ],
        flowchart: `Start ──> Process Input ──> Validate Result ──> End`,
        importantPoints: [
          'Code executes within strict 256MB memory and 3s timeout limits.'
        ],
        vivaQuestions: [
          {
            q: 'How does isolated container execution protect the host system?',
            a: 'By dropping all Linux capabilities, enforcing non-root user, and disabling external networking.'
          }
        ]
      }
    };

    setConversationMap((prev) => ({
      ...prev,
      [activeSessionId]: [...(prev[activeSessionId] || []), userMsg, assistantMsg],
    }));

    // Update session title if default
    if (currentSession && currentSession.title === 'New Conversation') {
      const updatedTitle = text.slice(0, 24) + (text.length > 24 ? '...' : '');
      setSessions((prev) =>
        prev.map((s) => (s.id === activeSessionId ? { ...s, title: updatedTitle } : s))
      );
    }
  };

  return (
    <AppShell
      sessions={sessions}
      activeSessionId={activeSessionId}
      onSelectSession={handleSelectSession}
      onNewChat={handleNewChat}
      activeView={activeView}
      onSelectView={setActiveView}
      isStudyMode={isStudyMode}
      onToggleStudyMode={setIsStudyMode}
    >
      {activeView === 'chat' && (
        <ChatWorkspace
          messages={activeMessages}
          isStudyMode={isStudyMode}
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
