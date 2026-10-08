import React from 'react';
import CodeArtifact from '../code/CodeArtifact';
import StudySections from '../study/StudySections';

export default function AssistantMessage({ message, isStudyMode = false }) {
  const { content, codeBlock, explanation, example, study } = message;

  const sectionHeaderStyle = {
    fontSize: 'var(--text-xs)',
    fontWeight: 600,
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
    color: 'var(--text-muted)',
    marginTop: 'var(--space-3)',
    marginBottom: 'var(--space-1)',
  };

  return (
    <div
      style={{
        padding: 'var(--space-4) 0',
        borderBottom: '1px solid var(--border-subtle)',
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          marginBottom: 'var(--space-2)',
        }}
      >
        <span
          style={{
            fontSize: 'var(--text-xs)',
            fontWeight: 600,
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            color: 'var(--text-primary)',
          }}
        >
          Bhasha2Code
        </span>
      </div>

      {/* Main Text Content */}
      {content && (
        <div
          style={{
            fontSize: 'var(--text-base)',
            color: 'var(--text-primary)',
            lineHeight: 'var(--leading-relaxed)',
            marginBottom: 'var(--space-3)',
            whiteSpace: 'pre-wrap',
          }}
        >
          {content}
        </div>
      )}

      {/* Code Block Artifact */}
      {codeBlock && (
        <div>
          <div style={sectionHeaderStyle}>Code</div>
          <CodeArtifact
            initialCode={codeBlock.code}
            filename={codeBlock.filename}
            language={codeBlock.language}
            initialValidation={codeBlock.validationStatus}
            initialExecution={codeBlock.executionStatus}
            initialOutput={codeBlock.output}
            durationMs={codeBlock.durationMs}
          />
        </div>
      )}

      {/* Explanation Section */}
      {explanation && explanation.length > 0 && (
        <div style={{ marginTop: 'var(--space-3)' }}>
          <div style={sectionHeaderStyle}>Explanation</div>
          <ul
            style={{
              paddingLeft: '18px',
              fontSize: 'var(--text-sm)',
              color: 'var(--text-secondary)',
              lineHeight: 'var(--leading-relaxed)',
            }}
          >
            {explanation.map((item, idx) => (
              <li key={idx} style={{ marginBottom: '4px' }}>
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Example Section */}
      {example && (
        <div style={{ marginTop: 'var(--space-3)' }}>
          <div style={sectionHeaderStyle}>Example</div>
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
            {example}
          </div>
        </div>
      )}

      {/* Study Mode Expanded Sections */}
      {isStudyMode && study && (
        <StudySections studyData={study} />
      )}
    </div>
  );
}
