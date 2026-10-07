# Bhasha2Code — Design Specification

## Phase 7 — Design

**Project:** Bhasha2Code  
**Phase:** 7 — Design  
**Version:** 1.2  
**Status:** FINAL  
**Primary Platform:** Desktop / Laptop  
**Frontend:** React + Vite  
**Code Editor:** Monaco Editor

---

# 1. Purpose

This document defines the visual and user-experience design of Bhasha2Code.

The design focuses on creating a:

> **Minimalist, clean, professional, white-first coding and study workspace.**

The application should feel suitable for:

- Coding
- Learning
- Academic work
- Office/productivity work
- Long study sessions
- Long coding sessions

---

# 2. Design Vision

Bhasha2Code should combine:

```text
Minimalist UI
      +
Coding Workspace
      +
Study Workspace
      +
Professional Productivity Tool
```

The application should look modern through:

- Clean spacing
- Good typography
- Strong visual hierarchy
- Consistent components
- Simple navigation
- Excellent readability

It should NOT depend on visual effects to look modern.

---

# 3. Core Design Principles

## 3.1 Minimalism

Only necessary information and controls should be visible.

Avoid unnecessary:

- Cards
- Buttons
- Panels
- Icons
- Charts
- Decorations
- Animations

---

## 3.2 Content First

The user's:

- Question
- Answer
- Code
- Explanation
- Study material

must receive the most visual attention.

---

## 3.3 Coding First

Code must be:

- Easy to read
- Easy to copy
- Easy to edit
- Easy to validate
- Easy to understand

---

## 3.4 Study Friendly

The UI should remain comfortable during long reading and revision sessions.

It should not feel like a gaming or entertainment application.

---

## 3.5 Professional

The design should look appropriate for:

- Engineering students
- Developers
- Researchers
- Office users
- Technical teams

---

# 4. Visual Direction

The final visual direction is:

```text
Minimalist
White-first
Professional
Calm
Clean
Study-friendly
Coding-focused
Modern
```

---

# 5. Visual References

The design philosophy should feel closer to:

```text
Professional productivity software
+
Modern code editor
+
Clean documentation tool
+
Study workspace
```

It should NOT imitate:

```text
Gaming dashboard
Crypto dashboard
Neon AI website
Social media application
Marketing landing page
```

---

# 6. Color System

## 6.1 Default Theme

The default theme is **Light**.

Primary colors should remain neutral:

```text
Background
→ White / Soft White

Surface
→ White

Border
→ Very Light Gray

Primary Text
→ Dark Neutral

Secondary Text
→ Gray

Accent
→ One restrained accent color
```

The exact accent color can be finalized during frontend implementation.

---

# 7. Color Usage Rule

Color must communicate meaning, not decoration.

Example:

```text
Success
→ Subtle success color

Error
→ Subtle error color

Warning
→ Subtle warning color

Primary Action
→ Accent color
```

Do not use multiple bright colors simultaneously.

---

# 8. White-First Design

The application should visually remain mostly white/light.

The user should get the feeling:

> "This is a clean workspace where I can focus."

Not:

> "This is a colorful AI dashboard."

---

# 9. Dark Mode

Dark mode may be supported.

Dark mode should maintain the same principles:

- Minimal
- Professional
- Low distraction
- High readability
- Coding-friendly

Light mode remains the default.

---

# 10. Typography

Typography should be:

- Modern
- Simple
- Highly readable
- Professional

Use a clean sans-serif font for UI text.

Use a monospaced font for code.

Keep the number of font sizes limited.

---

# 11. Typography Hierarchy

Recommended hierarchy:

```text
Page Title
    ↓
Section Heading
    ↓
Message
    ↓
Secondary Information
```

Do not create excessive typography levels.

---

# 12. Main Application Layout

The primary desktop layout:

