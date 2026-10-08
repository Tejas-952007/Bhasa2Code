# Bhasha2Code Labeled Tone Dataset (T10)

## Purpose

The Bhasha2Code Tone Dataset provides high-quality, labeled conversational programming queries to train and evaluate future tone classifiers (Task T11).

Bhasha2Code adapts its response presentation style based on the user's conversational tone. To prevent confounding factors, all samples are grounded in the **coding domain** while displaying distinct conversational tones across 6 major Indian linguistic styles.

---

## Dataset Schema

The dataset is stored in both CSV (`tone_dataset.csv`) and JSON Lines (`tone_dataset.jsonl`) formats with the following fields:

| Column | Type | Description |
|---|---|---|
| `id` | Integer | Unique sample identifier (1-indexed) |
| `text` | String | Raw conversational coding query |
| `tone` | String | Primary tone class (`CASUAL`, `FORMAL`, `SIMPLE`, `TECHNICAL`, `SHORT`, `DETAILED`) |
| `language` | String | Language style (`English`, `Hindi`, `Marathi`, `Hinglish`, `Marathi-English`, `Hindi-English`) |
| `domain` | String | Fixed context domain (`coding`) |

### Example Records:

```csv
id,text,tone,language,domain
1,"bro ha code check kar na",CASUAL,Marathi-English,coding
2,"Please explain the implementation of this algorithm.",FORMAL,English,coding
3,"simple language madhe samjhav",SIMPLE,Marathi-English,coding
4,"Analyze the algorithmic time and space complexity with formal Big-O proofs.",TECHNICAL,English,coding
5,"fakt answer de",SHORT,Marathi-English,coding
6,"step by step detail madhe explain kar",DETAILED,Marathi-English,coding
```

---

## Supported Tone Labels & Operational Definitions

### 1. CASUAL
Informal, conversational, peer-to-peer, friendly, abbreviated, or slang-style requests (`bro`, `bhai`, `yaar`, `re`, `na`, `arre`, `dude`).
- **Signal**: Informal greeting or relationship marker with conversational phrasing.
- **Example**: `bro can you check why my python loop is infinite`

### 2. FORMAL
Polite, respectful, professional, academic, or office-style language (`Please`, `Kindly`, `Could you please`, `कृपया`, `विनंती`).
- **Signal**: Explicit polite request markers and professional syntax.
- **Example**: `Please explain the architecture and design of this Python module.`

### 3. SIMPLE
The user explicitly asks for beginner-friendly, plain-language, non-jargon, or easy explanations (`simple words`, `beginner friendly`, `for a 5-year-old`, `sope shabdat`, `aasan bhasha me`).
- **Signal**: Simplicity requirement dominates over technical jargon.
- **Example**: `Explain this recursion concept using very simple words for a beginner.`

### 4. TECHNICAL
The user explicitly demands low-level mechanics, architectural depth, memory footprint, Big-O proofs, compiler AST, or internal execution details.
- **Signal**: Request focuses on deep technical internals or formal algorithmic complexity.
- **Note**: Technical programming words (e.g. `python`, `code`, `function`) alone do NOT make a query `TECHNICAL`.
- **Example**: `Analyze the algorithmic time and space complexity with formal Big-O proofs.`

### 5. SHORT
The user explicitly requests a brief, concise, direct, one-line, or code-only response (`just the code`, `only output`, `one line`, `briefly`, `fakt code de`, `bus code do`).
- **Signal**: Brevity and directness requirement.
- **Example**: `Just give me the Python code, nothing else.`

### 6. DETAILED
The user explicitly requests an exhaustive, comprehensive, step-by-step walk-through, covering edge cases, examples, and deep commentary.
- **Signal**: Depth, completeness, and step-by-step tutorial requirement.
- **Example**: `Explain this code step by step with complete details and examples.`

---

## Label Priority & Disambiguation Rules

When user requests contain multiple competing markers, the annotation prioritizes the **user's intended response format**:

$$\text{SHORT} \succ \text{DETAILED} \succ \text{SIMPLE} \succ \text{TECHNICAL} \succ \text{FORMAL} \succ \text{CASUAL}$$

### Disambiguation Examples:
- `"bro detail madhe samjhav"` $\rightarrow$ **DETAILED** (Depth requirement overrides casual greeting)
- `"bro fakt answer de"` $\rightarrow$ **SHORT** (Brevity requirement overrides casual greeting)
- `"technical but short answer de"` $\rightarrow$ **SHORT** (Format brevity overrides domain depth)
- `"simple and detailed explanation de"` $\rightarrow$ **DETAILED** (Comprehensive breakdown with beginner accessibility)
- `"Please explain this code briefly."` $\rightarrow$ **SHORT** (Format constraint overrides polite framing)

---

## Dataset Statistics

- **Total Samples**: 600 unique samples
- **Duplicate Texts**: 0
- **Null / Empty Fields**: 0
- **Text Length**:
  - Minimum: 21 characters
  - Maximum: 101 characters
  - Average: 61.9 characters

### Distribution by Tone Label (Balanced):
| Tone | Count | Percentage |
|---|---|---|
| `CASUAL` | 100 | 16.67% |
| `FORMAL` | 100 | 16.67% |
| `SIMPLE` | 100 | 16.67% |
| `TECHNICAL` | 100 | 16.67% |
| `SHORT` | 100 | 16.67% |
| `DETAILED` | 100 | 16.67% |
| **Total** | **600** | **100.0%** |

### Distribution by Language Style:
| Language | Count | Percentage |
|---|---|---|
| `English` | 102 | 17.0% |
| `Hindi` | 102 | 17.0% |
| `Marathi` | 102 | 17.0% |
| `Hinglish` | 102 | 17.0% |
| `Marathi-English` | 96 | 16.0% |
| `Hindi-English` | 96 | 16.0% |
| **Total** | **600** | **100.0%** |

---

## Dataset Splits

To prevent data leakage and provide benchmark comparability for T11 (Tone Classifier), the dataset is partitioned using a deterministic stratified split (random seed `42`):

- **Train Set** (`tone_train.csv`): 420 samples (70%, 70 per tone)
- **Validation Set** (`tone_validation.csv`): 90 samples (15%, 15 per tone)
- **Test Set** (`tone_test.csv`): 90 samples (15%, 15 per tone)

---

## Validation Procedure

Run the automated verification script:

```bash
python scripts/validate_tone_dataset.py
```

This validates:
1. File existence and schema completeness.
2. Zero duplicate texts or duplicate IDs.
3. Absence of null or empty fields.
4. Compliance with allowed tone and language sets.
5. Minimum sample threshold adherence ($\ge 300$).
6. Consistency between CSV and JSONL formats.

---

## Known Limitations

1. **Synthetic & Curated Seed**: All 600 samples were systematically authored based on authentic multilingual developer queries rather than web-scraped forums. While grammatically authentic, rare regional slang variants may not yet be covered.
2. **Single-Label Formulation**: Real-world user messages occasionally combine subtle intents (e.g. casual tone asking for a simple solution). The dataset uses single dominant operational labels as defined by the priority hierarchy.
3. **Future Extension**: As user interactions accumulate in Bhasha2Code, production logs will augment this baseline dataset with anonymized real-world conversational turns.
