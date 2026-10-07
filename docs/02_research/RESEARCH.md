# Bhasha2Code — Research

## Phase 2 — Research

**Project:** Bhasha2Code  
**Research Focus:** Multilingual Natural-Language-to-Code Generation, Code-Switched Programming Interaction, Context-Aware Coding Assistance, Debugging, Explanation, and Offline Local LLMs  
**Review Period:** 2023–2026  
**Status:** RESEARCH BASELINE COMPLETE — READY FOR USER DEFINITION

---

# 1. Research Purpose

The purpose of this research is to understand the current state of:

- Natural-language-to-code generation
- Multilingual code generation
- Code-mixed / code-switched programming prompts
- LLM-based debugging and program repair
- Multilingual programming education
- Context-aware coding assistants
- Local / offline LLM deployment
- Existing AI coding assistants

The research is used to determine:

1. What already exists
2. What works well
3. What limitations remain
4. What users still struggle with
5. Where Bhasha2Code can make a meaningful contribution
6. What can realistically be implemented and evaluated

---

# 2. Research Method

The initial research used:

### Academic literature

Recent peer-reviewed or research-preprint literature from 2023–2026 was examined for:

- Code generation
- Multilingual code generation
- Code-mixing
- Code debugging
- Programming education
- Multilingual LLMs

### Existing systems

Current AI coding products were reviewed for:

- Code generation
- Codebase context
- Agentic coding
- Code review
- Debugging
- Session/context handling
- Repository understanding

### Evidence rule

A research gap must not be claimed merely because a feature is absent from one product or paper.

Bhasha2Code's final novelty claim must be based on:

```text
Academic Evidence
+
Existing-System Comparison
+
Observed Limitation
+
Proposed Improvement
+
Experimental Validation
```

---

# 3. Research Area 1 — LLM Code Generation

Large Language Models have become major tools for source-code generation and other code-related software-engineering tasks.

A 2024 survey of Code LLM research organizes developments across data curation, model advances, evaluation, applications, ethical issues, and environmental considerations. It also highlights the difference between benchmark capability and practical software-engineering use. [1]

### Key observation

Code generation is already a mature research area.

Therefore:

> **"Using an LLM to generate code" alone is NOT sufficient research novelty for Bhasha2Code.**

The project must add a more specific contribution.

---

# 4. Research Area 2 — Multilingual Code Generation

## 4.1 HumanEval-XL

HumanEval-XL was introduced to evaluate natural-language generalization for multilingual code generation.

It connects:

- 23 natural languages
- 12 programming languages
- 22,080 prompts
- approximately 8.33 test cases per prompt

The study specifically addresses limitations of earlier benchmarks that were focused on English prompts or a restricted set of languages. [2]

### Research implication

Multilingual NL-to-code is already an established research direction.

Therefore:

> Bhasha2Code should NOT claim that multilingual code generation itself is a new concept.

The contribution should instead focus on the **interaction and system workflow around multilingual programming requests**.

---

# 5. Research Area 3 — Low-Resource and Multilingual Prompting

mHumanEval extends multilingual code-generation evaluation to more than 200 natural languages, with expert translations for 15 languages.

The paper points out that conventional code-generation benchmarks often emphasize English-to-Python scenarios and therefore do not adequately represent low-resource-language prompting. [3]

### Key limitation identified

Benchmark performance can hide the difficulty of multilingual prompting.

This supports the importance of testing coding assistance across multiple user languages rather than assuming that English performance generalizes automatically.

---

# 6. Research Area 4 — Multilingual Bias

A 2024 study on multilingual bias in large code models reports that code-generation performance can differ substantially depending on the natural language of the instruction and the target programming language.

The paper reports that non-English prompts can reduce Pass@1 performance and that model behavior also varies across programming languages. The authors explore translation and multilingual instruction tuning as ways to reduce this bias. [4]

### Implication for Bhasha2Code

The following assumption is unsafe:

```text
English Prompt Performance
        =
Marathi/Hindi/Hinglish Prompt Performance
```

Instead:

```text
Language
↓
Prompt Interpretation
↓
Code Generation Quality
```

must be treated as an experimental variable.

---

# 7. Research Area 5 — Code-Mixed Prompts

## 7.1 CodeMixBench

CodeMixBench evaluates code generation under code-mixed prompts.

It specifically includes:

- Hinglish
- Spanish-English
- Chinese Pinyin-English

The study evaluates open-source code-generation models and reports that code-mixed prompts can degrade Pass@1 performance compared with English-only prompts. It also reports that degradation can become stronger with increased code-mixing, especially for smaller models. [5]

### Major relevance to Bhasha2Code

This is directly relevant to:

```text
"Hinglish madhe code de"

"python madhe calculator banav"

"हा code fix कर"

"yat error handling add kar"
```

These are not purely English or purely Marathi/Hindi interactions.