```text
┌──────────────────────────────────────────────────────────────┐
│ Bhasha2Code                                  ● Local Model   │
├────────────┬─────────────────────────────────────────────────┤
│            │                                                 │
│ + New Chat │                                                 │
│            │                                                 │
│ Recent     │                 CHAT AREA                       │
│            │                                                 │
│ Python...  │  User                                           │
│ DBMS...    │  python madhe calculator banav                  │
│ NLP...     │                                                 │
│            │  Assistant                                      │
│            │  Here's a simple calculator...                  │
│ Saved      │                                                 │
│ Notes      │  ┌───────────────────────────────────────────┐  │
│ Study      │  │ Python Code                               │  │
│ Search     │  │                                           │  │
│            │  └───────────────────────────────────────────┘  │
│ Settings   │                                                 │
│            │                                                 │
├────────────┴─────────────────────────────────────────────────┤
│ Ask anything about coding...                           Send  │
└──────────────────────────────────────────────────────────────┘
```

---

# 13. Layout Philosophy

The main layout contains:

```text
Small Sidebar
+
Large Main Workspace
```

The main workspace should receive most of the screen.

---

# 14. No Permanent Right Panel

The right-side context panel is **not required by default**.

This keeps the interface clean.

Context information can appear:

- Inline
- Through a compact indicator
- In a collapsible panel
- In a details view when required

The main chat must remain spacious.

---

# 15. Header

The header should remain minimal.

Example:

```text
Bhasha2Code                              ● Local Model
```

Optional:

```text
Session Name
Settings
```

Do not create a large header.

---

# 16. Sidebar

The sidebar should be simple and narrow.

Structure:

```text
+ New Chat

Recent

Session 1
Session 2
Session 3

────────────

Saved
Notes
Study Mode
Search

────────────

Settings
```

---

# 17. Sidebar Behavior

The sidebar should:

- Remain visually quiet
- Use subtle separators
- Highlight the active session
- Avoid large cards
- Avoid unnecessary icons

On smaller screens it becomes collapsible.

---

# 18. Active Session

The active session should have a subtle highlight.

Example:

```text
▌ Python Calculator
```

The highlight should be clear but not visually aggressive.

---

# 19. Session List

Each session should show:

```text
Session Title
Optional last-updated information
```

Example:

```text
Python Calculator
Today

NLP Assignment
Yesterday

DBMS Project
2 days ago
```

---

# 20. Main Chat

The chat is the primary workspace.

It should have:

- Comfortable reading width
- Good vertical spacing
- Clear message hierarchy
- Easy scrolling

The interface should avoid excessive chat bubbles.

---

# 21. User Message

User messages should be visually distinguishable but subtle.

Example:

```text
You

python madhe calculator banav
```

Avoid oversized colorful bubbles.

---

# 22. Assistant Message

Assistant messages should be highly readable.

Possible structure:

```text
Assistant

Explanation

Code

Validation

Suggestions
```

Only relevant sections should be displayed.

---

# 23. Free-Form Coding Conversation

The main interaction must always be:

```text
Ask anything about coding...
```

The user should NOT be forced to select an operation first.

For example:

```text
"हा code slow का आहे?"

"यात error handling add कर"

"Python मध्ये better approach आहे का?"

"हा code explain कर"

"याला C++ मध्ये convert कर"
```

The NLP system determines the appropriate intent.

---

# 24. Input Composer

The input composer should remain simple.

Example:

```text
┌─────────────────────────────────────────────────────────────┐
│ Ask anything about coding...                           Send │
└─────────────────────────────────────────────────────────────┘
```

It should support:

- Multiline input
- Send
- Enter to send
- Shift + Enter for new line

---

# 25. Input Composer Appearance

The input should have:

- Clean border
- Comfortable padding
- Rounded but restrained corners
- Clear focus state

Avoid oversized floating input components.

---

# 26. Empty Chat

When no conversation exists:

```text
                    Bhasha2Code

              Your local coding workspace

Ask a coding question in English, Hindi,
Marathi, Hinglish or mixed language.

        Ask anything about coding...
```

Optional examples:

```text
"Python madhe calculator banav"

"हा code Marathi madhe explain kar"

"Why is my loop slow?"
```

Keep examples limited.

---

# 27. Code Block

Code blocks are a major component.

Example:

```text
Python

┌──────────────────────────────────────────────┐
│ 1  def calculator():                         │
│ 2      a = float(input())                    │
│ 3      b = float(input())                    │
│ 4      return a + b                          │
│                                              │
├──────────────────────────────────────────────┤
│ Copy   Edit   Validate   Run                 │
└──────────────────────────────────────────────┘
```

