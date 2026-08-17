const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

const normalizeAssetPath = (path: string) => (path ?? "").trim();

export const isRemoteAsset = (path: string) => /^https?:\/\//i.test(normalizeAssetPath(path));

export const assetUrl = (path: string) => {
  const value = normalizeAssetPath(path);
  if (!value) return "";
  if (isRemoteAsset(value) || value.startsWith("data:") || value.startsWith("blob:")) return value;
  return value.startsWith("/images/") ? `${BASE_PATH}${value}` : value;
};
