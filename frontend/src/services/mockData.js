/**
 * Deterministic mock data for Bhasha2Code frontend foundation.
 * Simulates local workspace state without requiring an active backend in T20.
 */

export const INITIAL_SESSIONS = [
  {
    id: "session-1",
    title: "Python Calculator",
    lastUpdated: "Today",
    language: "python",
    active: true,
  },
  {
    id: "session-2",
    title: "DBMS Normalization",
    lastUpdated: "Yesterday",
    language: "sql",
    active: false,
  },
  {
    id: "session-3",
    title: "NLP Assignment",
    lastUpdated: "2 days ago",
    language: "python",
    active: false,
  },
];

export const DEMO_CONVERSATION = [
  {
    id: "msg-1",
    role: "user",
    timestamp: "10:30 AM",
    content: "python madhe calculator bana",
    language: "MARATHI_ENGLISH",
  },
  {
    id: "msg-2",
    role: "assistant",
    timestamp: "10:30 AM",
    content: "Here is a clean Python command-line calculator with modular functions and defensive division-by-zero validation.",
    codeBlock: {
      filename: "calculator.py",
      language: "python",
      code: `def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def calculator():
    print("Simple Python Calculator")
    num1 = float(input("Enter first number: "))
    op = input("Enter operator (+, -, *, /): ")
    num2 = float(input("Enter second number: "))

    if op == '+':
        result = add(num1, num2)
    elif op == '-':
        result = subtract(num1, num2)
    elif op == '*':
        result = multiply(num1, num2)
    elif op == '/':
        result = divide(num1, num2)
    else:
        print("Invalid operator")
        return

    print(f"Result: {result}")

if __name__ == "__main__":
    calculator()`,
      validationStatus: "VALID", // VALID | INVALID | NOT_VALIDATED | UNSUPPORTED
      executionStatus: "SUCCESS", // SUCCESS | RUNTIME_ERROR | TIMEOUT | RESOURCE_LIMIT
      output: "Simple Python Calculator\nEnter first number: 10\nEnter operator (+, -, *, /): +\nEnter second number: 5\nResult: 15.0",
      durationMs: 152.4,
    },
    explanation: [
      "Modular arithmetic functions (add, subtract, multiply, divide) keep core logic reusable.",
      "Defensive validation prevents ZeroDivisionError crashes during calculation.",
      "The script uses standard formatted input/output with clear operator dispatching."
    ],
    example: "Input: 10, +, 5 → Result: 15.0",
    study: {
      problemUnderstanding: "A basic command-line arithmetic evaluator that parses two numerical operands and an operator symbol, evaluates the expression, and safely displays the result.",
      algorithm: [
        "1. Prompt the user for the first operand and convert input to floating-point.",
        "2. Prompt for the operator symbol (+, -, *, /).",
        "3. Prompt for the second numerical operand.",
        "4. Branch based on the selected operator.",
        "5. Guard against division by zero before dividing.",
        "6. Return and print the formatted evaluation result."
      ],
      flowchart: `Start
  ↓
Input num1
  ↓
Input operator (+, -, *, /)
  ↓
Input num2
  ↓
Is operator '/' and num2 == 0?
  ├── Yes ──> Display "Cannot divide by zero" ──> End
  └── No  ──> Calculate result
  ↓
Display Result
  ↓
End`,
      importantPoints: [
        "Always convert input() strings to numeric types (int or float) before arithmetic operations.",
        "Guard division operations explicitly before evaluation to prevent unhandled runtime crashes.",
        "Use if __name__ == '__main__': to keep the calculator module importable in tests."
      ],
      vivaQuestions: [
        {
          q: "Why is division by zero checked before performing division?",
          a: "In Python, dividing by zero raises a ZeroDivisionError which terminates the script ungracefully unless guarded."
        },
        {
          q: "What is the benefit of defining separate functions for each operation?",
          a: "Separation of concerns allows unit testing individual functions independently and simplifies extending new operations later."
        }
      ]
    }
  }
];

export const DEMO_NOTES = [
  {
    id: "note-1",
    title: "Python Recursion & Base Conditions",
    date: "Oct 7, 2026",
    content: "Recursion requires two components: 1) Base case that terminates the stack, 2) Recursive step moving toward the base case. Always analyze stack frame depth."
  },
  {
    id: "note-2",
    title: "NLP Intent Classification Features",
    date: "Oct 6, 2026",
    content: "Multilingual code queries benefit from character and word n-grams (1-3) to capture code keywords mixed with Marathi/Hindi grammatical particles."
  },
  {
    id: "note-3",
    title: "DBMS BCNF vs 3NF Trade-offs",
    date: "Oct 4, 2026",
    content: "3NF always preserves functional dependencies. BCNF guarantees zero redundancy from functional dependencies but may not always preserve all dependencies."
  }
];

export const DEMO_SAVED_ITEMS = [
  {
    id: "saved-1",
    title: "Python Calculator implementation",
    sessionTitle: "Python Calculator",
    date: "Oct 8, 2026",
    snippet: "def divide(a, b): if b == 0: raise ValueError('Cannot divide by zero')"
  },
  {
    id: "saved-2",
    title: "DBMS 3NF Normalization Steps",
    sessionTitle: "DBMS Normalization",
    date: "Oct 7, 2026",
    snippet: "For every non-trivial FD X -> A, either X is a superkey or A is a prime attribute."
  },
  {
    id: "saved-3",
    title: "Time complexity of recursive Fibonacci",
    sessionTitle: "Algorithm Concepts",
    date: "Oct 5, 2026",
    snippet: "Naive recursion has O(2^n) time complexity; memoization reduces it to O(n)."
  }
];
