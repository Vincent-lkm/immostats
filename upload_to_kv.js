#!/usr/bin/env node
/**
 * Upload data to Cloudflare KV
 */

const fs = require('fs');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

async function uploadToKV() {
  console.log('📤 Upload des données vers Cloudflare KV...');

  // Lire les données
  const data = JSON.parse(fs.readFileSync('output/kv_data.json', 'utf8'));

  // Upload top_cities
  console.log('   Uploading top_cities...');
  await execPromise(`echo '${JSON.stringify(data.top_cities)}' | wrangler kv:key put --binding=DATA_KV "top_cities"`);

  // Upload all_cities
  console.log('   Uploading all_cities list...');
  await execPromise(`echo '${JSON.stringify(data.all_cities)}' | wrangler kv:key put --binding=DATA_KV "all_cities"`);

  // Upload each city
  console.log(`   Uploading ${data.cities.length} city data...`);
  for (const city of data.cities) {
    const key = `city:${city.code}`;
    const value = JSON.stringify(city.data);

    // Write to temp file to avoid shell escaping issues
    fs.writeFileSync('/tmp/city_data.json', value);
    await execPromise(`wrangler kv:key put --binding=DATA_KV "${key}" --path=/tmp/city_data.json`);
    console.log(`     ✓ ${city.data.name} (${city.code})`);
  }

  console.log('✅ Upload terminé!');
}

uploadToKV().catch(console.error);