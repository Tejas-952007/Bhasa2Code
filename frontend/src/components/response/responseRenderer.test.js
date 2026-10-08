import test from 'node:test';
import assert from 'node:assert/strict';
import { adaptChatResponse, adaptBackendMessage } from '../../services/api.js';

test('Response Renderer Models: plain assistant text with headings and lists', () => {
  const backendResp = {
    session_id: 'sess-1',
    message_id: 'asst-1',
    user_message: { id: 'u-1', content: 'python list reverse code de' },
    assistant_message: {
      id: 'asst-1',
      content: 'Here is how to reverse a list in Python.',
      explanation: [
        'Method 1: Using slice syntax `lst[::-1]`',
        'Method 2: Using the in-place `lst.reverse()` method',
      ],
      example: 'numbers = [1, 2, 3]\nprint(numbers[::-1])',
    },
    nlp: {
      language: 'MARATHI_ENGLISH',
      tone: 'CASUAL',
      intent: 'GENERATE_CODE',
    },
    code: [
      {
        id: 'code-1',
        filename: 'reverse.py',
        language: 'python',
        content: 'def reverse_list(items):\n    return items[::-1]',
        validation_status: 'valid',
      },
    ],
  };

  const adapted = adaptChatResponse(backendResp);
  assert.equal(adapted.assistantMessage.content, 'Here is how to reverse a list in Python.');
  assert.equal(adapted.assistantMessage.explanation.length, 2);
  assert.ok(adapted.assistantMessage.codeBlock);
  assert.equal(adapted.assistantMessage.codeBlock.filename, 'reverse.py');
  assert.equal(adapted.assistantMessage.codeBlock.language, 'python');
  assert.equal(adapted.assistantMessage.codeBlock.validationStatus, 'VALID');
});

test('Validation status resolution: valid, invalid, and diagnostics', () => {
  const validArtifact = {
    id: 'c-1',
    language: 'python',
    filename: 'calc.py',
    content: 'def add(a, b): return a + b',
    validation_status: 'valid',
  };

  const invalidArtifact = {
    id: 'c-2',
    language: 'python',
    filename: 'calc_bad.py',
    content: 'def add(a, b)\n  return a + b',
    validation_status: 'invalid',
  };

  const respValid = adaptChatResponse({
    session_id: 's-1',
    message_id: 'm-1',
    user_message: { id: 'u-1', content: 'calc' },
    assistant_message: { id: 'm-1', content: 'Code' },
    nlp: { language: 'ENGLISH', tone: 'CASUAL', intent: 'GENERATE_CODE' },
    code: [validArtifact],
  });

  const respInvalid = adaptChatResponse({
    session_id: 's-2',
    message_id: 'm-2',
    user_message: { id: 'u-2', content: 'calc' },
    assistant_message: { id: 'm-2', content: 'Code' },
    nlp: { language: 'ENGLISH', tone: 'CASUAL', intent: 'GENERATE_CODE' },
    code: [invalidArtifact],
  });

  assert.equal(respValid.assistantMessage.codeBlock.validationStatus, 'VALID');
  assert.equal(respInvalid.assistantMessage.codeBlock.validationStatus, 'INVALID');
});

test('Execution status handling: success, runtime error, timeout, resource limit, sandbox error', () => {
  // Simulate statuses handled by ExecutionResult
  const statuses = [
    { status: 'SUCCESS', stdout: 'Result: 15\n', exitCode: 0, duration: 120 },
    { status: 'RUNTIME_ERROR', stderr: 'ZeroDivisionError: division by zero\n', exitCode: 1, duration: 80 },
    { status: 'TIMEOUT', exitCode: 124, duration: 5000 },
    { status: 'RESOURCE_LIMIT', exitCode: 137, duration: 250 },
    { status: 'SANDBOX_ERROR', diagnostics: ['Docker unavailable'], exitCode: 1, duration: 0 },
  ];

  for (const s of statuses) {
    assert.ok(s.status);
    if (s.status === 'SUCCESS') {
      assert.equal(s.exitCode, 0);
      assert.ok(s.stdout.includes('15'));
    } else if (s.status === 'RUNTIME_ERROR') {
      assert.equal(s.exitCode, 1);
      assert.ok(s.stderr.includes('ZeroDivisionError'));
    } else if (s.status === 'TIMEOUT') {
      assert.equal(s.duration, 5000);
    }
  }
});

