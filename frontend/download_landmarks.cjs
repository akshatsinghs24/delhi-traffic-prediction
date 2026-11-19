const fs = require('fs');
const path = require('path');

const outDir = path.join(__dirname, 'public', 'landmarks');

async function searchAndDownload(filename, searchQuery, overwrite = false) {
  const dest = path.join(outDir, filename);
  if (!overwrite && fs.existsSync(dest) && fs.statSync(dest).size > 1000) {
    console.log(`Already have ${filename} (${fs.statSync(dest).size} bytes)`);
    return;
  }
  const s = encodeURIComponent(searchQuery);
  const apiUrl = `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=${s}&gsrnamespace=6&gsrlimit=10&prop=imageinfo&iiprop=url&format=json`;
  
  console.log(`Searching for "${searchQuery}"...`);
  try {
    const res = await fetch(apiUrl, {
      headers: {
        'User-Agent': 'TrafficSenseDelhiBot/1.0 (admin@trafficsense.local)'
      }
    });
    const data = await res.json();
    if (!data.query || !data.query.pages) {
      console.log(`No results for ${searchQuery}`);
      return;
    }
    const pageKeys = Object.keys(data.query.pages);
    for (const key of pageKeys) {
      const page = data.query.pages[key];
      if (page.imageinfo && page.imageinfo[0] && page.imageinfo[0].url) {
        const rawUrl = page.imageinfo[0].url;
        const cleanUrl = rawUrl.split('?')[0];
        if (!cleanUrl.match(/\.(jpg|jpeg|png|webp)$/i)) continue;
        console.log(`Downloading ${filename} from ${rawUrl}...`);
        const imgRes = await fetch(rawUrl, {
          headers: {
            'User-Agent': 'TrafficSenseDelhiBot/1.0 (admin@trafficsense.local)'
          }
        });
        if (imgRes.ok) {
          const buf = Buffer.from(await imgRes.arrayBuffer());
          fs.writeFileSync(dest, buf);
          console.log(`SUCCESS: Saved ${filename} (${buf.length} bytes)`);
          return;
        }
      }
    }
  } catch (err) {
    console.error(`Error ${filename}:`, err);
  }
}

async function main() {
  await searchAndDownload('akshardham.jpg', 'Akshardham temple Delhi', true);
  await searchAndDownload('barapullah.jpg', 'Delhi elevated corridor flyover', true);
  await searchAndDownload('dhaula_kuan.jpg', 'Delhi Dhaula Kuan flyover', true);
}

main();
