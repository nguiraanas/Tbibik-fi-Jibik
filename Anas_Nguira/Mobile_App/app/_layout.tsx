import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Stack } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import React, { useEffect } from "react";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { AppProvider } from "@/contexts/AppContext";

// Prevent the splash screen from auto-hiding before asset loading is complete
SplashScreen.preventAutoHideAsync();

const queryClient = new QueryClient();

function RootLayoutNav() {
  return (
    <Stack screenOptions={{ headerShown: false }}>
      {/* Auth & Landing */}
      <Stack.Screen name="index" />
      <Stack.Screen name="login" />
      <Stack.Screen name="signup" />

      {/* Main */}
      <Stack.Screen name="home" />
      <Stack.Screen name="settings" />
      <Stack.Screen name="notifications" />

      {/* Medical Features */}
      <Stack.Screen name="wound" />
      <Stack.Screen name="sign-language" />
      <Stack.Screen name="heart" />
      <Stack.Screen name="allergy" />
      <Stack.Screen name="stroke" />
      <Stack.Screen name="speech-to-text" />
      <Stack.Screen name="chat" />
    </Stack>
  );
}

export default function RootLayout() {
  useEffect(() => {
    SplashScreen.hideAsync();
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <AppProvider>
        <GestureHandlerRootView style={{ flex: 1 }}>
          <RootLayoutNav />
        </GestureHandlerRootView>
      </AppProvider>
    </QueryClientProvider>
  );
}
