import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Read API_BASE_URL from environment variables, default to empty string for relative paths
const apiBaseUrl = process.env.API_BASE_URL || '';

const configContent = `// Aethel AI Frontend Configuration
// Generated automatically - do not modify manually
window.APP_CONFIG = {
  API_BASE_URL: ${JSON.stringify(apiBaseUrl)}
};
`;

try {
  fs.writeFileSync(path.join(__dirname, 'public', 'config.js'), configContent);
  console.log(`[build-config] Successfully generated public/config.js with API_BASE_URL: "${apiBaseUrl}"`);
} catch (err) {
  console.error('[build-config] Failed to write public/config.js:', err);
  process.exit(1);
}
