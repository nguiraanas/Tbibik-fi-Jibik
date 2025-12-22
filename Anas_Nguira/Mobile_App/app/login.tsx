import { useRouter } from 'expo-router';
import { ArrowLeft } from 'lucide-react-native';
import React, { useState } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  Image,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useApp } from '@/contexts/AppContext';
import { getTheme } from '@/constants/theme';

export default function LoginScreen() {
  const router = useRouter();
  const { login, theme } = useApp();
  const currentTheme = getTheme(theme);

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    console.log('LOGIN CLICKED');
    console.log('username:', username);
    console.log('password:', password);

    try {
      const success = await login(username, password);
      console.log('LOGIN RESULT:', success);

      if (success) {
        router.replace('/home' as any);
      } else {
        console.log('Invalid credentials');
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };


  return (
    <SafeAreaView
      style={[styles.container, { backgroundColor: currentTheme.colors.background }]}
    >
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={{ flex: 1 }}
      >
        <View style={styles.content}>
          {/* Header */}
          <View style={styles.header}>
            <TouchableOpacity
              style={styles.backButton}
              onPress={() => router.back()}
            >
              <ArrowLeft color={currentTheme.colors.text} size={22} />
            </TouchableOpacity>
          </View>

          {/* Logo */}
          <View style={styles.logoContainer}>
            <Image
              source={require('@/assets/images/logo.png')}
              style={styles.logo}
              resizeMode="contain"
            />
            <Text
              style={[styles.appName, { color: currentTheme.colors.primary }]}
            >
              Medical AI
            </Text>
            <Text style={styles.subtitle}>
              Sign in to continue
            </Text>
          </View>

          {/* Form */}
          <View
            style={[
              styles.formCard,
              { backgroundColor: currentTheme.colors.cardBackground },
            ]}
          >
            <Text
              style={[styles.formTitle, { color: currentTheme.colors.text }]}
            >
              Login
            </Text>

            <TextInput
              style={styles.input}
              placeholder="Email or username"
              placeholderTextColor={currentTheme.colors.textSecondary}
              value={username}
              onChangeText={setUsername}
              autoCapitalize="none"
            />

            <TextInput
              style={styles.input}
              placeholder="Password"
              placeholderTextColor={currentTheme.colors.textSecondary}
              value={password}
              onChangeText={setPassword}
              secureTextEntry
            />

            <TouchableOpacity style={styles.forgotPassword}>
              <Text
                style={[
                  styles.forgotPasswordText,
                  { color: currentTheme.colors.primary },
                ]}
              >
                Forgot your password?
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.loginButton,
                { backgroundColor: currentTheme.colors.primary },
              ]}
              onPress={handleLogin}
            >
              <Text style={styles.loginButtonText}>Sign In</Text>
            </TouchableOpacity>


            <TouchableOpacity
              style={styles.signupLink}
              onPress={() => router.push('/signup')}
            >
              <Text style={styles.signupText}>
                Don’t have an account?{' '}
                <Text style={styles.signupBold}>Sign up</Text>
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },

  content: {
    flex: 1,
    padding: 24,
    justifyContent: 'center',
  },

  header: {
    position: 'absolute',
    top: 24,
    left: 24,
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },

  logoContainer: {
    alignItems: 'center',
    marginBottom: 32,
  },
  logo: {
    width: 90,
    height: 90,
    marginBottom: 12,
  },
  appName: {
    fontSize: 26,
    fontWeight: '800',
  },
  subtitle: {
    marginTop: 6,
    fontSize: 13,
    color: '#64748b',
  },

  formCard: {
    borderRadius: 24,
    padding: 24,
  },
  formTitle: {
    fontSize: 20,
    fontWeight: '700',
    marginBottom: 20,
  },

  input: {
    height: 52,
    borderRadius: 14,
    paddingHorizontal: 16,
    marginBottom: 16,
    backgroundColor: '#f8fafc',
    borderWidth: 1,
    borderColor: '#e2e8f0',
    fontSize: 15,
  },

  forgotPassword: {
    alignItems: 'center',
    marginBottom: 20,
  },
  forgotPasswordText: {
    fontSize: 14,
    fontWeight: '600',
  },

  loginButton: {
    height: 56,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loginButtonText: {
    color: '#fff',
    fontWeight: '700',
    fontSize: 16,
  },

  signupLink: {
    marginTop: 18,
    alignItems: 'center',
  },
  signupText: {
    fontSize: 14,
    color: '#64748b',
  },
  signupBold: {
    fontWeight: '700',
    color: '#0f172a',
  },
});