They are code-switched programming conversations.

---

# 8. Research Area 6 — Broader Code-Mixing

A broader 2025 CodeMixBench study covering 18 languages reports that LLMs consistently underperform on code-mixed datasets across different language families. The study also identifies model scale, training data, and few-shot learning as factors that can influence performance. [6]

A 2026 practitioner-oriented review further describes code-mixing as a continuing challenge for LLMs and highlights weaknesses in current evaluation coverage, reproducibility, and linguistic diversity. [7]

### Research implication

Code-mixed input should be treated as a first-class NLP problem rather than as a minor UI feature.

This supports the Bhasha2Code pipeline:

```text
Raw Input
↓
Language Detection
↓
Code-Switch Understanding
↓
Intent Detection
↓
Requirement Extraction
↓
LLM
```

---

# 9. Research Area 7 — Hindi-English NLP Resources

COMI-LINGUA introduces a large manually annotated Hindi-English code-mixed dataset with more than 125K instances across multiple NLP tasks, covering both Devanagari and Roman-script text.

The dataset demonstrates that code-mixed Hindi-English processing can be evaluated as a structured NLP problem rather than being treated only as informal text. [8]

### Relevance

Bhasha2Code initially targets:

- Hindi
- Hinglish
- Hindi-English mixed input

Therefore, existing code-mixed NLP resources can inform:

- language identification
- preprocessing
- token-level language detection
- code-switch handling
- future dataset construction

---

# 10. Research Area 8 — Native-Language Programming Education

Research in computing education has examined whether non-native-English students can use generative AI with prompts written in their native languages.

A 2024 study reports that students were able to successfully use native-language prompts for programming tasks, while still experiencing difficulty specifying some programming terminology and concepts. [9]

### Important observation

The problem is not simply:

> "Students cannot code in English."

A more realistic problem is:

> Students may understand the programming task but have difficulty expressing the complete technical requirement in a second language.

This supports a system that interprets natural-language programming requests instead of forcing formal prompt construction.

---

# 11. Research Area 9 — Multilingual Prompt Quality

A 2026 study evaluates code generation from English, Chinese, Hindi, Spanish, and Italian prompts across Python and Java tasks.

The researchers evaluate:

- Functional correctness
- Structural code quality
- Static-analysis issues
- Identifier/comment language

The study reports that English does not consistently produce the best functional correctness or code quality and that the effect varies by programming language and LLM. [10]

### Major implication

Prompt language itself can affect code-generation behavior.

Therefore, Bhasha2Code can experimentally compare:

```text
Direct Prompt
vs.
NLP-Processed Prompt
```

for equivalent programming tasks.

This can become a concrete research experiment rather than just a product feature.

---

# 12. Research Area 10 — Code Debugging

LLM-based program repair and debugging are already active research areas.

A 2024 systematic literature review examined 189 papers on LLM-based automated program repair between 2020 and 2025 and identified multiple strategies for using LLMs in software repair, while also outlining remaining research challenges. [11]

### Implication

Debugging through an LLM is not new.

Therefore:

> Bhasha2Code should not claim "LLM-based debugging" as its sole innovation.

The stronger direction is:

```text
Multilingual Request
+
Context
+
Code
+
Error Information
+
Execution Feedback
↓
Local Debugging Workflow
```

---

# 13. Research Area 11 — Self-Debugging

Research on self-debugging shows that LLMs can improve generated programs by using execution results and explanation-based feedback.

The Self-Debugging study reports improvements on several code-generation benchmarks and demonstrates the value of iterative feedback instead of relying only on one-shot generation. [12]

### Implication

Bhasha2Code should not use:

```text
Generate Once
↓
Return Code
```

as the complete architecture.

A better workflow is:

```text
Generate
↓
Validate
↓
Detect Error
↓
Generate Feedback
↓
Repair
↓
Validate Again
```

---

# 14. Research Area 12 — Program Analysis + LLM

Other repair research shows that raw LLM output can be improved by combining generation with program-specific analysis.

For example, hybrid program-repair approaches constrain or refine LLM-generated patches instead of trusting the raw model output directly.

### Research implication

This supports the Bhasha2Code design principle:

> **LLM output should be verified by deterministic software tools whenever possible.**

Therefore:

```text
LLM
↓
Code Parser
↓
Static Validation
↓
Compiler / Interpreter
↓
Execution Result
↓
Repair Loop
```

is preferred over blindly displaying generated code as correct.

---

# 15. Existing-System Analysis

## 15.1 GitHub Copilot

GitHub Copilot currently provides:

- Chat
- Code completion
- Agent mode
- Repository/code context
- Code editing
- Code review
- Workspace indexing
- Custom instructions
- Agent capabilities

GitHub documentation describes agent mode as capable of analyzing files, editing code, running commands, and iterating toward task completion. Copilot also supports code review with repository context. [13][14]

### Strengths

