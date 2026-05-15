const headingRules = [
  { pattern: /^###\s*(.+)$/gm, tag: 'h3', className: 'analysis-h3' },
  { pattern: /^##\s*(.+)$/gm, tag: 'h2', className: 'analysis-h2' },
  { pattern: /^#\s*(.+)$/gm, tag: 'h1', className: 'analysis-h1' },
]

function escapeHtml(text: string) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

export function formatAnalysisHtml(text: string) {
  let html = escapeHtml(text)

  for (const rule of headingRules) {
    html = html.replace(
      rule.pattern,
      `<${rule.tag} class="${rule.className}">$1</${rule.tag}>`,
    )
  }

  return html
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>')
}
