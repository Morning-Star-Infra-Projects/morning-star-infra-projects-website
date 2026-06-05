#!/usr/bin/env node
// Sync master header and footer from index.html into all site HTML pages.
// Usage: node tools/sync-header-footer.js

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const indexPath = path.join(root, 'index.html');
const componentsDir = path.join(root, 'components');
if(!fs.existsSync(indexPath)){
  console.error('index.html not found at', indexPath);
  process.exit(1);
}
if(!fs.existsSync(componentsDir)) fs.mkdirSync(componentsDir, { recursive: true });

const html = fs.readFileSync(indexPath, 'utf8');

function extract(tag){
  const re = new RegExp(`<${tag}([\\s\\S]*?)<\\/${tag}>`, 'i');
  const m = html.match(re);
  if(!m) return null;
  return `<${tag}${m[1]}</${tag}>`;
}

const headerHtml = extract('header');
const footerHtml = extract('footer');
if(!headerHtml || !footerHtml){
  console.error('Could not extract header/footer from index.html');
  process.exit(1);
}

// Write components files (home remains source of truth, but components are convenient)
fs.writeFileSync(path.join(componentsDir, 'header.html'), headerHtml, 'utf8');
fs.writeFileSync(path.join(componentsDir, 'footer.html'), footerHtml, 'utf8');
console.log('Wrote components/header.html and components/footer.html');

// Recursively find .html files
function walkDir(dir, fileList){
  const files = fs.readdirSync(dir);
  files.forEach(f=>{
    const full = path.join(dir, f);
    const rel = path.relative(root, full).replace(/\\\\/g, '/');
    // skip components, node_modules, .git, assets, screenshots and backups
    if(rel.startsWith('components') || rel.startsWith('node_modules') || rel.startsWith('.git') || rel.startsWith('assets') || rel.startsWith('screenshots')) return;
    const stat = fs.statSync(full);
    if(stat.isDirectory()) walkDir(full, fileList);
    else if(stat.isFile() && f.endsWith('.html')) fileList.push(full);
  });
}

const files = [];
walkDir(root, files);

// Exclude index.html (home is source of truth)
const targetFiles = files.filter(p => path.basename(p).toLowerCase() !== 'index.html');

console.log('Found', targetFiles.length, 'HTML files to process');

let changed = 0;
let skipped = 0;

targetFiles.forEach(file=>{
  try{
    const content = fs.readFileSync(file, 'utf8');
    const headerRe = /<header[\s\S]*?<\/header>/i;
    const footerRe = /<footer[\s\S]*?<\/footer>/i;
    let out = content;
    let replaced = false;
    if(headerRe.test(content)){
      out = out.replace(headerRe, headerHtml);
      replaced = true;
    }
    if(footerRe.test(content)){
      out = out.replace(footerRe, footerHtml);
      replaced = true;
    }
    if(replaced){
      // backup original
      const bak = file + '.bak';
      if(!fs.existsSync(bak)) fs.copyFileSync(file, bak);
      else {
        const ts = Date.now();
        fs.copyFileSync(file, file + '.bak.' + ts);
      }
      fs.writeFileSync(file, out, 'utf8');
      changed++;
      console.log('Updated:', path.relative(root, file));
    } else skipped++;
  }catch(e){ console.error('Error processing', file, e); }
});

console.log('\nSummary:');
console.log('Updated files:', changed);
console.log('Skipped files:', skipped);
console.log('Backups saved with .bak or .bak.TIMESTAMP');
console.log('NOTE: Home page (index.html) remains the source of truth. Run this script after editing header/footer on the home page to propagate changes.');
