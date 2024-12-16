export interface Farmer {
  id: number;
  name: string;
  phone_number: string;
  language: string;
}

export interface FarmBill {
  area: number;
  cost: number;
  crop: string;
  farm_id: number;
  fertilizer_type: string;
  quantity: number;
  quantity_unit: string;
  village: string;
}

export interface FarmerBill {
  farmer_id: number;
  farmer_name: string;
  farms: FarmBill[];
  total_cost: number;
}
