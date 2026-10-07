# Bhasha2Code — User Definition

## Phase 3 — User Definition

**Project:** Bhasha2Code  
**Phase:** 3 — User Definition  
**Status:** COMPLETE — READY FOR PRD

---

# 1. Purpose

This document defines the intended users of Bhasha2Code, their problems, workflows, expectations, and interaction patterns.

The purpose is to ensure that product requirements are based on real user needs rather than only technical capabilities.

---

# 2. Primary User

## Engineering Student / Beginner-to-Intermediate Programmer

### Profile

The primary user is a student who:

- Is learning programming
- Works on academic assignments
- Builds mini-projects
- Participates in hackathons
- Uses multiple programming languages
- May not be highly confident in technical English
- May naturally communicate using Marathi, Hindi, Hinglish, or mixed-language text
- Needs both coding assistance and conceptual understanding

### Typical Technical Level

Beginner to intermediate.

Typical activities:

```text
Learn
↓
Write Code
↓
Run Code
↓
Get Error
↓
Ask for Help
↓
Fix Code
↓
Understand Code
↓
Improve Code
```

---

# 3. Secondary Users

## 3.1 Self-Learners

People learning programming independently.

Needs:

- Explanation
- Examples
- Practice
- Debugging
- Learning continuity

---

## 3.2 Hackathon Participants

Students or beginner developers working under time constraints.

Needs:

- Fast code generation
- Debugging
- Architecture suggestions
- Feature ideas
- Code review
- Context continuity

---

## 3.3 Beginner Developers

Developers with limited professional experience.

Needs:

- Code suggestions
- Error explanations
- Performance guidance
- Best practices
- Security suggestions

---

# 4. User Persona 1 — Engineering Student

**Name:** Aarav

**Age Group:** 18–23

**Role:** Engineering Student

**Technical Level:** Beginner / Intermediate

**Languages:** Marathi + Hindi + English

### Goals

- Complete programming assignments
- Understand concepts
- Build projects
- Fix errors quickly
- Improve coding skills
- Prepare for viva/exams
- Work without depending completely on internet services

### Pain Points

- Difficult technical terminology
- Unclear error messages
- Repeating the same context
- Difficulty writing good AI prompts
- Generated code may not work immediately
- Wants explanations in simple language
- Switching between coding tools and learning resources

### Typical Query

```text
python madhe student marks calculate karnara program de
```

---

# 5. User Persona 2 — Hackathon Developer

**Name:** Neha

**Age Group:** 19–25

**Role:** Student Developer / Hackathon Participant

**Technical Level:** Intermediate

**Languages:** English + Hinglish + Hindi

### Goals

- Build features quickly
- Debug project errors
- Improve implementation
- Understand unfamiliar code
- Generate test cases
- Get architecture ideas

### Pain Points

- Limited development time
- Large codebase context
- Integration errors
- Repetitive prompting
- Difficult debugging
- Multiple tools

### Typical Query

```text
हा API चालतोय पण response slow आहे,
कुठे bottleneck असू शकतो?
```

---

# 6. User Persona 3 — Self-Learner

**Name:** Rahul

**Age Group:** 17–30

**Role:** Programming Learner

**Technical Level:** Beginner

**Languages:** Hindi / Hinglish / English

### Goals

- Learn programming
- Understand concepts
- Practice coding
- Ask basic questions without hesitation

### Pain Points

- Fear of asking basic questions
- Complex explanations
- Lack of personalized continuity
- Difficulty connecting theory with code

### Typical Query

```text
loop ani recursion madhla difference simple Hinglish madhe samjav.
```

---

# 7. User Pain Points

The primary pain points are grouped into five categories.

## 7.1 Language Pain

Users may know the programming requirement but prefer to express it in:

- Marathi
- Hindi
- Hinglish
- Mixed-language text

---

## 7.2 Prompt Pain

Users may know:

> What they want

but not:

> How to write the perfect AI prompt.

---

## 7.3 Context Pain

Users may need to repeatedly provide:

- Code
- Programming language
- Previous requirement
- Error
- Previous changes

---

## 7.4 Learning Pain

Users need more than the final code.

They may also need:

- Explanation
- Reasoning
- Examples
- Common mistakes
- Practice questions

---

## 7.5 Reliability Pain

Generated code may:

- Contain syntax errors
- Fail compilation
- Produce wrong output
- Ignore requirements
- Introduce security issues

Therefore validation is important.

---

