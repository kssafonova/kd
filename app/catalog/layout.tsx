import "../catalog-filters-v123.css";
import "../catalog-filters-kultura-v124.css";
import "../mobile-quick-add.css";
import "../product-media-scroll.css";
import "../product-card-gallery.css";
import "../boutique-drawer.css";
import "../mobile-pdp-overrides.css";
import "../zara-editorial.css";
import "../luna-editorial.css";
import "../collection-flow.css";
import "../editorial-magazine.css";
import "../ice-editorial-zara.css";
import "../editorial-story-overlay.css";
import "../constructor-entry.css";
import "../menu-zara-premium.css";
import "../site-ux-polish-v1.css";
import "../gift-wrap-flow.css";
import "../image-square-system-v15.css";
import "../collection-purchase-v16.css";
import "../cart-redesign-v17.css";
import "../cart-controls-v18.css";
import "../cart-controls-v19.css";
import "../auth-flow-v20.css";
import "../profile-address-book-v16.css";
import "../profile-address-book-order-v21.css";
import "../unified-stories-v52.css";
import "../commerce-zara-kultura-v41.css";
import "../commerce-hypotheses-v42.css";
import "../commerce-clarity-v43.css";
import "../collections-v65.css";
import "../collections-zara-kultura-v66.css";
import "../mobile-cart-checkout-v67.css";
import "../one-screen-checkout-v68.css";
import "../cart-checkout-mockup-v69.css";
import "../cart-checkout-kultura-v78.css";
import "../editorial-commerce-v81.css";
import "../checkout-kultura-v82.css";
import "../checkout-v83.css";
import "../checkout-bonus-v84.css";
import "../checkout-kultura-v85.css";
import "../truth-commerce.css";
import "../catalog-human-eye-v127.css";
import "../catalog-loading-state-v127.css";
import "../catalog-mobile-premium-v128.css";
import "../catalog-mobile-human-eye-v131.css";
import "../catalog-togas-v132.css";
import "../cart-checkout-human-eye-v136.css";
import { ProductCardGalleryEnhancer } from "../product-card-gallery";
import { CollectionPurchaseEnhancer } from "../collection-purchase-enhancer";
import { ProfileAddressBookEnhancer } from "../profile-address-book";
import { TruthCommerceEnhancer } from "../truth-commerce-enhancer";
import { CatalogLoadingStateV127 } from "../catalog-loading-state-v127";
import { CatalogTogasV132Enhancer } from "../catalog-togas-v132-enhancer";
import { CartCheckoutHumanEyeV136Enhancer } from "../cart-checkout-human-eye-v136-enhancer";

export default function CatalogLayout({children}:{children:React.ReactNode}){
  return <>
    <ProductCardGalleryEnhancer />
    <CollectionPurchaseEnhancer />
    <ProfileAddressBookEnhancer />
    <TruthCommerceEnhancer />
    <CatalogLoadingStateV127 />
    <CatalogTogasV132Enhancer />
    <CartCheckoutHumanEyeV136Enhancer />
    {children}
  </>;
}