- Mature developer workflow
- Strong repository context
- Agentic development
- Code review
- Broad ecosystem integration

### Relevant limitation for Bhasha2Code

Its primary product proposition is general-purpose AI-assisted software development rather than:

```text
Indian multilingual conversation
+
Code-switched student interaction
+
Offline-first local LLM
+
Study workspace
```

---

# 16. Existing-System Analysis — Cursor

Cursor's Agent mode can:

- Search the codebase
- Edit multiple files
- Run terminal commands
- Fix errors
- Write tests
- Maintain coding context

Cursor also supports conversation search, codebase understanding, and different interaction modes such as Agent, Ask, Plan, and Debug. [15][16]

### Strengths

- Strong codebase context
- Multi-file editing
- Agentic workflow
- Debugging workflow
- Planning and review

### Relevance

Cursor demonstrates that context-aware coding agents are technically practical.

Therefore:

> Bhasha2Code's context-aware conversation is not itself novel.

The differentiation must come from **multilingual/code-switched interaction + NLP routing + offline local deployment + learning workflow**.

---

# 17. Existing-System Analysis — Windsurf / Devin Desktop

Windsurf's current product direction combines IDE capabilities with coding agents, local/cloud agent workflows, contextual awareness, and an agent command center.

Its current product positioning also emphasizes codebase understanding and agents that work across software-development tasks. [17][18]

### Strengths

- Deep context
- Agent-based coding
- Local/cloud workflow
- Debugging and project-level development

### Relevance

Again, the existence of strong coding agents means Bhasha2Code should not attempt to compete simply by copying agentic coding features.

---

# 18. Local LLM Ecosystem

Ollama provides a practical mechanism for running open models locally and exposing them to applications through local interfaces.

Ollama also provides local coding models and integrations for coding workflows. [19][20]

### Relevance

This makes the following architecture practical:

```text
Bhasha2Code
     ↓
Local API
     ↓
Ollama
     ↓
Local Coding Model
```

However, model choice must be experimentally validated based on:

- Available RAM
- VRAM
- Model size
- Quantization
- Context length
- Latency
- Coding quality

No model should be declared "best" before testing.

---

# 19. Existing-System Comparison

| Capability | GitHub Copilot | Cursor | Windsurf / Devin | Research Systems | Bhasha2Code |
|---|---|---|---|---|---|
| Code generation | Yes | Yes | Yes | Yes | Yes |
| Debugging | Yes | Yes | Yes | Yes | Yes |
| Code explanation | Yes | Yes | Yes | Yes | Yes |
| Code review | Yes | Yes | Yes | Some | Yes |
| Agentic workflow | Yes | Yes | Yes | Research-specific | Controlled local workflow |
| Codebase context | Yes | Yes | Yes | Varies | Planned |
| Multilingual prompting | General-purpose | General-purpose | General-purpose | Strong research focus | Core focus |
| Hinglish/code-mixed focus | Not primary focus | Not primary focus | Not primary focus | Research focus | Core focus |
| Indian-language NLP pipeline | Not primary focus | Not primary focus | Not primary focus | Limited / task-specific | Core focus |
| Offline local LLM | Not the central product model | Local/cloud options vary | Local/cloud options | Varies | Core requirement |
| Persistent study sessions | Not primary focus | Not primary focus | Not primary focus | Rare | Core feature |
| Study Mode | Not primary focus | Not primary focus | Not primary focus | Rare | Core feature |
| Personal notes | Limited / ecosystem dependent | Limited / ecosystem dependent | Project-oriented | Not central | Core feature |
| Local PDF learning export | Not central | Not central | Not central | Not central | Planned |
| NLP intent classifier before LLM | Not central | Not central | Not central | Varies | Core research component |

**Interpretation:** Bhasha2Code should not try to outperform mature coding agents in general-purpose software engineering. Its differentiation should be narrower and research-driven.

---

# 20. Major Findings from Literature

The research produces the following findings.

## Finding 1 — Multilingual Code Generation Is Already Established

HumanEval-XL, mHumanEval, MultiPL-E, and McEval demonstrate that multilingual code generation has become a recognized research area. [2][3][21][22]

Therefore:

```text
"Multilingual code generation"
```

alone is insufficient novelty.

---

## Finding 2 — Code-Mixed Programming Input Remains Difficult

CodeMixBench and related research show performance degradation under code-mixed prompts.

Hinglish is explicitly included in recent research. [5][6]

Therefore:

```text
Marathi-English
Hindi-English
Hinglish
```

should be treated as a real research condition.

---

## Finding 3 — Prompt Language Can Affect Code Quality

Recent research indicates that equivalent programming tasks can produce different results depending on natural-language prompt language. [4][10]

Therefore, the project can perform controlled experiments across languages.

---

## Finding 4 — Students Can Use Native-Language Programming Prompts

