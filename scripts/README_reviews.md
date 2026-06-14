Google Reviews fetcher
======================

This repository includes a small helper to fetch Google Places reviews and cache them to `data/reviews.json` for use by the static site.

Usage (server-side, recommended):

1. Create a Google Cloud project and enable the Places API. Obtain an API key.
2. On your development machine or server run:

```powershell
$env:GOOGLE_API_KEY = "YOUR_KEY"
node scripts/fetch-google-reviews.js "PLACE_ID"
```

Replace `PLACE_ID` with the Place ID of the business (use the Place ID Finder or the Places API).

The script will write `data/reviews.json`. The client-side widget (`/assets/js/google-reviews.js`) will attempt to fetch `/data/reviews.json` and fall back to `/data/reviews.sample.json` if not present.

Notes:
- Do NOT embed your API key in client-side code — fetch reviews server-side and cache the results.
- If you host the static site via a server (Netlify, Vercel, static server), ensure `/data/reviews.json` is served publicly.
