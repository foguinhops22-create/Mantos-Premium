const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname);
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

// Old nav HTML with emojis (to remove from inner pages)
const oldNavPatterns = [
  { find: '🇧🇷 ', replace: '' },
  { find: '🇪🇺 ', replace: '' },
  { find: '🌎 ', replace: '' },
  { find: '🏆 ', replace: '' },
  { find: '⭐ ', replace: '' },
  { find: '👦 ', replace: '' },
  { find: '🔥 ', replace: '' },
];

let count = 0;
for (const file of files) {
  const filePath = path.join(dir, file);
  let content = fs.readFileSync(filePath, 'utf8');
  let changed = false;
  for (const { find, replace } of oldNavPatterns) {
    if (content.includes(find)) {
      content = content.split(find).join(replace);
      changed = true;
    }
  }
  if (changed) {
    fs.writeFileSync(filePath, content, 'utf8');
    count++;
    console.log('Updated: ' + file);
  }
}
console.log('Done. ' + count + ' files updated.');
