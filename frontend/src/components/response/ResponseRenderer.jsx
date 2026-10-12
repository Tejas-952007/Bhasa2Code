import React from 'react';
import ResponseSection from './ResponseSection';
import MarkdownContent from './MarkdownContent';
import CodeArtifact from '../code/CodeArtifact';
import ValidationDetails from './ValidationDetails';
import ExecutionResult from './ExecutionResult';
import SuggestionList from './SuggestionList';
import VisualFlowchart from '../study/VisualFlowchart';
import { GitBranch, CheckCircle2, History, AlertCircle, AlertTriangle } from 'lucide-react';

/**
 * ResponseRenderer
 * The centralized response section orchestrator for Bhasha2Code.
 * Renders structured assistant responses based on:
 * - Normal code generation
 * - Study Mode education layout
 * - Debugging layout
 * - Follow-up continuity
 */
export default function ResponseRenderer({
  message,
  isStudyMode = false,
  onSelectSuggestion = null,
  onCodeChange = null,
}) {
  if (!message) return null;

  const {
    content = '',
    codeBlock = null,
    explanation = [],
    example = null,
    study = null,
    validation = null,
    execution = null,
    suggestions = [],
    changes = [],
    activeContext = null,
    isFollowUp = false,
    debug = null,
  } = message;

  // Determine mode & available sections
  const hasStudySections = Boolean(
    isStudyMode &&
      study &&
      (study.problemUnderstanding ||
        (study.algorithm && study.algorithm.length > 0) ||
        study.flowchart ||
        (study.flowchartNodes && study.flowchartNodes.length > 0) ||
        (study.importantPoints && study.importantPoints.length > 0) ||
        (study.vivaQuestions && study.vivaQuestions.length > 0))
  );

  const hasDebugSections = Boolean(
    debug && (debug.problem || debug.cause || debug.fix)
  );

  return (
    <div className="b2c-assistant-response" style={{ width: '100%' }}>
      {/* 1. Context / Follow-Up Continuity Indicator */}
      {(isFollowUp || activeContext) && (
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            padding: '3px 8px',
            marginBottom: '10px',
            backgroundColor: 'var(--bg-subtle)',
            border: '1px solid var(--border-color)',
            borderRadius: 'var(--radius-xs)',
            fontSize: '0.72rem',
            color: 'var(--text-secondary)',
          }}
        >
          <History size={12} color="var(--accent-primary)" />
          <span>
            {typeof activeContext === 'string'
              ? activeContext
              : activeContext?.filename
              ? `Using current code: ${activeContext.filename}`
              : 'Using current session context'}
          </span>
        </div>
      )}

      {/* Incomplete Output Recovery Notice */}
      {(message.isIncomplete || codeBlock?.validationStatus === 'INCOMPLETE') && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '8px',
            padding: '10px 14px',
            marginBottom: '14px',
            backgroundColor: 'rgba(245, 158, 11, 0.12)',
            border: '1px solid rgba(245, 158, 11, 0.35)',
            borderRadius: 'var(--radius-sm)',
            fontSize: 'var(--text-xs)',
            color: '#fbbf24',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertTriangle size={15} color="#f59e0b" style={{ flexShrink: 0 }} />
            <span>
              {message.isContinuation ? (
                <>
                  <strong>Generation truncated again:</strong> Model reached token limit during continuation. The code remains incomplete.
                </>
              ) : (
                <>
                  <strong>Generation truncated:</strong> Output stopped at token limit or is incomplete.
                </>
              )}
            </span>
          </div>
          {onSelectSuggestion && !message.isContinuation && (
            <button
              type="button"
              onClick={() => onSelectSuggestion('Complete the code from where it stopped')}
              style={{
                backgroundColor: '#f59e0b',
                color: '#0f172a',
                border: 'none',
                borderRadius: 'var(--radius-xs)',
                padding: '4px 10px',
                fontSize: '0.75rem',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Complete Code
            </button>
          )}
        </div>
      )}

      {/* ------------------------------------------------------------- */}
      {/* CASE A: DEBUGGING WORKSPACE LAYOUT                           */}
      {/* ------------------------------------------------------------- */}
      {hasDebugSections ? (
        <>
          {debug.problem && (
            <ResponseSection title="Problem">
              <MarkdownContent content={debug.problem} />
            </ResponseSection>
          )}

          {debug.cause && (
            <ResponseSection title="Cause">
              <MarkdownContent content={debug.cause} />
            </ResponseSection>
          )}

          {debug.fix && (
            <ResponseSection title="Fix">
              <MarkdownContent content={debug.fix} />
            </ResponseSection>
          )}

          {codeBlock && (
            <ResponseSection title="Corrected Code">
              <CodeArtifact
                initialCode={codeBlock.code}
                filename={codeBlock.filename}
                language={codeBlock.language}
                initialValidation={codeBlock.validationStatus || 'VALID'}
                initialDiagnostics={codeBlock.diagnostics || []}
                initialExecution={codeBlock.executionStatus}
                initialOutput={codeBlock.output}
                durationMs={codeBlock.durationMs || 0}
                onCodeChange={onCodeChange}
              />
            </ResponseSection>
          )}
        </>
      ) : hasStudySections ? (
        /* ----------------------------------------------------------- */
        /* CASE B: STUDY MODE WORKSPACE LAYOUT                         */
        /* 1. Problem Understanding                                    */
        /* 2. Algorithm                                                */
        /* 3. Flowchart                                                */
        /* 4. Code                                                     */
        /* 5. Explanation                                              */
        /* 6. Example / Output                                         */
        /* 7. Important Points                                         */
        /* 8. Viva Questions                                           */
        /* ----------------------------------------------------------- */
        <>
          {/* Main prose introduction if present and not duplicating study sections */}
          {content &&
            !study?.problemUnderstanding?.includes(content.trim()) &&
            !content.trim().includes(study?.problemUnderstanding?.trim() || '___') &&
            !/(-->|->|\[start\]|┌──|├──|\[init|arr\[mid\]|mid\s*=|low\s*<=)/i.test(content) && (
              <div style={{ marginBottom: '12px' }}>
                <MarkdownContent content={content} />
              </div>
          )}

          {/* 1. Problem Understanding */}
          {study.problemUnderstanding && (
            <ResponseSection title="Problem Understanding">
              <MarkdownContent content={study.problemUnderstanding} />
            </ResponseSection>
          )}

          {/* 2. Algorithm */}
          {study.algorithm && study.algorithm.length > 0 && (
            <ResponseSection title="Algorithm">
              <ol
                style={{
                  margin: 0,
                  paddingLeft: '20px',
                  fontSize: 'var(--text-sm)',
                  color: 'var(--text-primary)',
                  lineHeight: 'var(--leading-relaxed)',
                }}
              >
                {study.algorithm.map((step, idx) => (
                  <li key={idx} style={{ marginBottom: '4px' }}>
                    <MarkdownContent content={step} />
                  </li>
                ))}
              </ol>
            </ResponseSection>
          )}

          {/* 3. Flowchart */}
          {(study.flowchart || study.flowchartNodes) && (
            <ResponseSection title="Algorithm Flowchart">
              <VisualFlowchart
                flowchart={study.flowchart}
                flowchartNodes={study.flowchartNodes}
              />
            </ResponseSection>
          )}

          {/* 4. Code */}
          {codeBlock && (
            <ResponseSection title="Code">
              <CodeArtifact
                initialCode={codeBlock.code}
                filename={codeBlock.filename}
                language={codeBlock.language}
                initialValidation={codeBlock.validationStatus || 'VALID'}
                initialDiagnostics={codeBlock.diagnostics || []}
                initialExecution={codeBlock.executionStatus}
                initialOutput={codeBlock.output}
                durationMs={codeBlock.durationMs || 0}
                onCodeChange={onCodeChange}
              />
            </ResponseSection>
          )}

          {/* 5. Explanation */}
          {explanation && explanation.length > 0 && (
            <ResponseSection title="Explanation">
              <ul
                style={{
                  margin: 0,
                  paddingLeft: '18px',
                  fontSize: 'var(--text-sm)',
                  color: 'var(--text-secondary)',
                  lineHeight: 'var(--leading-relaxed)',
                }}
              >
                {explanation.map((item, idx) => (
                  <li key={idx} style={{ marginBottom: '4px' }}>
                    <MarkdownContent content={item} />
                  </li>
                ))}
              </ul>
            </ResponseSection>
          )}

          {/* 6. Example / Output */}
          {example && (
            <ResponseSection title="Example / Output">
              <div
                style={{
                  padding: '8px 12px',
                  backgroundColor: 'var(--bg-subtle)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: 'var(--text-sm)',
                  fontFamily: 'var(--font-mono)',
                  color: 'var(--text-primary)',
                }}
              >
                <MarkdownContent content={example} />
              </div>
            </ResponseSection>
          )}

          {/* 7. Important Points */}
          {study.importantPoints && study.importantPoints.length > 0 && (
            <ResponseSection title="Important Points">
              <ul
                style={{
                  margin: 0,
                  paddingLeft: '18px',
                  fontSize: 'var(--text-sm)',
                  color: 'var(--text-secondary)',
                  lineHeight: 'var(--leading-relaxed)',
                }}
              >
                {study.importantPoints.map((point, idx) => (
                  <li key={idx} style={{ marginBottom: '4px' }}>
                    <MarkdownContent content={point} />
                  </li>
                ))}
              </ul>
            </ResponseSection>
          )}

          {/* 8. Viva Questions */}
          {study.vivaQuestions && study.vivaQuestions.length > 0 && (
            <ResponseSection title="Viva Questions">
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {study.vivaQuestions.map((qItem, idx) => {
                  const questionText = qItem.question || qItem.q || '';
                  const answerText = qItem.answer || qItem.a || '';
                  return (
                    <div
                      key={idx}
                      style={{
                        padding: '10px 14px',
                        backgroundColor: 'var(--bg-surface)',
                        border: '1px solid var(--border-color)',
                        borderRadius: 'var(--radius-sm)',
                      }}
                    >
                      <div
                        style={{
                          fontSize: 'var(--text-sm)',
                          fontWeight: 600,
                          color: 'var(--text-primary)',
                          marginBottom: '4px',
                        }}
                      >
                        Q{idx + 1}: {questionText}
                      </div>
                      <div
                        style={{
                          fontSize: 'var(--text-sm)',
                          color: 'var(--text-secondary)',
                          lineHeight: 'var(--leading-normal)',
                        }}
                      >
                        <strong style={{ color: 'var(--accent-text)' }}>Ans: </strong>
                        {answerText}
                      </div>
                    </div>
                  );
                })}
              </div>
            </ResponseSection>
          )}
        </>
      ) : (
        /* ----------------------------------------------------------- */
        /* CASE C: TYPICAL / NORMAL CODE GENERATION LAYOUT             */
        /* 1. Introduction / Prose                                     */
        /* 2. Changes (if follow-up)                                   */
        /* 3. Code                                                     */
        /* 4. Explanation                                              */
        /* 5. Example                                                  */
        /* 6. Validation (if not in code block)                        */
        /* 7. Execution (if not in code block)                         */
        /* ----------------------------------------------------------- */
        <>
          {content && (
            <div style={{ marginBottom: '12px' }}>
              <MarkdownContent content={content} />
            </div>
          )}

          {/* Follow-up Changes List */}
          {changes && changes.length > 0 && (
            <ResponseSection title="Changes">
              <ul
                style={{
                  margin: 0,
                  paddingLeft: '18px',
                  fontSize: 'var(--text-sm)',
                  color: 'var(--text-primary)',
                  lineHeight: 'var(--leading-relaxed)',
                }}
              >
                {changes.map((change, idx) => (
                  <li key={idx} style={{ marginBottom: '3px' }}>
                    <MarkdownContent content={change} />
                  </li>
                ))}
              </ul>
            </ResponseSection>
          )}

          {/* Primary Code Block */}
          {codeBlock && (
            <ResponseSection title={isFollowUp ? 'Updated Code' : 'Code'}>
              <CodeArtifact
                initialCode={codeBlock.code}
                filename={codeBlock.filename}
                language={codeBlock.language}
                initialValidation={codeBlock.validationStatus || 'VALID'}
                initialDiagnostics={codeBlock.diagnostics || []}
                initialExecution={codeBlock.executionStatus}
                initialOutput={codeBlock.output}
                durationMs={codeBlock.durationMs || 0}
                onCodeChange={onCodeChange}
              />
            </ResponseSection>
          )}

          {/* Explanation Section */}
          {explanation && explanation.length > 0 && (
            <ResponseSection title="Explanation">
              <ul
                style={{
                  margin: 0,
                  paddingLeft: '18px',
                  fontSize: 'var(--text-sm)',
                  color: 'var(--text-secondary)',
                  lineHeight: 'var(--leading-relaxed)',
                }}
              >
                {explanation.map((item, idx) => (
                  <li key={idx} style={{ marginBottom: '4px' }}>
                    <MarkdownContent content={item} />
                  </li>
                ))}
              </ul>
            </ResponseSection>
          )}

          {/* Example Section */}
          {example && (
            <ResponseSection title="Example">
              <div
                style={{
                  padding: '8px 12px',
                  backgroundColor: 'var(--bg-subtle)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: 'var(--text-sm)',
                  fontFamily: 'var(--font-mono)',
                  color: 'var(--text-primary)',
                }}
              >
                <MarkdownContent content={example} />
              </div>
            </ResponseSection>
          )}
        </>
      )}

      {/* Standalone Validation (if separate from code block) */}
      {validation && (
        <ResponseSection title="Validation">
          <ValidationDetails
            status={validation.status}
            diagnostics={validation.diagnostics}
            lineCount={validation.line_count}
            language={validation.language}
          />
        </ResponseSection>
      )}

      {/* Standalone Execution (if separate from code block) */}
      {execution && (
        <ResponseSection title="Execution">
          <ExecutionResult
            status={execution.status}
            stdout={execution.stdout}
            stderr={execution.stderr}
            exitCode={execution.exit_code}
            durationMs={execution.duration_ms}
            diagnostics={execution.diagnostics}
          />
        </ResponseSection>
      )}

      {/* 8. Suggestions List */}
      {suggestions && suggestions.length > 0 && (
        <SuggestionList
          suggestions={suggestions}
          onSelectSuggestion={onSelectSuggestion}
        />
      )}
    </div>
  );
}
