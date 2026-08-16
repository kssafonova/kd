import type { Metadata } from "next";
import "./globals.css";
import "./mobile-quick-add.css";
import "./product-media-scroll.css";
import "./boutique-drawer.css";
import "./mobile-pdp-overrides.css";
import "./zara-editorial.css";

export const metadata: Metadata = {
  title: "Культура дома — премиальные товары для дома",
  description: "Текстиль, посуда и предметы для дома с русским характером.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ru">
      <body>{children}</body>
    </html>
  );
}
