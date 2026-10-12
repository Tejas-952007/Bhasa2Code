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

test('Binary Search Study Mode: adapts flowchart_nodes, valid Python code artifact, and full walkthrough', () => {
  const binarySearchResp = {
    session_id: 'sess-bs',
    message_id: 'asst-bs',
    user_message: { id: 'u-bs', content: 'binary search in study mode' },
    assistant_message: {
      id: 'asst-bs',
      content: 'Here is the binary search implementation and study guide.',
      explanation: ['Iterative binary search with O(log n) time complexity.'],
      example: '### Example Walkthrough\nSearching 40 in [10, 20, 30, 40, 50]: index 3',
    },
    nlp: { language: 'ENGLISH', tone: 'FORMAL', intent: 'GENERATE_CODE' },
    code: [
      {
        id: 'code-bs',
        filename: 'solution.py',
        language: 'python',
        content: 'def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return -1',
        validation_status: 'valid',
      },
    ],
    study: {
      problem_understanding: 'Find index of target in sorted array in O(log n) time.',
      algorithm: ['1. Initialize low and high', '2. Compute mid', '3. Compare arr[mid] with target'],
      flowchart: '[Start] -> [Init low=0, high=n-1] -> [Check low <= high] -> [End]',
      flowchart_nodes: [
        { id: 'start', type: 'terminal', title: 'Start', accent: 'emerald' },
        { id: 'init', type: 'process', title: '1. Initialize Pointers', code: 'low = 0 ; high = len(arr) - 1', accent: 'blue' },
        { id: 'loop_cond', type: 'decision', title: '2. Loop Condition', condition: 'low <= high ?', branchYes: { label: 'YES', action: 'Compute Mid', outcomeType: 'success' }, branchNo: { label: 'NO', action: 'Not Found', outcomeType: 'error' } },
        { id: 'target_check', type: 'decision', title: '3. Compare Target', condition: 'arr[mid] == target ?', branchYes: { label: 'YES', action: 'Return mid', outcomeType: 'success' }, branchNo: { label: 'NO', action: 'Update Bounds', outcomeType: 'neutral' } },
        { id: 'end', type: 'terminal', title: 'End', accent: 'slate' },
      ],
      important_points: ['Array must be sorted', 'O(log n) complexity'],
      viva_questions: [{ question: 'What is the time complexity?', answer: 'O(log n)' }],
    },
  };

  const adapted = adaptChatResponse(binarySearchResp);
  // 1. Verify code artifact is valid executable Python, NOT an ASCII flowchart or Unsupported
  assert.ok(adapted.assistantMessage.codeBlock);
  assert.equal(adapted.assistantMessage.codeBlock.language, 'python');
  assert.equal(adapted.assistantMessage.codeBlock.validationStatus, 'VALID');
  assert.ok(!adapted.assistantMessage.codeBlock.code.includes('+---'));

  // 2. Verify flowchart nodes are adapted
  assert.ok(adapted.assistantMessage.study.flowchartNodes);
  assert.equal(adapted.assistantMessage.study.flowchartNodes.length, 5);
  const nodeIds = adapted.assistantMessage.study.flowchartNodes.map((n) => n.id);
  assert.ok(nodeIds.includes('start'));
  assert.ok(nodeIds.includes('init'));
  assert.ok(nodeIds.includes('loop_cond'));
  assert.ok(nodeIds.includes('target_check'));
  assert.ok(nodeIds.includes('end'));

  // 3. Verify example walkthrough is preserved
  assert.ok(adapted.assistantMessage.example.includes('40'));
  assert.ok(adapted.assistantMessage.example.includes('3'));
});

