declare module "*.png";
declare module "*.jpg";

declare module "*.svg" {
  const url: string;
  export const ReactComponent: import("react").ComponentType<import("react").ComponentProps<
    "svg"
  >>;
  export default url;
}
