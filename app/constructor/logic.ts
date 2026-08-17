import type {
  CandidateRow,
  CartPayloadItem,
  CatalogRow,
  ConstructorData,
  PresetRow,
  ProductView,
  SlotState,
} from "./types";

export const toNumber = (value: unknown): number | null => {
  const normalized = String(value ?? "").trim().replace(/\s/g, "").replace(",", ".");
  if (!normalized) return null;
  const parsed = Number(normalized);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : null;
};

export const toBoolean = (value: unknown) =>
  ["true", "1", "yes", "да"].includes(String(value ?? "").trim().toLowerCase());

export const formatRub = (value: number) =>
  `${new Intl.NumberFormat("ru-RU").format(Math.round(value))} ₽`;

export const splitImages = (value: string | undefined) =>
  Array.from(
    new Set(
      String(value ?? "")
        .split("|")
        .map((item) => item.trim())
        .filter((item) => item.startsWith("https://")),
    ),
  );

export const isUnavailable = (value: string | undefined) => {
  const status = String(value ?? "").trim().toLowerCase();
  if (!status || status === "unknown_from_feed") return false;
  return [
    "out_of_stock",
    "unavailable",
    "not_available",
    "sold_out",
    "нет в наличии",
    "отсутствует",
  ].some((token) => status.includes(token));
};

export const computeQuantity = (preset: PresetRow, guests: number) => {
  const base = Number(preset.default_quantity) || 1;
  if (preset.quantity_rule !== "per_guest") return Math.max(1, Math.round(base));
  const defaultGuests = Number(preset.default_guests) || 2;
  return Math.max(1, Math.round((base * guests) / defaultGuests));
};

export const productTypesCompatible = (sourceType: string, candidateType: string) => {
  if (["tea_pair", "coffee_pair"].includes(sourceType)) {
    return ["tea_pair", "coffee_pair"].includes(candidateType);
  }
  return sourceType === candidateType;
};

export const createIndexes = (data: ConstructorData) => {
  const catalogByOffer = new Map(data.catalog.map((row) => [String(row.offer_id), row]));
  const catalogByGroup = new Map<string, CatalogRow[]>();
  data.catalog.forEach((row) => {
    const groupId = String(row.group_id || row.offer_id || "");
    if (!groupId) return;
    const list = catalogByGroup.get(groupId) ?? [];
    list.push(row);
    catalogByGroup.set(groupId, list);
  });
  const candidateByOffer = new Map(data.candidates.map((row) => [String(row.offer_id), row]));
  return { catalogByOffer, catalogByGroup, candidateByOffer };
};

export type ConstructorIndexes = ReturnType<typeof createIndexes>;

const resolveCatalog = (offerId: string, indexes: ConstructorIndexes) =>
  indexes.catalogByOffer.get(String(offerId));

export const getReplacementCandidates = (
  scenarioId: string,
  sourceProductType: string,
  currentOfferId: string,
  data: ConstructorData,
) =>
  data.candidates.filter(
    (candidate) =>
      candidate.scenario_id === scenarioId &&
      String(candidate.offer_id) !== String(currentOfferId) &&
      productTypesCompatible(sourceProductType, candidate.product_type),
  );

export const getVariantOptions = (
  preset: PresetRow,
  slot: SlotState,
  indexes: ConstructorIndexes,
) => {
  if (!toBoolean(preset.variant_selection_required)) return [];
  const activeOfferId = String(slot.replacementOfferId || preset.offer_id);
  const activeCatalog = resolveCatalog(activeOfferId, indexes);
  const groupId = String(activeCatalog?.group_id || preset.group_id || activeOfferId);
  return (indexes.catalogByGroup.get(groupId) ?? [])
    .filter((row) => row.product_type === (activeCatalog?.product_type || preset.product_type))
    .filter((row) => Boolean(row.size?.trim()))
    .sort(
      (left, right) =>
        (toNumber(left.price) ?? Number.MAX_SAFE_INTEGER) -
        (toNumber(right.price) ?? Number.MAX_SAFE_INTEGER),
    );
};