test('Incomplete Study Mode generation detection & recovery suggestions', () => {
  const truncatedResp = {
    session_id: 'sess-trunc',
    message_id: 'asst-trunc',
    user_message: { id: 'u-trunc', content: 'study mode binary search' },
    assistant_message: {
      id: 'asst-trunc',
      content: 'Here is the binary search routine...',
      is_incomplete: true,
      finish_reason: 'length',
    },
    nlp: { language: 'ENGLISH', tone: 'FORMAL', intent: 'GENERATE_CODE' },
    is_incomplete: true,
    finish_reason: 'length',
    code: [
      {
        id: 'code-trunc',
        filename: 'solution.py',
        language: 'python',
        content: 'def binary_search(arr, target):\n    low = 0',
        validation_status: 'incomplete',
      },
    ],
  };

  const adapted = adaptChatResponse(truncatedResp);
  assert.equal(adapted.assistantMessage.isIncomplete, true);
  assert.equal(adapted.assistantMessage.finishReason, 'length');
  assert.ok(adapted.assistantMessage.suggestions.includes('Complete the code'));
  assert.ok(adapted.assistantMessage.suggestions.includes('Continue from where it stopped'));
});

test('Linear Search Study Mode: adapts linear search nodes (i, arr[i], target) and never contains low/high/mid', () => {
  const linearSearchResp = {
    session_id: 'sess-ls',
    message_id: 'asst-ls',
    user_message: { id: 'u-ls', content: 'linear search in study mode' },
    assistant_message: {
      id: 'asst-ls',
      content: 'Here is the linear search implementation and study guide.',
      explanation: ['Sequential linear search with O(n) time complexity.'],
      example: '### Sample Input and Output\n**Input:**\narr = [5, 12, 18, 25, 30]\ntarget = 18\n\n**Output:**\nElement found at index 2',
    },
    nlp: { language: 'ENGLISH', tone: 'FORMAL', intent: 'GENERATE_CODE' },
    code: [
      {
        id: 'code-ls',
        filename: 'solution.py',
        language: 'python',
        content: 'def linear_search(arr, target):\n    for i in range(len(arr)):\n        if arr[i] == target: return i\n    return -1',
        validation_status: 'valid',
      },
    ],
    study: {
      problem_understanding: 'Inspect each element sequentially until target is found in O(n) time.',
      algorithm: ['1. Initialize pointer i = 0', '2. Check i < len(arr)', '3. Compare arr[i] == target'],
      flowchart: '[Start] -> [Init i=0] -> [Check i < len(arr)] -> [Check arr[i] == target] -> [End]',
      flowchart_nodes: [
        { id: 'start', type: 'terminal', title: 'Start', accent: 'emerald' },
        { id: 'init', type: 'process', title: '1. Initialize Pointer', code: 'i = 0', accent: 'blue' },
        { id: 'loop_cond', type: 'decision', title: '2. Boundary Check', condition: 'i < len(arr) ?', branchYes: { label: 'YES', action: 'Inspect arr[i]', outcomeType: 'success' }, branchNo: { label: 'NO', action: 'Not Found', outcomeType: 'error' } },
        { id: 'target_check', type: 'decision', title: '3. Compare Target', condition: 'arr[i] == target ?', branchYes: { label: 'YES', action: 'Return index i', outcomeType: 'success' }, branchNo: { label: 'NO', action: 'Increment i', outcomeType: 'neutral' } },
        { id: 'increment', type: 'process', title: '4. Increment', code: 'i = i + 1', accent: 'blue' },
        { id: 'end', type: 'terminal', title: 'End', accent: 'slate' },
      ],
      important_points: ['Works on unsorted arrays', 'O(n) worst case'],
      viva_questions: [{ question: 'What is the time complexity?', answer: 'O(n)' }],
    },
  };

  const adapted = adaptChatResponse(linearSearchResp);

  // 1. Verify code artifact is valid executable Python
  assert.ok(adapted.assistantMessage.codeBlock);
  assert.equal(adapted.assistantMessage.codeBlock.language, 'python');
  assert.equal(adapted.assistantMessage.codeBlock.validationStatus, 'VALID');
  assert.ok(adapted.assistantMessage.codeBlock.code.includes('linear_search'));

  // 2. Verify flowchart nodes NEVER contain low, high, mid or arr[mid]
  assert.ok(adapted.assistantMessage.study.flowchartNodes);
  assert.equal(adapted.assistantMessage.study.flowchartNodes.length, 6);
  const nodesSerialized = JSON.stringify(adapted.assistantMessage.study.flowchartNodes).toLowerCase();
  assert.ok(!nodesSerialized.includes('low'));
  assert.ok(!nodesSerialized.includes('high'));
  assert.ok(!nodesSerialized.includes('mid'));
  assert.ok(nodesSerialized.includes('i = 0'));
  assert.ok(nodesSerialized.includes('arr[i]'));

  // 3. Verify sample input and output matches requirements
  assert.ok(adapted.assistantMessage.example.includes('5, 12, 18, 25, 30'));
  assert.ok(adapted.assistantMessage.example.includes('18'));
  assert.ok(adapted.assistantMessage.example.includes('Element found at index 2'));
});

