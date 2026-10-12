/**
 * Bhasha2Code Centralized API Client
 * Connects React UI to FastAPI backend endpoints (/api/v1).
 */

const BASE_URL =
  (typeof import.meta !== 'undefined' &&
    import.meta.env &&
    import.meta.env.VITE_API_BASE_URL) ||
  'http://127.0.0.1:8000/api/v1';

class APIError extends Error {
  constructor(code, message, status = 500) {
    super(message);
    this.name = 'APIError';
    this.code = code;
    this.status = status;
  }
}

/**
 * Perform JSON request with robust network and HTTP error handling.
 */
async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    });

    if (!res.ok) {
      let errorData;
      try {
        errorData = await res.json();
      } catch {
        errorData = null;
      }

      if (errorData && errorData.error) {
        throw new APIError(
          errorData.error.code || 'API_ERROR',
          errorData.error.message || `Request failed with status ${res.status}`,
          res.status
        );
      }

      throw new APIError(
        'HTTP_ERROR',
        `Request failed with status ${res.status}`,
        res.status
      );
    }

    return await res.json();
  } catch (err) {
    if (err instanceof APIError) {
      throw err;
    }
    // Network / connection drop
    throw new APIError(
      'NETWORK_ERROR',
      'Unable to connect to the backend server. Please verify FastAPI is running.',
      0
    );
  }
}

// ---------------------------------------------------------------------------
// Health
// ---------------------------------------------------------------------------

export async function health() {
  return await request('/health');
}

// ---------------------------------------------------------------------------
// Sessions
// ---------------------------------------------------------------------------

export async function listSessions(limit = 100, offset = 0) {
  return await request(`/sessions?limit=${limit}&offset=${offset}`);
}

export async function createSession(title = '') {
  return await request('/sessions', {
    method: 'POST',
    body: JSON.stringify({ title }),
  });
}

export async function getSession(sessionId) {
  return await request(`/sessions/${sessionId}`);
}

export async function renameSession(sessionId, title) {
  return await request(`/sessions/${sessionId}`, {
    method: 'PATCH',
    body: JSON.stringify({ title }),
  });
}

export async function deleteSession(sessionId) {
  return await request(`/sessions/${sessionId}`, {
    method: 'DELETE',
  });
}

// ---------------------------------------------------------------------------
// Chat
// ---------------------------------------------------------------------------

export async function sendMessage({ sessionId = null, message, studyMode = false, clientTurnId = null }) {
  return await request('/chat', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      message,
      study_mode: studyMode,
      client_turn_id: clientTurnId,
    }),
  });
}

/**
 * Stream a chat message via SSE (Server-Sent Events) over fetch POST.
 *
 * Returns an async generator yielding parsed event objects:
 *   {type: 'start',    session_id, user_message_id}
 *   {type: 'token',    token}
 *   {type: 'complete', session_id, message_id, user_message, assistant_message, nlp, code, study}
 *   {type: 'error',    code, message}
 *
 * @param {Object} params
 * @param {string|null} params.sessionId
 * @param {string} params.message
 * @param {boolean} params.studyMode
 * @param {string|null} [params.clientTurnId]
 * @param {AbortSignal} [params.signal] - optional AbortController signal for cancellation
 */
