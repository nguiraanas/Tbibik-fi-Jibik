import { useRouter } from 'expo-router';
import React from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  Image,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useApp } from '@/contexts/AppContext';
import { getTheme } from '@/constants/theme';
import {
  Camera,
  HeartPulse,
  Hand,
  Mic,
  Brain,
  Apple,
  Stethoscope,
  FileText,
  Settings,
} from 'lucide-react-native';

export default function HomeScreen() {
  const router = useRouter();
  const { currentUser, theme } = useApp();
  const currentTheme = getTheme(theme);

  const features = [
    { title: 'Wound Analysis', icon: FileText, route: '/wound' },
    { title: 'Sign Language', icon: Hand, route: '/sign-language' },
    { title: 'Heart Health', icon: HeartPulse, route: '/heart' },
    { title: 'Allergy Diagnosis', icon: Stethoscope, route: '/allergy' },
    { title: 'Stroke Detection', icon: Brain, route: '/stroke' },
    { title: 'Speech to Text', icon: Mic, route: '/speech-to-text' },
    { title: 'Insulin Chatbot', icon: Apple, route: '/chat?mode=insulin' },
    { title: 'Dermato Chatbot', icon: Camera, route: '/chat?mode=dermato' },
  ];

  return (
    <SafeAreaView
      style={[styles.container, { backgroundColor: currentTheme.colors.background }]}
    >
      {/* Header */}
      <View style={[styles.header, { backgroundColor: currentTheme.colors.cardBackground }]}>
        <View style={styles.headerLeft}>
          <Image
            source={{ uri: 'https://ui-avatars.com/api/?name=' + currentUser?.firstName }}
            style={styles.avatar}
          />
          <View>
            <Text style={[styles.welcomeText, { color: currentTheme.colors.text }]}>
              Welcome,
            </Text>
            <Text style={[styles.userName, { color: currentTheme.colors.text }]}>
              {currentUser?.firstName} {currentUser?.surname}
            </Text>
          </View>
        </View>

        <TouchableOpacity onPress={() => router.push('/settings' as any)}>
          <Settings color={currentTheme.colors.text} size={24} />
        </TouchableOpacity>
      </View>

      {/* Content */}
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={[styles.title, { color: currentTheme.colors.text }]}>
          Medical AI Hub
        </Text>
        <Text style={[styles.subtitle, { color: currentTheme.colors.textSecondary }]}>
          Choose a service
        </Text>

        <View style={styles.grid}>
          {features.map((item, index) => {
            const Icon = item.icon;
            return (
              <TouchableOpacity
                key={index}
                style={[
                  styles.card,
                  { backgroundColor: currentTheme.colors.cardBackground },
                ]}
                onPress={() => router.push(item.route as any)}
              >
                <Icon size={32} color={currentTheme.colors.primary} />
                <Text style={[styles.cardText, { color: currentTheme.colors.text }]}>
                  {item.title}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },

  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  avatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
  },
  welcomeText: {
    fontSize: 14,
  },
  userName: {
    fontSize: 16,
    fontWeight: '700',
  },

  content: {
    padding: 20,
  },
  title: {
    fontSize: 26,
    fontWeight: '800',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    marginBottom: 24,
  },

  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  card: {
    width: '47%',
    height: 120,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
    elevation: 6,
  },
  cardText: {
    marginTop: 10,
    fontSize: 14,
    fontWeight: '600',
    textAlign: 'center',
  },
});
