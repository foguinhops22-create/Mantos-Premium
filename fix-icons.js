const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname);
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

// SVG icons for each category
const svgIcons = {
  'brasileiros.html': `<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#10bd66" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.38 3.46L16 2 12 5 8 2 3.62 3.46a2 2 0 00-1.34 2.23l.58 3.47a1 1 0 00.99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 002-2V10h2.15a1 1 0 00.99-.84l.58-3.47a2 2 0 00-1.34-2.23z"/></svg>`,
  'europeus.html': `<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#3e73ff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.38 3.46L16 2 12 5 8 2 3.62 3.46a2 2 0 00-1.34 2.23l.58 3.47a1 1 0 00.99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 002-2V10h2.15a1 1 0 00.99-.84l.58-3.47a2 2 0 00-1.34-2.23z"/></svg>`,
  'selecoes.html': `<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>`,
  'retro.html': `<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 010-5H6"/><path d="M18 9h1.5a2.5 2.5 0 000-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20 17 22"/><path d="M18 2H6v7a6 6 0 0012 0V2z"/></svg>`,
  'player-version.html': `<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`,
  'infantis.html': `<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#ec4899" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.38 3.46L16 2 12 5 8 2 3.62 3.46a2 2 0 00-1.34 2.23l.58 3.47a1 1 0 00.99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 002-2V10h2.15a1 1 0 00.99-.84l.58-3.47a2 2 0 00-1.34-2.23z"/><path d="M9 22v-4M15 22v-4" stroke-width="1.4"/></svg>`,
  'lancamentos.html': `<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>`
};

// Category name -> html filename mapping
const catMap = {
  'brasileiros.html': 'brasileiros.html',
  'europeus.html': 'europeus.html',
  'selecoes.html': 'selecoes.html',
  'retro.html': 'retro.html',
  'player-version.html': 'player-version.html',
  'infantis.html': 'infantis.html',
  'lancamentos.html': 'lancamentos.html'
};

// Replace emoji spans in cat cards
const emojiMap = {
  '🇧🇷': svgIcons['brasileiros.html'],
  '🇪🇺': svgIcons['europeus.html'],
  '🌎': svgIcons['selecoes.html'],
  '🏆': svgIcons['retro.html'],
  '⭐': svgIcons['player-version.html'],
  '👦': svgIcons['infantis.html'],
  '🔥': svgIcons['lancamentos.html']
};

let count = 0;
for (const file of files) {
  const fp = path.join(dir, file);
  let c = fs.readFileSync(fp, 'utf8');
  let changed = false;

  // Replace emoji spans with SVG icons
  for (const [emoji, svg] of Object.entries(emojiMap)) {
    // Match <span>EMOJI</span> pattern in cat cards
    const re = new RegExp(`<span>${emoji.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}</span>`, 'g');
    if (re.test(c)) {
      c = c.replace(re, `<span class="cat-icon">${svg}</span>`);
      changed = true;
    }
  }

  if (changed) {
    fs.writeFileSync(fp, c, 'utf8');
    count++;
    console.log('Updated: ' + file);
  }
}
console.log('Done. ' + count + ' files updated.');
