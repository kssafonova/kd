"use client";

import { useEffect, useRef, useState } from "react";
import type { ImgHTMLAttributes, SyntheticEvent } from "react";
import { assetUrl, isRemoteAsset } from "./assets";

type RemoteImageProps = Omit<ImgHTMLAttributes<HTMLImageElement>, "src"> & {
  src: string;
  fallbackSrc?: string;
};

export function RemoteImage({
  src,
  fallbackSrc = "/images/image-placeholder.svg",
  onError,
  ...props
}: RemoteImageProps) {
  const [resolvedSrc, setResolvedSrc] = useState(() => assetUrl(src));
  const [stage, setStage] = useState<"direct" | "fetch" | "fallback">("direct");
  const objectUrlRef = useRef<string | null>(null);

  useEffect(() => {
    if (objectUrlRef.current) {
      URL.revokeObjectURL(objectUrlRef.current);
      objectUrlRef.current = null;
    }
    setResolvedSrc(assetUrl(src));
    setStage("direct");

    return () => {
      if (objectUrlRef.current) {
        URL.revokeObjectURL(objectUrlRef.current);
        objectUrlRef.current = null;
      }
    };
  }, [src]);

  const requestImageByUrl = async () => {
    try {
      const response = await fetch(src, {
        method: "GET",
        mode: "cors",
        credentials: "omit",
        redirect: "follow",
        cache: "force-cache",
        referrerPolicy: "no-referrer",
      });

      if (!response.ok) {
        throw new Error(`Image request failed with ${response.status}`);
      }

      const contentType = response.headers.get("content-type") ?? "";
      if (contentType && !contentType.toLowerCase().startsWith("image/")) {
        throw new Error(`URL did not return an image: ${contentType}`);
      }

      const blob = await response.blob();
      if (!blob.size) throw new Error("Image response is empty");

      if (objectUrlRef.current) URL.revokeObjectURL(objectUrlRef.current);
      const objectUrl = URL.createObjectURL(blob);
      objectUrlRef.current = objectUrl;
      setResolvedSrc(objectUrl);
    } catch {
      setStage("fallback");
      setResolvedSrc(assetUrl(fallbackSrc));
    }
  };

  const handleError = (event: SyntheticEvent<HTMLImageElement, Event>) => {
    if (stage === "direct" && isRemoteAsset(src)) {
      setStage("fetch");
      void requestImageByUrl();
      return;
    }

    if (stage !== "fallback") {
      setStage("fallback");
      setResolvedSrc(assetUrl(fallbackSrc));
      return;
    }

    onError?.(event);
  };

  return (
    <img
      {...props}
      src={resolvedSrc}
      onError={handleError}
      data-image-source={src}
      data-image-stage={stage}
    />
  );
}