Research in computing education indicates that native-language prompting can help non-native-English learners perform programming tasks, while language/technical terminology remains a challenge. [9]

Therefore, a natural-language interface can have educational value.

---

## Finding 5 — One-Shot Code Generation Is Not Enough

Self-debugging and program-repair research demonstrates the value of feedback, execution results, iterative repair, and program analysis. [11][12]

Therefore, code validation should be part of the system rather than an optional final check.

---

## Finding 6 — Context-Aware Coding Agents Already Exist

GitHub Copilot, Cursor, and Windsurf demonstrate strong repository-aware and agentic coding workflows. [13][15][17]

Therefore:

> Context awareness itself is not a sufficient novelty claim.

The context layer in Bhasha2Code must be specialized for multilingual coding conversations and learning continuity.

---

## Finding 7 — Local LLM Deployment Is Practically Feasible

Ollama demonstrates a mature local model-serving ecosystem, including local coding models and local application interfaces. [19][20]

Therefore, offline-first deployment is technically realistic, subject to hardware constraints.

---

# 21. Research Gap

## 21.1 What Is Already Well Studied?

The following are already well-established:

```text
LLM Code Generation
Multilingual Code Generation
Code Translation
LLM-based Debugging
Code Review
Agentic Coding
Codebase Context
```

Therefore, Bhasha2Code cannot claim these features individually as novel.

---

# 22. Identified Gap — System-Level Integration

Based on the reviewed literature and current products, a more specific gap is identified:

> **Research has extensively studied multilingual code generation, code-mixed prompts, LLM-based debugging, and context-aware coding agents as separate areas. However, there is an opportunity to investigate a unified offline student-oriented coding assistant that explicitly combines Indian multilingual/code-switched NLP routing, context-aware coding dialogue, code validation/repair, persistent learning sessions, and local LLM execution in one workflow.**

This is a **system-level research gap**, not a claim that every individual component is novel.

---

# 23. Gap Breakdown

## Gap 1 — Indian Code-Switched Programming Interaction

Existing research demonstrates difficulty with code-mixed prompting, particularly Hinglish, but the space remains relatively limited compared with English-centric code-generation research. [5][6][7]

### Proposed direction

Support:

```text
Hindi
Marathi
Hinglish
Hindi-English
Marathi-English
English
```

within one coding conversation.

---

## Gap 2 — NLP Before Code LLM

Many coding systems focus directly on LLM interaction.

Bhasha2Code proposes an explicit preprocessing/routing layer:

```text
User Input
↓
Language
↓
Tone
↓
Intent
↓
Programming Language
↓
Requirement
↓
Context
↓
LLM
```

The research question is not whether these classifiers are novel individually.

The question is:

> **Does structured NLP preprocessing improve task interpretation or coding outcomes for multilingual/code-switched programming requests?**

---

## Gap 3 — Multilingual Contextual Follow-Up

Existing coding agents support codebase/repository context, but Bhasha2Code focuses on conversational context across multilingual follow-ups.

Example:

```text
User:
Python madhe calculator banav.

User:
yat error handling add kar.

User:
ata simple Marathi madhe explain kar.

User:
C++ madhe convert kar.
```

The system must maintain the relevant object and task across turns.

This gives a measurable research variable:

```text
Context Preservation Success Rate
```

---

## Gap 4 — Coding + Learning in One Offline Workspace

Research on coding generation, debugging, and education exists separately.

Bhasha2Code combines:

```text
Coding Assistance
+
Study Mode
+
Sessions
+
Notes
+
Saved Messages
+
PDF Export
```

The purpose is not to claim a new educational algorithm.

The intended contribution is a practical **offline coding-learning workflow**.

---

## Gap 5 — Deterministic Validation Around Local LLMs

Research supports combining program analysis/execution feedback with LLM-based repair. [11][12]

Bhasha2Code therefore proposes:

```text
Local LLM
↓
AST / Parser
↓
Validation
↓
Sandbox Execution
↓
Error Feedback
↓
Repair
```

This reduces dependence on unverified LLM output.

---

# 24. Proposed Research Contribution

The research contribution should be framed as:

> **Design and experimental evaluation of an offline multilingual coding assistant that uses an NLP-based routing layer and conversation context to improve interaction with a local code LLM for code generation, debugging, explanation, and learning support.**

---

# 25. Proposed Research Hypotheses

## H1 — NLP Routing

Structured NLP preprocessing will improve identification of:

- User language
- Intent
- Programming language
- Coding requirement

compared with direct LLM interpretation alone.

---

## H2 — Code-Mixed Robustness

A context-aware preprocessing layer can reduce the negative effect of code-mixed input on coding-task interpretation.

---

## H3 — Context Preservation

Maintaining conversation-level coding context will reduce the need for users to repeat previously supplied information.

---

## H4 — Validation Loop

Adding deterministic validation and iterative repair will improve the functional reliability of generated code compared with one-shot generation.

