import { useRouter } from 'expo-router';
import { ArrowLeft, Moon, Sun, LogOut, User } from 'lucide-react-native';
import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  Alert,
  Image,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useApp } from '@/contexts/AppContext';
import { getTheme } from '@/constants/theme';

export default function SettingsScreen() {
  const router = useRouter();
  const { currentUser, theme, updateTheme, logout } = useApp();
  const currentTheme = getTheme(theme);

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Logout',
          style: 'destructive',
          onPress: async () => {
            await logout();
            router.replace('/' as any);
          },
        },
      ]
    );
  };

  return (
    <SafeAreaView
      style={[styles.container, { backgroundColor: currentTheme.colors.background }]}
    >
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <ArrowLeft color={currentTheme.colors.text} size={22} />
        </TouchableOpacity>
        <Text style={[styles.title, { color: currentTheme.colors.text }]}>
          Settings
        </Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Profile Card */}
        <View
          style={[
            styles.profileCard,
            { backgroundColor: currentTheme.colors.cardBackground },
          ]}
        >
          <Image
            source={require('@/assets/images/logo.png')}
            style={styles.logo}
            resizeMode="contain"
          />

          <Text style={[styles.name, { color: currentTheme.colors.text }]}>
            {currentUser?.firstName} {currentUser?.surname}
          </Text>

          <View style={styles.infoRow}>
            <User size={16} color={currentTheme.colors.textSecondary} />
            <Text style={styles.infoText}>
              Age: {currentUser?.age}
            </Text>
          </View>

          <Text style={styles.infoText}>
            Emergency contact: {currentUser?.emergencyContact}
          </Text>
        </View>

        {/* Theme Section */}
        <View
          style={[
            styles.section,
            { backgroundColor: currentTheme.colors.cardBackground },
          ]}
        >
          <Text style={[styles.sectionTitle, { color: currentTheme.colors.text }]}>
            Appearance & Accessibility
          </Text>

          <TouchableOpacity
            style={[
              styles.themeOption,
              theme === 'default' && {
                backgroundColor: currentTheme.colors.primary,
              },
            ]}
            onPress={() => updateTheme('default')}
          >
            <Moon
              size={22}
              color={
                theme === 'default'
                  ? currentTheme.colors.background
                  : currentTheme.colors.text
              }
            />
            <Text
              style={[
                styles.themeText,
                theme === 'default' && {
                  color: currentTheme.colors.background,
                },
              ]}
            >
              Default Theme (Dark)
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.themeOption,
              theme === 'elderly' && {
                backgroundColor: currentTheme.colors.primary,
              },
            ]}
            onPress={() => updateTheme('elderly')}
          >
            <Sun
              size={22}
              color={
                theme === 'elderly'
                  ? currentTheme.colors.background
                  : currentTheme.colors.text
              }
            />
            <Text
              style={[
                styles.themeText,
                theme === 'elderly' && {
                  color: currentTheme.colors.background,
                },
              ]}
            >
              Elderly-friendly (Light & Large Text)
            </Text>
          </TouchableOpacity>
        </View>

        {/* Logout */}
        <TouchableOpacity
          style={[styles.logoutButton, { backgroundColor: currentTheme.colors.error }]}
          onPress={handleLogout}
        >
          <LogOut color="#fff" size={20} />
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },

  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 20,
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
  },

  scrollContent: {
    padding: 24,
    gap: 20,
  },

  profileCard: {
    borderRadius: 20,
    padding: 24,
    alignItems: 'center',
  },
  logo: {
    width: 70,
    height: 70,
    marginBottom: 12,
  },
  name: {
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 8,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 6,
  },
  infoText: {
    fontSize: 14,
    color: '#64748b',
  },

  section: {
    borderRadius: 20,
    padding: 20,
  },
  sectionTitle: {
    fontSize: 17,
    fontWeight: '700',
    marginBottom: 16,
  },

  themeOption: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    padding: 16,
    borderRadius: 14,
    marginBottom: 12,
    backgroundColor: '#f1f5f9',
  },
  themeText: {
    fontSize: 15,
    fontWeight: '600',
    color: '#0f172a',
  },

  logoutButton: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
    paddingVertical: 16,
    borderRadius: 18,
    marginTop: 10,
  },
  logoutText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '700',
  },
});
