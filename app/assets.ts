const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

export const assetUrl = (path: string) =>
  path.startsWith("/images/") ? `${BASE_PATH}${path}` : path;
