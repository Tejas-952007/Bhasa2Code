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

export async function sendMessage({ sessionId = null, message, studyMode = false }) {
  return await request('/chat', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      message,
      study_mode: studyMode,
    }),
  });
}

// ---------------------------------------------------------------------------
// Code Validate and Run
// ---------------------------------------------------------------------------

export async function validateCode({ language, code }) {
  return await request('/code/validate', {
    method: 'POST',
    body: JSON.stringify({ language, code }),
  });
}

export async function runCode({ language, code, stdin = '' }) {
  return await request('/code/run', {
    method: 'POST',
    body: JSON.stringify({ language, code, stdin }),
  });
}

// ---------------------------------------------------------------------------
// View Model Adapters
// ---------------------------------------------------------------------------

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
      importantPoints: msg.study.important_points || msg.study.importantPoints || [],
      vivaQuestions: msg.study.viva_questions || msg.study.vivaQuestions || [],
    };
  }

  return {
    id: msg.id,
    role: msg.role,
    content: msg.content,
    codeBlock,
    explanation: msg.explanation || (isAssistant ? [] : undefined),
    example: msg.example || null,
    study,
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
      importantPoints: chatResp.study.important_points || [],
      vivaQuestions: chatResp.study.viva_questions || [],
    };
  }

  const assistantMessage = {
    id: chatResp.assistant_message.id,
    role: 'assistant',
    content: chatResp.assistant_message.content,
    explanation: chatResp.assistant_message.explanation || [],
    example: chatResp.assistant_message.example || null,
    codeBlock,
    study,
    nlp: chatResp.nlp,
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
