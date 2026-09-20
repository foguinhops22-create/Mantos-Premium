const fs = require('fs');
const path = require('path');
const dir = path.join(__dirname);
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
let count = 0;
for (const file of files) {
  const fp = path.join(dir, file);
  let c = fs.readFileSync(fp, 'utf8');
  if (c.includes('href="style.css"')) {
    c = c.replace(/href="style\.css"/g, 'href="style.css?v=3"');
    fs.writeFileSync(fp, c, 'utf8');
    count++;
  }
}
console.log('Updated ' + count + ' files');
