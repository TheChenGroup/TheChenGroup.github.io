import type { ImageMetadata } from "astro";

export async function getImageMetadata(
  image: string | ImageMetadata,
): Promise<ImageMetadata> {
  if (typeof image !== "string") return image;
  const images = import.meta.glob<{ default: ImageMetadata }>(
    "/src/images/**/*",
  );
  const moduleFunc =
    images[image.replace(/^(\.\.\/)+images/, "src/images")] ??
    images["/src/images/" + image] ??
    images["/src/images/geee_icon.svg"];
  return (await moduleFunc()).default;
}
