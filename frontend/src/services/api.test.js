import test from 'node:test';
import assert from 'node:assert/strict';
import { adaptBackendMessage, adaptChatResponse } from './api.js';

test('adaptBackendMessage correctly transforms backend message and code artifact', () => {
  const backendMsg = {
    id: 'msg-123',
    role: 'assistant',
    content: 'Here is your Python code.',
    detected_language: 'MARATHI_ENGLISH',
    intent: 'GENERATE_CODE',
    tone: 'CASUAL',
    created_at: '2026-10-08T18:00:00Z',
    code_block: {
      id: 'code-456',
      code: 'print("hello")',
      filename: 'solution.py',
      language: 'python',
      validation_status: 'valid',
    },
    study: {
      problem_understanding: 'Understand problem',
      algorithm: ['Step 1', 'Step 2'],
      flowchart: 'Start -> End',
      important_points: ['Point 1'],
      viva_questions: [{ question: 'Q1', answer: 'A1' }],
    },
  };

  const adapted = adaptBackendMessage(backendMsg);

  assert.equal(adapted.id, 'msg-123');
  assert.equal(adapted.role, 'assistant');
  assert.equal(adapted.content, 'Here is your Python code.');
  assert.ok(adapted.codeBlock);
  assert.equal(adapted.codeBlock.id, 'code-456');
  assert.equal(adapted.codeBlock.code, 'print("hello")');
  assert.equal(adapted.codeBlock.validationStatus, 'VALID');

  assert.ok(adapted.study);
  assert.equal(adapted.study.problemUnderstanding, 'Understand problem');
  assert.deepEqual(adapted.study.algorithm, ['Step 1', 'Step 2']);
  assert.equal(adapted.study.flowchart, 'Start -> End');
});

test('adaptChatResponse correctly transforms ChatResponse schema into view models', () => {
  const chatResponse = {
    session_id: 'session-789',
    message_id: 'msg-asst-101',
    user_message: {
      id: 'msg-user-100',
      content: 'python madhe calculator bana',
      detected_language: 'MARATHI_ENGLISH',
    },
    assistant_message: {
      id: 'msg-asst-101',
      content: 'Calculater tayar aahe.',
      explanation: ['Line 1', 'Line 2'],
      example: 'calc(1, 2)',
    },
    nlp: {
      language: 'MARATHI_ENGLISH',
      tone: 'CASUAL',
      intent: 'GENERATE_CODE',
    },
    code: [
      {
        id: 'code-1',
        language: 'python',
        filename: 'solution.py',
        content: 'def calc(): pass',
        validation_status: 'valid',
      },
    ],
    study: {
      problem_understanding: 'Make calculator',
      algorithm: ['Step 1'],
      flowchart: 'Flow',
      important_points: ['Key point'],
      viva_questions: [{ question: 'Q', answer: 'A' }],
    },
    execution: null,
  };

  const result = adaptChatResponse(chatResponse);

  assert.equal(result.sessionId, 'session-789');
  assert.equal(result.userMessage.id, 'msg-user-100');
  assert.equal(result.userMessage.content, 'python madhe calculator bana');
  assert.equal(result.assistantMessage.id, 'msg-asst-101');
  assert.equal(result.assistantMessage.content, 'Calculater tayar aahe.');
  assert.deepEqual(result.assistantMessage.explanation, ['Line 1', 'Line 2']);
  assert.ok(result.assistantMessage.codeBlock);
  assert.equal(result.assistantMessage.codeBlock.code, 'def calc(): pass');
  assert.equal(result.assistantMessage.codeBlock.validationStatus, 'VALID');
  assert.equal(result.assistantMessage.study.problemUnderstanding, 'Make calculator');
});