---

# 28. Code Block Requirements

Code blocks should support:

- Syntax highlighting
- Line numbers
- Copy
- Edit
- Validate
- Run where supported
- Language identification

---

# 29. Code Editor

Use:

**Monaco Editor**

The editor should support:

- Syntax highlighting
- Line numbers
- Editing
- Error markers
- Language selection
- Search
- Readable spacing

---

# 30. Coding Workspace

When the user is working on a larger coding task, the application may provide a focused coding workspace.

```text
┌──────────┬───────────────────────────┬──────────────┐
│ Sessions │ Code Editor               │ AI           │
│          │                           │              │
│          │ Python code               │ Explanation  │
│          │                           │ Debug        │
│          │                           │ Suggestions  │
└──────────┴───────────────────────────┴──────────────┘
```

This should be used only when it improves productivity.

---

# 31. Multilingual Input

The UI should not require language selection.

Users can naturally write:

```text
python madhe calculator banav

Python mein calculator banao

हा code explain कर

Hinglish mein samjha
```

The NLP pipeline handles language detection.

---

# 32. Context Awareness

The UI should indicate that context is active without exposing unnecessary technical details.

Example:

```text
Using current session context
```

or:

```text
Current code: Python Calculator
```

---

# 33. Context Details

If the user wants more information, a details panel may show:

```text
Current Task
Python Calculator

Language
Python

Current Code
Available

Last Action
Debugging
```

This panel should be optional.

---

# 34. Model Status

The application should show a small local model status.

Example:

```text
● Local Model Ready
```

Possible states:

```text
Ready
Loading
Busy
Unavailable
Error
```

---

# 35. Model Loading

When the local model is loading:

```text
Local model is starting...
```

The UI should remain responsive.

---

# 36. Model Error

If Ollama/model is unavailable:

```text
Local model unavailable.

Please start Ollama and check the configured model.
```

Do not show raw stack traces to normal users.

---

# 37. NLP Metadata

The following should remain internal by default:

```text
Intent
Tone
Language
Programming Language
Entities
Confidence
```

A developer/debug view may expose these later.

---

# 38. Validation Status

Use simple states:

```text
✓ Validated

✕ Validation Failed

○ Not Validated

⚠ Unsupported
```

Validation state must be visually distinguishable.

---

# 39. Debugging UI

A debugging response should follow:

```text
Problem
↓
Cause
↓
Fix
↓
Corrected Code
↓
Validation
```

This makes debugging useful for both development and learning.

---

# 40. Suggestions

Suggestions should be compact.

Example:

```text
Suggestions

• Add input validation
• Handle division by zero
• Convert repeated logic into functions
```

Maximum recommended initial display:

```text
3–5 suggestions
```

Suggestions must be relevant to the current context.

---

# 41. No Suggestion Spam

The system must NOT attach suggestions to every answer.

Suggestions should appear only when they provide genuine value.

---

# 42. Saved Messages

Saved messages should be accessible through:

```text
Saved
```

Example:

```text
Saved

Python Recursion
DBMS Joins
NLP Intent Classification
```

The design should remain list-oriented rather than card-heavy.

---

# 43. Notes

Notes should behave like a lightweight study notebook.

```text
Notes

+ New Note

Python Recursion
NLP Intent Classification
DBMS Joins
```

Each note can contain:

- Title
- Content
- Created date
- Updated date
- Optional linked session

---

# 44. Study Mode

Study Mode should remain minimalist.

Example:

```text
Study Mode

Recursion

────────────────────────

Explanation

Simple explanation...

Example

[Code]

Important Points

• Point 1
• Point 2
• Point 3

Common Mistakes

...

Practice Questions

1. ...
2. ...

[Start Mini Quiz]
```

---

# 45. Study Mode Philosophy

Study Mode should feel like:

```text
Clean Digital Notebook
```

Not:

```text
Colorful Educational Dashboard
```

---

# 46. Study + Coding Integration

A user should be able to move naturally:

