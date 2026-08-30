"use client";

import { useEffect, useState } from "react";
import StorefrontApp from "../storefront-app";

export default function CatalogClient(){
  const [category,setCategory]=useState("Все товары");
  useEffect(()=>{
    setCategory(new URLSearchParams(window.location.search).get("category")||"Все товары");
  },[]);
  return <StorefrontApp initialView="catalog" initialCatalogCategory={category}/>;
}
