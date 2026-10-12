# Centralized lexical resources for offline language detection in Bhasha2Code

TECHNICAL_WORDS = {
    # Programming languages
    "python", "java", "javascript", "c", "cpp", "csharp", "ruby", "go", "rust",
    "php", "html", "css", "sql", "bash", "shell", "r", "swift", "kotlin", "typescript",
    # Core concepts and programming vocabulary
    "code", "program", "function", "class", "method", "variable", "loop", "array",
    "list", "dictionary", "dict", "set", "tuple", "api", "endpoint", "debug",
    "debugger", "error", "exception", "compile", "compiler", "import", "return",
    "if", "else", "elif", "for", "while", "database", "query", "model",
    "machine", "learning", "algorithm", "async", "await", "promise", "frontend",
    "backend", "server", "client", "rest", "json", "xml", "framework", "package",
    "library", "module", "stack", "trace", "traceback", "file", "script", "line",
    "terminal", "calculator", "palindrome", "sort", "sorting", "bubble", "search",
    "binary", "recursion", "node", "tree", "graph", "object", "instance",
    "inheritance", "interface", "null", "undefined", "true", "false", "boolean",
    "integer", "int", "float", "string", "str", "char", "git", "github", "commit",
    "schema", "table", "column", "syntax", "runtime", "thread", "process",
    # Popular libraries and frameworks
    "numpy", "pandas", "matplotlib", "scipy", "sklearn", "seaborn", "tensorflow", "pytorch", "keras",
    "flask", "django", "fastapi", "react", "vue", "angular", "express", "docker", "kubernetes",
    # Devanagari technical loan words
    "कोड", "प्रोग्राम", "फंक्शन", "क्लास", "एरर", "डेटाबेस", "पायथन", "कॅल्क्युलेटर",
}

# Homographs between Latin Indian transliterations and English
HOMOGRAPH_WORDS = {"in", "is", "do", "to", "me", "us", "so", "the"}

UNAMBIGUOUS_ENGLISH_WORDS = {
    "write", "writes", "writing", "explain", "explains", "explained", "how", "does", "work",
    "works", "working", "what", "are", "was", "were", "be", "been", "can", "could", "would",
    "should", "will", "you", "your", "please", "help", "we", "our", "with", "this", "that",
    "these", "those", "why", "when", "where", "which", "who", "on", "at", "for", "from",
    "by", "of", "detail", "detailed", "step", "steps", "create", "implement", "build", "fix",
    "solve", "show", "find", "give", "tell", "clarify", "meaning", "difference", "between",
    "overview", "example", "examples", "tutorial", "understand", "guide", "issue", "problem",
    "simple", "best", "practice", "generate", "review", "optimize", "fast", "slow", "correct",
    "wrong", "good", "better", "want", "need", "about", "have", "has", "had", "there", "then",
    "just", "now", "here",
}

DEVANAGARI_MARATHI_WORDS = {
    "मला", "माझा", "माझी", "माझे", "माझं", "तुला", "तुझा", "तुझी", "तुझे", "आम्हाला",
    "त्याला", "तिला", "त्यांना", "त्याचा", "त्याची", "त्याचे", "त्यांच्या",
    "आहे", "नाही", "आहेत", "नाहीत", "होता", "होती", "होते",
    "काय", "कसा", "कशी", "कसे", "कसं", "कधी", "कुठे", "का", "कशासाठी",
    "कर", "करा", "करायचा", "करायचे", "करायची", "करावे", "करतो", "करते", "करतात", "केला", "केली", "केले", "करून",
    "पाहिजे", "हवे", "हवा", "हवी", "सांग", "सांगा", "समजत", "समजावून", "सांगतो", "सांगते",
    "मध्ये", "मधले", "मधून", "साठी", "सोबत",
    "हा", "ही", "हे", "या", "तो", "ती", "ते", "त्या", "असा", "अशी", "असे",
    "चा", "ची", "चे", "च्या", "ने", "नी", "ला", "ना", "तयार", "दाखव", "दाखवा",
}