```text
Chat
 ↓
Explanation
 ↓
Study Mode
 ↓
Practice
 ↓
Code
 ↓
Debug
```

Both experiences belong to the same application.

---

# 47. Search

Search should be simple.

Placeholder:

```text
Search sessions, messages and notes...
```

Search results should lead directly to the relevant content.

---

# 48. Settings

Settings should remain compact.

Sections:

```text
Appearance
AI Model
Execution
Data
```

Example:

```text
Appearance
Light / Dark / System

AI Model
Local Model

Execution
Sandbox

Data
History / Storage
```

---

# 49. PDF Export

Export should be available through a simple action:

```text
Export PDF
```

Possible options:

```text
Current Response
Current Session
Study Material
Notes
```

---

# 50. Loading States

Use simple status messages.

Examples:

```text
Generating response...

Validating code...

Running secure sandbox...

Creating PDF...
```

Avoid complex loading animations.

---

# 51. Error States

Errors should be human-readable.

Bad:

```text
500 Internal Server Error
```

Better:

```text
The local model could not respond.

Please check Ollama and try again.
```

---

# 52. Confirmation Dialogs

Use confirmation only when necessary.

Example:

```text
Delete this session?

Cancel       Delete
```

Keep dialogs simple.

---

# 53. Buttons

Buttons should be:

- Compact
- Clear
- Consistent
- Professional

Primary action:

```text
Send
Save
Validate
```

Secondary actions:

```text
Copy
Edit
Export
```

Avoid making every action visually prominent.

---

# 54. Cards

Cards should be used sparingly.

Use cards only when grouping improves understanding.

Do NOT create cards for every:

- Feature
- Message
- Setting
- Statistic
- Navigation item

---

# 55. Borders

Use subtle borders.

Borders should define structure without becoming visually heavy.

---

# 56. Shadows

Use minimal shadows.

The application should rely primarily on:

```text
Spacing
Borders
Typography
Alignment
```

rather than large shadows.

---

# 57. Rounded Corners

Use restrained corner rounding.

Avoid making every component look like a large pill.

---

# 58. Icons

Use a consistent icon library.

Icons should support the text labels.

Important actions must remain understandable without relying only on icons.

---

# 59. Animation

Animations must be minimal.

Allowed:

```text
Message streaming
Small loading indicator
Hover state
Panel opening/closing
```

Avoid:

```text
Background animation
Glow effects
Large transitions
Continuous motion
AI sparkle animations
```

---

# 60. AI Visual Effects

Do NOT use:

```text
AI sparkles
Neon gradients
Glowing borders
Animated robots
Large AI illustrations
```

Bhasha2Code should communicate intelligence through functionality.

---

# 61. Professional Office Feel

The application should look appropriate for:

```text
College
Office
Software Development
Research
Technical Work
Study
```

The UI should remain mature and neutral.

---

# 62. Study Feel

The application should also feel comfortable for:

```text
Revision
Assignments
Programming Practice
Exam Preparation
Notes
Concept Learning
```

The interface should remain calm during long sessions.

---

# 63. Coding Feel

Coding areas should receive stronger visual hierarchy than decorative UI.

Priority:

```text
Code
Explanation
Validation
Debugging
Context
```

---

# 64. Responsive Design

Primary target:

```text
Desktop / Laptop
```

For smaller screens:

```text
Sidebar
→ Collapsible

Context
→ Hidden by default

Chat
→ Full Width

Editor
→ Scrollable
```

---

# 65. Accessibility

Minimum requirements:

- Keyboard navigation
- Visible focus states
- Good contrast
- Readable text
- Clear labels
- Text-based error messages
- Color-independent status communication

---

# 66. Keyboard Shortcuts

Recommended:

```text
Enter
→ Send

Shift + Enter
→ New Line

Ctrl/Cmd + K
→ Search

Esc
→ Close Modal / Panel
```

---

# 67. Message Actions

Assistant message:

```text
Copy
Save
Regenerate
Ask Follow-up
Export
```

Code:

```text
Copy
Edit
Validate
Run
```

These actions should remain visually subtle.

---

# 68. Session Management

Each session should support:

```text
Create
Open
Rename
Delete
Continue
Search
```

