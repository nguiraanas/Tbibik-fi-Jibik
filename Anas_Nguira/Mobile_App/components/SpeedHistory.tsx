import React from "react";
import { View, Text, StyleSheet, Dimensions } from "react-native";
import { getTheme } from "@/constants/theme";
import { useApp } from "@/contexts/AppContext";
import { SpeedData } from "@/types";

const { width } = Dimensions.get("window");

export default function SpeedHistory({ data }: { data: SpeedData[] }) {
  const { theme } = useApp();
  const currentTheme = getTheme(theme);

  if (!data || data.length === 0) {
    return (
      <Text style={{ color: currentTheme.colors.text, textAlign: "center", marginTop: 20 }}>
        Aucun historique de vitesse disponible
      </Text>
    );
  }

  const maxSpeed = Math.max(...data.map(d => Math.max(d.userSpeed, d.recommendedSpeed)), 100);

  return (
    <View style={[styles.card, { backgroundColor: currentTheme.colors.cardBackground }]}>
      <Text style={[styles.title, { color: currentTheme.colors.text }]}>
        Speed History
      </Text>

      <View style={styles.graph}>
        {data.map((d, index) => {
          const userHeight = (d.userSpeed / maxSpeed) * 100;
          const recHeight = (d.recommendedSpeed / maxSpeed) * 100;
          const barWidth = (width - 80) / 30;

          return (
            <View key={index} style={styles.bar}>
              <View
                style={[
                  styles.userBar,
                  {
                    height: `${userHeight}%`,
                    width: barWidth - 2,
                    backgroundColor: currentTheme.colors.primary,
                  },
                ]}
              />
              <View
                style={[
                  styles.recBar,
                  {
                    height: `${recHeight}%`,
                    width: barWidth - 2,
                    backgroundColor: currentTheme.colors.textSecondary,
                    opacity: 0.5,
                  },
                ]}
              />
            </View>
          );
        })}
      </View>

      <View style={styles.legend}>
        <View style={styles.legendItem}>
          <View style={[styles.dot, { backgroundColor: currentTheme.colors.primary }]} />
          <Text style={[styles.legendText, { color: currentTheme.colors.text }]}>Your Speed</Text>
        </View>

        <View style={styles.legendItem}>
          <View
            style={[styles.dot, { backgroundColor: currentTheme.colors.textSecondary, opacity: 0.5 }]}
          />
          <Text style={[styles.legendText, { color: currentTheme.colors.text }]}>Recommended</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 16,
    padding: 20,
    marginTop: 20,
  },
  title: {
    fontSize: 16,
    fontWeight: "700",
    marginBottom: 16,
  },
  graph: {
    flexDirection: "row",
    alignItems: "flex-end",
    height: 120,
    gap: 1,
  },
  bar: {
    flex: 1,
    alignItems: "center",
    justifyContent: "flex-end",
    position: "relative",
  },
  userBar: {
    borderRadius: 2,
  },
  recBar: {
    borderRadius: 2,
    position: "absolute",
    bottom: 0,
  },
  legend: {
    flexDirection: "row",
    justifyContent: "center",
    gap: 24,
    marginTop: 16,
  },
  legendItem: {
    flexDirection: "row",
    gap: 8,
    alignItems: "center",
  },
  dot: {
    width: 12,
    height: 12,
    borderRadius: 6,
  },
  legendText: {
    fontSize: 12,
  },
  rideHeaderRight: {
    flexDirection: "row",
    alignItems: "center",
    },

});