---

## H5 — Offline Practicality

A local LLM can provide useful coding assistance with acceptable latency on consumer hardware when model size and quantization are selected appropriately.

---

# 26. Proposed Experimental Design

## Experiment 1 — Language Comparison

Use the same coding task in:

```text
English
Hindi
Marathi
Hinglish
Hindi-English
Marathi-English
```

Measure:

- Intent accuracy
- Requirement extraction accuracy
- Code generation correctness
- Compilation success
- Execution success
- Latency

---

# 27. Experiment 2 — Direct Prompt vs NLP Pipeline

### Baseline

```text
User Prompt
↓
Local LLM
↓
Output
```

### Proposed

```text
User Prompt
↓
NLP Pipeline
↓
Structured Context
↓
Local LLM
↓
Output
```

Compare:

- Task interpretation
- Code correctness
- Language consistency
- Response time
- Debug success

---

# 28. Experiment 3 — Context vs No Context

### Test A

Each prompt is treated independently.

### Test B

Conversation context is preserved.

Example:

```text
Turn 1:
Create calculator.

Turn 2:
Add error handling.

Turn 3:
Explain it in Marathi.

Turn 4:
Convert it to C++.
```

Measure whether the system correctly maintains the active code/task.

---

# 29. Experiment 4 — Validation Loop

### Baseline

```text
Generate → Return
```

### Proposed

```text
Generate
↓
Validate
↓
Run
↓
Collect Error
↓
Repair
↓
Validate Again
```

Measure:

- Compilation success
- Execution success
- Repair success
- Number of repair iterations
- Latency

---

# 30. Experiment 5 — Local Model Comparison

Candidate local coding models may be compared.

Evaluation dimensions:

- Code correctness
- Instruction following
- Multilingual response quality
- Context handling
- Debugging
- Latency
- Memory usage
- GPU/CPU usage

No model should be selected solely from online popularity.

---

# 31. Evaluation Metrics

## NLP Metrics

- Accuracy
- Precision
- Recall
- F1-score

For multi-class classification:

```text
Intent
Tone
Programming Language
```

---

## Code Metrics

- Compilation success rate
- Execution success rate
- Functional correctness
- Test pass rate
- Repair success rate

---

## Conversation Metrics

- Context preservation rate
- Follow-up correctness
- Information repetition rate

---

## Performance Metrics

- Time to first token
- Total response time
- CPU usage
- RAM usage
- VRAM usage
- Model load time

---

## Educational Metrics

Potential qualitative measures:

- Explanation usefulness
- Concept clarity
- Student understanding
- Practice-question usefulness

These should be evaluated using a defined rubric rather than arbitrary scoring.

---

# 32. Research Dataset Strategy

The project may initially construct a small controlled evaluation dataset containing:

### Languages

```text
English
Hindi
Marathi
Hinglish
Hindi-English
Marathi-English
```

### Task Types

```text
Code Generation
Debugging
Explanation
Optimization
Conversion
Algorithm
Concept
Code Review
Security
Performance
```

### Example

```text
English:
Create a Python program to check whether a number is prime.

Hindi:
एक Python प्रोग्राम बनाओ जो जाँच करे कि संख्या prime है या नहीं।

Marathi:
Python मध्ये संख्या prime आहे की नाही ते तपासणारा program बनव.

Hinglish:
Python mein prime number check karne ka code de.
```

Equivalent tasks should preserve the intended technical meaning as much as possible.

---

# 33. Research Risks

## R1 — Dataset Bias

A small self-created dataset may not represent real-world multilingual programming conversations.

### Mitigation

Use:

- public benchmarks where appropriate
- controlled templates
- human-reviewed examples
- diverse prompt styles

---

## R2 — Translation Bias

Translated prompts may not represent natural speech.

### Mitigation

Include naturally written prompts, not only direct translations.

---

## R3 — Model Bias

Different local models may behave very differently.

### Mitigation

Evaluate multiple candidate models.

---

## R4 — Hardware Constraints

Large models may be impractical locally.

### Mitigation

Benchmark model sizes and quantization.

---

## R5 — Evaluation Subjectivity

Explanation quality and suggestion usefulness are partly subjective.

### Mitigation

Define explicit evaluation rubrics.

---

# 34. Research Limitations

The current research has the following limitations:

1. It is not yet a systematic review of every paper in the field.
2. Some 2026 studies are recent preprints and may not yet have extensive citation history.
3. Existing-product comparisons are based on publicly documented features.
4. The final research gap must be refined after prototype experiments.
5. Actual performance numbers for Bhasha2Code do not yet exist.

Therefore:

> **No Bhasha2Code performance claim should be made until experiments are executed.**

---

# 35. Research-to-Product Mapping

