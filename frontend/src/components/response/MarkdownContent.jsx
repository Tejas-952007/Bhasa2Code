import React from 'react';

/**
 * Lightweight, secure Markdown renderer for Bhasha2Code assistant prose.
 * Supports headings, bullet/numbered lists, bold, italic, inline code, and paragraphs.
 */

function renderInline(text) {
  if (!text) return null;

  // Split by inline code first
  const codeParts = text.split(/(`[^`]+`)/g);

  return codeParts.map((part, i) => {
    if (part.startsWith('`') && part.endsWith('`') && part.length > 2) {
      return (
        <code
          key={i}
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.85em',
            padding: '2px 5px',
            backgroundColor: 'var(--bg-subtle)',
            border: '1px solid var(--border-color)',
            borderRadius: 'var(--radius-xs)',
            color: 'var(--text-primary)',
          }}
        >
          {part.slice(1, -1)}
        </code>
      );
    }

    // Now format bold and italic within non-code text
    // Replace **bold** with <strong> and *italic* with <em>
    const boldParts = part.split(/(\*\*[^*]+\*\*)/g);
    return boldParts.map((bPart, j) => {
      if (bPart.startsWith('**') && bPart.endsWith('**') && bPart.length > 4) {
        return <strong key={`${i}-${j}`}>{bPart.slice(2, -2)}</strong>;
      }

      const italicParts = bPart.split(/(\*[^*]+\*)/g);
      return italicParts.map((itPart, k) => {
        if (itPart.startsWith('*') && itPart.endsWith('*') && itPart.length > 2) {
          return <em key={`${i}-${j}-${k}`}>{itPart.slice(1, -1)}</em>;
        }
        return itPart;
      });
    });
  });
}

export default function MarkdownContent({ content = '', className = '', style = {} }) {
  if (!content) return null;

  const lines = content.split('\n');
  const elements = [];
  let currentList = null;
  let listType = null;
  let keyIndex = 0;

  const flushList = () => {
    if (currentList && currentList.length > 0) {
      const ListTag = listType === 'ol' ? 'ol' : 'ul';
      elements.push(
        <ListTag
          key={`list-${keyIndex++}`}
          style={{
            margin: '8px 0',
            paddingLeft: '22px',
            lineHeight: 'var(--leading-relaxed)',
            color: 'var(--text-primary)',
            fontSize: 'var(--text-sm)',
          }}
        >
          {currentList.map((item, idx) => (
            <li key={idx} style={{ marginBottom: '4px' }}>
              {renderInline(item)}
            </li>
          ))}
        </ListTag>
      );
      currentList = null;
      listType = null;
    }
  };

  let inCodeFence = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    if (trimmed.startsWith('```') || trimmed.startsWith('~~~')) {
      inCodeFence = !inCodeFence;
      flushList();
      continue;
    }

    if (inCodeFence) {
      // Do not render raw code lines as markdown paragraphs
      continue;
    }

    if (!trimmed) {
      flushList();
      continue;
    }

    // Headings
    if (trimmed.startsWith('### ')) {
      flushList();
      elements.push(
        <h4
          key={`h4-${keyIndex++}`}
          style={{
            fontSize: 'var(--text-sm)',
            fontWeight: 700,
            textTransform: 'uppercase',
            letterSpacing: '0.04em',
            color: 'var(--text-secondary)',
            margin: '16px 0 6px',
          }}
        >
          {trimmed.slice(4)}
        </h4>
      );
      continue;
    }

    if (trimmed.startsWith('## ')) {
      flushList();
      elements.push(
        <h3
          key={`h3-${keyIndex++}`}
          style={{
            fontSize: 'var(--text-base)',
            fontWeight: 700,
            color: 'var(--text-primary)',
            margin: '18px 0 8px',
          }}
        >
          {trimmed.slice(3)}
        </h3>
      );
      continue;
    }

    if (trimmed.startsWith('# ')) {
      flushList();
      elements.push(
        <h2
          key={`h2-${keyIndex++}`}
          style={{
            fontSize: 'var(--text-lg)',
            fontWeight: 700,
            color: 'var(--text-primary)',
            margin: '20px 0 10px',
          }}
        >
          {trimmed.slice(2)}
        </h2>
      );
      continue;
    }

    // Bullet items
    const bulletMatch = trimmed.match(/^[-*•]\s+(.+)$/);
    if (bulletMatch) {
      if (listType !== 'ul') flushList();
      listType = 'ul';
      if (!currentList) currentList = [];
      currentList.push(bulletMatch[1]);
      continue;
    }

    // Numbered items
    const numMatch = trimmed.match(/^\d+\.\s+(.+)$/);
    if (numMatch) {
      if (listType !== 'ol') flushList();
      listType = 'ol';
      if (!currentList) currentList = [];
      currentList.push(numMatch[1]);
      continue;
    }

    // Blockquote
    if (trimmed.startsWith('> ')) {
      flushList();
      elements.push(
        <blockquote
          key={`quote-${keyIndex++}`}
          style={{
            margin: '10px 0',
            padding: '6px 14px',
            borderLeft: '3px solid var(--accent-primary)',
            backgroundColor: 'var(--bg-subtle)',
            borderRadius: '0 var(--radius-xs) var(--radius-xs) 0',
            color: 'var(--text-secondary)',
            fontSize: 'var(--text-sm)',
            fontStyle: 'italic',
          }}
        >
          {renderInline(trimmed.slice(2))}
        </blockquote>
      );
      continue;
    }

    // Standard paragraph
    flushList();
    elements.push(
      <p
        key={`p-${keyIndex++}`}
        style={{
          margin: '6px 0',
          fontSize: 'var(--text-sm)',
          lineHeight: 'var(--leading-relaxed)',
          color: 'var(--text-primary)',
        }}
      >
        {renderInline(trimmed)}
      </p>
    );
  }

  flushList();

  return (
    <div className={`b2c-markdown-content ${className}`} style={style}>
      {elements}
    </div>
  );
}