# 8. User Jobs-to-be-Done

## Job 1 — Generate

> "I want to describe a programming task naturally and get usable code."

---

## Job 2 — Understand

> "I want to understand what my code is doing in simple language."

---

## Job 3 — Fix

> "I want to know why my code is failing and how to fix it."

---

## Job 4 — Improve

> "I want to make my code cleaner, faster, safer, or easier to maintain."

---

## Job 5 — Continue

> "I want to continue the same coding task without explaining everything again."

---

## Job 6 — Learn

> "I want to learn the concept behind the code instead of only copying the answer."

---

## Job 7 — Preserve

> "I want my previous coding conversations and study material to remain available."

---

# 9. User Journey — Normal Coding Task

```text
User Gets Problem
      ↓
Thinks About Solution
      ↓
Asks Bhasha2Code
      ↓
NLP Understands Request
      ↓
Local LLM Generates Code
      ↓
Validation
      ↓
Result
      ↓
User Runs / Reviews Code
      ↓
Follow-up Question
      ↓
Context Maintained
      ↓
Code Improved
```

---

# 10. User Journey — Debugging

```text
User Has Error
      ↓
Pastes Code / Error
      ↓
System Detects Debug Intent
      ↓
Analyzes Code
      ↓
Identifies Likely Cause
      ↓
Suggests Fix
      ↓
Generates Corrected Code
      ↓
Validation
      ↓
User Continues Conversation
```

---

# 11. User Journey — Learning

```text
Choose Topic
      ↓
Ask Question
      ↓
Simple Explanation
      ↓
Example
      ↓
Important Points
      ↓
Common Mistakes
      ↓
Practice Questions
      ↓
Mini Quiz
      ↓
Save Session
      ↓
Reopen Later
```

---

# 12. User Journey — Multilingual Interaction

Example:

```text
Turn 1:
"python madhe calculator banav"

Turn 2:
"yat divide by zero handle kar"

Turn 3:
"ata ha code simple Marathi madhe explain kar"

Turn 4:
"same code C++ madhe convert kar"
```

The system should preserve the coding object and task context across all turns.

---

# 13. User Expectations

Users expect:

### Response

- Fast
- Relevant
- Clear
- Technically useful

### Language

- Natural
- Understandable
- Consistent with user preference

### Code

- Correct
- Readable
- Validated where possible
- Appropriate to requested programming language

### Conversation

- Context-aware
- Does not repeatedly ask for known information

### Learning

- Simple explanations
- Examples
- Practice material

### Privacy

- Local storage
- No unnecessary external transfer

---

# 14. User Interaction Principles

## Principle 1 — Natural Language First

Users should be able to communicate naturally.

They should not need to know internal intent labels such as:

```text
GENERATE_CODE
DEBUG_CODE
EXPLAIN_CODE
```

---

## Principle 2 — Context Before Clarification

The system should first use available session context before asking the user to repeat information.

---

## Principle 3 — Appropriate Response Type

The system should determine what the user needs.

Examples:

```text
"code de"
→ Code generation

"error ka?"
→ Debugging / error explanation

"simple madhe samjav"
→ Explanation

"slow ka?"
→ Performance analysis

"approach correct aahe ka?"
→ Approach suggestion

"security problem aahe ka?"
→ Security analysis
```

---

## Principle 4 — Learning, Not Blind Copying

The system should encourage understanding by providing explanations and learning support when relevant.

---

## Principle 5 — No Unnecessary Complexity

Beginner users should not receive unnecessarily advanced explanations unless requested.

---

# 15. User Intent Categories

The initial intent taxonomy is:

```text
GENERATE_CODE
DEBUG_CODE
EXPLAIN_CODE
OPTIMIZE_CODE
CONVERT_CODE
ALGORITHM
CONCEPT
CODE_REVIEW
CODE_SUGGESTION
PERFORMANCE_ANALYSIS
ERROR_EXPLANATION
APPROACH_SUGGESTION
BEST_PRACTICE
ARCHITECTURE_SUGGESTION
FEATURE_SUGGESTION
TEST_CASE_GENERATION
SECURITY_ANALYSIS
```

The taxonomy may evolve based on testing.

---

# 16. User Language Categories

Initial application categories:

```text
ENGLISH
HINDI
MARATHI
HINGLISH
MARATHI_ENGLISH
HINDI_ENGLISH
```

The system should also identify mixed-language input where appropriate.

---

# 17. User Tone Categories

Initial tone categories:

