import test from 'node:test';
import assert from 'node:assert/strict';

/**
 * Unit & Component Model Tests for T24 Real-Time Code Validation & Execution UX
 */

// Helper to mimic diagnostic parser logic
function parseDiagnostic(diag) {
  if (typeof diag !== 'string') return { text: String(diag), line: null, col: null, severity: 'ERROR' };
  const lineColMatch = diag.match(/\(line\s+(\d+)(?:,\s*col(?:umn)?\s*(\d+))?\)/i);
  const line = lineColMatch ? parseInt(lineColMatch[1], 10) : null;
  const col = lineColMatch && lineColMatch[2] ? parseInt(lineColMatch[2], 10) : null;
  const sevMatch = diag.match(/^\[(ERROR|WARNING|INFO)\]/i);
  const severity = sevMatch ? sevMatch[1].toUpperCase() : 'ERROR';
  const cleanMsg = diag.replace(/^\[(ERROR|WARNING|INFO)\]\s*/i, '').replace(/\(line\s+\d+.*?\)/i, '').trim();
  return { text: cleanMsg || diag, line, col, severity };
}

test('T24 Diagnostic Parser: accurately extracts line, column, and severity', () => {
  const diag1 = "[ERROR] Expected ':' (line 4, column 12)";
  const parsed1 = parseDiagnostic(diag1);
  assert.equal(parsed1.line, 4);
  assert.equal(parsed1.col, 12);
  assert.equal(parsed1.severity, 'ERROR');
  assert.equal(parsed1.text, "Expected ':'");

  const diag2 = "[WARNING] variable 'temp' unused (line 15)";
  const parsed2 = parseDiagnostic(diag2);
  assert.equal(parsed2.line, 15);
  assert.equal(parsed2.col, null);
  assert.equal(parsed2.severity, 'WARNING');
  assert.equal(parsed2.text, "variable 'temp' unused");

  const diag3 = "Simple syntax error";
  const parsed3 = parseDiagnostic(diag3);
  assert.equal(parsed3.line, null);
  assert.equal(parsed3.col, null);
  assert.equal(parsed3.severity, 'ERROR');
  assert.equal(parsed3.text, "Simple syntax error");
});

test('T24 Code Revision Model: edits mark validation and execution stale', () => {
  class CodeRevisionManager {
    constructor(initialCode) {
      this.code = initialCode;
      this.revision = 1;
      this.validatedRevision = 1;
      this.validationStatus = 'VALID';
      this.executionResult = { status: 'SUCCESS', stdout: '42', isStale: false };
      this.executedRevision = 1;
    }

    applyEdit(newCode) {
      if (newCode === this.code) return;
      this.code = newCode;
      this.revision += 1;
      // Invalidate existing validation
      this.validationStatus = 'NOT_VALIDATED';
      // Mark execution as stale
      if (this.executionResult) {
        this.executionResult.isStale = true;
      }
    }

    applyValidationResult(targetRevision, status) {
      // Stale-result protection
      if (targetRevision === this.revision) {
        this.validationStatus = status;
        this.validatedRevision = targetRevision;
        return true;
      }
      return false; // Ignored as stale
    }
  }

  const manager = new CodeRevisionManager('x = 10\nprint(x)');
  assert.equal(manager.validationStatus, 'VALID');
  assert.equal(manager.executionResult.isStale, false);

  // User edits code
  manager.applyEdit('x = 10\nprint(x + 5)');
  assert.equal(manager.revision, 2);
  assert.equal(manager.validationStatus, 'NOT_VALIDATED');
  assert.equal(manager.executionResult.isStale, true);

  // Late response for Revision 1 arrives — must be rejected
  const lateApplied = manager.applyValidationResult(1, 'VALID');
  assert.equal(lateApplied, false);
  assert.equal(manager.validationStatus, 'NOT_VALIDATED');

  // Response for Revision 2 arrives — accepted
  const freshApplied = manager.applyValidationResult(2, 'VALID');
  assert.equal(freshApplied, true);
  assert.equal(manager.validationStatus, 'VALID');
  assert.equal(manager.validatedRevision, 2);
});

test('T24 Execution Gating: invalid code cannot be executed', () => {
  function canExecuteCode(validationStatus, isValidatedForCurrentRevision) {
    if (validationStatus === 'INVALID' && isValidatedForCurrentRevision) {
      return { allowed: false, reason: 'VALIDATION_FAILED' };
    }
    return { allowed: true };
  }

  // Case 1: Code is VALID
  const check1 = canExecuteCode('VALID', true);
  assert.equal(check1.allowed, true);

  // Case 2: Code is INVALID for current revision
  const check2 = canExecuteCode('INVALID', true);
  assert.equal(check2.allowed, false);
  assert.equal(check2.reason, 'VALIDATION_FAILED');

  // Case 3: Code was NOT_VALIDATED yet (backend T18 gate will validate on run)
  const check3 = canExecuteCode('NOT_VALIDATED', false);
  assert.equal(check3.allowed, true);
});

test('T24 Debounce Behavior: rapid typing resets timer', async () => {
  let callCount = 0;
  let timer = null;

  function scheduleValidation(delayMs) {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      callCount++;
    }, delayMs);
  }

  // Simulate 3 rapid keystrokes within 50ms intervals
  scheduleValidation(100);
  await new Promise((r) => setTimeout(r, 30));
  scheduleValidation(100);
  await new Promise((r) => setTimeout(r, 30));
  scheduleValidation(100);

  // Only wait 50ms — timer should not have fired yet
  await new Promise((r) => setTimeout(r, 50));
  assert.equal(callCount, 0);

  // Wait full delay
  await new Promise((r) => setTimeout(r, 120));
  assert.equal(callCount, 1);
});

test('T24 Concurrency & Duplicate Click Prevention: locks active operation', () => {
  let inFlight = false;
  let runCount = 0;

  function triggerRun() {
    if (inFlight) return false;
    inFlight = true;
    runCount++;
    return true;
  }

  // First click succeeds
  assert.equal(triggerRun(), true);
  assert.equal(runCount, 1);

  // Rapid duplicate clicks while running are blocked
  assert.equal(triggerRun(), false);
  assert.equal(triggerRun(), false);
  assert.equal(runCount, 1);

  // Once finished, subsequent clicks work
  inFlight = false;
  assert.equal(triggerRun(), true);
  assert.equal(runCount, 2);
});

test('T24 Security & Integrity: Flowcharts are excluded from code execution', () => {
  const NON_CODE_KINDS = ['FLOWCHART', 'DIAGRAM', 'ASCII'];

  function isExecutableCodeArtifact(item) {
    if (!item) return false;
    if (NON_CODE_KINDS.includes((item.type || '').toUpperCase())) return false;
    const lang = (item.language || '').toLowerCase();
    const VALID_EXEC_LANGUAGES = ['python', 'c', 'cpp', 'java', 'javascript', 'sql'];
    return VALID_EXEC_LANGUAGES.includes(lang);
  }

  assert.equal(isExecutableCodeArtifact({ type: 'FLOWCHART', language: 'python' }), false);
  assert.equal(isExecutableCodeArtifact({ type: 'CODE', language: 'python' }), true);
  assert.equal(isExecutableCodeArtifact({ type: 'CODE', language: 'c' }), true);
  assert.equal(isExecutableCodeArtifact({ language: 'ascii' }), false);
});
