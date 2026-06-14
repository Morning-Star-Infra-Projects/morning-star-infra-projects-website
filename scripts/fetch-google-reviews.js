#!/usr/bin/env node
// Simple script to fetch Google Place Details (reviews) and cache to data/reviews.json
// Usage: set GOOGLE_API_KEY=your_key && node fetch-google-reviews.js PLACE_ID
// Requires Node 18+ (fetch available) or install node-fetch.

const fs = require('fs');
const path = require('path');

async function main() {
  const apiKey = process.env.GOOGLE_API_KEY;
  const placeId = process.argv[2];
  if (!apiKey || !placeId) {
    console.error('Usage: GOOGLE_API_KEY=KEY node fetch-google-reviews.js PLACE_ID');
    process.exit(1);
  }

  const url = `https://maps.googleapis.com/maps/api/place/details/json?place_id=${placeId}&fields=name,rating,user_ratings_total,reviews&key=${apiKey}`;
  console.log('Fetching reviews from Google Places...');

  try {
    const res = await fetch(url);
    const data = await res.json();
    if (data.status !== 'OK') {
      console.error('Google API error:', data.status, data.error_message || '');
      process.exit(1);
    }
    const outDir = path.join(__dirname, '..', 'data');
    if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
    const outPath = path.join(outDir, 'reviews.json');
    fs.writeFileSync(outPath, JSON.stringify(data.result.reviews || [], null, 2));
    console.log('Wrote', outPath);
  } catch (err) {
    console.error('Fetch failed', err);
    process.exit(1);
  }
}

main();
