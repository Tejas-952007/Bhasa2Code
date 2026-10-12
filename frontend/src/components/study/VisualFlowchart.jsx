import React, { useState } from 'react';
import {
  Play,
  CheckCircle2,
  AlertTriangle,
  GitBranch,
  CornerDownRight,
  ArrowDown,
  Layers,
  FileText,
  Terminal,
  RotateCcw,
  Info,
} from 'lucide-react';

/**
 * ISO / ANSI Standard Flowchart SVG for Binary Search
 * Complies with textbook flowchart rules:
 * - Oval / Capsule: Terminal (Start / End)
 * - Rectangle: Process / Arithmetic Action
 * - Diamond: Decision Point (Conditional Branch)
 * - Flow Lines: Directed orthogonal arrows
 * - Loopback: While loop repeat edge returning to loop condition diamond
 */
function BinarySearchSvgDiagram({ hoveredNode, setHoveredNode }) {
  return (
    <div style={{ width: '100%', overflowX: 'auto', display: 'flex', justifyContent: 'center' }}>
      <svg
        viewBox="0 0 660 710"
        style={{
          width: '100%',
          maxWidth: '660px',
          height: 'auto',
          display: 'block',
          fontFamily: 'var(--font-sans, system-ui, -apple-system, sans-serif)',
        }}
      >
        <defs>
          {/* Arrow markers */}
          <marker
            id="arrow-std"
            viewBox="0 0 10 10"
            refX="6"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#334155" />
          </marker>
          <marker
            id="arrow-yes"
            viewBox="0 0 10 10"
            refX="6"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#16a34a" />
          </marker>
          <marker
            id="arrow-no"
            viewBox="0 0 10 10"
            refX="6"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#dc2626" />
          </marker>
          <marker
            id="arrow-loop"
            viewBox="0 0 10 10"
            refX="6"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#2563eb" />
          </marker>

          {/* Filter for subtle drop-shadow */}
          <filter id="flow-shadow" x="-8%" y="-8%" width="116%" height="116%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#0f172a" floodOpacity="0.08" />
          </filter>
        </defs>

        {/* 1. START TERMINAL (Oval) */}
        <g
          onMouseEnter={() => setHoveredNode('start')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <rect
            x="260"
            y="18"
            width="140"
            height="40"
            rx="20"
            ry="20"
            fill={hoveredNode === 'start' ? '#d1fae5' : '#ecfdf5'}
            stroke="#059669"
            strokeWidth="2.5"
            filter="url(#flow-shadow)"
          />
          <text
            x="330"
            y="43"
            textAnchor="middle"
            fill="#065f46"
            fontSize="14"
            fontWeight="700"
            letterSpacing="0.03em"
          >
            Start
          </text>
        </g>

        {/* Flow: Start -> Init */}
        <line
          x1="330"
          y1="58"
          x2="330"
          y2="92"
          stroke="#475569"
          strokeWidth="2"
          markerEnd="url(#arrow-std)"
        />

        {/* 2. INITIALIZATION (Process Rectangle) */}
        <g
          onMouseEnter={() => setHoveredNode('init')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <rect
            x="190"
            y="94"
            width="280"
            height="58"
            rx="4"
            ry="4"
            fill={hoveredNode === 'init' ? '#eff6ff' : '#ffffff'}
            stroke="#2563eb"
            strokeWidth="2"
            filter="url(#flow-shadow)"
          />
          <text
            x="330"
            y="114"
            textAnchor="middle"
            fill="#1e40af"
            fontSize="12"
            fontWeight="700"
          >
            low = 0 , high = N - 1
          </text>
          <text
            x="330"
            y="136"
            textAnchor="middle"
            fill="#334155"
            fontSize="12"
            fontFamily="var(--font-mono, monospace)"
            fontWeight="600"
          >
            mid = (low + high) // 2
          </text>
        </g>

        {/* Flow: Init -> Decision 1 */}
        <line
          x1="330"
          y1="152"
          x2="330"
          y2="186"
          stroke="#475569"
          strokeWidth="2"
          markerEnd="url(#arrow-std)"
        />

        {/* 3. LOOP CONDITION (Decision Diamond 1) */}
        <g
          onMouseEnter={() => setHoveredNode('loop_cond')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <polygon
            points="330,188 475,238 330,288 185,238"
            fill={hoveredNode === 'loop_cond' ? '#fef3c7' : '#fffbeb'}
            stroke="#d97706"
            strokeWidth="2.5"
            filter="url(#flow-shadow)"
          />
          <text
            x="330"
            y="232"
            textAnchor="middle"
            fill="#92400e"
            fontSize="12"
            fontWeight="700"
          >
            low ≤ high &amp;&amp;
          </text>
          <text
            x="330"
            y="250"
            textAnchor="middle"
            fill="#92400e"
            fontSize="12"
            fontWeight="700"
            fontFamily="var(--font-mono, monospace)"
          >
            arr[mid] != target ?
          </text>
        </g>

        {/* FLOW: Decision 1 -> NO branch (Loop Exit: Not Found or Terminated) */}
        <path
          d="M 475 238 L 565 238 L 565 572 L 446 572"
          fill="none"
          stroke="#dc2626"
          strokeWidth="2"
          markerEnd="url(#arrow-no)"
        />
        <rect x="488" y="222" width="34" height="18" rx="4" fill="#fee2e2" stroke="#ef4444" strokeWidth="1" />
        <text x="505" y="235" textAnchor="middle" fill="#991b1b" fontSize="10" fontWeight="700">
          NO
        </text>

        {/* FLOW: Decision 1 -> YES branch (Enter Loop Body) */}
        <line
          x1="330"
          y1="288"
          x2="330"
          y2="324"
          stroke="#16a34a"
          strokeWidth="2"
          markerEnd="url(#arrow-yes)"
        />
        <rect x="338" y="294" width="38" height="18" rx="4" fill="#dcfce7" stroke="#22c55e" strokeWidth="1" />
        <text x="357" y="307" textAnchor="middle" fill="#166534" fontSize="10" fontWeight="700">
          YES
        </text>

        {/* 4. TARGET CHECK (Decision Diamond 2) */}
        <g
          onMouseEnter={() => setHoveredNode('target_check')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <polygon
            points="330,326 445,372 330,418 215,372"
            fill={hoveredNode === 'target_check' ? '#fef3c7' : '#fffbeb'}
            stroke="#d97706"
            strokeWidth="2"
            filter="url(#flow-shadow)"
          />
          <text
            x="330"
            y="370"
            textAnchor="middle"
            fill="#92400e"
            fontSize="12"
            fontWeight="700"
            fontFamily="var(--font-mono, monospace)"
          >
            target &lt; arr[mid] ?
          </text>
        </g>

        {/* Diamond 2 -> YES branch (Search left: high = mid - 1) */}
        <path
          d="M 445 372 L 495 372 L 495 408"
          fill="none"
          stroke="#16a34a"
          strokeWidth="2"
          markerEnd="url(#arrow-yes)"
        />
        <rect x="452" y="358" width="36" height="18" rx="4" fill="#dcfce7" stroke="#22c55e" strokeWidth="1" />
        <text x="470" y="371" textAnchor="middle" fill="#166534" fontSize="10" fontWeight="700">
          YES
        </text>

        {/* Process: high = mid - 1 */}
        <g
          onMouseEnter={() => setHoveredNode('update_high')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <rect
            x="430"
            y="410"
            width="130"
            height="38"
            rx="4"
            fill={hoveredNode === 'update_high' ? '#dbeafe' : '#f0f9ff'}
            stroke="#0284c7"
            strokeWidth="1.5"
            filter="url(#flow-shadow)"
          />
          <text
            x="495"
            y="434"
            textAnchor="middle"
            fill="#0369a1"
            fontSize="12"
            fontFamily="var(--font-mono, monospace)"
            fontWeight="700"
          >
            high = mid - 1
          </text>
        </g>

        {/* Diamond 2 -> NO branch (Search right: low = mid + 1) */}
        <line
          x1="330"
          y1="418"
          x2="330"
          y2="444"
          stroke="#dc2626"
          strokeWidth="2"
          markerEnd="url(#arrow-no)"
        />
        <rect x="338" y="420" width="34" height="18" rx="4" fill="#fee2e2" stroke="#ef4444" strokeWidth="1" />
        <text x="355" y="433" textAnchor="middle" fill="#991b1b" fontSize="10" fontWeight="700">
          NO
        </text>

        {/* Process: low = mid + 1 */}
        <g
          onMouseEnter={() => setHoveredNode('update_low')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <rect
            x="265"
            y="446"
            width="130"
            height="38"
            rx="4"
            fill={hoveredNode === 'update_low' ? '#dbeafe' : '#f0f9ff'}
            stroke="#0284c7"
            strokeWidth="1.5"
            filter="url(#flow-shadow)"
          />
          <text
            x="330"
            y="470"
            textAnchor="middle"
            fill="#0369a1"
            fontSize="12"
            fontFamily="var(--font-mono, monospace)"
            fontWeight="700"
          >
            low = mid + 1
          </text>
        </g>

        {/* Connector from high = mid - 1 into mid calculation */}
        <path
          d="M 495 448 L 495 504 L 406 504"
          fill="none"
          stroke="#475569"
          strokeWidth="1.5"
          markerEnd="url(#arrow-std)"
        />

        {/* Connector from low = mid + 1 into mid calculation */}
        <line
          x1="330"
          y1="484"
          x2="330"
          y2="494"
          stroke="#475569"
          strokeWidth="2"
          markerEnd="url(#arrow-std)"
        />

        {/* 5. RECALCULATE MIDPOINT (Process Rectangle) */}
        <g
          onMouseEnter={() => setHoveredNode('recalc')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <rect
            x="225"
            y="496"
            width="210"
            height="44"
            rx="4"
            fill={hoveredNode === 'recalc' ? '#eff6ff' : '#ffffff'}
            stroke="#2563eb"
            strokeWidth="2"
            filter="url(#flow-shadow)"
          />
          <text
            x="330"
            y="523"
            textAnchor="middle"
            fill="#1e40af"
            fontSize="12"
            fontFamily="var(--font-mono, monospace)"
            fontWeight="700"
          >
            mid = (low + high) // 2
          </text>
        </g>

        {/* ============================================================== */}
        {/* 6. LOOPBACK ARROW (Authentic While-Loop cycle back to Decision 1) */}
        {/* ============================================================== */}
        <path
          d="M 225 518 L 80 518 L 80 238 L 181 238"
          fill="none"
          stroke="#2563eb"
          strokeWidth="2.5"
          markerEnd="url(#arrow-loop)"
        />
        {/* Loop label badge on vertical left line */}
        <rect x="52" y="360" width="56" height="24" rx="4" fill="#dbeafe" stroke="#3b82f6" strokeWidth="1" />
        <text
          x="80"
          y="376"
          textAnchor="middle"
          fill="#1d4ed8"
          fontSize="10"
          fontWeight="700"
        >
          ↺ Loop
        </text>

        {/* 7. RESULT / RETURN PROCESS (After Loop Exit) */}
        <g
          onMouseEnter={() => setHoveredNode('result')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <rect
            x="215"
            y="552"
            width="230"
            height="46"
            rx="4"
            fill={hoveredNode === 'result' ? '#f1f5f9' : '#f8fafc'}
            stroke="#475569"
            strokeWidth="2"
            filter="url(#flow-shadow)"
          />
          <text
            x="330"
            y="571"
            textAnchor="middle"
            fill="#334155"
            fontSize="11"
            fontWeight="600"
          >
            return mid if target == arr[mid]
          </text>
          <text
            x="330"
            y="588"
            textAnchor="middle"
            fill="#64748b"
            fontSize="11"
            fontWeight="600"
          >
            else return -1
          </text>
        </g>

        {/* Flow: Result -> End */}
        <line
          x1="330"
          y1="598"
          x2="330"
          y2="630"
          stroke="#475569"
          strokeWidth="2"
          markerEnd="url(#arrow-std)"
        />

        {/* 8. END TERMINAL (Oval) */}
        <g
          onMouseEnter={() => setHoveredNode('end')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <rect
            x="260"
            y="632"
            width="140"
            height="40"
            rx="20"
            ry="20"
            fill={hoveredNode === 'end' ? '#e2e8f0' : '#f1f5f9'}
            stroke="#475569"
            strokeWidth="2.5"
            filter="url(#flow-shadow)"
          />
          <text
            x="330"
            y="657"
            textAnchor="middle"
            fill="#1e293b"
            fontSize="14"
            fontWeight="700"
            letterSpacing="0.03em"
          >
            End
          </text>
        </g>
      </svg>
    </div>
  );
}

/**
 * ISO / ANSI Standard Flowchart SVG for Linear Search
 * Conforms to:
 * Start -> initialize i = 0 -> check i < len(arr) -> compare arr[i] with target
 * -> if matched, return index i -> otherwise increment i and loop
 * -> if array ends, report not found -> End.
 * Strict constraint: NEVER uses low, high, mid or arr[mid].
 */
function LinearSearchSvgDiagram({ hoveredNode, setHoveredNode }) {
  return (
    <div style={{ width: '100%', overflowX: 'auto', display: 'flex', justifyContent: 'center' }}>
      <svg
        viewBox="0 0 660 620"
        style={{
          width: '100%',
          maxWidth: '660px',
          height: 'auto',
          display: 'block',
          fontFamily: 'var(--font-sans, system-ui, -apple-system, sans-serif)',
        }}
      >
        <defs>
          <marker
            id="ls-arrow-std"
            viewBox="0 0 10 10"
            refX="6"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#334155" />
          </marker>
          <marker
            id="ls-arrow-yes"
            viewBox="0 0 10 10"
            refX="6"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#16a34a" />
          </marker>
          <marker
            id="ls-arrow-no"
            viewBox="0 0 10 10"
            refX="6"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#dc2626" />
          </marker>
          <marker
            id="ls-arrow-loop"
            viewBox="0 0 10 10"
            refX="6"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#2563eb" />
          </marker>
          <filter id="ls-shadow" x="-8%" y="-8%" width="116%" height="116%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#0f172a" floodOpacity="0.08" />
          </filter>
        </defs>

        {/* 1. START TERMINAL (Oval) */}
        <g
          onMouseEnter={() => setHoveredNode('start')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <rect
            x="260"
            y="18"
            width="140"
            height="40"
            rx="20"
            ry="20"
            fill={hoveredNode === 'start' ? '#d1fae5' : '#ecfdf5'}
            stroke="#059669"
            strokeWidth="2.5"
            filter="url(#ls-shadow)"
          />
          <text
            x="330"
            y="43"
            textAnchor="middle"
            fill="#065f46"
            fontSize="14"
            fontWeight="700"
            letterSpacing="0.03em"
          >
            Start
          </text>
        </g>

        {/* Flow: Start -> Init */}
        <line
          x1="330"
          y1="58"
          x2="330"
          y2="92"
          stroke="#475569"
          strokeWidth="2"
          markerEnd="url(#ls-arrow-std)"
        />

        {/* 2. INITIALIZE (Process Rectangle: i = 0) */}
        <g
          onMouseEnter={() => setHoveredNode('init')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <rect
            x="210"
            y="94"
            width="240"
            height="50"
            rx="4"
            ry="4"
            fill={hoveredNode === 'init' ? '#eff6ff' : '#ffffff'}
            stroke="#2563eb"
            strokeWidth="2"
            filter="url(#ls-shadow)"
          />
          <text
            x="330"
            y="114"
            textAnchor="middle"
            fill="#1e40af"
            fontSize="12"
            fontWeight="700"
          >
            Initialize Index Pointer
          </text>
          <text
            x="330"
            y="132"
            textAnchor="middle"
            fill="#334155"
            fontSize="13"
            fontFamily="var(--font-mono, monospace)"
            fontWeight="700"
          >
            i = 0
          </text>
        </g>

        {/* Flow: Init -> Decision 1 */}
        <line
          x1="330"
          y1="144"
          x2="330"
          y2="178"
          stroke="#475569"
          strokeWidth="2"
          markerEnd="url(#ls-arrow-std)"
        />

        {/* 3. LOOP CONDITION: Array Boundary Check (Diamond 1) */}
        <g
          onMouseEnter={() => setHoveredNode('loop_cond')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <polygon
            points="330,180 460,225 330,270 200,225"
            fill={hoveredNode === 'loop_cond' ? '#fef3c7' : '#fffbeb'}
            stroke="#d97706"
            strokeWidth="2.5"
            filter="url(#ls-shadow)"
          />
          <text
            x="330"
            y="222"
            textAnchor="middle"
            fill="#92400e"
            fontSize="12"
            fontWeight="700"
          >
            Boundary Check:
          </text>
          <text
            x="330"
            y="240"
            textAnchor="middle"
            fill="#92400e"
            fontSize="13"
            fontWeight="700"
            fontFamily="var(--font-mono, monospace)"
          >
            i &lt; len(arr) ?
          </text>
        </g>

        {/* FLOW: Decision 1 -> NO branch (Array exhausted -> Element not found -> return -1) */}
        <path
          d="M 460 225 L 560 225 L 560 480 L 446 480"
          fill="none"
          stroke="#dc2626"
          strokeWidth="2"
          markerEnd="url(#ls-arrow-no)"
        />
        <rect x="475" y="210" width="34" height="18" rx="4" fill="#fee2e2" stroke="#ef4444" strokeWidth="1" />
        <text x="492" y="223" textAnchor="middle" fill="#991b1b" fontSize="10" fontWeight="700">
          NO
        </text>

        {/* FLOW: Decision 1 -> YES branch (Within bounds -> check arr[i] == target) */}
        <line
          x1="330"
          y1="270"
          x2="330"
          y2="306"
          stroke="#16a34a"
          strokeWidth="2"
          markerEnd="url(#ls-arrow-yes)"
        />
        <rect x="338" y="278" width="38" height="18" rx="4" fill="#dcfce7" stroke="#22c55e" strokeWidth="1" />
        <text x="357" y="291" textAnchor="middle" fill="#166534" fontSize="10" fontWeight="700">
          YES
        </text>

        {/* 4. TARGET COMPARISON (Diamond 2) */}
        <g
          onMouseEnter={() => setHoveredNode('target_check')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <polygon
            points="330,308 450,352 330,396 210,352"
            fill={hoveredNode === 'target_check' ? '#fef3c7' : '#fffbeb'}
            stroke="#d97706"
            strokeWidth="2.5"
            filter="url(#ls-shadow)"
          />
          <text
            x="330"
            y="350"
            textAnchor="middle"
            fill="#92400e"
            fontSize="12"
            fontWeight="700"
            fontFamily="var(--font-mono, monospace)"
          >
            arr[i] == target ?
          </text>
        </g>

        {/* Diamond 2 -> YES branch (Element found -> Return index i) */}
        <path
          d="M 450 352 L 500 352 L 500 388"
          fill="none"
          stroke="#16a34a"
          strokeWidth="2"
          markerEnd="url(#ls-arrow-yes)"
        />
        <rect x="456" y="338" width="36" height="18" rx="4" fill="#dcfce7" stroke="#22c55e" strokeWidth="1" />
        <text x="474" y="351" textAnchor="middle" fill="#166534" fontSize="10" fontWeight="700">
          YES
        </text>

        {/* Process: Found target at index i */}
        <g
          onMouseEnter={() => setHoveredNode('found')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <rect
            x="430"
            y="390"
            width="140"
            height="42"
            rx="4"
            fill={hoveredNode === 'found' ? '#dcfce7' : '#f0fdf4'}
            stroke="#16a34a"
            strokeWidth="2"
            filter="url(#ls-shadow)"
          />
          <text
            x="500"
            y="408"
            textAnchor="middle"
            fill="#15803d"
            fontSize="11"
            fontWeight="700"
          >
            Match Found!
          </text>
          <text
            x="500"
            y="424"
            textAnchor="middle"
            fill="#166534"
            fontSize="11"
            fontFamily="var(--font-mono, monospace)"
            fontWeight="700"
          >
            return index i
          </text>
        </g>

        {/* Route Found target down to End */}
        <path
          d="M 500 432 L 500 560 L 396 560"
          fill="none"
          stroke="#16a34a"
          strokeWidth="1.5"
          markerEnd="url(#ls-arrow-std)"
        />

        {/* Diamond 2 -> NO branch (Mismatch -> Increment pointer i = i + 1) */}
        <line
          x1="330"
          y1="396"
          x2="330"
          y2="430"
          stroke="#dc2626"
          strokeWidth="2"
          markerEnd="url(#ls-arrow-no)"
        />
        <rect x="338" y="402" width="34" height="18" rx="4" fill="#fee2e2" stroke="#ef4444" strokeWidth="1" />
        <text x="355" y="415" textAnchor="middle" fill="#991b1b" fontSize="10" fontWeight="700">
          NO
        </text>

        {/* 5. INCREMENT (Process Rectangle: i = i + 1) */}
        <g
          onMouseEnter={() => setHoveredNode('increment')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <rect
            x="240"
            y="432"
            width="180"
            height="44"
            rx="4"
            fill={hoveredNode === 'increment' ? '#eff6ff' : '#ffffff'}
            stroke="#2563eb"
            strokeWidth="2"
            filter="url(#ls-shadow)"
          />
          <text
            x="330"
            y="450"
            textAnchor="middle"
            fill="#1e40af"
            fontSize="11"
            fontWeight="700"
          >
            Advance Pointer
          </text>
          <text
            x="330"
            y="467"
            textAnchor="middle"
            fill="#1e40af"
            fontSize="12"
            fontFamily="var(--font-mono, monospace)"
            fontWeight="700"
          >
            i = i + 1
          </text>
        </g>

        {/* 6. LOOPBACK ARROW: from i = i + 1 back to Decision 1 */}
        <path
          d="M 240 454 L 80 454 L 80 225 L 196 225"
          fill="none"
          stroke="#2563eb"
          strokeWidth="2.5"
          markerEnd="url(#ls-arrow-loop)"
        />
        <rect x="52" y="325" width="56" height="24" rx="4" fill="#dbeafe" stroke="#3b82f6" strokeWidth="1" />
        <text
          x="80"
          y="341"
          textAnchor="middle"
          fill="#1d4ed8"
          fontSize="10"
          fontWeight="700"
        >
          ↺ Loop
        </text>

        {/* 7. NOT FOUND RESULT BOX (From Decision 1 NO branch) */}
        <g
          onMouseEnter={() => setHoveredNode('not_found')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <rect
            x="230"
            y="498"
            width="200"
            height="42"
            rx="4"
            fill={hoveredNode === 'not_found' ? '#fee2e2' : '#fef2f2'}
            stroke="#ef4444"
            strokeWidth="1.5"
            filter="url(#ls-shadow)"
          />
          <text
            x="330"
            y="516"
            textAnchor="middle"
            fill="#b91c1c"
            fontSize="11"
            fontWeight="700"
          >
            End of Array (Not Found)
          </text>
          <text
            x="330"
            y="532"
            textAnchor="middle"
            fill="#991b1b"
            fontSize="11"
            fontFamily="var(--font-mono, monospace)"
            fontWeight="700"
          >
            return -1
          </text>
        </g>

        {/* Flow: Not Found -> End */}
        <line
          x1="330"
          y1="540"
          x2="330"
          y2="570"
          stroke="#475569"
          strokeWidth="2"
          markerEnd="url(#ls-arrow-std)"
        />

        {/* 8. END TERMINAL (Oval) */}
        <g
          onMouseEnter={() => setHoveredNode('end')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <rect
            x="260"
            y="572"
            width="140"
            height="38"
            rx="19"
            ry="19"
            fill={hoveredNode === 'end' ? '#e2e8f0' : '#f1f5f9'}
            stroke="#475569"
            strokeWidth="2.5"
            filter="url(#ls-shadow)"
          />
          <text
            x="330"
            y="596"
            textAnchor="middle"
            fill="#1e293b"
            fontSize="14"
            fontWeight="700"
            letterSpacing="0.03em"
          >
            End
          </text>
        </g>
      </svg>
    </div>
  );
}

/**
 * ISO Standard Flowchart SVG for Calculator Routine
 */
function CalculatorSvgDiagram({ hoveredNode, setHoveredNode }) {
  return (
    <div style={{ width: '100%', overflowX: 'auto', display: 'flex', justifyContent: 'center' }}>
      <svg
        viewBox="0 0 660 580"
        style={{
          width: '100%',
          maxWidth: '660px',
          height: 'auto',
          display: 'block',
          fontFamily: 'var(--font-sans, system-ui, -apple-system, sans-serif)',
        }}
      >
        <defs>
          <marker id="calc-arrow-std" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#334155" />
          </marker>
          <marker id="calc-arrow-yes" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#dc2626" />
          </marker>
          <marker id="calc-arrow-no" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#16a34a" />
          </marker>
          <filter id="calc-shadow" x="-8%" y="-8%" width="116%" height="116%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#0f172a" floodOpacity="0.08" />
          </filter>
        </defs>

        {/* Start Oval */}
        <rect x="270" y="18" width="120" height="38" rx="19" fill="#ecfdf5" stroke="#059669" strokeWidth="2.5" filter="url(#calc-shadow)" />
        <text x="330" y="42" textAnchor="middle" fill="#065f46" fontSize="14" fontWeight="700">Start</text>
        <line x1="330" y1="56" x2="330" y2="88" stroke="#475569" strokeWidth="2" markerEnd="url(#calc-arrow-std)" />

        {/* Input Parallelogram */}
        <polygon points="210,140 470,140 450,90 190,90" fill="#eff6ff" stroke="#3b82f6" strokeWidth="2" filter="url(#calc-shadow)" />
        <text x="330" y="112" textAnchor="middle" fill="#1e40af" fontSize="12" fontWeight="700">Input / Read</text>
        <text x="330" y="129" textAnchor="middle" fill="#334155" fontSize="11" fontFamily="var(--font-mono, monospace)">num1, op (+, -, *, /), num2</text>
        <line x1="330" y1="140" x2="330" y2="174" stroke="#475569" strokeWidth="2" markerEnd="url(#calc-arrow-std)" />

        {/* Decision Diamond: Division by zero */}
        <polygon points="330,176 460,222 330,268 200,222" fill="#fffbeb" stroke="#d97706" strokeWidth="2" filter="url(#calc-shadow)" />
        <text x="330" y="217" textAnchor="middle" fill="#92400e" fontSize="12" fontWeight="700">op == '/' &amp;&amp;</text>
        <text x="330" y="235" textAnchor="middle" fill="#92400e" fontSize="12" fontWeight="700" fontFamily="var(--font-mono, monospace)">num2 == 0 ?</text>

        {/* YES Branch -> Error */}
        <path d="M 460 222 L 530 222 L 530 270" fill="none" stroke="#dc2626" strokeWidth="2" markerEnd="url(#calc-arrow-yes)" />
        <text x="485" y="215" fill="#dc2626" fontSize="10" fontWeight="700">YES</text>
        <polygon points="460,314 590,314 575,272 445,272" fill="#fef2f2" stroke="#ef4444" strokeWidth="1.5" />
        <text x="518" y="291" textAnchor="middle" fill="#b91c1c" fontSize="11" fontWeight="700">Output Error</text>
        <text x="518" y="306" textAnchor="middle" fill="#991b1b" fontSize="10">"Cannot divide by 0"</text>

        {/* Route error to End */}
        <path d="M 518 314 L 518 510 L 396 510" fill="none" stroke="#dc2626" strokeWidth="1.5" markerEnd="url(#calc-arrow-std)" />

        {/* NO Branch -> Calculate */}
        <line x1="330" y1="268" x2="330" y2="304" stroke="#16a34a" strokeWidth="2" markerEnd="url(#calc-arrow-no)" />
        <text x="340" y="286" fill="#16a34a" fontSize="10" fontWeight="700">NO</text>

        {/* Process: Compute */}
        <rect x="200" y="306" width="260" height="50" rx="4" fill="#ffffff" stroke="#2563eb" strokeWidth="2" filter="url(#calc-shadow)" />
        <text x="330" y="326" textAnchor="middle" fill="#1e40af" fontSize="12" fontWeight="700">Execute Arithmetic Operation</text>
        <text x="330" y="344" textAnchor="middle" fill="#334155" fontSize="11" fontFamily="var(--font-mono, monospace)">result = evaluate(num1, op, num2)</text>
        <line x1="330" y1="356" x2="330" y2="390" stroke="#475569" strokeWidth="2" markerEnd="url(#calc-arrow-std)" />

        {/* Output Parallelogram */}
        <polygon points="220,444 460,444 440,392 200,392" fill="#eff6ff" stroke="#3b82f6" strokeWidth="2" filter="url(#calc-shadow)" />
        <text x="330" y="415" textAnchor="middle" fill="#1e40af" fontSize="12" fontWeight="700">Output / Display</text>
        <text x="330" y="432" textAnchor="middle" fill="#334155" fontSize="11" fontFamily="var(--font-mono, monospace)">print(f"Result: &#123;result&#125;")</text>
        <line x1="330" y1="444" x2="330" y2="488" stroke="#475569" strokeWidth="2" markerEnd="url(#calc-arrow-std)" />

        {/* End Oval */}
        <rect x="270" y="490" width="120" height="38" rx="19" fill="#f1f5f9" stroke="#475569" strokeWidth="2.5" filter="url(#calc-shadow)" />
        <text x="330" y="514" textAnchor="middle" fill="#1e293b" fontSize="14" fontWeight="700">End</text>
      </svg>
    </div>
  );
}

/**
 * Dynamic Flowchart Parser: Extracts sequential nodes from ASCII boxes, arrows, or lines
 */
function parseFlowchartSteps(flowchartText) {
  if (!flowchartText || typeof flowchartText !== 'string') return [];

  const lines = flowchartText.split('\n');
  const boxMatches = [];

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('|') && trimmed.endsWith('|') && !trimmed.includes('+---')) {
      const content = trimmed.replace(/^\|/, '').replace(/\|$/, '').trim();
      if (content && !/^[-+=_|]+$/.test(content)) {
        boxMatches.push(content);
      }
    }
  }

  if (boxMatches.length >= 2) {
    return boxMatches.map((step, idx) => ({
      id: `step_${idx}`,
      type: idx === 0 ? 'terminal' : idx === boxMatches.length - 1 ? 'terminal' : /decision|\?|if\b/i.test(step) ? 'decision' : 'process',
      title: step,
      subtitle: idx === 0 ? 'Start' : idx === boxMatches.length - 1 ? 'End' : `Step ${idx}`,
      accent: idx === 0 ? 'emerald' : idx === boxMatches.length - 1 ? 'slate' : 'blue',
    }));
  }

  // Check arrow separated: "A -> B -> C"
  if (flowchartText.includes('->') || flowchartText.includes('-->') || flowchartText.includes('↓')) {
    const parts = flowchartText
      .split(/->|-->|↓|\n/)
      .map((s) => s.trim().replace(/^\[|\]$/g, '').replace(/^\(|\)$/g, ''))
      .filter((s) => s && !/^[-+=_v|]+$/.test(s));
    if (parts.length >= 2) {
      return parts.map((step, idx) => ({
        id: `step_${idx}`,
        type: idx === 0 ? 'terminal' : idx === parts.length - 1 ? 'terminal' : /decision|\?|if\b/i.test(step) ? 'decision' : 'process',
        title: step,
        subtitle: idx === 0 ? 'Start' : idx === parts.length - 1 ? 'End' : `Step ${idx}`,
        accent: idx === 0 ? 'emerald' : idx === parts.length - 1 ? 'slate' : 'blue',
      }));
    }
  }

  return [];
}

/**
 * ISO Standard Generic Flowchart SVG
 * Dynamically renders parsed steps or provided nodes in an intuitive directed flow
 */
function GenericFlowchartSvgDiagram({ nodes, hoveredNode, setHoveredNode }) {
  const displayNodes = nodes && nodes.length > 0 ? nodes : [
    { id: 'start', type: 'terminal', title: 'Start' },
    { id: 'proc', type: 'process', title: 'Process Logic' },
    { id: 'end', type: 'terminal', title: 'End' },
  ];

  const nodeHeight = 44;
  const gap = 34;
  const startY = 24;
  const totalHeight = Math.max(260, startY * 2 + displayNodes.length * (nodeHeight + gap) - gap);

  return (
    <div style={{ width: '100%', overflowX: 'auto', display: 'flex', justifyContent: 'center' }}>
      <svg
        viewBox={`0 0 660 ${totalHeight}`}
        style={{
          width: '100%',
          maxWidth: '660px',
          height: 'auto',
          display: 'block',
          fontFamily: 'var(--font-sans, system-ui, -apple-system, sans-serif)',
        }}
      >
        <defs>
          <marker id="gen-arrow-std" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#334155" />
          </marker>
          <filter id="gen-shadow" x="-8%" y="-8%" width="116%" height="116%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#0f172a" floodOpacity="0.08" />
          </filter>
        </defs>

        {displayNodes.map((node, index) => {
          const y = startY + index * (nodeHeight + gap);
          const isHovered = hoveredNode === node.id;
          const isStart = index === 0;
          const isEnd = index === displayNodes.length - 1;
          const isTerminal = node.type === 'terminal' || isStart || isEnd;
          const isDecision = node.type === 'decision';

          const textLabel = node.title || node.name || `Step ${index + 1}`;
          const truncatedLabel = textLabel.length > 42 ? textLabel.slice(0, 39) + '...' : textLabel;

          return (
            <g
              key={node.id || index}
              onMouseEnter={() => setHoveredNode(node.id)}
              onMouseLeave={() => setHoveredNode(null)}
              style={{ cursor: 'pointer' }}
            >
              {/* Connector line to next node */}
              {index < displayNodes.length - 1 && (
                <line
                  x1="330"
                  y1={y + nodeHeight}
                  x2="330"
                  y2={y + nodeHeight + gap}
                  stroke="#475569"
                  strokeWidth="2"
                  markerEnd="url(#gen-arrow-std)"
                />
              )}

              {/* Node Shape */}
              {isTerminal ? (
                <rect
                  x="230"
                  y={y}
                  width="200"
                  height={nodeHeight}
                  rx="22"
                  fill={isStart ? (isHovered ? '#d1fae5' : '#ecfdf5') : (isHovered ? '#e2e8f0' : '#f1f5f9')}
                  stroke={isStart ? '#059669' : '#475569'}
                  strokeWidth="2.5"
                  filter="url(#gen-shadow)"
                />
              ) : isDecision ? (
                <polygon
                  points={`330,${y} 480,${y + nodeHeight / 2} 330,${y + nodeHeight} 180,${y + nodeHeight / 2}`}
                  fill={isHovered ? '#fef3c7' : '#fffbeb'}
                  stroke="#d97706"
                  strokeWidth="2"
                  filter="url(#gen-shadow)"
                />
              ) : (
                <rect
                  x="180"
                  y={y}
                  width="300"
                  height={nodeHeight}
                  rx="6"
                  fill={isHovered ? '#eff6ff' : '#ffffff'}
                  stroke="#2563eb"
                  strokeWidth="2"
                  filter="url(#gen-shadow)"
                />
              )}

              {/* Node Text */}
              <text
                x="330"
                y={y + nodeHeight / 2 + 5}
                textAnchor="middle"
                fill={isTerminal ? (isStart ? '#065f46' : '#1e293b') : isDecision ? '#92400e' : '#1e40af'}
                fontSize={isTerminal ? '13' : '12'}
                fontWeight="700"
              >
                {truncatedLabel}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

/**
 * Main VisualFlowchart Component
 */
export default function VisualFlowchart({ flowchart, flowchartNodes }) {
  // 'diagram' (Standard Vector Flowchart) | 'steps' (Step Cards) | 'text' (ASCII Trace)
  const [activeTab, setActiveTab] = useState('diagram');
  const [hoveredNode, setHoveredNode] = useState(null);

  // Binary search flowchart nodes for the Step Cards view
  const defaultBinarySearchNodes = [
    {
      id: 'start',
      type: 'terminal',
      title: 'Start',
      subtitle: 'Binary search algorithm begins (requires sorted array)',
      accent: 'emerald',
    },
    {
      id: 'init',
      type: 'process',
      title: '1. Initialize Pointers',
      subtitle: 'Set search space boundaries and compute pivot midpoint',
      code: 'low = 0 ; high = len(arr) - 1 ; mid = (low + high) // 2',
      accent: 'blue',
    },
    {
      id: 'loop_cond',
      type: 'decision',
      title: '2. Loop Condition: Range & Target Check',
      condition: 'low <= high && arr[mid] != target ?',
      accent: 'amber',
      branchYes: {
        label: 'YES (Continue Search)',
        action: 'Divide Interval in Half',
        detail: 'Proceed to target comparison to discard left or right partition',
        outcomeType: 'success',
      },
      branchNo: {
        label: 'NO (Exit Loop)',
        action: 'Inspect Exit Status',
        detail: 'Either element found at index mid, or search interval exhausted (return -1)',
        outcomeType: 'neutral',
      },
    },
    {
      id: 'target_check',
      type: 'decision',
      title: '3. Partition Check',
      condition: 'target < arr[mid] ?',
      accent: 'indigo',
      branchYes: {
        label: 'YES (Target in Left Half)',
        action: 'Update Upper Bound',
        detail: 'Discard right half: high = mid - 1',
        outcomeType: 'neutral',
      },
      branchNo: {
        label: 'NO (Target in Right Half)',
        action: 'Update Lower Bound',
        detail: 'Discard left half: low = mid + 1',
        outcomeType: 'neutral',
      },
    },
    {
      id: 'recalc',
      type: 'process',
      title: '4. Recalculate Midpoint',
      subtitle: 'Compute new middle index for the updated boundaries',
      code: 'mid = (low + high) // 2',
      accent: 'blue',
    },
    {
      id: 'end',
      type: 'terminal',
      title: 'End / Outcome',
      subtitle: 'Return found index (e.g. 3) or -1 if not found',
      accent: 'slate',
    },
  ];

  // Linear search flowchart nodes for the Step Cards view
  const defaultLinearSearchNodes = [
    {
      id: 'start',
      type: 'terminal',
      title: 'Start',
      subtitle: 'Linear search algorithm begins (sequential scan)',
      accent: 'emerald',
    },
    {
      id: 'init',
      type: 'process',
      title: '1. Initialize Index Pointer',
      subtitle: 'Set pointer to scan from the first element',
      code: 'i = 0',
      accent: 'blue',
    },
    {
      id: 'loop_cond',
      type: 'decision',
      title: '2. Loop Condition: Boundary Check',
      condition: 'i < len(arr) ?',
      accent: 'amber',
      branchYes: {
        label: 'YES (Within Bounds)',
        action: 'Inspect Current Element',
        detail: 'Proceed to compare arr[i] with target',
        outcomeType: 'success',
      },
      branchNo: {
        label: 'NO (End of Array)',
        action: 'Target Not Found',
        detail: 'All elements scanned without match; return -1',
        outcomeType: 'error',
      },
    },
    {
      id: 'target_check',
      type: 'decision',
      title: '3. Target Comparison',
      condition: 'arr[i] == target ?',
      accent: 'indigo',
      branchYes: {
        label: 'YES (Match Found)',
        action: 'Return Found Index',
        detail: 'Target matches arr[i]; return current index i',
        outcomeType: 'success',
      },
      branchNo: {
        label: 'NO (Mismatch)',
        action: 'Advance to Next Item',
        detail: 'arr[i] != target; increment pointer i = i + 1',
        outcomeType: 'neutral',
      },
    },
    {
      id: 'increment',
      type: 'process',
      title: '4. Increment Index Pointer',
      subtitle: 'Advance index to check next element in the collection',
      code: 'i = i + 1',
      accent: 'blue',
    },
    {
      id: 'end',
      type: 'terminal',
      title: 'End / Outcome',
      subtitle: 'Return found index i (e.g. 2) or -1 (not found)',
      accent: 'slate',
    },
  ];

  const defaultCalculatorNodes = [
    {
      id: 'start',
      type: 'terminal',
      title: 'Start',
      subtitle: 'Calculator routine initiates',
      accent: 'emerald',
    },
    {
      id: 'input',
      type: 'process',
      title: '1. Read User Inputs',
      subtitle: 'Prompt first operand (num1), operator (+, -, *, /), and second operand (num2)',
      code: 'num1 = float(...) ; op = input(...) ; num2 = float(...)',
      accent: 'blue',
    },
    {
      id: 'decision',
      type: 'decision',
      title: 'Decision: Division by Zero Check',
      condition: "Is op == '/' and num2 == 0 ?",
      accent: 'amber',
      branchYes: {
        label: 'YES (Invalid Input)',
        action: 'Raise ZeroDivisionError',
        detail: 'Display error: "Cannot divide by zero"',
        outcomeType: 'error',
      },
      branchNo: {
        label: 'NO (Valid Arithmetic)',
        action: 'Dispatch Calculation Routine',
        detail: 'Invoke corresponding function: add, subtract, multiply, or divide',
        outcomeType: 'success',
      },
    },
    {
      id: 'output',
      type: 'process',
      title: '2. Return & Display Output',
      subtitle: 'Format calculated numeric result and stream to output',
      code: 'print(f"Result: {result}")',
      accent: 'blue',
    },
    {
      id: 'end',
      type: 'terminal',
      title: 'End',
      subtitle: 'Program terminates gracefully',
      accent: 'slate',
    },
  ];

  const isLinearSearch = Boolean(
    (flowchart && /linear\s*search|arr\[i\]|i\s*<\s*len/i.test(flowchart)) ||
    (flowchartNodes && flowchartNodes.some(n => /linear|arr\[i\]|i\s*=\s*0|i\s*<\s*len/i.test(n.title || n.subtitle || n.code || n.condition || '')))
  );

  const isCalculator = Boolean(
    !isLinearSearch &&
    flowchart &&
    (/\b(calculator|arithmetic\s*operation|divide\s*by\s*zero|zero\s*division)\b/i.test(flowchart) ||
     (flowchart.includes('num1') && flowchart.includes('num2')) ||
     (flowchart.toLowerCase().includes('operator') && (flowchart.toLowerCase().includes('operand') || flowchart.toLowerCase().includes('divide'))))
  );

  const isBinarySearch = Boolean(
    !isLinearSearch &&
    !isCalculator &&
    ((flowchart && /binary\s*search|arr\[mid\]|mid\s*=|low\s*<=?\s*high/i.test(flowchart)) ||
     (flowchartNodes && flowchartNodes.some(n => /binary|mid\s*=|arr\[mid\]|low\s*<=?\s*high/i.test(n.title || n.subtitle || n.code || n.condition || ''))))
  );

  const parsedGenericNodes = parseFlowchartSteps(flowchart);

  const defaultGenericNodes = [
    {
      id: 'start',
      type: 'terminal',
      title: 'Start',
      subtitle: 'Execution begins',
      accent: 'emerald',
    },
    {
      id: 'step_1',
      type: 'process',
      title: '1. Execute Logic',
      subtitle: 'Run core instructions and routines',
      accent: 'blue',
    },
    {
      id: 'end',
      type: 'terminal',
      title: 'End',
      subtitle: 'Execution finishes',
      accent: 'slate',
    },
  ];

  const nodes =
    flowchartNodes && flowchartNodes.length > 0
      ? flowchartNodes
      : isLinearSearch
      ? defaultLinearSearchNodes
      : isCalculator
      ? defaultCalculatorNodes
      : isBinarySearch
      ? defaultBinarySearchNodes
      : parsedGenericNodes && parsedGenericNodes.length > 0
      ? parsedGenericNodes
      : defaultGenericNodes;

  const getNodeIcon = (node) => {
    if (node.icon && typeof node.icon === 'function') return node.icon;
    if (node.type === 'terminal') {
      return node.id === 'start' ? Play : CheckCircle2;
    }
    if (node.type === 'decision') return GitBranch;
    if (node.code) return Terminal;
    return Layers;
  };

  const getBranchTheme = (branch) => {
    const outcome = branch?.outcomeType || 'neutral';
    if (outcome === 'error') {
      return {
        bg: '#fef2f2',
        border: '#ef4444',
        text: '#b91c1c',
        badgeBg: '#fee2e2',
        badgeText: '#991b1b',
        badgeLabel: 'Branch Exit',
        Icon: AlertTriangle,
      };
    }
    if (outcome === 'success') {
      return {
        bg: '#f0fdf4',
        border: '#22c55e',
        text: '#15803d',
        badgeBg: '#dcfce7',
        badgeText: '#166534',
        badgeLabel: 'Valid / Found',
        Icon: CheckCircle2,
      };
    }
    return {
      bg: '#eff6ff',
      border: '#3b82f6',
      text: '#1d4ed8',
      badgeBg: '#dbeafe',
      badgeText: '#1e40af',
      badgeLabel: 'Next Step',
      Icon: CornerDownRight,
    };
  };

  // Support legacy tab naming
  const effectiveTab = activeTab === 'visual' ? 'diagram' : activeTab;

  return (
    <div
      style={{
        backgroundColor: 'var(--bg-surface)',
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-lg)',
        overflow: 'hidden',
        boxShadow: '0 2px 8px rgba(15, 23, 42, 0.05)',
      }}
    >
      {/* Header with View Tabs */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '8px',
          padding: '10px 14px',
          backgroundColor: 'var(--bg-subtle)',
          borderBottom: '1px solid var(--border-color)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div
            style={{
              width: '22px',
              height: '22px',
              borderRadius: 'var(--radius-xs)',
              backgroundColor: 'var(--accent-subtle)',
              color: 'var(--accent-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <GitBranch size={14} />
          </div>
          <span style={{ fontSize: 'var(--text-sm)', fontWeight: 600, color: 'var(--text-primary)' }}>
            Algorithm Flowchart
          </span>
          <span
            style={{
              fontSize: '0.68rem',
              backgroundColor: '#ecfdf5',
              color: '#065f46',
              border: '1px solid #a7f3d0',
              fontWeight: 600,
              padding: '1px 6px',
              borderRadius: 'var(--radius-xs)',
            }}
          >
            ISO Standard
          </span>
        </div>

        {/* Tab switchers */}
        <div
          style={{
            display: 'flex',
            backgroundColor: 'var(--bg-surface)',
            borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--border-color)',
            padding: '2px',
            gap: '2px',
          }}
        >
          <button
            type="button"
            onClick={() => setActiveTab('diagram')}
            style={{
              padding: '4px 10px',
              fontSize: 'var(--text-xs)',
              fontWeight: effectiveTab === 'diagram' ? 600 : 500,
              color: effectiveTab === 'diagram' ? 'var(--accent-primary)' : 'var(--text-secondary)',
              backgroundColor: effectiveTab === 'diagram' ? 'var(--accent-subtle)' : 'transparent',
              borderRadius: 'var(--radius-xs)',
              cursor: 'pointer',
              border: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
            }}
          >
            <span>📐</span> Standard Flowchart
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('steps')}
            style={{
              padding: '4px 10px',
              fontSize: 'var(--text-xs)',
              fontWeight: effectiveTab === 'steps' ? 600 : 500,
              color: effectiveTab === 'steps' ? 'var(--accent-primary)' : 'var(--text-secondary)',
              backgroundColor: effectiveTab === 'steps' ? 'var(--accent-subtle)' : 'transparent',
              borderRadius: 'var(--radius-xs)',
              cursor: 'pointer',
              border: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
            }}
          >
            <span>📑</span> Step Cards
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('text')}
            style={{
              padding: '4px 10px',
              fontSize: 'var(--text-xs)',
              fontWeight: effectiveTab === 'text' ? 600 : 500,
              color: effectiveTab === 'text' ? 'var(--accent-primary)' : 'var(--text-secondary)',
              backgroundColor: effectiveTab === 'text' ? 'var(--accent-subtle)' : 'transparent',
              borderRadius: 'var(--radius-xs)',
              cursor: 'pointer',
              border: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
            }}
          >
            <span>📋</span> Text / ASCII
          </button>
        </div>
      </div>

      {/* Main Flowchart Content Area */}
      <div style={{ padding: '20px 16px', backgroundColor: '#fcfdfe' }}>
        {/* 1. STANDARD FLOWCHART SVG DIAGRAM (Default) */}
        {effectiveTab === 'diagram' && (
          <div>
            {isLinearSearch ? (
              <LinearSearchSvgDiagram
                hoveredNode={hoveredNode}
                setHoveredNode={setHoveredNode}
              />
            ) : isCalculator ? (
              <CalculatorSvgDiagram
                hoveredNode={hoveredNode}
                setHoveredNode={setHoveredNode}
              />
            ) : isBinarySearch ? (
              <BinarySearchSvgDiagram
                hoveredNode={hoveredNode}
                setHoveredNode={setHoveredNode}
              />
            ) : (
              <GenericFlowchartSvgDiagram
                nodes={nodes}
                hoveredNode={hoveredNode}
                setHoveredNode={setHoveredNode}
              />
            )}

            {/* Standard Flowchart ISO Legend Bar */}
            <div
              style={{
                marginTop: '18px',
                padding: '10px 14px',
                backgroundColor: '#f8fafc',
                border: '1px solid #e2e8f0',
                borderRadius: 'var(--radius-md)',
                display: 'flex',
                flexWrap: 'wrap',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '16px',
                fontSize: '0.72rem',
                color: '#475569',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 600 }}>
                <span
                  style={{
                    display: 'inline-block',
                    width: '26px',
                    height: '14px',
                    borderRadius: '7px',
                    backgroundColor: '#ecfdf5',
                    border: '1.5px solid #059669',
                  }}
                />
                <span>Oval: Start / End (Terminal)</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 600 }}>
                <span
                  style={{
                    display: 'inline-block',
                    width: '20px',
                    height: '14px',
                    backgroundColor: '#ffffff',
                    border: '1.5px solid #2563eb',
                    borderRadius: '2px',
                  }}
                />
                <span>Rectangle: Process / Arithmetic Action</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 600 }}>
                <span
                  style={{
                    display: 'inline-block',
                    width: '14px',
                    height: '14px',
                    backgroundColor: '#fffbeb',
                    border: '1.5px solid #d97706',
                    transform: 'rotate(45deg)',
                    margin: '0 4px',
                  }}
                />
                <span>Diamond: Decision (Branching)</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 600 }}>
                <span
                  style={{
                    display: 'inline-block',
                    width: '20px',
                    height: '14px',
                    backgroundColor: '#eff6ff',
                    border: '1.5px solid #3b82f6',
                    transform: 'skewX(-15deg)',
                  }}
                />
                <span>Parallelogram: Input / Output</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 600 }}>
                <span
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: '#2563eb',
                    fontWeight: 700,
                  }}
                >
                  <RotateCcw size={13} />
                </span>
                <span>Loopback Arrow: While-Loop Cycle</span>
              </div>
            </div>
          </div>
        )}

        {/* 2. STEP CARDS VIEW */}
        {effectiveTab === 'steps' && (
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              width: '100%',
              maxWidth: '680px',
              margin: '0 auto',
            }}
          >
            {nodes.map((node, index) => {
              const isDecision = node.type === 'decision';
              const isTerminal = node.type === 'terminal';
              const Icon = getNodeIcon(node);
              const branchYesTheme = isDecision && node.branchYes ? getBranchTheme(node.branchYes) : null;
              const branchNoTheme = isDecision && node.branchNo ? getBranchTheme(node.branchNo) : null;
              const BranchYesIcon = branchYesTheme?.Icon || AlertTriangle;
              const BranchNoIcon = branchNoTheme?.Icon || CheckCircle2;

              return (
                <React.Fragment key={node.id}>
                  {index > 0 && (
                    <div
                      style={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        margin: '2px 0',
                        color: '#94a3b8',
                      }}
                    >
                      <div
                        style={{
                          width: '2px',
                          height: '20px',
                          backgroundColor: '#cbd5e1',
                        }}
                      />
                      <svg width="12" height="8" viewBox="0 0 12 8" fill="none">
                        <path d="M6 8L0.803848 0.5L11.1962 0.5L6 8Z" fill="#94a3b8" />
                      </svg>
                    </div>
                  )}

                  {/* Terminal Node */}
                  {isTerminal && (
                    <div
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '8px 24px',
                        borderRadius: '9999px',
                        backgroundColor:
                          node.accent === 'emerald' ? '#ecfdf5' : '#f1f5f9',
                        border: `2px solid ${
                          node.accent === 'emerald' ? '#10b981' : '#64748b'
                        }`,
                        color:
                          node.accent === 'emerald' ? '#047857' : '#334155',
                        fontWeight: 700,
                        fontSize: 'var(--text-sm)',
                        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.04)',
                      }}
                    >
                      {Icon && <Icon size={14} strokeWidth={2.5} />}
                      <span>{node.title}</span>
                      <span
                        style={{
                          fontSize: '0.72rem',
                          fontWeight: 500,
                          opacity: 0.8,
                          marginLeft: '4px',
                        }}
                      >
                        ({node.subtitle})
                      </span>
                    </div>
                  )}

                  {/* Process Node */}
                  {!isTerminal && !isDecision && (
                    <div
                      onMouseEnter={() => setHoveredNode(node.id)}
                      onMouseLeave={() => setHoveredNode(null)}
                      style={{
                        width: '100%',
                        maxWidth: '480px',
                        backgroundColor: '#ffffff',
                        border: '1.5px solid #3b82f6',
                        borderRadius: 'var(--radius-md)',
                        padding: '12px 16px',
                        boxShadow:
                          hoveredNode === node.id
                            ? '0 6px 16px rgba(59, 130, 246, 0.15)'
                            : '0 2px 6px rgba(15, 23, 42, 0.05)',
                        transform:
                          hoveredNode === node.id
                            ? 'translateY(-1px)'
                            : 'translateY(0)',
                        transition: 'all 150ms ease',
                      }}
                    >
                      <div
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          marginBottom: '4px',
                        }}
                      >
                        <div
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '6px',
                            fontWeight: 700,
                            fontSize: 'var(--text-sm)',
                            color: '#1e40af',
                          }}
                        >
                          {Icon && <Icon size={14} />}
                          <span>{node.title}</span>
                        </div>
                        <span
                          style={{
                            fontSize: '0.65rem',
                            backgroundColor: '#eff6ff',
                            color: '#2563eb',
                            padding: '1px 6px',
                            borderRadius: 'var(--radius-xs)',
                            fontWeight: 600,
                          }}
                        >
                          Process Step
                        </span>
                      </div>

                      <p
                        style={{
                          fontSize: 'var(--text-xs)',
                          color: 'var(--text-secondary)',
                          lineHeight: '1.45',
                          margin: '4px 0',
                        }}
                      >
                        {node.subtitle}
                      </p>

                      {node.code && (
                        <div
                          style={{
                            marginTop: '6px',
                            padding: '4px 8px',
                            backgroundColor: '#f8fafc',
                            border: '1px solid #e2e8f0',
                            borderRadius: 'var(--radius-xs)',
                            fontFamily: 'var(--font-mono)',
                            fontSize: '0.72rem',
                            color: '#0f172a',
                          }}
                        >
                          {node.code}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Decision Node */}
                  {isDecision && (
                    <div
                      style={{
                        width: '100%',
                        maxWidth: '560px',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        position: 'relative',
                      }}
                    >
                      <div
                        style={{
                          width: '100%',
                          maxWidth: '460px',
                          backgroundColor: '#fffbeb',
                          border: '2px solid #f59e0b',
                          borderRadius: 'var(--radius-md)',
                          padding: '12px 16px',
                          boxShadow: '0 4px 12px rgba(245, 158, 11, 0.12)',
                          textAlign: 'center',
                        }}
                      >
                        <div
                          style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '6px',
                            fontSize: 'var(--text-xs)',
                            fontWeight: 700,
                            color: '#b45309',
                            textTransform: 'uppercase',
                            letterSpacing: '0.05em',
                            marginBottom: '4px',
                          }}
                        >
                          <GitBranch size={13} />
                          <span>Conditional Branch</span>
                        </div>
                        <div
                          style={{
                            fontFamily: 'var(--font-mono)',
                            fontSize: 'var(--text-sm)',
                            fontWeight: 700,
                            color: '#92400e',
                          }}
                        >
                          {node.condition}
                        </div>
                      </div>

                      <div
                        style={{
                          width: '100%',
                          display: 'grid',
                          gridTemplateColumns: '1fr 1fr',
                          gap: '12px',
                          marginTop: '12px',
                        }}
                      >
                        {node.branchYes && (
                          <div
                            style={{
                              backgroundColor: branchYesTheme.bg,
                              border: `1.5px solid ${branchYesTheme.border}`,
                              borderRadius: 'var(--radius-md)',
                              padding: '10px 12px',
                              display: 'flex',
                              flexDirection: 'column',
                              gap: '4px',
                            }}
                          >
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                              <span
                                style={{
                                  fontSize: '0.72rem',
                                  fontWeight: 700,
                                  color: branchYesTheme.text,
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: '4px',
                                }}
                              >
                                <BranchYesIcon size={12} />
                                {node.branchYes.label}
                              </span>
                              <span
                                style={{
                                  fontSize: '0.65rem',
                                  backgroundColor: branchYesTheme.badgeBg,
                                  color: branchYesTheme.badgeText,
                                  padding: '1px 5px',
                                  borderRadius: 'var(--radius-xs)',
                                  fontWeight: 600,
                                }}
                              >
                                {branchYesTheme.badgeLabel}
                              </span>
                            </div>
                            <strong style={{ fontSize: 'var(--text-xs)', color: branchYesTheme.text }}>
                              {node.branchYes.action}
                            </strong>
                            <p style={{ fontSize: '0.72rem', color: branchYesTheme.text, margin: 0, lineHeight: 1.35 }}>
                              {node.branchYes.detail}
                            </p>
                          </div>
                        )}

                        {node.branchNo && (
                          <div
                            style={{
                              backgroundColor: branchNoTheme.bg,
                              border: `1.5px solid ${branchNoTheme.border}`,
                              borderRadius: 'var(--radius-md)',
                              padding: '10px 12px',
                              display: 'flex',
                              flexDirection: 'column',
                              gap: '4px',
                            }}
                          >
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                              <span
                                style={{
                                  fontSize: '0.72rem',
                                  fontWeight: 700,
                                  color: branchNoTheme.text,
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: '4px',
                                }}
                              >
                                <BranchNoIcon size={12} />
                                {node.branchNo.label}
                              </span>
                              <span
                                style={{
                                  fontSize: '0.65rem',
                                  backgroundColor: branchNoTheme.badgeBg,
                                  color: branchNoTheme.badgeText,
                                  padding: '1px 5px',
                                  borderRadius: 'var(--radius-xs)',
                                  fontWeight: 600,
                                }}
                              >
                                {branchNoTheme.badgeLabel}
                              </span>
                            </div>
                            <strong style={{ fontSize: 'var(--text-xs)', color: branchNoTheme.text }}>
                              {node.branchNo.action}
                            </strong>
                            <p style={{ fontSize: '0.72rem', color: branchNoTheme.text, margin: 0, lineHeight: 1.35 }}>
                              {node.branchNo.detail}
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </React.Fragment>
              );
            })}
          </div>
        )}

        {/* 3. TEXT / ASCII VIEW */}
        {effectiveTab === 'text' && (
          <div
            style={{
              padding: '14px 16px',
              backgroundColor: '#161a23',
              borderRadius: 'var(--radius-md)',
              border: '1px solid #2a3142',
              color: '#f1f5f9',
            }}
          >
            <div
              style={{
                fontSize: '0.7rem',
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
                color: '#94a3b8',
                marginBottom: '8px',
                borderBottom: '1px solid #2d3748',
                paddingBottom: '4px',
              }}
            >
              ASCII Algorithmic Trace
            </div>
            <pre
              style={{
                fontFamily: 'var(--font-mono)',
                fontSize: 'var(--text-xs)',
                lineHeight: '1.6',
                margin: 0,
                color: '#e2e8f0',
                whiteSpace: 'pre-wrap',
              }}
            >
              {flowchart ||
                (isLinearSearch
                  ? `[Start]
  │
  ▼
[1. Initialize: i = 0]
  │
  ▼
┌──────────────────────────────┐
│  Loop: Is i < len(arr) ?     │
└──────────────┬───────────────┘
               │ YES
               ▼
        ┌──────────────┐
        │   arr[i]     │── YES ──> [Found target at index 'i'] ──> [End]
        │ == target ?  │
        └──────┬───────┘
               │ NO
               ▼
        [Increment: i = i + 1]
               │
               └──────────────────▶ (Loop back to condition)
               ┌──────────────────┘
               ▼ NO (i >= len(arr))
[Target Not Found: return -1]
  │
  ▼
[End]`
                  : `[Start]
  │
  ▼
[1. Initialize: low = 0, high = len(arr) - 1]
  │
  ▼
┌──────────────────────────────────────┐
│  Loop: Is low <= high && arr[mid] != target ?
└──────────────┬───────────────────────┘
               │ YES
               ▼
        ┌──────────────────────┐
        │ target < arr[mid] ?  │── YES ──> [high = mid - 1] ──┐
        └──────────────┬───────┘                              │
                       │ NO                                   │
                       ▼                                      │
               [low = mid + 1]                                │
                       │                                      │
                       └──────────────┬───────────────────────┘
                                      │
                                      ▼
                       [mid = (low + high) // 2]
                                      │
                                      └─────▶ (Loop back to condition)
               ┌──────────────────────┘
               ▼ NO (Exits loop)
[return mid if arr[mid] == target else -1]
  │
  ▼
[End]`)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
