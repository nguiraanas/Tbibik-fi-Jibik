import React, { useRef, useEffect } from "react";
import { View, Text, Animated, StyleSheet } from "react-native";
import { getTheme } from "@/constants/theme";
import { useApp } from "@/contexts/AppContext";

export default function SpeedDisplay({ speed, optimalSpeed }: { speed: number; optimalSpeed: number | null }) {
  const { theme } = useApp();
  const currentTheme = getTheme(theme);

  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.1,
          duration: 800,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 800,
          useNativeDriver: true,
        }),
      ])
    ).start();
  }, []);

  return (
    <View style={styles.container}>
      <Animated.View
        style={[
          styles.circle,
          {
            backgroundColor: currentTheme.colors.primary,
            transform: [{ scale: pulseAnim }],
          },
        ]}
      >
        {/* OPTIMAL SPEED EN GRAND */}
        <Text style={[styles.optimalLabel, { color: currentTheme.colors.background }]}>
          Optimal Speed
        </Text>

        <Text style={[styles.optimalValue, { color: currentTheme.colors.background }]}>
          {optimalSpeed !== null ? optimalSpeed : "--"}
        </Text>

        <Text style={[styles.unit, { color: currentTheme.colors.background }]}>
          km/h
        </Text>

        {/* CURRENT SPEED EN PETIT */}
        <Text style={[styles.currentLabel, { color: currentTheme.colors.background }]}>
          Current: {speed} km/h
        </Text>
      </Animated.View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
  },

  circle: {
    width: 220,
    height: 220,
    borderRadius: 110,
    justifyContent: "center",
    alignItems: "center",
    elevation: 10,
  },

  optimalLabel: {
    fontSize: 14,
    fontWeight: "600",
    marginBottom: 5,
  },

  optimalValue: {
    fontSize: 62,   // 🔥 BIG NUMBER
    fontWeight: "900",
  },

  unit: {
    fontSize: 20,
    marginBottom: 8,
    fontWeight: "600",
  },

  currentLabel: {
    fontSize: 16,   // 🔥 plus petit
    fontWeight: "500",
    marginTop: 10,
  },
});