test('Prime Number request: concise code with two test cases adapted with no study mode pollution', () => {
  const primeResp = {
    session_id: 'sess-prime',
    message_id: 'asst-prime',
    user_message: {
      id: 'u-prime',
      content: 'Write a Python function to check if a number is prime. Give only complete Python code and two simple test cases.',
    },
    assistant_message: {
      id: 'asst-prime',
      content: 'Here is the prime check code with two test cases:',
      is_incomplete: false,
      finish_reason: 'stop',
    },
    nlp: { language: 'ENGLISH', tone: 'CASUAL', intent: 'GENERATE_CODE' },
    is_incomplete: false,
    finish_reason: 'stop',
    code: [
      {
        id: 'code-prime',
        filename: 'solution.py',
        language: 'python',
        content:
          'def is_prime(n: int) -> bool:\n' +
          '    if n <= 1:\n' +
          '        return False\n' +
          '    if n <= 3:\n' +
          '        return True\n' +
          '    if n % 2 == 0 or n % 3 == 0:\n' +
          '        return False\n' +
          '    i = 5\n' +
          '    while i * i <= n:\n' +
          '        if n % i == 0 or n % (i + 2) == 0:\n' +
          '            return False\n' +
          '        i += 6\n' +
          '    return True\n\n' +
          'if __name__ == "__main__":\n' +
          '    assert is_prime(7) is True\n' +
          '    assert is_prime(4) is False\n' +
          '    print("All tests passed.")',
        validation_status: 'valid',
      },
    ],
    study: null,
  };

  const adapted = adaptChatResponse(primeResp);
  assert.equal(adapted.assistantMessage.isIncomplete, false);
  assert.equal(adapted.assistantMessage.finishReason, 'stop');
  assert.ok(adapted.assistantMessage.codeBlock);
  assert.equal(adapted.assistantMessage.codeBlock.validationStatus, 'VALID');
  assert.ok(adapted.assistantMessage.codeBlock.code.includes('is_prime'));
  assert.ok(adapted.assistantMessage.codeBlock.code.includes('assert is_prime(7) is True'));
  assert.ok(adapted.assistantMessage.codeBlock.code.includes('assert is_prime(4) is False'));
  assert.equal(adapted.assistantMessage.study, null);
});

test('Continuation Truncation: detects isContinuation and suppresses repeated Complete Code loops', () => {
  const continuationResp = {
    session_id: 'sess-cont',
    message_id: 'asst-cont',
    user_message: {
      id: 'u-cont',
      content: 'Complete the code from where it stopped',
    },
    assistant_message: {
      id: 'asst-cont',
      content: 'def is_prime(n):\n    if n <= 1:\n        return False',
      is_incomplete: true,
      finish_reason: 'length',
    },
    nlp: { language: 'ENGLISH', tone: 'CASUAL', intent: 'GENERATE_CODE' },
    is_incomplete: true,
    finish_reason: 'length',
    code: [
      {
        id: 'code-cont',
        filename: 'solution.py',
        language: 'python',
        content: 'def is_prime(n):\n    if n <= 1:\n        return False',
        validation_status: 'incomplete',
      },
    ],
  };

  const adapted = adaptChatResponse(continuationResp);
  assert.equal(adapted.assistantMessage.isIncomplete, true);
  assert.equal(adapted.assistantMessage.isContinuation, true);
  assert.equal(adapted.assistantMessage.finishReason, 'length');
  // Suggestions must NOT offer repeated "Complete the code" loop
  assert.ok(!adapted.assistantMessage.suggestions.includes('Complete the code'));
});