DEVANAGARI_HINDI_WORDS = {
    "मुझे", "मेरा", "मेरी", "मेरे", "मुझको", "तुझे", "तेरा", "तेरी", "तेरे", "हमें",
    "हमारा", "हमारी", "हमारे", "उसको", "उसे", "उसका", "उसकी", "उसके", "उनको", "उन्हें",
    "है", "हैं", "हो", "था", "थी", "थे", "रहा", "रही", "रहे",
    "क्या", "कैसे", "कैसा", "कैसी", "कब", "कहाँ", "क्यों",
    "करो", "करना", "कीजिए", "करता", "करती", "करते", "किया", "किए", "की", "करके",
    "चाहिए", "बताओ", "बताइए", "समझाओ", "समझाइए", "समझ", "समझा", "आ",
    "में", "से", "को", "का", "की", "के", "लिए", "पर", "और", "या", "लेकिन",
    "यह", "ये", "वह", "वो", "इस", "उस", "इन", "उन",
    "सकता", "सकती", "सकते",
    "कृपया", "बनाओ", "बनाना", "दो", "दिखाओ",
}

UNAMBIGUOUS_LATIN_MARATHI_WORDS = {
    "mala", "majha", "maza", "majhi", "mazhi", "majhe", "maze", "mazha", "majh", "mazh",
    "tula", "tujha", "tuza", "tujhi", "tuzhi", "tujhe", "tuze",
    "aamhala", "amhala", "tyala", "tila", "tyanna", "tyancha", "tyanchi", "tyanche",
    "ahe", "aahe", "ahet", "aahet", "nahit", "hota", "hoti", "hote",
    "kay", "kasa", "kashi", "kase", "kasaa", "kashii", "kasee", "kas", "kadhi", "kuthe", "kuth", "ka",
    "kara", "karaycha", "karayche", "karaychi", "karave", "karto", "karte", "kartat", "kela", "keli", "kele", "karun",
    "pahije", "pahijet", "hava", "havi", "have", "sang", "sanga", "sangna", "samjavun", "samjat", "kalat", "kalala",
    "madhe", "madhye", "madhun", "sathi", "sobat", "sobath",
    "cha", "chi", "che", "chya", "var", "khali", "suddha", "tayar", "dakhva", "kiti",
    "yat", "ani", "de", "banav", "banva", "kahi", "tar", "karr", "krr", "sangg", "dakhav", "dakva",
}

UNAMBIGUOUS_LATIN_HINDI_WORDS = {
    "mujhe", "mera", "meri", "mere", "mujhko", "tujhe", "tera", "teri", "tere",
    "hume", "humara", "humari", "humare", "usko", "use", "uska", "uski", "uske",
    "unko", "unhe", "unka", "unki", "unke",
    "hai", "hain", "ho", "tha", "thi", "raha", "rahi", "rahe",
    "kya", "kaise", "kaisa", "kaisi", "kab", "kahan", "kyu", "kyun",
    "karo", "karna", "kijiye", "karta", "karti", "karte", "kiya", "kiye", "karke",
    "chahiye", "batao", "bataiye", "samjhao", "samjhado", "samajh", "samjha", "samjhana",
    "mein", "liye", "aur", "lekin",
    "ye", "yeh", "wo", "woh",
    "sakta", "sakti", "sakte", "sake",
    "banao", "banana", "dijiye", "dikhao", "bata", "ek",
}

SHARED_INDIAN_WORDS = {"nahi", "nahin", "nhi", "kar", "karr", "krr", "kr", "pan", "ha", "hi", "he", "ya", "bana"}

# Re-exported combined dictionaries for general compatibility
ENGLISH_WORDS = UNAMBIGUOUS_ENGLISH_WORDS | HOMOGRAPH_WORDS
LATIN_MARATHI_WORDS = UNAMBIGUOUS_LATIN_MARATHI_WORDS | SHARED_INDIAN_WORDS
LATIN_HINDI_WORDS = UNAMBIGUOUS_LATIN_HINDI_WORDS | SHARED_INDIAN_WORDS

HINGLISH_PHRASE_PATTERNS = [
    r"\bbanana\s+hai\b",
    r"\bbana\s+do\b",
    r"\bkaise\s+fix\b",
    r"\bfix\s+kare\b",
    r"\bkaru\s+kya\b",
    r"\bkarega\b",
    r"\bkarenge\b",
    r"\bpython\s+me\b",
    r"\bme\s+ye\b",
]