```text
CASUAL
FORMAL
SIMPLE
TECHNICAL
SHORT
DETAILED
```

Tone should influence response style but must not override technical correctness.

---

# 18. User Context

The system may maintain the following active context:

```text
Session
↓
Conversation History
↓
Current Code
↓
Programming Language
↓
Current Task
↓
User Language
↓
User Tone
↓
Current Intent
```

Not every historical message needs to be included in every LLM request.

Only relevant context should be selected.

---

# 19. User Data

The application may locally store:

- Sessions
- Messages
- Generated code
- Debug history
- Saved messages
- Notes
- Study content
- PDF export information

The system should avoid collecting data that is not required for functionality.

---

# 20. User Constraints

The primary user may have:

- Limited technical knowledge
- Limited computational resources
- Limited internet availability
- Limited time
- Limited understanding of AI prompting
- Limited programming confidence

The product must therefore prioritize:

```text
Simplicity
+
Speed
+
Clarity
+
Context
+
Reliability
```

---

# 21. User Acceptance Expectations

A typical user should be able to:

1. Open the application.
2. Start a new session.
3. Ask a coding question naturally.
4. Receive a useful answer.
5. Ask a follow-up without repeating the previous code.
6. Debug or modify the generated code.
7. Understand the explanation.
8. Save the conversation.
9. Close the application.
10. Reopen the session later.
11. Continue from the previous context.
12. Export the useful session if required.

---

# 22. User Experience Priority

Feature priorities from the user's perspective:

```text
                    HIGH
                      ↑
            Context Awareness
                 Code Help
              Fast Response
            Natural Language
             Error Fixing
                 Learning
             Session History
                      ↓
                    LOW
```

The initial product should prioritize core user value rather than secondary UI features.

---

# 23. User Problems → Product Responses

| User Problem | Bhasha2Code Response |
|---|---|
| Cannot formulate technical prompt | Natural-language input |
| Prefers Marathi/Hindi/Hinglish | Multilingual NLP |
| Repeats previous code | Context manager |
| Gets incorrect generated code | Validation |
| Does not understand code | Explanation |
| Has programming errors | Debugging workflow |
| Wants better code | Optimization/review/suggestions |
| Forgets previous work | Persistent sessions |
| Wants to learn | Study Mode |
| Wants offline use | Local LLM + local storage |

---

# 24. Core User Value Proposition

For engineering students and beginner programmers:

> **Bhasha2Code lets users communicate about programming naturally in the languages they are comfortable with, while preserving coding context and providing generation, debugging, explanation, and learning support locally.**

---

# 25. User Definition Boundaries

Bhasha2Code is primarily optimized for:

- Students
- Beginners
- Intermediate learners
- Academic projects
- Personal learning
- Hackathon development
- Small-to-medium coding tasks

It is not initially optimized for:

- Large enterprise software teams
- Massive production repositories
- High-scale autonomous software engineering
- Safety-critical software development without human review

---

# 26. User Research Questions

These questions should be validated through actual user testing later:

### URQ1

Do students prefer natural multilingual programming requests over formal English prompts?

### URQ2

Which languages and code-mixed forms are most commonly used?

### URQ3

Does context preservation reduce repeated user input?

### URQ4

Which coding assistance tasks are most frequently requested?

### URQ5

Do users value explanations alongside generated code?

### URQ6

Are students willing to use a local/offline coding assistant?

### URQ7

Which Study Mode features provide the most value?

---

# 27. Phase 3 Acceptance Criteria

- [x] Primary user defined
- [x] Secondary users defined
- [x] Personas defined
- [x] Pain points identified
- [x] Jobs-to-be-done defined
- [x] User journeys defined
- [x] User expectations defined
- [x] User intent categories defined
- [x] User language categories defined
- [x] User tone categories defined
- [x] User context defined
- [x] User constraints identified
- [x] User acceptance expectations defined
- [x] User research questions defined

---

# 28. Phase 3 Status

**STATUS: COMPLETE**

The target users, their workflows, pain points, expectations, and core interaction patterns are defined.

---

# 29. Next Phase

## Phase 4 — Product Requirements Document (PRD)

The next phase will convert:

```text
Problem
+
Research
+
User Needs
↓
Functional Requirements
+
Non-Functional Requirements
+
User Stories
+
Feature Priorities
+
Edge Cases
+
Acceptance Criteria
```

into a formal product specification.

The PRD will become the primary functional reference for development.