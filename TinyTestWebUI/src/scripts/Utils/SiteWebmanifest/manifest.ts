import { getEnvironment } from "@/components/WithAppProps";

export default async function generateSiteWebmanifest(): Promise<string> {
  `
  "icons": [
    {
      "src": "/android-chrome-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/android-chrome-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "theme_color": "#FFF603",
  "background_color": "#FFF603",
  `;
  const json = JSON.parse(`{
  "name": "TinyTest",
  "short_name": "TinyTest",
  "description": "A distributed testing program for chess engines.",
  "start_url": "/",
  
  "display": "standalone"
}`);
  json.name = json.short_name = `TinyTest${(() => {
    switch (getEnvironment()) {
      case "development": {
        return " Development";
      }
      case "preview": {
        return " Beta";
      }
      default:
      case "production": {
        return "";
      }
    }
  })()}`;
  return JSON.stringify(json, undefined, 2);
}
