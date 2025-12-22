import createContextHook from '@nkzw/create-context-hook';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useState, useEffect } from 'react';
import {
  User,
  Vehicle,
  Ride,
  MaintenanceLog,
  MaintenanceAlert,
  Theme,
  SpeedData,
} from '@/types';

export const [AppProvider, useApp] = createContextHook(() => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [currentVehicle, setCurrentVehicle] = useState<Vehicle | null>(null);
  const [rides, setRides] = useState<Ride[]>([]);
  const [maintenanceLogs, setMaintenanceLogs] = useState<MaintenanceLog[]>([]);
  const [maintenanceAlerts, setMaintenanceAlerts] = useState<MaintenanceAlert[]>([]);
  const [theme, setTheme] = useState<Theme>('default');
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const userData = await AsyncStorage.getItem('user');
      const vehiclesData = await AsyncStorage.getItem('vehicles');
      const ridesData = await AsyncStorage.getItem('rides');
      const maintenanceLogsData = await AsyncStorage.getItem('maintenanceLogs');
      const maintenanceAlertsData = await AsyncStorage.getItem('maintenanceAlerts');
      const themeData = await AsyncStorage.getItem('theme');
      const currentVehicleData = await AsyncStorage.getItem('currentVehicle');

      if (userData) {
        const user = JSON.parse(userData);
        setCurrentUser(user);
        setIsAuthenticated(true);
      }
      if (vehiclesData) setVehicles(JSON.parse(vehiclesData));
      if (ridesData) setRides(JSON.parse(ridesData));
      if (maintenanceLogsData) setMaintenanceLogs(JSON.parse(maintenanceLogsData));
      if (maintenanceAlertsData) setMaintenanceAlerts(JSON.parse(maintenanceAlertsData));
      if (themeData) setTheme(JSON.parse(themeData) as Theme);
      if (currentVehicleData) setCurrentVehicle(JSON.parse(currentVehicleData));
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const signUp = async (userData: Omit<User, 'id' | 'createdAt'>) => {
    try {
      const newUser: User = {
        ...userData,
        id: Date.now().toString(),
        createdAt: new Date().toISOString(),
      };
      await AsyncStorage.setItem('user', JSON.stringify(newUser));
      setCurrentUser(newUser);
      setIsAuthenticated(true);
      return newUser;
    } catch (error) {
      console.error('Error signing up:', error);
      throw error;
    }
  };

  const login = async (username: string, password: string) => {
    try {
      const userData = await AsyncStorage.getItem('user');
      if (userData) {
        const user = JSON.parse(userData);
        setCurrentUser(user);
        setIsAuthenticated(true);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error logging in:', error);
      return false;
    }
  };

  const logout = async () => {
    try {
      setCurrentUser(null);
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  const addVehicle = async (vehicleData: Omit<Vehicle, 'id' | 'userId' | 'createdAt'>) => {
    try {
      const newVehicle: Vehicle = {
        ...vehicleData,
        id: Date.now().toString(),
        userId: currentUser?.id || '',
        createdAt: new Date().toISOString(),
      };
      const updatedVehicles = [...vehicles, newVehicle];
      await AsyncStorage.setItem('vehicles', JSON.stringify(updatedVehicles));
      setVehicles(updatedVehicles);
      if (!currentVehicle) {
        setCurrentVehicle(newVehicle);
        await AsyncStorage.setItem('currentVehicle', JSON.stringify(newVehicle));
      }
      return newVehicle;
    } catch (error) {
      console.error('Error adding vehicle:', error);
      throw error;
    }
  };

  const updateVehicle = async (vehicleId: string, updates: Partial<Vehicle>) => {
    try {
      const updatedVehicles = vehicles.map((v) =>
        v.id === vehicleId ? { ...v, ...updates } : v
      );
      await AsyncStorage.setItem('vehicles', JSON.stringify(updatedVehicles));
      setVehicles(updatedVehicles);
      if (currentVehicle?.id === vehicleId) {
        const updated = { ...currentVehicle, ...updates };
        setCurrentVehicle(updated);
        await AsyncStorage.setItem('currentVehicle', JSON.stringify(updated));
      }
    } catch (error) {
      console.error('Error updating vehicle:', error);
      throw error;
    }
  };

  const selectVehicle = async (vehicle: Vehicle) => {
    try {
      setCurrentVehicle(vehicle);
      await AsyncStorage.setItem('currentVehicle', JSON.stringify(vehicle));
    } catch (error) {
      console.error('Error selecting vehicle:', error);
    }
  };

  const startRide = async (vehicleId: string) => {
    try {
      const newRide: Ride = {
        id: Date.now().toString(),
        userId: currentUser?.id || '',
        vehicleId,
        startTime: new Date().toISOString(),
        speedData: [],
        points: 0,
        averageSpeed: 0,
        recommendedAverageSpeed: 0,
      };
      const updatedRides = [...rides, newRide];
      await AsyncStorage.setItem('rides', JSON.stringify(updatedRides));
      setRides(updatedRides);
      return newRide;
    } catch (error) {
      console.error('Error starting ride:', error);
      throw error;
    }
  };

  const addSpeedData = async (rideId: string, speedData: SpeedData) => {
    try {
      const updatedRides = rides.map((r) => {
        if (r.id === rideId) {
          const newSpeedData = [...r.speedData, speedData];
          const points = calculatePoints(speedData, r.points);
          return { ...r, speedData: newSpeedData, points };
        }
        return r;
      });
      await AsyncStorage.setItem('rides', JSON.stringify(updatedRides));
      setRides(updatedRides);
    } catch (error) {
      console.error('Error adding speed data:', error);
    }
  };

  const calculatePoints = (speedData: SpeedData, currentPoints: number): number => {
    const speedDiff = Math.abs(speedData.userSpeed - speedData.recommendedSpeed);
    if (speedDiff <= 5) {
      return currentPoints + 10;
    } else if (speedData.userSpeed > speedData.recommendedSpeed) {
      return currentPoints - Math.floor(speedDiff / 5) * 5;
    }
    return currentPoints;
  };

  const endRide = async (rideId: string) => {
    try {
      const updatedRides = rides.map((r) => {
        if (r.id === rideId) {
          const avgSpeed =
            r.speedData.reduce((sum, data) => sum + data.userSpeed, 0) / r.speedData.length || 0;
          const avgRecommended =
            r.speedData.reduce((sum, data) => sum + data.recommendedSpeed, 0) /
              r.speedData.length || 0;
          return {
            ...r,
            endTime: new Date().toISOString(),
            averageSpeed: avgSpeed,
            recommendedAverageSpeed: avgRecommended,
          };
        }
        return r;
      });
      await AsyncStorage.setItem('rides', JSON.stringify(updatedRides));
      setRides(updatedRides);
    } catch (error) {
      console.error('Error ending ride:', error);
      throw error;
    }
  };

  const addMaintenanceLog = async (
    log: Omit<MaintenanceLog, 'id' | 'createdAt'>
  ) => {
    try {
      const newLog: MaintenanceLog = {
        ...log,
        id: Date.now().toString(),
        createdAt: new Date().toISOString(),
      };
      const updatedLogs = [...maintenanceLogs, newLog];
      await AsyncStorage.setItem('maintenanceLogs', JSON.stringify(updatedLogs));
      setMaintenanceLogs(updatedLogs);

      if (log.type === 'oil_change') {
        await updateVehicle(log.vehicleId, { lastOilChangeDate: log.date });
        removeMaintenanceAlert(log.vehicleId, 'oil_change');
      }
      return newLog;
    } catch (error) {
      console.error('Error adding maintenance log:', error);
      throw error;
    }
  };

  const addMaintenanceAlert = async (
    alert: Omit<MaintenanceAlert, 'id' | 'createdAt'>
  ) => {
    try {
      const newAlert: MaintenanceAlert = {
        ...alert,
        id: Date.now().toString(),
        createdAt: new Date().toISOString(),
      };
      const updatedAlerts = [...maintenanceAlerts, newAlert];
      await AsyncStorage.setItem('maintenanceAlerts', JSON.stringify(updatedAlerts));
      setMaintenanceAlerts(updatedAlerts);
      return newAlert;
    } catch (error) {
      console.error('Error adding maintenance alert:', error);
      throw error;
    }
  };

  const removeMaintenanceAlert = async (vehicleId: string, type: string) => {
    try {
      const updatedAlerts = maintenanceAlerts.filter(
        (a) => !(a.vehicleId === vehicleId && a.type === type)
      );
      await AsyncStorage.setItem('maintenanceAlerts', JSON.stringify(updatedAlerts));
      setMaintenanceAlerts(updatedAlerts);
    } catch (error) {
      console.error('Error removing maintenance alert:', error);
    }
  };

  const markAlertAsRead = async (alertId: string) => {
    try {
      const updatedAlerts = maintenanceAlerts.map((a) =>
        a.id === alertId ? { ...a, isRead: true } : a
      );
      await AsyncStorage.setItem('maintenanceAlerts', JSON.stringify(updatedAlerts));
      setMaintenanceAlerts(updatedAlerts);
    } catch (error) {
      console.error('Error marking alert as read:', error);
    }
  };

  const updateTheme = async (newTheme: Theme) => {
    try {
      await AsyncStorage.setItem('theme', JSON.stringify(newTheme));
      setTheme(newTheme);
    } catch (error) {
      console.error('Error updating theme:', error);
    }
  };

  return {
    isAuthenticated,
    currentUser,
    vehicles,
    currentVehicle,
    rides,
    maintenanceLogs,
    maintenanceAlerts,
    theme,
    isLoading,
    signUp,
    login,
    logout,
    addVehicle,
    updateVehicle,
    selectVehicle,
    startRide,
    addSpeedData,
    endRide,
    addMaintenanceLog,
    addMaintenanceAlert,
    markAlertAsRead,
    updateTheme,
  };
});
