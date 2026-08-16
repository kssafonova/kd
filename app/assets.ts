const ASSET_ORIGIN = "https://kultura-doma-premium.micromaaash.chatgpt.site";

export const assetUrl = (path: string) =>
  path.startsWith("/images/") ? `${ASSET_ORIGIN}${path}` : path;