| Research Finding | Product Decision |
|---|---|
| Multilingual bias exists | Add multilingual evaluation |
| Code-mixing is difficult | Add code-switch-aware NLP |
| Prompt language affects output | Compare languages experimentally |
| Native-language programming can help learners | Add natural-language coding interface |
| Self-debugging can improve code | Add validation/repair loop |
| Context-aware agents are powerful | Add persistent coding context |
| Local LLMs are practical | Use Ollama/local inference |
| Existing coding agents are mature | Avoid copying generic agent features |
| Education workflow is fragmented | Add Study Mode + sessions |
| LLM output can be incorrect | Add deterministic validation |

---

# 36. Bhasha2Code Research Positioning

Bhasha2Code should be positioned as:

> **An offline multilingual and code-switched coding assistant with explicit NLP-based request understanding, persistent conversation context, local LLM coding assistance, validation-driven debugging, and integrated study support.**

---

# 37. What Bhasha2Code Is NOT Claiming

The project does NOT claim that:

- Multilingual code generation is new
- LLM debugging is new
- Context-aware coding assistants are new
- Local LLMs are new
- Code review is new
- NLP classification is new

Instead, the research contribution is the **integration and experimental evaluation of these components for an offline, multilingual, student-oriented coding workflow**.

---

# 38. Final Research Gap Statement

## Primary Gap

> **Current literature provides strong advances in multilingual code-generation benchmarks, code-mixed language evaluation, LLM-based program repair, and multilingual programming assistance, while commercial coding agents provide sophisticated codebase context and agentic workflows. However, there remains a practical system-level opportunity to study an offline, student-oriented coding environment that integrates Indian multilingual/code-switched NLP understanding, contextual multi-turn coding assistance, deterministic code validation and repair, and persistent study support using a local LLM.**

---

# 39. Proposed Bhasha2Code Research Model

```text
                   USER
                     ↓
        Multilingual / Code-Mixed Input
                     ↓
              NLP Processing
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
   Language       Intent         Tone
   Detection    Detection      Detection
       └─────────────┼─────────────┘
                     ↓
      Programming Language Detection
                     ↓
         Requirement Extraction
                     ↓
              Context Manager
                     ↓
              Prompt Builder
                     ↓
               Local LLM
                     ↓
        ┌────────────┼────────────┐
        ↓            ↓            ↓
      Generate     Explain      Debug
        ↓            ↓            ↓
        └────────────┼────────────┘
                     ↓
              Code Validation
                     ↓
          ┌──────────┴──────────┐
          ↓                     ↓
        PASS                   FAIL
          ↓                     ↓
      Response               Repair Loop
                                ↓
                             Validate
                     ↓
                 Final Response
                     ↓
            Session / Study Store
```

---

# 40. Research Questions Finalized

### RQ1
How does the natural language used in a programming request affect code-generation quality?

### RQ2
How robust are local coding LLMs to Hindi, Marathi, Hinglish, and code-switched prompts?

### RQ3
Does explicit NLP-based request understanding improve task interpretation compared with direct prompting?

### RQ4
Does conversation context improve follow-up coding-task completion?

### RQ5
Does validation-driven iterative repair improve code reliability?

### RQ6
Can local coding LLMs provide practical multilingual coding assistance on consumer hardware?

### RQ7
Can coding assistance and study support be effectively combined in an offline workflow?

---

# 41. Phase 2 Acceptance Criteria

- [x] Existing research identified
- [x] Recent literature reviewed
- [x] Multilingual code-generation research reviewed
- [x] Code-mixing research reviewed
- [x] Debugging/program-repair research reviewed
- [x] Programming education research reviewed
- [x] Current coding assistants reviewed
- [x] Local LLM ecosystem reviewed
- [x] Existing limitations identified
- [x] Research gap identified
- [x] Research gap constrained to a system-level claim
- [x] Research questions defined
- [x] Research hypotheses defined
- [x] Experimental direction defined
- [x] Evaluation metrics defined
- [x] Risks and limitations documented

---

# 42. Phase 2 Status

**STATUS: COMPLETE**

**Decision:**

Proceed to:

## Phase 3 — User Definition

The next phase will identify:

- Primary users
- Secondary users
- Personas
- User pain points
- User journeys
- Jobs-to-be-done
- Typical coding conversations
- User expectations
- User constraints

---

# 43. References

## [1] A Survey on Large Language Models for Code Generation

Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, Sunghun Kim.  
2024. *ACM Transactions on Software Engineering and Methodology*.  
Citation count in retrieved academic index: **1185**.