The session should preserve relevant context.

---

# 69. Session Reopen Experience

When reopening a session:

```text
Previous Conversation
        ↓
Current Code
        ↓
Context Restored
        ↓
User Continues Naturally
```

The user should not have to explain the previous conversation again.

---

# 70. Visual Hierarchy

The application follows:

```text
1. User Question
2. Assistant Answer
3. Code
4. Explanation
5. Validation
6. Relevant Suggestions
7. Secondary Metadata
```

---

# 71. Workspace Priority

Screen space priority:

```text
Main Chat / Code
        ↓
Session Navigation
        ↓
Context
        ↓
Secondary Features
```

The workspace must never be dominated by navigation or decoration.

---

# 72. Feature Visibility

Primary:

```text
Chat
Code
Input
Sessions
```

Secondary:

```text
Saved
Notes
Search
Study Mode
```

Supporting:

```text
Settings
Model Status
Context Details
```

---

# 73. Empty State Design Rule

Empty states should:

- Explain what the user can do
- Provide 2–3 examples
- Provide a clear first action

They should not contain large illustrations or promotional content.

---

# 74. Do Not Overdesign

The following are explicitly prohibited unless a later design review approves them:

```text
Large dashboards
Excessive gradients
Neon UI
Excessive shadows
Too many cards
Too many colors
Large decorative illustrations
Unnecessary charts
Complex animations
Forced AI branding
```

---

# 75. Design Quality Checklist

Before accepting the frontend:

```text
[ ] Is the interface minimalist?
[ ] Is the default appearance white/light?
[ ] Is the UI professional?
[ ] Is the workspace spacious?
[ ] Is coding easy?
[ ] Is reading comfortable?
[ ] Is Study Mode calm?
[ ] Are there unnecessary components?
[ ] Are there unnecessary colors?
[ ] Are there unnecessary animations?
[ ] Can the user understand the interface quickly?
[ ] Does the application look suitable for office use?
[ ] Does it look suitable for college/study use?
```

---

# 76. Critical Preview Flow

The design must support this complete flow:

```text
New Chat
   ↓
Marathi Query
   ↓
Generate Python Code
   ↓
Follow-up Question
   ↓
Add Error Handling
   ↓
Validate
   ↓
Explain in Marathi
   ↓
Optimize
   ↓
Save
   ↓
Close Session
   ↓
Reopen Session
   ↓
Continue
   ↓
Export PDF
```

---

# 77. Final Design Direction

The final design identity is:

> **Bhasha2Code is a minimalist, white-first, professional coding and study workspace that prioritizes usability, readability, context, and productivity over decoration.**

Short version:

```text
MINIMAL
+
WHITE
+
PROFESSIONAL
+
STUDY
+
CODING
+
CLEAN
```

---

# 78. Phase 7 Acceptance Criteria

- [x] Minimalist design direction locked
- [x] White-first theme locked
- [x] Professional office feel defined
- [x] Study-friendly design defined
- [x] Coding-focused design defined
- [x] Main layout defined
- [x] Sidebar defined
- [x] Chat defined
- [x] Input defined
- [x] Code block defined
- [x] Monaco editor defined
- [x] Context behavior defined
- [x] Session behavior defined
- [x] Study Mode defined
- [x] Notes defined
- [x] Saved messages defined
- [x] Search defined
- [x] PDF export defined
- [x] Settings defined
- [x] Loading states defined
- [x] Error states defined
- [x] Responsive behavior defined
- [x] Accessibility basics defined
- [x] Animation limits defined
- [x] Anti-overdesign rules defined
- [x] Critical preview flow defined

---

# 79. Phase Status

**PHASE 7 — DESIGN: COMPLETE**

The visual direction is now locked.

No frontend implementation should introduce a significantly different visual style without updating this document and reviewing the change.

---

# 80. Next Phase

## Phase 8 — RULES.md

Next we define the project constitution for Antigravity:

```text
Coding Rules
Architecture Rules
UI Rules
Security Rules
Database Rules
Git Rules
Testing Rules
LLM Rules
Dependency Rules
Do-Not-Do Rules
```

This document will control how Bhasha2Code is actually built.