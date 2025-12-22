import { useRouter } from 'expo-router';
import React, { useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  Image,
} from 'react-native';
import { useApp } from '@/contexts/AppContext';
import { getTheme } from '@/constants/theme';

export default function SplashScreen() {
  const router = useRouter();
  const { isAuthenticated, isLoading, theme } = useApp();
  const currentTheme = getTheme(theme);

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.replace('/home' as any);
    }
  }, [isAuthenticated, isLoading]);

  if (isLoading) {
    return (
      <View
        style={[
          styles.container,
          { backgroundColor: currentTheme.colors.background },
        ]}
      >
        <ActivityIndicator size="large" color={currentTheme.colors.primary} />
      </View>
    );
  }

  return (
    <View
      style={[
        styles.container,
        { backgroundColor: currentTheme.colors.background },
      ]}
    >
      {/* Logo */}
      <View style={styles.logoContainer}>
        <Image
          source={require('@/assets/images/logo.png')}
          style={styles.logo}
          resizeMode="contain"
        />
        <Text
          style={[
            styles.appName,
            { color: currentTheme.colors.primary },
          ]}
        >
          Medical AI
        </Text>
        <Text
          style={[
            styles.subtitle,
            { color: currentTheme.colors.textSecondary },
          ]}
        >
          Smart assistance for modern healthcare
        </Text>
      </View>

      {/* Actions */}
      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={[
            styles.button,
            { backgroundColor: currentTheme.colors.primary },
          ]}
          onPress={() => router.push('/login')}
        >
          <Text
            style={[
              styles.buttonText,
              { color: currentTheme.colors.background },
            ]}
          >
            Sign In
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[
            styles.button,
            styles.secondaryButton,
            { borderColor: currentTheme.colors.primary },
          ]}
          onPress={() => router.push('/signup')}
        >
          <Text
            style={[
              styles.secondaryButtonText,
              { color: currentTheme.colors.primary },
            ]}
          >
            Create Account
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 24,
    paddingVertical: 60,
    justifyContent: 'space-between',
    alignItems: 'center',
  },

  logoContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logo: {
    width: 140,
    height: 140,
    marginBottom: 16,
  },
  appName: {
    fontSize: 30,
    fontWeight: '800',
    marginBottom: 6,
  },
  subtitle: {
    fontSize: 14,
    textAlign: 'center',
    maxWidth: 260,
  },

  buttonContainer: {
    width: '100%',
    gap: 16,
  },
  button: {
    paddingVertical: 16,
    borderRadius: 20,
    alignItems: 'center',
  },
  buttonText: {
    fontSize: 16,
    fontWeight: '700',
  },

  secondaryButton: {
    backgroundColor: 'transparent',
    borderWidth: 2,
  },
  secondaryButtonText: {
    fontSize: 16,
    fontWeight: '700',
  },
});
