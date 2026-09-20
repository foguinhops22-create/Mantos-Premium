const fs = require('fs');
const path = require('path');
const dir = path.join(__dirname);
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
let count = 0;
for (const file of files) {
  const fp = path.join(dir, file);
  let c = fs.readFileSync(fp, 'utf8');
  if (c.includes('style.css?v=')) {
    c = c.replace(/style\.css\?v=\d+/g, 'style.css?v=6');
    fs.writeFileSync(fp, c, 'utf8');
    count++;
  }
}
console.log('Updated ' + count);
