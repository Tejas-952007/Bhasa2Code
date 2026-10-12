import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle

os.makedirs("/home/tejas/Desktop/Bhasa2code/report/diagrams", exist_ok=True)

def draw_system_architecture():
    fig, ax = plt.subplots(figsize=(16, 12), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 13)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    # Title
    ax.text(8, 12.5, "Bhasha2Code — Detailed Layered System Architecture", 
            fontsize=20, fontweight='bold', ha='center', va='center', color='#0F172A', fontfamily='sans-serif')
    ax.text(8, 12.1, "Multilingual NLP Pipeline • Local Code LLM • AST Validation • Containerized Sandbox", 
            fontsize=12, ha='center', va='center', color='#475569', fontfamily='sans-serif')

    layers = [
        {"y": 10.3, "h": 1.4, "title": "1. PRESENTATION LAYER (React 18 + Vite + Tailwind CSS)", 
         "color": "#E0F2FE", "border": "#0284C7", "boxes": [
             ("User Interface / Web Client", "Monaco Code Editor", "Chat & Prompt Input Bar", "Study Mode & Explanation UI", "Terminal Execution Console")
         ]},
        {"y": 8.5, "h": 1.4, "title": "2. API & GATEWAY LAYER (FastAPI Async Framework)", 
         "color": "#F1F5F9", "border": "#475569", "boxes": [
             ("REST API Endpoints", "Pydantic Request Schemas", "CORS & Security Middleware", "Session Router", "Health & Telemetry Checks")
         ]},
        {"y": 6.3, "h": 1.8, "title": "3. NLP & INTELLIGENCE LAYER (scikit-learn + Custom Indic Pipeline)", 
         "color": "#CCFBF1", "border": "#0D9488", "boxes": [
             ("Indic Normalizer & Tokenizer", "TF-IDF Feature Extractor\n(Word & Char N-grams)", "Logistic Regression\nTone Classifier", "18-Class Intent Classifier\n(92.59% Test Accuracy)", "Dynamic Prompt Builder\n& Directive Synthesizer")
         ]},
        {"y": 4.5, "h": 1.4, "title": "4. LOCAL LLM INFERENCE ENGINE (Ollama + Qwen2.5-Coder)", 
         "color": "#FEF3C7", "border": "#D97706", "boxes": [
             ("Ollama HTTP Client API", "Qwen2.5-Coder:1.5B (GGUF)", "CPU Autoregressive Inference\n(16.54 tok/sec)", "Streaming / Block Output Parser", "Context Window Buffer")
         ]},
        {"y": 2.7, "h": 1.4, "title": "5. CODE VALIDATION & SECURITY LAYER (Python AST Engine)", 
         "color": "#FEE2E2", "border": "#DC2626", "boxes": [
             ("Markdown Code Extractor", "Python AST Syntax Parser", "Static Safety Filter\n(Restricted Syscalls)", "Self-Correction Error Feedback", "Telemetry Logger")
         ]},
        {"y": 0.8, "h": 1.5, "title": "6. ISOLATED EXECUTION & DATA PERSISTENCE LAYER (Docker + SQLite)", 
         "color": "#F3E8FF", "border": "#7C3AED", "boxes": [
             ("Docker Sandbox Container\n(bhasha2code-sandbox)", "Resource Isolation\n(256MB RAM, 1 CPU, No Net)", "Ephemeral Execution Worker", "SQLite Relational Database", "SQLAlchemy ORM Models\n(Sessions & History)")
         ]},
    ]

    for layer in layers:
        # Layer backdrop
        rect = FancyBboxPatch((0.5, layer["y"]), 15.0, layer["h"],
                              boxstyle="round,pad=0.1,rounding_size=0.15",
                              facecolor=layer["color"], edgecolor=layer["border"], linewidth=1.5, alpha=0.9)
        ax.add_patch(rect)
        ax.text(0.8, layer["y"] + layer["h"] - 0.25, layer["title"], 
                fontsize=11, fontweight='bold', color='#0F172A', va='center')

        # Sub boxes
        n = len(layer["boxes"][0])
        box_w = 14.2 / n
        for i, text in enumerate(layer["boxes"][0]):
            bx = 0.9 + i * box_w
            by = layer["y"] + 0.15
            bw = box_w - 0.2
            bh = layer["h"] - 0.55
            sub_rect = FancyBboxPatch((bx, by), bw, bh,
                                      boxstyle="round,pad=0.08,rounding_size=0.1",
                                      facecolor='#FFFFFF', edgecolor=layer["border"], linewidth=1.0)
            ax.add_patch(sub_rect)
            ax.text(bx + bw/2, by + bh/2, text, fontsize=9, ha='center', va='center', 
                    color='#1E293B', fontweight='semibold', multialignment='center')

    # Draw vertical flow arrows connecting layers
    arrow_xs = [2.5, 5.5, 8.5, 11.5, 14.0]
    for y_top, y_bot in [(10.3, 9.9), (8.5, 8.1), (6.3, 5.9), (4.5, 4.1), (2.7, 2.3)]:
        for ax_x in [4.0, 8.0, 12.0]:
            ax.annotate('', xy=(ax_x, y_bot), xytext=(ax_x, y_top),
                        arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.4", 
                                        color="#475569", lw=1.5))

    plt.tight_layout()
    plt.savefig("/home/tejas/Desktop/Bhasa2code/report/diagrams/system_architecture.png", dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("Generated system_architecture.png")

def draw_block_diagram():
    fig, ax = plt.subplots(figsize=(15, 10), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    ax.text(7.5, 9.5, "Bhasha2Code — Hardware & Functional Block Diagram", 
            fontsize=19, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(7.5, 9.1, "Interaction between Subsystems, Modules, and Storage Components", 
            fontsize=12, ha='center', va='center', color='#475569')

    # Main blocks definition
    blocks = [
        {"id": "CLIENT", "x": 0.8, "y": 6.8, "w": 3.0, "h": 1.6, "bg": "#E0F2FE", "border": "#0284C7",
         "title": "USER INTERFACE BLOCK\n(React Web Client)", "desc": "• Multilingual input\n• Monaco Editor\n• Output viewer"},
        {"id": "API", "x": 4.6, "y": 6.8, "w": 3.0, "h": 1.6, "bg": "#F1F5F9", "border": "#475569",
         "title": "API CONTROLLER BLOCK\n(FastAPI Server)", "desc": "• Request dispatcher\n• Session management\n• Endpoint routing"},
        {"id": "NLP", "x": 8.4, "y": 6.8, "w": 3.0, "h": 1.6, "bg": "#CCFBF1", "border": "#0D9488",
         "title": "NLP PROCESSING BLOCK\n(scikit-learn)", "desc": "• TF-IDF Vectorizer\n• Tone Classifier\n• 18 Intent Classifier"},
        {"id": "PROMPT", "x": 12.0, "y": 6.8, "w": 2.4, "h": 1.6, "bg": "#FEF3C7", "border": "#D97706",
         "title": "PROMPT BUILDER", "desc": "• Context injection\n• Few-shot templates\n• Target language"},
        {"id": "LLM", "x": 10.5, "y": 3.5, "w": 3.7, "h": 1.8, "bg": "#FEF3C7", "border": "#D97706",
         "title": "LOCAL LLM INFERENCE BLOCK\n(Ollama Runtime)", "desc": "• Qwen2.5-Coder:1.5B (GGUF)\n• CPU execution (16.5 tok/s)\n• Raw response generator"},
        {"id": "VALID", "x": 5.8, "y": 3.5, "w": 3.8, "h": 1.8, "bg": "#FEE2E2", "border": "#DC2626",
         "title": "VALIDATION & AST BLOCK\n(Syntax Inspector)", "desc": "• Code block extractor\n• Python AST parser\n• Static security filters"},
        {"id": "SANDBOX", "x": 0.8, "y": 3.5, "w": 4.2, "h": 1.8, "bg": "#F3E8FF", "border": "#7C3AED",
         "title": "SANDBOX EXECUTION BLOCK\n(Docker Isolated Engine)", "desc": "• Ephemeral Container\n• 256MB RAM / 1 CPU limit\n• Disabled network / 10s cap"},
        {"id": "DB", "x": 4.6, "y": 0.8, "w": 5.8, "h": 1.5, "bg": "#E2E8F0", "border": "#334155",
         "title": "DATABASE PERSISTENCE BLOCK (SQLite + SQLAlchemy)", "desc": "• User chat sessions • Historical code snippets • Sandbox execution telemetry"}
    ]

    for b in blocks:
        rect = FancyBboxPatch((b["x"], b["y"]), b["w"], b["h"],
                              boxstyle="round,pad=0.1,rounding_size=0.12",
                              facecolor=b["bg"], edgecolor=b["border"], linewidth=1.5)
        ax.add_patch(rect)
        ax.text(b["x"] + b["w"]/2, b["y"] + b["h"] - 0.35, b["title"], 
                fontsize=9.5, fontweight='bold', ha='center', va='center', color='#0F172A', multialignment='center')
        ax.text(b["x"] + b["w"]/2, b["y"] + 0.45, b["desc"], 
                fontsize=8, ha='center', va='center', color='#334155', multialignment='center')

    # Draw arrows connecting blocks
    arrows = [
        ((3.8, 7.6), (4.6, 7.6), "HTTP POST Request"),
        ((7.6, 7.6), (8.4, 7.6), "Raw User Query"),
        ((11.4, 7.6), (12.0, 7.6), "Intent & Tone"),
        ((13.2, 6.8), (12.5, 5.3), "System Prompt"),
        ((10.5, 4.4), (9.6, 4.4), "Generated Code"),
        ((5.8, 4.4), (5.0, 4.4), "AST Valid Code"),
        ((2.3, 5.3), (2.3, 6.8), "Execution Output"),
        ((6.5, 6.8), (6.5, 2.3), "Save Session"),
        ((7.7, 3.5), (7.7, 2.3), "Log Run")
    ]

    for (x1, y1), (x2, y2), label in arrows:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.4", 
                                    color="#1E293B", lw=1.5))
        # Label placement
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        ax.text(mid_x, mid_y + 0.22, label, fontsize=7.5, ha='center', va='center', 
                color='#0F172A', fontweight='bold', bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=0.5))

    plt.tight_layout()
    plt.savefig("/home/tejas/Desktop/Bhasa2code/report/diagrams/block_diagram.png", dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("Generated block_diagram.png")

def draw_system_flowchart():
    fig, ax = plt.subplots(figsize=(14, 16), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 18)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    ax.text(7, 17.5, "Bhasha2Code — End-to-End Execution Flowchart", 
            fontsize=20, fontweight='bold', ha='center', va='center', color='#0F172A')
    ax.text(7, 17.1, "Step-by-step logic from Multilingual Query Input to Dockerized Execution", 
            fontsize=12, ha='center', va='center', color='#475569')

    # Node definitions
    # Flow elements:
    # 1. Start (Oval) at (7, 16.2)
    # 2. Input (Parallelogram) User Multilingual Request (7, 15.0)
    # 3. Process: Preprocess & Indic Normalization (7, 13.8)
    # 4. Process: TF-IDF Extraction & Dual Classification (7, 12.6)
    # 5. Process: Prompt Assembly with Directives (7, 11.4)
    # 6. Process: Local LLM Generation via Ollama (7, 10.2)
    # 7. Process: Extract Markdown & Code Blocks (7, 9.0)
    # 8. Decision: Contains Code Block? (7, 7.6)
    #    - No -> (11.5, 7.6) Render Conversational Response -> (11.5, 1.8) -> End
    #    - Yes -> 9. Process: AST Syntax & Security Parse (7, 6.2)
    # 10. Decision: Does AST Parse Pass? (7, 4.8)
    #    - No -> (2.5, 4.8) Generate Syntax Error Feedback & Warning -> (2.5, 2.8) -> Render
    #    - Yes -> 11. Decision: Execute in Sandbox? (7, 3.4)
    #      - No -> (7, 2.0) Display Code in Monaco Editor
    #      - Yes -> (7, 2.0) Execute in Ephemeral Docker Container
    # 12. Save to SQLite & Display Output (7, 0.8)
    # 13. End (Oval) at (7, -0.2) -> adjust coordinates so everything fits nicely between 0.5 and 16.5

    def draw_oval(x, y, w, h, text, color, border):
        patch = patches.Ellipse((x, y), w, h, facecolor=color, edgecolor=border, linewidth=1.5)
        ax.add_patch(patch)
        ax.text(x, y, text, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#0F172A')

    def draw_box(x, y, w, h, title, subtitle, color, border):
        patch = FancyBboxPatch((x - w/2, y - h/2), w, h,
                               boxstyle="round,pad=0.08,rounding_size=0.1",
                               facecolor=color, edgecolor=border, linewidth=1.5)
        ax.add_patch(patch)
        ax.text(x, y + 0.12, title, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#0F172A')
        ax.text(x, y - 0.22, subtitle, fontsize=8, ha='center', va='center', color='#334155')

    def draw_diamond(x, y, w, h, text, color, border):
        pts = [[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]]
        patch = patches.Polygon(pts, closed=True, facecolor=color, edgecolor=border, linewidth=1.5)
        ax.add_patch(patch)
        ax.text(x, y, text, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#0F172A', multialignment='center')

    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color="#1E293B", lw=1.5))
        if label:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            ax.text(mid_x + 0.25, mid_y, label, fontsize=8, fontweight='bold', color='#0F172A',
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=0.5))

    # Elements
    draw_oval(7, 16.3, 3.2, 0.8, "START", "#E2E8F0", "#475569")
    draw_arrow(7, 15.9, 7, 15.1)

    draw_box(7, 14.6, 6.2, 0.9, "1. User Input Received", "Natural Language Prompt (Hindi / Marathi / Hinglish / English)", "#E0F2FE", "#0284C7")
    draw_arrow(7, 14.15, 7, 13.45)

    draw_box(7, 13.0, 6.2, 0.9, "2. Preprocessing & Normalization", "Indic script cleaning, Unicode normalization, whitespace trimming", "#F1F5F9", "#475569")
    draw_arrow(7, 12.55, 7, 11.85)

    draw_box(7, 11.4, 6.2, 0.9, "3. Feature Extraction & Classification", "Dual TF-IDF Vectorizers + Logistic Regression (Tone & 18 Intents)", "#CCFBF1", "#0D9488")
    draw_arrow(7, 10.95, 7, 10.25)

    draw_box(7, 9.8, 6.2, 0.9, "4. Contextual Prompt Assembly", "Dynamic System Directives + Target Language + Anti-Placeholder Rules", "#FEF3C7", "#D97706")
    draw_arrow(7, 9.35, 7, 8.65)

    draw_box(7, 8.2, 6.2, 0.9, "5. Local LLM Inference", "Qwen2.5-Coder:1.5B via Ollama HTTP API (CPU Execution @ 16.5 tok/s)", "#FEF3C7", "#D97706")
    draw_arrow(7, 7.75, 7, 7.05)

    draw_diamond(7, 6.3, 3.6, 1.4, "Contains\nCode Block?", "#F8FAFC", "#0284C7")

    # If No code block -> Explanation
    draw_arrow(8.8, 6.3, 11.5, 6.3, "NO")
    draw_box(11.5, 4.8, 3.4, 1.0, "Conversational Output", "Render conceptual explanation\nor debugging guidance", "#F1F5F9", "#64748B")
    draw_arrow(11.5, 6.3, 11.5, 5.3)

    # If Yes code block -> AST Syntax validation
    draw_arrow(7, 5.6, 7, 4.8, "YES")
    draw_box(7, 4.3, 6.2, 0.9, "6. AST Validation & Security Check", "Python AST parse tree validation + restricted imports scanning", "#FEE2E2", "#DC2626")
    draw_arrow(7, 3.85, 7, 3.15)

    draw_diamond(7, 2.4, 3.6, 1.4, "AST Valid & Safe?", "#F8FAFC", "#DC2626")

    # If AST fails -> Syntax error feedback
    draw_arrow(5.2, 2.4, 2.5, 2.4, "NO")
    draw_box(2.5, 1.2, 3.4, 1.0, "Syntax Error Warning", "Display line-number errors &\nprompt for model regeneration", "#FEE2E2", "#DC2626")
    draw_arrow(2.5, 2.4, 2.5, 1.7)

    # If AST passes -> Execute Sandbox?
    draw_arrow(8.8, 2.4, 10.5, 2.4, "YES")
    draw_box(10.5, 1.2, 4.0, 1.1, "7. Docker Sandbox Run", "Ephemeral container, 256MB RAM,\n1 CPU, network off, 10s timeout", "#F3E8FF", "#7C3AED")

    # Final Convergence to Result / DB
    draw_box(6.5, 0.8, 3.6, 0.7, "8. Session Persistence", "Save prompt, code & run to SQLite", "#E2E8F0", "#334155")
    draw_arrow(10.5, 0.65, 8.3, 0.8)
    draw_arrow(2.5, 0.7, 4.7, 0.8)
    draw_arrow(11.5, 4.3, 8.3, 0.8)

    draw_oval(6.5, -0.2, 2.8, 0.6, "END", "#E2E8F0", "#475569")
    draw_arrow(6.5, 0.45, 6.5, 0.1)

    plt.tight_layout()
    plt.savefig("/home/tejas/Desktop/Bhasa2code/report/diagrams/flowchart.png", dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print("Generated flowchart.png")

if __name__ == "__main__":
    draw_system_architecture()
    draw_block_diagram()
    draw_system_flowchart()
    print("All diagrams generated successfully!")
