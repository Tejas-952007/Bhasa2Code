import React, { useState } from 'react';
import { Check, X, AlertTriangle, HelpCircle, ChevronDown, ChevronRight } from 'lucide-react';

/**
 * ValidationDetails
 * Compact, clear representation of syntax/structural validation status.
 * Semantic distinction: Validated means syntactically valid, not logically correct.
 */
export default function ValidationDetails({
  status = 'VALID',
  diagnostics = [],
  lineCount = null,
  language = 'python',
}) {
  const [showDetails, setShowDetails] = useState(false);
  const normalized = (status || 'VALID').toUpperCase();

  const isSuccess = normalized === 'VALID';
  const isFailed = normalized === 'INVALID';
  const isUnsupported = normalized === 'UNSUPPORTED';
  const isPending = normalized === 'VALIDATING';

  const badgeConfig = isSuccess
    ? {
        label: 'Validated',
        icon: Check,
        color: '#15803d',
        bgColor: '#f0fdf4',
        borderColor: '#bbf7d0',
      }
    : isFailed
    ? {
        label: 'Validation Failed',
        icon: X,
        color: '#b91c1c',
        bgColor: '#fef2f2',
        borderColor: '#fecaca',
      }
    : isUnsupported
    ? {
        label: 'Validation Unsupported',
        icon: AlertTriangle,
        color: '#b45309',
        bgColor: '#fffbeb',
        borderColor: '#fde68a',
      }
    : isPending
    ? {
        label: 'Validating code...',
        icon: HelpCircle,
        color: '#2563eb',
        bgColor: '#eff6ff',
        borderColor: '#bfdbfe',
      }
    : {
        label: 'Not Validated',
        icon: HelpCircle,
        color: 'var(--text-muted)',
        bgColor: 'var(--bg-subtle)',
        borderColor: 'var(--border-color)',
      };

  const Icon = badgeConfig.icon;
  const hasDiagnostics = diagnostics && diagnostics.length > 0;

  return (
    <div
      style={{
        margin: '8px 0',
        padding: '10px 14px',
        backgroundColor: 'var(--bg-surface)',
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-sm)',
        fontSize: 'var(--text-xs)',
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '8px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '5px',
              padding: '2px 8px',
              borderRadius: 'var(--radius-xs)',
              fontWeight: 600,
              fontSize: '0.72rem',
              color: badgeConfig.color,
              backgroundColor: badgeConfig.bgColor,
              border: `1px solid ${badgeConfig.borderColor}`,
            }}
          >
            <Icon size={12} strokeWidth={2.5} />
            <span>{isSuccess ? '✓ ' : isFailed ? '✕ ' : ''}{badgeConfig.label}</span>
          </span>

          <span
            style={{
              color: 'var(--text-muted)',
              fontSize: '0.72rem',
            }}
          >
            {isSuccess
              ? 'Syntax verified'
              : isFailed
              ? 'Syntax error detected'
              : 'Static check'}
            {lineCount ? ` · ${lineCount} lines` : ''}
          </span>
        </div>

        {hasDiagnostics && (
          <button
            type="button"
            onClick={() => setShowDetails(!showDetails)}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              color: 'var(--text-secondary)',
              fontSize: '0.72rem',
              padding: '2px 6px',
              borderRadius: 'var(--radius-xs)',
              cursor: 'pointer',
              border: '1px solid var(--border-subtle)',
              backgroundColor: 'transparent',
            }}
          >
            {showDetails ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
            <span>{showDetails ? 'Hide details' : 'Show details'}</span>
          </button>
        )}
      </div>

      {/* Diagnostics details if failed or user expands */}
      {(showDetails || isFailed) && hasDiagnostics && (
        <div
          style={{
            marginTop: '8px',
            padding: '8px 10px',
            backgroundColor: '#1e293b',
            color: '#f87171',
            borderRadius: 'var(--radius-xs)',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.72rem',
            lineHeight: '1.4',
            whiteSpace: 'pre-wrap',
            maxHeight: '180px',
            overflowY: 'auto',
          }}
        >
          {diagnostics.map((diag, idx) => (
            <div key={idx} style={{ marginBottom: '2px' }}>
              {diag}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
