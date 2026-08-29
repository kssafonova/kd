"use client";

import { useEffect, useState } from "react";
import Home from "../page";

export default function CatalogPage(){
  const [category,setCategory]=useState("Все товары");

  useEffect(()=>{
    setCategory(new URLSearchParams(window.location.search).get("category")||"Все товары");
  },[]);

  return <Home initialView="catalog" initialCatalogCategory={category}/>;
}
