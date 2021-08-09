export enum SupermarketSource {
  Marketin = "Marketin",
  Lidl = "Lidl",
}
export class AddDealDto {
  link: string;
  image_url: string;
  title: string;
  old_price: string;
  new_price: string;
  discount_details: string;
  label: string;
  source:SupermarketSource;
}