export async function* streamMessage({ sessionId = null, message, studyMode = false, clientTurnId = null, signal } = {}) {
  const url = `${BASE_URL}/chat/stream`;

  let response;
  try {
    response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        message,
        study_mode: studyMode,
        client_turn_id: clientTurnId,
      }),
      signal,
    });
  } catch (err) {
    if (err.name === 'AbortError') return;
    throw new APIError(
      'NETWORK_ERROR',
      'Unable to connect to the backend server. Please verify FastAPI is running.',
      0
    );
  }

  if (!response.ok) {
    let errorData = null;
    try { errorData = await response.json(); } catch { /* ignore */ }
    const msg = errorData?.error?.message || `Stream request failed with status ${response.status}`;
    throw new APIError(errorData?.error?.code || 'HTTP_ERROR', msg, response.status);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // Process complete SSE lines
      const lines = buffer.split('\n');
      // Keep the last incomplete line in buffer
      buffer = lines.pop() ?? '';

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed.startsWith('data:')) continue;
        const jsonStr = trimmed.slice(5).trim();
        if (!jsonStr) continue;
        try {
          const event = JSON.parse(jsonStr);
          yield event;
          // Stop iteration after terminal events
          if (event.type === 'complete' || event.type === 'error') return;
        } catch {
          // Malformed JSON in stream — skip
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

// ---------------------------------------------------------------------------
// Code Validate and Run
// ---------------------------------------------------------------------------

export async function validateCode({ language, code, signal }) {
  return await request('/code/validate', {
    method: 'POST',
    body: JSON.stringify({ language, code }),
    signal,
  });
}

export async function runCode({ language, code, stdin = '', signal }) {
  return await request('/code/run', {
    method: 'POST',
    body: JSON.stringify({ language, code, stdin }),
    signal,
  });
}

export function getInteractiveRunWsUrl() {
  const httpUrl = BASE_URL;
  const wsUrl = httpUrl.replace(/^http:/i, 'ws:').replace(/^https:/i, 'wss:');
  return `${wsUrl}/code/interactive-run`;
}

// ---------------------------------------------------------------------------
// View Model Adapters
// ---------------------------------------------------------------------------

function stripCodeBlocks(text) {
  if (!text) return '';
  let cleaned = text.replace(/(?:```|~~~)[\s\S]*?(?:```|~~~)/g, '');
  cleaned = cleaned.replace(/(?:```|~~~)[\s\S]*$/g, '');
  return cleaned.trim();
}

/**
 * Adapt a backend message item from GET /sessions/{id} into frontend view model.
 */
export function adaptBackendMessage(msg) {
  const isAssistant = msg.role === 'assistant';
  let codeBlock = null;

  if (msg.code_block) {
    codeBlock = {
      id: msg.code_block.id,
      code: msg.code_block.code || msg.code_block.content || '',
      filename: msg.code_block.filename || 'solution.py',
      language: msg.code_block.language || 'python',
      validationStatus: (msg.code_block.validationStatus || msg.code_block.validation_status || 'VALID').toUpperCase(),
      diagnostics: msg.code_block.diagnostics || [],
      executionStatus: msg.code_block.executionStatus || null,
      output: msg.code_block.output || null,
      durationMs: msg.code_block.durationMs || 0,
    };
  }

  let study = null;
  if (msg.study) {
    study = {
      problemUnderstanding: msg.study.problem_understanding || msg.study.problemUnderstanding,
      algorithm: msg.study.algorithm || [],
      flowchart: msg.study.flowchart || null,
      flowchartNodes: msg.study.flowchart_nodes || msg.study.flowchartNodes || null,
      importantPoints: msg.study.important_points || msg.study.importantPoints || [],
      vivaQuestions: msg.study.viva_questions || msg.study.vivaQuestions || [],
    };
  }

  const cleanContent = isAssistant && msg.content ? stripCodeBlocks(msg.content) : msg.content;
  const isIncomplete = Boolean(
    msg.is_incomplete ||
      msg.finish_reason === 'length' ||
      (codeBlock && codeBlock.validationStatus === 'INCOMPLETE')
  );

  return {
    id: msg.id,
    role: msg.role,
    content: cleanContent,
    codeBlock,
    explanation: msg.explanation || (isAssistant ? [] : undefined),
    example: msg.example || null,
    study,
    isIncomplete,
    finishReason: msg.finish_reason || (isIncomplete ? 'length' : 'stop'),
    timestamp: msg.created_at,
  };
}

/**
 * Adapt backend ChatResponse into frontend assistant message model.
 */
export function adaptChatResponse(chatResp) {
  const primaryCode = chatResp.code && chatResp.code.length > 0 ? chatResp.code[0] : null;

  const codeBlock = primaryCode
    ? {
        id: primaryCode.id,
        code: primaryCode.content,
        filename: primaryCode.filename,
        language: primaryCode.language,
        validationStatus: primaryCode.validation_status.toUpperCase(),
        diagnostics: primaryCode.diagnostics || [],
        executionStatus: null,
        output: null,
        durationMs: 0,
      }
    : null;

  let study = null;
  if (chatResp.study) {
    study = {
      problemUnderstanding: chatResp.study.problem_understanding,
      algorithm: chatResp.study.algorithm || [],
      flowchart: chatResp.study.flowchart || null,
      flowchartNodes: chatResp.study.flowchart_nodes || chatResp.study.flowchartNodes || null,
      importantPoints: chatResp.study.important_points || [],
      vivaQuestions: chatResp.study.viva_questions || [],
    };
  }

  const intent = chatResp.nlp?.intent || '';
  const isFollowUp = intent === 'MODIFY_CODE' || intent === 'DEBUG_CODE';
  const isIncomplete = Boolean(
    chatResp.is_incomplete ||
      chatResp.finish_reason === 'length' ||
      chatResp.assistant_message?.is_incomplete ||
      chatResp.assistant_message?.finish_reason === 'length' ||
      (primaryCode && primaryCode.validation_status.toUpperCase() === 'INCOMPLETE')
  );

  const isContinuation = Boolean(
    chatResp.user_message?.content &&
      /\b(complete\s+(?:the\s+)?code|continue\s+(?:the\s+)?code|finish\s+(?:the\s+)?code|continue\s+from\s+where\s+it\s+stopped)\b/i.test(
        chatResp.user_message.content
      )
  );

  // Build subtle, relevant suggestions (max 3-4)
  const suggestions = [];
  if (isIncomplete && !isContinuation) {
    suggestions.push('Complete the code');
    suggestions.push('Continue from where it stopped');
  }
  if (codeBlock) {
    if (!isFollowUp) {
      if (!isIncomplete) {
        suggestions.push('Add input validation');
        suggestions.push('Handle division by zero');
      }
      suggestions.push('Explain this code step by step');
    } else {
      suggestions.push('Add unit tests');
      suggestions.push('Format with type annotations');
      suggestions.push('Run secure sandbox');
    }
  }

  // Extract changes if this is an update
  const changes = [];
  if (isFollowUp && chatResp.assistant_message.explanation) {
    chatResp.assistant_message.explanation.forEach((exp) => {
      if (/add|handl|fix|updat|check|validat/i.test(exp)) {
        changes.push(exp);
      }
    });
  }

  const cleanContent = chatResp.assistant_message.content
    ? stripCodeBlocks(chatResp.assistant_message.content)
    : '';

  const assistantMessage = {
    id: chatResp.assistant_message.id,
    role: 'assistant',
    content: cleanContent,
    explanation: chatResp.assistant_message.explanation || [],
    example: chatResp.assistant_message.example || null,
    codeBlock,
    study,
    nlp: chatResp.nlp,
    suggestions,
    changes: changes.length > 0 ? changes : undefined,
    isFollowUp,
    isIncomplete,
    isContinuation,
    finishReason: chatResp.finish_reason || chatResp.assistant_message?.finish_reason || (isIncomplete ? 'length' : 'stop'),
    activeContext: isFollowUp && primaryCode ? { filename: primaryCode.filename } : null,
  };

  const userMessage = {
    id: chatResp.user_message.id,
    role: 'user',
    content: chatResp.user_message.content,
    detectedLanguage: chatResp.user_message.detected_language,
  };

  return {
    sessionId: chatResp.session_id,
    messageId: chatResp.message_id,
    userMessage,
    assistantMessage,
  };
}
