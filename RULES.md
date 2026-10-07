# Bhasha2Code — Development Rules

> These rules are mandatory for all AI-assisted development, including Antigravity-generated code.

---

# 1. Core Principle

Bhasha2Code must be developed as an engineered product, not as a collection of disconnected AI-generated files.

Every implementation must fit the existing architecture.

---

# 2. Antigravity Rules

Antigravity must:

1. Inspect the existing repository before making changes.
2. Read relevant documentation before implementing a feature.
3. Read existing code before modifying it.
4. Reuse existing components where possible.
5. Avoid unnecessary rewrites.
6. Avoid creating duplicate modules.
7. Follow the approved architecture.
8. Follow the current PRD.
9. Follow security requirements.
10. Add or update tests for meaningful code changes.
11. Clearly report files changed.
12. Clearly report assumptions.
13. Clearly report unresolved issues.
14. Never claim a feature is complete without verification.

---

# 3. No Blind Vibe Coding

Never use this pattern:

```text
Prompt AI
↓
Generate huge codebase
↓
Assume it works
```

Required approach:

```text
Understand
↓
Plan
↓
Implement
↓
Test
↓
Review
↓
Fix
↓
Verify
```

---

# 4. Existing Code First

Before modifying a feature:

```text
Inspect
↓
Understand
↓
Identify dependencies
↓
Modify
↓
Test
```

Do not replace working code simply because a new implementation looks cleaner.

---

# 5. Architecture Rule

All new features must have a clear architectural location.

Do not place unrelated functionality into random files.

For example:

```text
NLP → backend/nlp/
LLM → backend/llm/
Code → backend/code_engine/
Database → backend/database/
API → backend/api/
UI → frontend/
Tests → tests/
```

---

# 6. No Duplicate Logic

Before creating a helper/function/class:

Check whether equivalent functionality already exists.

If it exists:

- reuse it
- extend it
- refactor it carefully

Do not create duplicate implementations.

---

# 7. Documentation Rule

Every major architectural or technical decision should be documented.

When implementation changes the architecture:

1. Update documentation.
2. Explain why.
3. Update affected tasks.
4. Add/update tests.

---

# 8. Requirement Rule

Every major feature should map to a requirement.

Example:

```text
FR-001 → Multilingual Input
FR-002 → Code Generation
FR-003 → Debugging
```

Implementation should not silently introduce major scope changes.

---

# 9. Scope Control

### MUST HAVE

Must be completed before production release.

### IMPORTANT

Should be implemented after the core MVP is stable.

### V2

Do not allow V2 features to destabilize MUST HAVE features.

---

# 10. NLP Rules

NLP functionality must remain visible and testable.

The project must not become only:

```text
User → LLM → Answer
```

The intended pipeline is:

```text
Input
↓
Preprocessing
↓
Language Detection
↓
Tone Detection
↓
Intent Detection
↓
Programming Language Detection
↓
Requirement Extraction
↓
Context
↓
LLM
```

---

# 11. LLM Rules

The local LLM must be treated as a component, not the entire application.

LLM output must be:

- Parsed
- Validated where applicable
- Contextually checked
- Safely displayed

Do not trust generated code automatically.

---

# 12. Offline Rule

Core functionality must not require an internet connection.

Do not introduce mandatory cloud APIs for:

- Code generation
- Chat
- NLP
- Session storage
- Study Mode
- PDF export

Optional online functionality may exist only as a separate mode.

---

# 13. Context Rule

Follow-up questions must use relevant conversation context.

Example:

```text
User:
Create calculator.

User:
Add error handling.
```

The second request must resolve to the previous calculator unless the user explicitly changes context.

Do not unnecessarily ask the user to repeat information already available in the active session.

---

# 14. Suggestion Rule

Suggestions must be:

- Relevant
- Useful
- Short
- Technically justified

Do not generate unnecessary suggestions simply to make the response longer.

Possible suggestion categories:

```text
Performance
Security
Best Practice
Architecture
Error Handling
Maintainability
Feature Improvement
```

---

# 15. Code Execution Rule

Generated code must NEVER be directly executed on the production host.

Execution must use a controlled sandbox.

Required protections:

