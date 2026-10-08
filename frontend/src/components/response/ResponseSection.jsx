import React from 'react';

/**
 * ResponseSection
 * Structural section wrapper maintaining consistent typography and quiet spacing.
 * Renders only genuine sections provided by the backend response.
 */
export default function ResponseSection({
  title = '',
  children,
  badge = null,
  style = {},
  className = '',
  action = null,
}) {
  if (!children && children !== 0) return null;

  return (
    <section
      className={`b2c-response-section ${className}`}
      style={{
        marginTop: 'var(--space-3)',
        marginBottom: 'var(--space-3)',
        ...style,
      }}
    >
      {title && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: 'var(--space-2)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h4
              style={{
                fontSize: 'var(--text-xs)',
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: '0.06em',
                color: 'var(--text-muted)',
                margin: 0,
              }}
            >
              {title}
            </h4>
            {badge && (
              <span
                style={{
                  fontSize: '0.68rem',
                  padding: '1px 6px',
                  borderRadius: 'var(--radius-xs)',
                  backgroundColor: 'var(--bg-subtle)',
                  color: 'var(--text-secondary)',
                  border: '1px solid var(--border-subtle)',
                }}
              >
                {badge}
              </span>
            )}
          </div>
          {action && <div>{action}</div>}
        </div>
      )}

      <div className="b2c-section-content">{children}</div>
    </section>
  );
}
