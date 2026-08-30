import type { Metadata } from "next";
import "./globals.css";

export const metadata:Metadata={
  title:"Культура дома — премиальные товары для дома",
  description:"Текстиль, посуда и предметы для дома с русским характером.",
};

export default function RootLayout({children}:{children:React.ReactNode}){
  return <html lang="ru"><body>{children}</body></html>;
}