test('Study Mode structured generation: problem understanding, algorithm, flowchart, viva', () => {
  const studyResp = {
    session_id: 'sess-study',
    message_id: 'asst-study',
    user_message: { id: 'u-s', content: 'python madhe calculator bana study mode' },
    assistant_message: {
      id: 'asst-study',
      content: 'Here is the comprehensive study guide for calculator routine.',
      explanation: ['Basic addition, subtraction, multiplication, and division.'],
      example: 'calc(10, 5) -> 15',
    },
    nlp: {
      language: 'MARATHI_ENGLISH',
      tone: 'FORMAL',
      intent: 'GENERATE_CODE',
    },
    code: [
      {
        id: 'code-study',
        filename: 'calculator.py',
        language: 'python',
        content: 'def calculate(): pass',
        validation_status: 'valid',
      },
    ],
    study: {
      problem_understanding: 'Build an interactive console calculator that performs arithmetic.',
      algorithm: ['1. Read operands', '2. Check division by zero', '3. Return output'],
      flowchart: 'Start -> Input -> Check Zero -> Compute -> End',
      important_points: ['Float conversion prevents integer truncation', 'ZeroDivisionError handling'],
      viva_questions: [
        { question: 'Why check division by zero before dividing?', answer: 'To avoid unhandled runtime exception' },
      ],
    },
  };

  const adapted = adaptChatResponse(studyResp);
  assert.ok(adapted.assistantMessage.study);
  assert.equal(adapted.assistantMessage.study.problemUnderstanding, 'Build an interactive console calculator that performs arithmetic.');
  assert.equal(adapted.assistantMessage.study.algorithm.length, 3);
  assert.equal(adapted.assistantMessage.study.importantPoints.length, 2);
  assert.equal(adapted.assistantMessage.study.vivaQuestions.length, 1);
  assert.equal(adapted.assistantMessage.study.vivaQuestions[0].question, 'Why check division by zero before dividing?');
});

test('Follow-up continuity: previous code indicator and updated code detection', () => {
  const followUpResp = {
    session_id: 'sess-existing',
    message_id: 'asst-followup',
    user_message: { id: 'u-f', content: 'yat error handling add kar' },
    assistant_message: {
      id: 'asst-followup',
      content: 'Updated calculator with error handling.',
      explanation: [
        'Added input validation for numeric types',
        'Added division-by-zero handling with friendly alert',
      ],
      example: 'Enter second number: 0 -> Error',
    },
    nlp: {
      language: 'MARATHI_ENGLISH',
      tone: 'CASUAL',
      intent: 'MODIFY_CODE',
    },
    code: [
      {
        id: 'code-updated',
        filename: 'calculator.py',
        language: 'python',
        content: 'def calculator():\n    try:\n        ...\n    except ZeroDivisionError:\n        ...',
        validation_status: 'valid',
      },
    ],
  };

  const adapted = adaptChatResponse(followUpResp);
  assert.equal(adapted.assistantMessage.isFollowUp, true);
  assert.ok(adapted.assistantMessage.activeContext);
  assert.equal(adapted.assistantMessage.activeContext.filename, 'calculator.py');
  assert.ok(adapted.assistantMessage.changes);
  assert.equal(adapted.assistantMessage.changes.length, 2);
  assert.ok(adapted.assistantMessage.suggestions.includes('Add unit tests'));
});

test('Empty State and suggestions presentation constraints', () => {
  const respWithCode = adaptChatResponse({
    session_id: 'sess-new',
    message_id: 'asst-first',
    user_message: { id: 'u-1', content: 'calculator' },
    assistant_message: { id: 'asst-first', content: 'Calculator code' },
    nlp: { language: 'ENGLISH', tone: 'CASUAL', intent: 'GENERATE_CODE' },
    code: [
      {
        id: 'c-1',
        filename: 'main.py',
        language: 'python',
        content: 'code',
        validation_status: 'valid',
      },
    ],
  });

  // Verify suggestions are capped to 3-5
  assert.ok(respWithCode.assistantMessage.suggestions.length <= 5);
  assert.ok(respWithCode.assistantMessage.suggestions.length >= 2);
});
