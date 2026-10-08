import React from 'react';

export default function StudySections({ studyData }) {
  if (!studyData) return null;

  const {
    problemUnderstanding,
    algorithm,
    flowchart,
    importantPoints,
    vivaQuestions,
  } = studyData;

  const sectionHeaderStyle = {
    fontSize: 'var(--text-sm)',
    fontWeight: 600,
    textTransform: 'uppercase',
    letterSpacing: '0.04em',
    color: 'var(--text-primary)',
    marginBottom: 'var(--space-2)',
    paddingBottom: '4px',
    borderBottom: '1px solid var(--border-subtle)',
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: 'var(--space-5)',
        marginTop: 'var(--space-4)',
        paddingTop: 'var(--space-3)',
      }}
    >
      {/* 1. Problem Understanding */}
      {problemUnderstanding && (
        <div>
          <h4 style={sectionHeaderStyle}>Problem Understanding</h4>
          <p
            style={{
              fontSize: 'var(--text-sm)',
              color: 'var(--text-secondary)',
              lineHeight: 'var(--leading-relaxed)',
            }}
          >
            {problemUnderstanding}
          </p>
        </div>
      )}

      {/* 2. Algorithm */}
      {algorithm && algorithm.length > 0 && (
        <div>
          <h4 style={sectionHeaderStyle}>Algorithm</h4>
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: 'var(--space-1)',
              fontSize: 'var(--text-sm)',
              color: 'var(--text-secondary)',
            }}
          >
            {algorithm.map((step, idx) => (
              <div key={idx} style={{ lineHeight: 'var(--leading-normal)' }}>
                {step}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 3. Flowchart */}
      {flowchart && (
        <div>
          <h4 style={sectionHeaderStyle}>Flowchart</h4>
          <pre
            style={{
              padding: '12px 16px',
              backgroundColor: 'var(--bg-subtle)',
              border: '1px solid var(--border-color)',
              borderRadius: 'var(--radius-sm)',
              fontSize: 'var(--text-xs)',
              color: 'var(--text-primary)',
              lineHeight: '1.4',
              overflowX: 'auto',
            }}
          >
            {flowchart}
          </pre>
        </div>
      )}

      {/* 4. Important Points */}
      {importantPoints && importantPoints.length > 0 && (
        <div>
          <h4 style={sectionHeaderStyle}>Important Points</h4>
          <ul
            style={{
              paddingLeft: '18px',
              fontSize: 'var(--text-sm)',
              color: 'var(--text-secondary)',
              lineHeight: 'var(--leading-relaxed)',
            }}
          >
            {importantPoints.map((point, idx) => (
              <li key={idx} style={{ marginBottom: '4px' }}>
                {point}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 5. Viva Questions */}
      {vivaQuestions && vivaQuestions.length > 0 && (
        <div>
          <h4 style={sectionHeaderStyle}>Viva Questions & Answers</h4>
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: 'var(--space-3)',
            }}
          >
            {vivaQuestions.map((item, idx) => (
              <div
                key={idx}
                style={{
                  padding: '10px 12px',
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
                  Q{idx + 1}: {item.q}
                </div>
                <div
                  style={{
                    fontSize: 'var(--text-sm)',
                    color: 'var(--text-secondary)',
                    lineHeight: 'var(--leading-normal)',
                  }}
                >
                  <strong style={{ color: 'var(--accent-text)' }}>Ans: </strong>
                  {item.a}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
