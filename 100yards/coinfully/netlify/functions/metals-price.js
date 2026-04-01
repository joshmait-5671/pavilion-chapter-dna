let cached = null;
let cachedAt = 0;
const CACHE_MS = 15 * 60 * 1000; // 15 minutes

exports.handler = async () => {
  const now = Date.now();

  if (cached && (now - cachedAt) < CACHE_MS) {
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=900' },
      body: JSON.stringify(cached)
    };
  }

  try {
    const apiKey = process.env.METALS_API_KEY || 'demo';
    const res = await fetch(`https://api.metals.dev/v1/latest?api_key=${apiKey}&currency=USD&unit=toz`);
    if (!res.ok) throw new Error('API error');
    const data = await res.json();

    cached = {
      gold: data.metals.gold,
      silver: data.metals.silver,
      timestamp: new Date().toISOString()
    };
    cachedAt = now;

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=900' },
      body: JSON.stringify(cached)
    };
  } catch (e) {
    // Hardcoded fallback if API fails
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gold: 3087, silver: 34.21, timestamp: new Date().toISOString(), fallback: true })
    };
  }
};
