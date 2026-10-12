import React from 'react';
import { Check, X, AlertCircle, AlertTriangle, Clock, Play } from 'lucide-react';

export default function ValidationStatus({
  type = 'validation', // 'validation' | 'execution'
  status = 'VALID',
  durationMs,
  className = '',
}) {
  const validationMap = {
    VALID: {
      label: 'Validated',
      icon: Check,
      color: 'var(--status-success)',
      bg: 'var(--status-success-bg)',
      border: 'var(--status-success-border)',
    },
    INVALID: {
      label: 'Validation Failed',
      icon: X,
      color: 'var(--status-error)',
      bg: 'var(--status-error-bg)',
      border: 'var(--status-error-border)',
    },
    INCOMPLETE: {
      label: 'Incomplete / Truncated',
      icon: AlertTriangle,
      color: 'var(--status-warning)',
      bg: 'var(--status-warning-bg)',
      border: 'var(--status-warning-border)',
    },
    VALIDATING: {
      label: 'Validating...',
      icon: Clock,
      color: '#60a5fa',
      bg: '#1e293b',
      border: '#3b82f6',
    },
    NOT_VALIDATED: {
      label: 'Not Validated',
      icon: AlertCircle,
      color: 'var(--text-muted)',
      bg: 'var(--bg-subtle)',
      border: 'var(--border-color)',
    },
    UNSUPPORTED: {
      label: 'Unsupported',
      icon: AlertTriangle,
      color: 'var(--status-warning)',
      bg: 'var(--status-warning-bg)',
      border: 'var(--status-warning-border)',
    },
    ERROR: {
      label: 'Validation Error',
      icon: AlertCircle,
      color: 'var(--status-error)',
      bg: 'var(--status-error-bg)',
      border: 'var(--status-error-border)',
    },
  };

  const executionMap = {
    RUNNING: {
      label: 'Running...',
      icon: Clock,
      color: '#60a5fa',
      bg: '#1e293b',
      border: '#3b82f6',
    },
    SUCCESS: {
      label: 'Ran successfully',
      icon: Check,
      color: 'var(--status-success)',
      bg: 'var(--status-success-bg)',
      border: 'var(--status-success-border)',
    },
    RUNTIME_ERROR: {
      label: 'Runtime error',
      icon: X,
      color: 'var(--status-error)',
      bg: 'var(--status-error-bg)',
      border: 'var(--status-error-border)',
    },
    TIMEOUT: {
      label: 'Timed out',
      icon: Clock,
      color: 'var(--status-warning)',
      bg: 'var(--status-warning-bg)',
      border: 'var(--status-warning-border)',
    },
    RESOURCE_LIMIT: {
      label: 'Resource limit',
      icon: AlertTriangle,
      color: 'var(--status-error)',
      bg: 'var(--status-error-bg)',
      border: 'var(--status-error-border)',
    },
    OUTPUT_LIMIT: {
      label: 'Output limit',
      icon: AlertTriangle,
      color: 'var(--status-warning)',
      bg: 'var(--status-warning-bg)',
      border: 'var(--status-warning-border)',
    },
    VALIDATION_FAILED: {
      label: 'Validation failed',
      icon: X,
      color: 'var(--status-error)',
      bg: 'var(--status-error-bg)',
      border: 'var(--status-error-border)',
    },
    UNSUPPORTED: {
      label: 'Unsupported',
      icon: AlertTriangle,
      color: 'var(--status-warning)',
      bg: 'var(--status-warning-bg)',
      border: 'var(--status-warning-border)',
    },
    SANDBOX_ERROR: {
      label: 'Sandbox error',
      icon: AlertCircle,
      color: 'var(--status-error)',
      bg: 'var(--status-error-bg)',
      border: 'var(--status-error-border)',
    },
  };

  const currentConfig = type === 'execution'
    ? (executionMap[status] || executionMap.SUCCESS)
    : (validationMap[status] || validationMap.VALID);

  const Icon = currentConfig.icon;

  return (
    <div
      className={`b2c-status-badge ${className}`}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '5px',
        padding: '2px 8px',
        borderRadius: 'var(--radius-xs)',
        fontSize: 'var(--text-xs)',
        fontWeight: 500,
        backgroundColor: currentConfig.bg,
        color: currentConfig.color,
        border: `1px solid ${currentConfig.border}`,
        userSelect: 'none',
      }}
    >
      <Icon size={12} strokeWidth={2.5} />
      <span>{currentConfig.label}</span>
      {durationMs && (
        <span style={{ opacity: 0.8, fontSize: '0.7rem', marginLeft: '2px' }}>
          ({Math.round(durationMs)}ms)
        </span>
      )}
    </div>
  );
}
