import type { Metadata } from "next";
import "./globals.css";
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
import { ProductCardGalleryEnhancer } from "./product-card-gallery";

export const metadata: Metadata = {
  title: "Культура дома — премиальные товары для дома",
  description: "Текстиль, посуда и предметы для дома с русским характером.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ru">
      <body>
        <ProductCardGalleryEnhancer />
        {children}
      </body>
    </html>
  );
}