export const deriveProductView = (
  preset: PresetRow,
  slot: SlotState,
  guests: number,
  indexes: ConstructorIndexes,
): ProductView => {
  const replacement = slot.replacementOfferId
    ? indexes.candidateByOffer.get(String(slot.replacementOfferId))
    : undefined;

  const sourceOfferId = String(replacement?.offer_id || preset.offer_id);
  const baseCatalog = resolveCatalog(sourceOfferId, indexes);
  const selectedVariant = slot.selectedVariantOfferId
    ? resolveCatalog(String(slot.selectedVariantOfferId), indexes)
    : undefined;
  const effectiveCatalog = selectedVariant || baseCatalog;
  const variantRequired = toBoolean(preset.variant_selection_required);
  const variantSelected = !variantRequired || Boolean(selectedVariant);

  const catalogPrimary = effectiveCatalog?.primary_image_url || baseCatalog?.primary_image_url || "";
  const candidatePrimary = replacement?.primary_image_url || "";
  const presetPrimary = preset.primary_image_url || "";
  const primaryImageUrl = [catalogPrimary, candidatePrimary, presetPrimary]
    .find((url) => url.startsWith("https://")) || "";
  const images = Array.from(
    new Set([
      primaryImageUrl,
      ...splitImages(effectiveCatalog?.all_image_urls || baseCatalog?.all_image_urls),
      ...splitImages(replacement?.all_image_urls),
    ].filter(Boolean)),
  );

  const fallbackPrice = toNumber(replacement?.price_rub || preset.price_rub);
  const catalogPrice = toNumber(effectiveCatalog?.price || baseCatalog?.price);
  const displayPrice = catalogPrice ?? fallbackPrice;
  const price = variantRequired && !variantSelected ? null : displayPrice;
  const oldPrice = toNumber(
    effectiveCatalog?.old_price || replacement?.old_price_rub || baseCatalog?.old_price,
  );

  return {
    key: slot.key,
    preset,
    sourceOfferId,
    offerId: String(selectedVariant?.offer_id || sourceOfferId),
    groupId: String(
      effectiveCatalog?.group_id || baseCatalog?.group_id || preset.group_id || sourceOfferId,
    ),
    name:
      effectiveCatalog?.product_name ||
      replacement?.product_name ||
      baseCatalog?.product_name ||
      preset.product_name,
    collection:
      effectiveCatalog?.collection ||
      replacement?.collection ||
      baseCatalog?.collection ||
      preset.collection,
    productType:
      effectiveCatalog?.product_type ||
      replacement?.product_type ||
      baseCatalog?.product_type ||
      preset.product_type,
    productUrl:
      [
        effectiveCatalog?.product_url,
        replacement?.product_url,
        baseCatalog?.product_url,
        preset.product_url,
      ].find((url) => String(url ?? "").startsWith("https://")) || "",
    primaryImageUrl,
    images,
    color: effectiveCatalog?.color || replacement?.color || baseCatalog?.color || "",
    size:
      selectedVariant?.size ||
      (!variantRequired
        ? effectiveCatalog?.size || replacement?.size || baseCatalog?.size || ""
        : ""),
    material:
      effectiveCatalog?.material || replacement?.material || baseCatalog?.material || "",
    availabilityStatus:
      effectiveCatalog?.availability_status || baseCatalog?.availability_status || "unknown_from_feed",
    status: preset.preset_status,
    quantityRule: preset.quantity_rule,
    quantity: computeQuantity(preset, guests),
    enabled: slot.enabled,
    variantRequired,
    variantSelected,
    price,
    displayPrice,
    oldPrice: oldPrice && displayPrice && oldPrice > displayPrice ? oldPrice : null,
    selectionReason: preset.selection_reason,
  };
};

export const calculateSummary = (views: ProductView[]) => {
  let total = 0;
  let oldTotal = 0;
  let units = 0;
  let positions = 0;

  views.forEach((view) => {
    if (!view.enabled) return;
    positions += 1;
    units += view.quantity;
    if (!view.price || isUnavailable(view.availabilityStatus)) return;
    total += view.price * view.quantity;
    oldTotal += (view.oldPrice || view.price) * view.quantity;
  });

  return { total, oldTotal, savings: Math.max(0, oldTotal - total), units, positions };
};

export const getBlockingReasons = (views: ProductView[]) => {
  const reasons: string[] = [];
  views.filter((view) => view.enabled).forEach((view) => {
    if (view.variantRequired && !view.variantSelected) {
      reasons.push(`Выберите размер для «${view.name}».`);
    }
    if (!view.price && !(view.variantRequired && !view.variantSelected)) {
      reasons.push(`Для «${view.name}» цена уточняется.`);
    }
    if (isUnavailable(view.availabilityStatus)) {
      reasons.push(
        view.status === "required"
          ? `Обязательный товар «${view.name}» недоступен — выберите замену.`
          : `«${view.name}» недоступен — замените или отключите позицию.`,
      );
    }
  });
  return Array.from(new Set(reasons));
};

export const buildCartPayload = (views: ProductView[]): CartPayloadItem[] => {
  const aggregated = new Map<string, number>();
  views.forEach((view) => {
    if (!view.enabled || !view.price || isUnavailable(view.availabilityStatus)) return;
    if (view.variantRequired && !view.variantSelected) return;
    aggregated.set(view.offerId, (aggregated.get(view.offerId) ?? 0) + view.quantity);
  });
  return Array.from(aggregated, ([offer_id, quantity]) => ({ offer_id, quantity }));
};

export const trackConstructorEvent = (
  event: string,
  detail: Record<string, unknown> = {},
) => {
  const payload = { event, ...detail };
  console.info("[constructor]", payload);
  if (typeof window === "undefined") return;
  window.dispatchEvent(new CustomEvent("kd:constructor", { detail: payload }));
  const layer = (window as Window & { dataLayer?: Record<string, unknown>[] }).dataLayer;
  layer?.push(payload);
};
