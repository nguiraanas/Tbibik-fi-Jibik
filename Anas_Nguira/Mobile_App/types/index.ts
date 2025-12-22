export type VehicleType = 'Sedan' | 'SUV' | 'Truck' | 'Van';

export type SpeedUnit = 'km/h' | 'mph';

export interface User {
  id: string;
  firstName: string;
  surname: string;
  username: string;
  age: string;
  emergencyContact: string;
  speedUnit: SpeedUnit;
  createdAt: string;
}

export interface Vehicle {
  id: string;
  userId: string;
  vehicleType: VehicleType;
  model: string;
  yearOfManufacture: string;
  tireCondition: string;
  brakeCondition: string;
  lastOilChangeDate: string;
  createdAt: string;
}

export interface SpeedData {
  timestamp: number;
  userSpeed: number;
  recommendedSpeed: number;
}

export interface Ride {
  id: string;
  userId: string;
  vehicleId: string;
  startTime: string;
  endTime?: string;
  speedData: SpeedData[];
  points: number;
  averageSpeed: number;
  recommendedAverageSpeed: number;
}

export interface MaintenanceLog {
  id: string;
  vehicleId: string;
  type: 'oil_change' | 'tire_pressure' | 'brake_check' | 'other';
  description: string;
  date: string;
  createdAt: string;
}

export interface MaintenanceAlert {
  id: string;
  vehicleId: string;
  type: 'oil_change' | 'tire_pressure' | 'brake_check';
  message: string;
  dueDate: string;
  isRead: boolean;
  createdAt: string;
}

export type Theme = 'default' | 'elderly';
