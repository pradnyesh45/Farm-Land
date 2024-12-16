export interface Schedule {
  id: number;
  farm_id: number;
  days_after_sowing: number;
  fertilizer_type: string;
  quantity: number;
  quantity_unit: string;
}

export interface DueSchedules {
  today_tomorrow: Schedule[];
}

export interface ScheduleResponse {
  data: {
    today_tomorrow: Schedule[];
  };
}