[Paper record](https://consensus.app/papers/a-survey-on-large-language-models-for-code-generation-jiang-wang/69d8c6bcb7ca5b008e012d0c33ffc614/?utm_source=chatgpt.com)

---

## [2] HumanEval-XL: A Multilingual Code Generation Benchmark for Cross-lingual Natural Language Generalization

Qiwei Peng, Yekun Chai, Xuhong Li.  
2024. Pages 8383–8394.  
Citation count in retrieved academic index: **124**.

[Paper record](https://consensus.app/papers/humanevalxl-a-multilingual-code-generation-benchmark-for-peng-chai/d9fcd0f77f1d5c1682a4821e454c5b74/?utm_source=chatgpt.com)

---

## [3] mHumanEval — A Multilingual Benchmark to Evaluate Large Language Models for Code Generation

Nishat Raihan, Antonios Anastasopoulos, Marcos Zampieri.  
2024. *arXiv:2410.15037*.  
Citation count in retrieved academic index: **55**.

[Paper record](https://consensus.app/papers/mhumaneval-a-multilingual-benchmark-to-evaluate-large-raihan-anastasopoulos/9bdec6a333c75cfbbc8d2bbfe7a95b40/?utm_source=chatgpt.com)

---

## [4] Exploring Multi-Lingual Bias of Large Code Models in Code Generation

Chaozheng Wang, Zong-Jie Li, Cuiyun Gao, Wenxuan Wang, Ting Peng, Hailiang Huang, Yuetang Deng, Shuai Wang, M. Lyu.  
2024. *ACM Transactions on Software Engineering and Methodology*.  
Citation count in retrieved academic index: **32**.

[Paper record](https://consensus.app/papers/details/c2d1caf41e8657689cf10de6c5afc97b/?utm_source=chatgpt.com)

---

## [5] CodeMixBench: Evaluating Large Language Models on Code Generation with Code-Mixed Prompts

Manik Sheokand, Parth Sawant.  
2025. *arXiv:2505.05063*.  
Citation count in retrieved academic index: **6**.

[Paper record](https://consensus.app/papers/codemixbench-evaluating-large-language-models-on-code-sheokand-sawant/534ccaa59b4e59bc9aeeefd786e58f8c/?utm_source=chatgpt.com)

---

## [6] CodeMixBench: Evaluating Code-Mixing Capabilities of LLMs Across 18 Languages

Yilun Yang, Yekun Chai.  
2025. Pages 2139–2169.  
Citation count in retrieved academic index: **14**.

[Paper record](https://consensus.app/papers/details/c05f9cd4f4de5f87a10a063724759213/?utm_source=chatgpt.com)

---

## [7] Code Mixologist: A Practitioner's Guide to Building Code-Mixed LLMs

Himanshu Gupta, Pratik Jayarao, Chaitanya Dwivedi, Neeraj Varshney.  
2026. *arXiv:2602.11181*.  
Citation count in retrieved academic index: **0**.

[Paper record](https://consensus.app/papers/code-mixologist-a-practitioners-guide-to-building-gupta-jayarao/ca940d10fab855ff909c2e560499d5ba/?utm_source=chatgpt.com)

---

## [8] COMI-LINGUA: Expert Annotated Large-Scale Dataset for Multitask NLP in Hindi-English Code-Mixing

Rajvee Sheth, Himanshu Beniwal, Mayank Singh.  
2025. *arXiv:2503.21670*.  
Citation count in retrieved academic index: **16**.

[Paper record](https://consensus.app/papers/comilingua-expert-annotated-largescale-dataset-for-sheth-beniwal/4cd0772a61225c7198a405bf67cf13eb/?utm_source=chatgpt.com)

---

## [9] Breaking the Programming Language Barrier: Multilingual Prompting to Empower Non-Native English Learners

J. Prather, Brent N. Reeves, Paul Denny, Juho Leinonen, Stephen Macneil, Andrew Luxton-Reilly, João Orvalho, Amin Alipour, Ali Alfageeh, Thezyrie Amarouche, Bailey Kimmel, Jared Wright, Musa Blake, Gweneth Barbre.  
2024. *Proceedings of the 27th Australasian Computing Education Conference*.  
Citation count in retrieved academic index: **22**.

[Paper record](https://consensus.app/papers/breaking-the-programming-language-barrier-multilingual-prather-reeves/75800c72394d59369a78612447fa9869/?utm_source=chatgpt.com)

---

## [10] Large Language Models for Code Generation from Multilingual Prompts: A Curated Benchmark and a Study on Code Quality

Saima Afrin, Alessandro Midolo, C. Escobar-Velasquez, Mario Linares-Vásquez, Weiyuan Ding, Bowen Xu, M. D. Di Penta, A. Mastropaolo.  
2026. *arXiv:2607.14816*.  
Citation count in retrieved academic index: **0**.

[Paper record](https://consensus.app/papers/large-language-models-for-code-generation-from-afrin-midolo/7643ca84283b5a39b56dd7173c823551/?utm_source=chatgpt.com)

---

## [11] A Systematic Literature Review on Large Language Models for Automated Program Repair

Quanjun Zhang, Chun-Rong Fang, Yang Xie, Yuxiang Ma, Weisong Sun, Yun Yang, Zhen-Yu Chen.  
2024. *ACM Transactions on Software Engineering and Methodology*.  
Citation count in retrieved academic index: **97**.

[Paper record](https://consensus.app/papers/a-systematic-literature-review-on-large-language-models-zhang-fang/4fb0e9df89425816a5c06b516148119f/?utm_source=chatgpt.com)

---

## [12] Teaching Large Language Models to Self-Debug

Xin-Yun Chen, Maxwell Lin, Nathanael Schärli, Denny Zhou.  
2023. *arXiv:2304.05128*.  
Citation count in retrieved academic index: **1379**.

[Paper record](https://consensus.app/papers/teaching-large-language-models-to-selfdebug-chen-lin/7cfefb6d86e553ae8a92e0881d16891a/?utm_source=chatgpt.com)

---

## [13] GitHub Copilot — About / Product Capabilities

GitHub Documentation and Product Documentation, accessed October 2026.

[GitHub Copilot documentation](https://docs.github.com/en/copilot/get-started/about-github-copilot?utm_source=chatgpt.com)

---

## [14] GitHub Copilot — Code Review

GitHub Documentation, accessed October 2026.

[GitHub Copilot Code Review](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review?utm_source=chatgpt.com)

---

## [15] Cursor Agent

Cursor Documentation, accessed October 2026.

[Cursor Agent documentation](https://prod.cursor.com/help/ai-features/agent?utm_source=chatgpt.com)

---

## [16] Cursor Modes and Agent Workflow

Cursor Documentation, accessed October 2026.

[Cursor modes documentation](https://docs.cursor.com/agent?utm_source=chatgpt.com)

---

## [17] Windsurf / Devin Desktop

Windsurf / Devin Desktop product documentation, accessed October 2026.

[Product page](https://windsurf.com/editor?utm_source=chatgpt.com)

---

## [18] Windsurf — Agentic IDE / Context

Windsurf product documentation, accessed October 2026.

[Windsurf documentation](https://windsurf.com/switch/cursor?utm_source=chatgpt.com)

---

## [19] Ollama — Local Coding Models

Ollama, 2026.

[Ollama coding models](https://ollama.com/blog/launch?utm_source=chatgpt.com)

---

## [20] Ollama — Local Model Execution

Ollama, 2023–2026.

[Ollama local execution information](https://registry.ollama.com/blog/ollama-is-now-available-as-an-official-docker-image?utm_source=chatgpt.com)

---

## [21] MultiPL-E: A Scalable and Polyglot Approach to Benchmarking Neural Code Generation

Federico Cassano, John Gouwar, Daniel Nguyen, S. Nguyen, Luna Phipps-Costin, Donald Pinckney, Ming-Ho Yee, Yangtian Zi, Carolyn Jane Anderson, Molly Q. Feldman, Arjun Guha, Michael Greenberg, Abhinav Jangda.  
2023. *IEEE Transactions on Software Engineering*, Vol. 49, pp. 3675–3691.  
Citation count in retrieved academic index: **304**.

[Paper record](https://consensus.app/papers/multiple-a-scalable-and-polyglot-approach-to-benchmarking-cassano-gouwar/ee2a238c4d375023933a33fd69bcdc55/?utm_source=chatgpt.com)

---

## [22] McEval: Massively Multilingual Code Evaluation

Lin-Zheng Chai, Shu-Kai Liu, Jian Yang, Yuwei Yin, Ke Jin, Jiaheng Liu, Tao Sun, Ge Zhang, Changyu Ren, Hongcheng Guo, Z. Wang, Boyang Wang, Xian-Jie Wu, Bing Wang, Tongliang Li, Liqun Yang, Sufeng Duan, Zhoujun Li.  
2024. *arXiv:2406.07436*.  
Citation count in retrieved academic index: **43**.

[Paper record](https://consensus.app/papers/mceval-massively-multilingual-code-evaluation-chai-liu/e52629fe360e55398246543c6bc78ac7/?utm_source=chatgpt.com)

---

# 44. Final Phase Decision

### Phase 2 Result

```text
Existing Work
      ↓
Multilingual Code Generation
      ↓
Code-Mixed Prompt Research
      ↓
LLM Debugging
      ↓
Agentic Coding
      ↓
Local LLMs
      ↓
Combined Analysis
      ↓
System-Level Opportunity Identified
```

### Final Direction

Bhasha2Code will investigate:

> **Whether a multilingual, code-switched, NLP-routed, context-aware and offline local coding workflow can improve practical coding assistance and learning continuity compared with direct local-LLM interaction.**

---

# 45. Next Phase

## Phase 3 — User Definition

Research now provides the technical and problem justification.

The next phase will define exactly:

```text
WHO
↓
has the problem
↓
HOW
they currently work
↓
WHY
existing tools are insufficient
↓
WHAT
Bhasha2Code must provide
```

**Phase 2 Status: COMPLETE**