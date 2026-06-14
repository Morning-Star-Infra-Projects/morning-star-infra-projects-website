#!/usr/bin/env node
// Scan images under assets/images and propose SEO-friendly filenames.
// Usage: node scripts/generate-image-rename-suggestions.js > image-rename-suggestions.csv

const fs = require('fs');
const path = require('path');

function slugify(name){
  return name.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,'');
}

function suggest(filePath){
  const parts = filePath.split(path.sep);
  // try to extract category from path segments e.g., optimized/Commercial and industrial/...
  const idx = parts.findIndex(p => /optimized|images/i.test(p));
  const filename = parts[parts.length-1];
  const base = path.parse(filename).name;
  const ext = path.parse(filename).ext || '.webp';
  const category = parts[parts.length-2] || '';
  let primary = base;
  // clean numbers and sizes
  primary = primary.replace(/[_\s]+/g,' ').replace(/-\d{3,4}$/,'').trim();
  const slug = slugify(`${primary} ${category} chennai morning star infra projects`);
  return slug + ext.toLowerCase();
}

function walk(dir){
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const fp = path.join(dir,file);
    const stat = fs.statSync(fp);
    if(stat && stat.isDirectory()) results = results.concat(walk(fp)); else results.push(fp);
  });
  return results;
}

const imagesDir = path.join(__dirname,'..','assets','images');
if(!fs.existsSync(imagesDir)){
  console.error('assets/images not found'); process.exit(1);
}

const files = walk(imagesDir).filter(f => /\.(jpe?g|png|webp|avif)$/i.test(f));
console.log('original_path,new_name');
files.forEach(f => {
  const rel = path.relative(process.cwd(), f).replace(/\\/g,'/');
  console.log(`${rel},${suggest(f)}`);
});
