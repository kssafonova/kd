export type PresetStatus = "required" | "default" | "optional";

export type PresetRow = {
  scenario_id: string;
  scenario_name: string;
  domain: string;
  default_guests: string;
  sort_order: string;
  offer_id: string;
  group_id: string;
  collection: string;
  product_name: string;
  product_type: string;
  preset_status: PresetStatus;
  default_quantity: string;
  quantity_rule: string;
  variant_selection_required: string;
  price_rub: string;
  product_url: string;
  primary_image_url: string;
  selection_reason: string;
};

export type CandidateRow = {
  scenario_id: string;
  scenario_name: string;
  role: string;
  preset_status: string;
  candidate_rank: string;
  is_recommended: string;
  offer_id: string;
  vendor_code: string;
  collection: string;
  product_name: string;
  product_type: string;
  price_rub: string;
  old_price_rub: string;
  color: string;
  size: string;
  material: string;
  product_url: string;
  primary_image_url: string;
  all_image_urls: string;
  palette: string;
  style_tags: string;
};

export type ScenarioMetaRow = {
  scenario_id: string;
  scenario_name: string;
  occasion: string;
  guests_supported: string;
  lead_collection_slug: string;
  allowed_collections: string;
  role: string;
  preset_status: string;
  quantity_rule: string;
  entry_collection: string;
  styling_message: string;
};

export type ExpansionRuleRow = {
  scenario_id: string;
  scenario_name: string;
  space: string;
  occasion: string;
  guests_supported: string;
  lead_collections: string;
  allowed_collections: string;
  role: string;
  allowed_product_types: string;
  preset_status: string;
  quantity_rule: string;
  flow_step: string;
  styling_message: string;
};

export type ExpansionPatchRow = {
  scenario_id: string;
  role: string;
  allowed_product_types: string;
  preset_status: string;
};

export type CatalogRow = {
  offer_id: string;
  group_id: string;
  vendor_code: string;
  collection: string;
  product_name: string;
  product_url: string;
  product_type: string;
  constructor_role: string;
  mix_role: string;
  builder_domain: string;
  palette: string;
  style_tags: string;
  price: string;
  old_price: string;
  color: string;
  size: string;
  material: string;
  volume: string;
  availability_status: string;
  primary_image_url: string;
  all_image_urls: string;
};

export type ConstructorData = {
  presets: PresetRow[];
  candidates: CandidateRow[];
  scenarios: ScenarioMetaRow[];
  catalog: CatalogRow[];
  expansionRules: ExpansionRuleRow[];
  expansionPatches: ExpansionPatchRow[];
};

export type SlotState = {
  key: string;
  enabled: boolean;
  replacementOfferId?: string;
  selectedVariantOfferId?: string;
};

export type ProductView = {
  key: string;
  preset: PresetRow;
  sourceOfferId: string;
  offerId: string;
  groupId: string;
  name: string;
  collection: string;
  productType: string;
  productUrl: string;
  primaryImageUrl: string;
  images: string[];
  color: string;
  size: string;
  material: string;
  availabilityStatus: string;
  status: PresetStatus;
  quantityRule: string;
  quantity: number;
  enabled: boolean;
  variantRequired: boolean;
  variantSelected: boolean;
  price: number | null;
  displayPrice: number | null;
  oldPrice: number | null;
  selectionReason: string;
};

export type CartPayloadItem = {
  offer_id: string;
  quantity: number;
};
