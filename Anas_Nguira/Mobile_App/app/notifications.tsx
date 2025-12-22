import { useRouter } from 'expo-router';
import { ArrowLeft, Bell } from 'lucide-react-native';
import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useApp } from '@/contexts/AppContext';
import { getTheme } from '@/constants/theme';

export default function NotificationsScreen() {
  const router = useRouter();
  const { maintenanceAlerts, markAlertAsRead, theme } = useApp();
  const currentTheme = getTheme(theme);

  const handleAlertPress = async (alertId: string) => {
    await markAlertAsRead(alertId);
  };

  return (
    <SafeAreaView
      style={[styles.container, { backgroundColor: currentTheme.colors.background }]}
      edges={['top']}
    >
      <View style={[styles.innerContainer, { backgroundColor: currentTheme.colors.background }]}>
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => router.back()}
          >
            <ArrowLeft color={currentTheme.colors.text} size={24} />
          </TouchableOpacity>
          <Text style={[styles.title, { color: currentTheme.colors.primary }]}>Notifications</Text>
          <View style={styles.placeholder} />
        </View>

        <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
          {maintenanceAlerts.length === 0 && (
            <View style={[styles.emptyCard, { backgroundColor: currentTheme.colors.cardBackground }]}>
              <Bell color={currentTheme.colors.textSecondary} size={48} />
              <Text style={[styles.emptyText, { color: currentTheme.colors.textSecondary }]}>
                No notifications
              </Text>
            </View>
          )}

          {maintenanceAlerts.map((alert) => (
            <TouchableOpacity
              key={alert.id}
              style={[
                styles.alertCard,
                {
                  backgroundColor: currentTheme.colors.cardBackground,
                  borderLeftColor: alert.isRead ? currentTheme.colors.border : currentTheme.colors.primary,
                },
              ]}
              onPress={() => handleAlertPress(alert.id)}
            >
              <View style={styles.alertHeader}>
                <Text style={[styles.alertType, { color: currentTheme.colors.text }]}>
                  {alert.type === 'oil_change' && 'Oil Change Due'}
                  {alert.type === 'tire_pressure' && 'Check Tire Pressure'}
                  {alert.type === 'brake_check' && 'Brake Inspection Due'}
                </Text>
                {!alert.isRead && (
                  <View style={[styles.unreadDot, { backgroundColor: currentTheme.colors.primary }]} />
                )}
              </View>
              <Text style={[styles.alertMessage, { color: currentTheme.colors.textSecondary }]}>
                {alert.message}
              </Text>
              <Text style={[styles.alertDate, { color: currentTheme.colors.textSecondary }]}>
                Due: {alert.dueDate}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  innerContainer: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
  },
  backButton: {
    padding: 8,
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
  },
  placeholder: {
    width: 40,
  },
  scrollContent: {
    padding: 24,
    gap: 16,
  },
  emptyCard: {
    borderRadius: 16,
    padding: 40,
    alignItems: 'center',
    gap: 16,
  },
  emptyText: {
    fontSize: 16,
    textAlign: 'center',
  },
  alertCard: {
    borderRadius: 16,
    padding: 20,
    borderLeftWidth: 4,
  },
  alertHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  alertType: {
    fontSize: 16,
    fontWeight: '700',
  },
  unreadDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
  },
  alertMessage: {
    fontSize: 14,
    marginBottom: 4,
  },
  alertDate: {
    fontSize: 12,
  },
});
