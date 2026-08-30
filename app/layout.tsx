import type { Metadata } from "next";
import "./globals.css";
import "./catalog-filters-v123.css";
import "./catalog-filters-kultura-v124.css";
import "./mobile-quick-add.css";
import "./product-media-scroll.css";
import "./product-card-gallery.css";
import "./boutique-drawer.css";
import "./mobile-pdp-overrides.css";
import "./zara-editorial.css";
import "./luna-editorial.css";
import "./collection-flow.css";
import "./editorial-magazine.css";
import "./ice-editorial-zara.css";
import "./editorial-story-overlay.css";
import "./constructor-entry.css";
import "./home-magazine-v2.css";
import "./home-commerce-v3.css";
import "./menu-zara-premium.css";
import "./home-v4.css";
import "./home-v4-traditions-collections.css";
import "./site-ux-polish-v1.css";
import "./home-reference-v5.css";
import "./home-ux-v6.css";
import "./home-ux-v7.css";
import "./home-ux-v8.css";
import "./home-ux-v9.css";
import "./home-togas-v10.css";
import "./home-ux-v11.css";
import "./home-ux-v11-mobile.css";
import "./home-video-v11.css";
import "./gift-wrap-flow.css";
import "./home-header-reference-v12.css";
import "./home-responsive-system-v13.css";
import "./home-card-type-v14.css";
import "./image-square-system-v15.css";
import "./collection-purchase-v16.css";
import "./cart-redesign-v17.css";
import "./cart-controls-v18.css";
import "./cart-controls-v19.css";
import "./auth-flow-v20.css";
import "./profile-address-book-v16.css";
import "./profile-address-book-order-v21.css";
import "./unified-stories-v52.css";
import "./commerce-zara-kultura-v41.css";
import "./commerce-hypotheses-v42.css";
import "./commerce-clarity-v43.css";
import "./home-zara-kultura-v44.css";
import "./home-sketch-v45.css";
import "./collections-v65.css";
import "./collections-zara-kultura-v66.css";
import "./mobile-cart-checkout-v67.css";
import "./one-screen-checkout-v68.css";
import "./cart-checkout-mockup-v69.css";
import "./cart-checkout-kultura-v78.css";
import "./editorial-commerce-v81.css";
import "./home-zara-togas-v86.css";
import "./checkout-kultura-v82.css";
import "./checkout-v83.css";
import "./checkout-bonus-v84.css";
import "./checkout-kultura-v85.css";
import "./truth-commerce.css";
import "./catalog-human-eye-v127.css";
import { ProductCardGalleryEnhancer } from "./product-card-gallery";
import { CollectionPurchaseEnhancer } from "./collection-purchase-enhancer";
import { ProfileAddressBookEnhancer } from "./profile-address-book";
import { HomeZaraTogasV86Enhancer } from "./home-zara-togas-v86-enhancer";
import { HomeReadySolutionsZaraV126Enhancer } from "./home-ready-solutions-zara-v126-enhancer";
import { TruthCommerceEnhancer } from "./truth-commerce-enhancer";

export const metadata: Metadata = {
  title: "Культура дома — премиальные товары для дома",
  description: "Текстиль, посуда и предметы для дома с русским характером.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ru">
      <body>
        <ProductCardGalleryEnhancer />
        <CollectionPurchaseEnhancer />
        <ProfileAddressBookEnhancer />
        <HomeZaraTogasV86Enhancer />
        <HomeReadySolutionsZaraV126Enhancer />
        <TruthCommerceEnhancer />
        {children}
      </body>
    </html>
  );
}
