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
} from 'lucide-react';

export default function VisualFlowchart({ flowchart, flowchartNodes }) {
  const [activeTab, setActiveTab] = useState('visual'); // 'visual' | 'text'
  const [hoveredNode, setHoveredNode] = useState(null);

  // Default rich nodes for standard coding problems if not explicitly passed
  const defaultCalculatorNodes = [
    {
      id: 'start',
      type: 'terminal',
      title: 'Start',
      subtitle: 'Calculator routine initiates',
      icon: Play,
      accent: 'emerald',
    },
    {
      id: 'input',
      type: 'process',
      title: '1. Read User Inputs',
      subtitle: 'Prompt first operand (num1), operator (+, -, *, /), and second operand (num2)',
      code: 'num1 = float(...) ; op = input(...) ; num2 = float(...)',
      icon: Terminal,
      accent: 'blue',
    },
    {
      id: 'parse',
      type: 'process',
      title: '2. Identify Operators & Types',
      subtitle: 'Cast string inputs to float numbers and validate arithmetic symbol',
      code: 'type(num1) -> float, type(num2) -> float',
      icon: Layers,
      accent: 'indigo',
    },
    {
      id: 'decision',
      type: 'decision',
      title: 'Decision: Division by Zero Check',
      condition: "Is op == '/' and num2 == 0 ?",
      icon: GitBranch,
      accent: 'amber',
      branchYes: {
        label: 'YES (Invalid Input)',
        action: 'Raise ZeroDivisionError',
        detail: 'Display error: "Cannot divide by zero" and prevent application crash',
        outcomeType: 'error',
      },
      branchNo: {
        label: 'NO (Valid Arithmetic)',
        action: 'Dispatch Calculation Routine',
        detail: 'Invoke corresponding function: add(a,b), subtract(a,b), multiply(a,b), or divide(a,b)',
        outcomeType: 'success',
      },
    },
    {
      id: 'output',
      type: 'process',
      title: '3. Return & Display Output',
      subtitle: 'Format calculated numeric result and stream to standard output',
      code: 'print(f"Result: {result}")',
      icon: FileText,
      accent: 'blue',
    },
    {
      id: 'end',
      type: 'terminal',
      title: 'End',
      subtitle: 'Program terminates gracefully with exit code 0',
      icon: CheckCircle2,
      accent: 'slate',
    },
  ];

  const nodes = flowchartNodes || defaultCalculatorNodes;

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
          padding: '10px 14px',
          backgroundColor: 'var(--bg-subtle)',
          borderBottom: '1px solid var(--border-color)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div
            style={{
              width: '20px',
              height: '20px',
              borderRadius: 'var(--radius-xs)',
              backgroundColor: 'var(--accent-subtle)',
              color: 'var(--accent-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <GitBranch size={13} />
          </div>
          <span style={{ fontSize: 'var(--text-sm)', fontWeight: 600, color: 'var(--text-primary)' }}>
            Algorithm Flowchart
          </span>
          <span
            style={{
              fontSize: '0.68rem',
              backgroundColor: '#dbeafe',
              color: '#1d4ed8',
              fontWeight: 600,
              padding: '1px 6px',
              borderRadius: 'var(--radius-xs)',
            }}
          >
            Visual Model
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
          }}
        >
          <button
            type="button"
            onClick={() => setActiveTab('visual')}
            style={{
              padding: '4px 10px',
              fontSize: 'var(--text-xs)',
              fontWeight: activeTab === 'visual' ? 600 : 500,
              color: activeTab === 'visual' ? 'var(--accent-primary)' : 'var(--text-secondary)',
              backgroundColor: activeTab === 'visual' ? 'var(--accent-subtle)' : 'transparent',
              borderRadius: 'var(--radius-xs)',
              cursor: 'pointer',
            }}
          >
            📊 Visual Diagram
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('text')}
            style={{
              padding: '4px 10px',
              fontSize: 'var(--text-xs)',
              fontWeight: activeTab === 'text' ? 600 : 500,
              color: activeTab === 'text' ? 'var(--accent-primary)' : 'var(--text-secondary)',
              backgroundColor: activeTab === 'text' ? 'var(--accent-subtle)' : 'transparent',
              borderRadius: 'var(--radius-xs)',
              cursor: 'pointer',
            }}
          >
            📋 Text View
          </button>
        </div>
      </div>

      {/* Main Flowchart Content */}
      <div style={{ padding: '24px 18px', backgroundColor: '#fcfdfe' }}>
        {activeTab === 'visual' ? (
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
            {/* Render Nodes sequentially */}
            {nodes.map((node, index) => {
              const isDecision = node.type === 'decision';
              const isTerminal = node.type === 'terminal';
              const Icon = node.icon;

              return (
                <React.Fragment key={node.id}>
                  {/* Connector Arrow before each step (except the first) */}
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

                  {/* 1. Terminal Node (Start / End) */}
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
                        transition: 'transform 150ms ease',
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

                  {/* 2. Process / Input Node */}
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
                            gap: '8px',
                          }}
                        >
                          <div
                            style={{
                              width: '20px',
                              height: '20px',
                              borderRadius: '4px',
                              backgroundColor: '#eff6ff',
                              color: '#2563eb',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                            }}
                          >
                            {Icon && <Icon size={12} />}
                          </div>
                          <span
                            style={{
                              fontSize: 'var(--text-sm)',
                              fontWeight: 600,
                              color: '#1e3a8a',
                            }}
                          >
                            {node.title}
                          </span>
                        </div>
                        <span
                          style={{
                            fontSize: '0.68rem',
                            backgroundColor: '#f1f5f9',
                            color: '#475569',
                            padding: '1px 6px',
                            borderRadius: 'var(--radius-xs)',
                            fontWeight: 500,
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

                  {/* 3. Decision Node with Dual Branches (Like Image 5!) */}
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
                      {/* Diamond Condition Card */}
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
                            fontSize: 'var(--text-sm)',
                            fontWeight: 700,
                            color: '#78350f',
                            fontFamily: 'var(--font-mono)',
                          }}
                        >
                          {node.condition}
                        </div>
                      </div>

                      {/* Branch Split Visualizer */}
                      <div
                        style={{
                          width: '100%',
                          display: 'grid',
                          gridTemplateColumns: '1fr 1fr',
                          gap: '16px',
                          marginTop: '16px',
                        }}
                      >
                        {/* Branch YES (Error Branch) */}
                        <div
                          style={{
                            backgroundColor: '#fef2f2',
                            border: '1.5px solid #ef4444',
                            borderRadius: 'var(--radius-md)',
                            padding: '10px 12px',
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '4px',
                          }}
                        >
                          <div
                            style={{
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'space-between',
                            }}
                          >
                            <span
                              style={{
                                fontSize: '0.72rem',
                                fontWeight: 700,
                                color: '#b91c1c',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '4px',
                              }}
                            >
                              <AlertTriangle size={12} />
                              {node.branchYes.label}
                            </span>
                            <span
                              style={{
                                fontSize: '0.65rem',
                                backgroundColor: '#fee2e2',
                                color: '#991b1b',
                                padding: '1px 5px',
                                borderRadius: 'var(--radius-xs)',
                                fontWeight: 600,
                              }}
                            >
                              Branch Exit
                            </span>
                          </div>
                          <strong style={{ fontSize: 'var(--text-xs)', color: '#991b1b' }}>
                            {node.branchYes.action}
                          </strong>
                          <p style={{ fontSize: '0.72rem', color: '#7f1d1d', margin: 0, lineHeight: 1.35 }}>
                            {node.branchYes.detail}
                          </p>
                        </div>

                        {/* Branch NO (Success / Valid Path) */}
                        <div
                          style={{
                            backgroundColor: '#f0fdf4',
                            border: '1.5px solid #22c55e',
                            borderRadius: 'var(--radius-md)',
                            padding: '10px 12px',
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '4px',
                          }}
                        >
                          <div
                            style={{
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'space-between',
                            }}
                          >
                            <span
                              style={{
                                fontSize: '0.72rem',
                                fontWeight: 700,
                                color: '#15803d',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '4px',
                              }}
                            >
                              <CheckCircle2 size={12} />
                              {node.branchNo.label}
                            </span>
                            <span
                              style={{
                                fontSize: '0.65rem',
                                backgroundColor: '#dcfce7',
                                color: '#166534',
                                padding: '1px 5px',
                                borderRadius: 'var(--radius-xs)',
                                fontWeight: 600,
                              }}
                            >
                              Continue Flow
                            </span>
                          </div>
                          <strong style={{ fontSize: 'var(--text-xs)', color: '#166534' }}>
                            {node.branchNo.action}
                          </strong>
                          <p style={{ fontSize: '0.72rem', color: '#14532d', margin: 0, lineHeight: 1.35 }}>
                            {node.branchNo.detail}
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </React.Fragment>
              );
            })}
          </div>
        ) : (
          /* Text View / ASCII Flow */
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
                `Start
  ↓
Input num1, operator, num2
  ↓
Is operator '/' and num2 == 0?
  ├── YES ──> Display "Cannot divide by zero" ──> Terminate
  └── NO  ──> Execute Arithmetic Function (add, sub, mul, div)
  ↓
Display Formatted Result
  ↓
End (Exit 0)`}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
