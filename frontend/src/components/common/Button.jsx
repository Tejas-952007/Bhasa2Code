import React from 'react';

export default function Button({
  children,
  variant = 'secondary',
  size = 'md',
  icon: Icon,
  className = '',
  disabled = false,
  onClick,
  type = 'button',
  title,
  ariaLabel,
  ...props
}) {
  const baseStyle = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '6px',
    borderRadius: 'var(--radius-sm)',
    fontWeight: 500,
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.5 : 1,
    transition: 'all var(--transition-fast)',
    whiteSpace: 'nowrap',
    userSelect: 'none',
  };

  const sizes = {
    sm: { padding: '4px 8px', fontSize: 'var(--text-xs)' },
    md: { padding: '6px 12px', fontSize: 'var(--text-sm)' },
    lg: { padding: '8px 16px', fontSize: 'var(--text-base)' },
    icon: { padding: '6px', fontSize: 'var(--text-sm)' },
  };

  const variants = {
    primary: {
      backgroundColor: 'var(--accent-primary)',
      color: '#ffffff',
      border: '1px solid var(--accent-primary)',
    },
    secondary: {
      backgroundColor: 'var(--bg-surface)',
      color: 'var(--text-primary)',
      border: '1px solid var(--border-color)',
    },
    subtle: {
      backgroundColor: 'var(--bg-subtle)',
      color: 'var(--text-primary)',
      border: '1px solid transparent',
    },
    ghost: {
      backgroundColor: 'transparent',
      color: 'var(--text-secondary)',
      border: '1px solid transparent',
    },
    outline: {
      backgroundColor: 'transparent',
      color: 'var(--accent-primary)',
      border: '1px solid var(--accent-primary)',
    },
  };

  const combinedStyle = {
    ...baseStyle,
    ...(sizes[size] || sizes.md),
    ...(variants[variant] || variants.secondary),
  };

  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      title={title}
      aria-label={ariaLabel || title}
      style={combinedStyle}
      className={`b2c-btn b2c-btn-${variant} ${className}`}
      {...props}
    >
      {Icon && <Icon size={size === 'sm' ? 14 : 16} />}
      {children}
    </button>
  );
}