- CPU limit
- Memory limit
- Execution timeout
- Restricted filesystem
- No network access
- Controlled processes

Docker should be used for the production sandbox.

---

# 16. Security Rule

Security must be considered during implementation, not only before deployment.

Relevant threats include:

- Prompt injection
- Command injection
- Malicious generated code
- Sandbox escape
- File-system access
- Network access
- Secret leakage
- Unsafe dependencies
- Malicious user input

---

# 17. Secrets

Never commit:

```text
API keys
Passwords
Tokens
Private credentials
.env files containing secrets
```

Use:

```text
.env
.env.example
```

`.env` must be ignored by Git.

---

# 18. Database Rules

Use SQLite for the initial local application.

Database operations should:

- Use clear models
- Validate input
- Avoid destructive operations without confirmation
- Handle database errors
- Preserve session integrity

---

# 19. Session Rules

Sessions must support:

- Create
- Rename
- Open
- Continue
- Delete
- Persist

Conversation context must be associated with the correct session.

---

# 20. UI Rules

The UI should be:

- Simple
- Fast
- Student-friendly
- Consistent
- Responsive where practical
- Clear about errors
- Clear about model status

Avoid unnecessary UI complexity.

---

# 21. Error Handling

Never silently fail.

Errors should provide useful information.

Bad:

```text
Something went wrong.
```

Better:

```text
Local model is unavailable.
Please start Ollama and try again.
```

Internal errors should be logged appropriately without exposing sensitive information.

---

# 22. Testing Rules

Every meaningful feature must have tests.

At minimum:

```text
Unit Test
+
Integration Test where applicable
```

Critical features must have end-to-end verification.

---

# 23. Testing Before Completion

A feature is not complete because:

```text
Code exists.
```

It is complete when:

```text
Code exists
+
Expected behavior works
+
Tests pass
+
Relevant edge cases checked
+
No known critical issue
```

---

# 24. Code Quality

Prefer:

- Clear names
- Small functions
- Single responsibility
- Type hints where useful
- Clear error handling
- Minimal duplication
- Maintainable structure

Avoid:

- Giant files
- Giant functions
- Hard-coded secrets
- Magic values without explanation
- Unused dependencies
- Dead code
- Duplicate utilities

---

# 25. Dependency Rules

Before adding a dependency:

Ask:

1. Is it necessary?
2. Is there already an existing solution?
3. Does it work offline?
4. Is it maintained?
5. Does it introduce security or deployment complexity?

Do not add libraries simply because they are popular.

---

# 26. Git Rules

Use meaningful commits.

Examples:

```text
feat: add multilingual language detection
feat: add intent classifier
feat: integrate local ollama model
fix: resolve session context bug
test: add code validator tests
docs: update architecture
refactor: simplify prompt builder
```

Do not commit broken experimental code to the main branch.

---

# 27. Change Reporting

After significant implementation, report:

```text
What changed
Files changed
Why changed
Tests added
Tests passed
Known issues
Next recommended task
```

---

# 28. No Fake Completion

Never claim:

```text
Implemented
Production ready
Secure
Offline
Tested
```

unless there is evidence.

Use accurate status:

```text
Implemented — not yet tested
Implemented — unit tested
Implemented — integration tested
Verified offline
Production candidate
```

---

# 29. Performance

Avoid unnecessary:

- LLM calls
- Database queries
- repeated preprocessing
- repeated model loading
- large context windows

The local machine has limited resources, so performance matters.

---

# 30. Local LLM Resource Awareness

Model selection must consider:

- RAM
- VRAM
- quantization
- context length
- response latency
- code quality

Do not assume a large model is automatically better.

---

# 31. Production Rule

Before production:

```text
Development
↓
Testing
↓
Security Review
↓
Code Review
↓
Preview
↓
QA
↓
Production
```

No skipping critical gates.

---

# 32. Definition of Done

A feature is DONE only when:

- Requirement identified
- Implementation completed
- Existing architecture respected
- Tests added/passed
- Security considered
- Documentation updated if necessary
- Manual verification completed where necessary
- No known critical blocker

---

# 33. Golden Rule

> **Do not make the project bigger than necessary. Make the existing features reliable first.**

And:

> **Never sacrifice correctness, security, or maintainability just to generate code faster.**