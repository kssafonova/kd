import type { Metadata } from "next";
import "./globals.css";
import "./kultura-design-system-v160.css";

export const metadata:Metadata={
  title:"Культура дома — премиальные товары для дома",
  description:"Текстиль, посуда и предметы для дома с русским характером.",
};

export default function RootLayout({children}:{children:React.ReactNode}){
  return <html lang="ru"><head><link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous"/><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Tenor+Sans&display=swap"/></head><body>{children}</body></html>;
}
