import { useRouter } from 'expo-router';
import { ArrowLeft } from 'lucide-react-native';
import React, { useState } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Image,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useApp } from '@/contexts/AppContext';
import { getTheme } from '@/constants/theme';
import { SpeedUnit } from '@/types';

export default function SignUpScreen() {
  const router = useRouter();
  const { signUp, theme } = useApp();
  const currentTheme = getTheme(theme);

  // 🔒 logique conservée
  const [firstName, setFirstName] = useState('');
  const [surname, setSurname] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [age, setAge] = useState('');
  const [ageError, setAgeError] = useState('');
  const [emergencyContact, setEmergencyContact] = useState('');
  const [emergencyContactError, setEmergencyContactError] = useState('');
  const [speedUnit, setSpeedUnit] = useState<SpeedUnit>('km/h'); // conservé

  const handleSignUp = async () => {
    try {
      if (!firstName || !surname || !username || !password || !age || !emergencyContact) {
        console.log('Please fill all fields');
        return;
      }

      const ageNum = parseInt(age);
      if (isNaN(ageNum) || ageNum < 18 || ageNum > 100) {
        setAgeError('Age must be between 18 and 100');
        return;
      }

      await signUp({
        firstName,
        surname,
        username,
        age,
        emergencyContact,
        speedUnit,
      });

      // ✅ REDIRECTION CORRIGÉE
      router.replace('/home' as any);
    } catch (error) {
      console.error('Sign up error:', error);
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
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          {/* Header */}
          <View style={styles.header}>
            <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
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
            <Text style={[styles.appName, { color: currentTheme.colors.primary }]}>
              Medical AI
            </Text>
            <Text style={styles.subtitle}>
              Create your account to access smart medical services
            </Text>
          </View>

          {/* Form */}
          <View
            style={[
              styles.formCard,
              { backgroundColor: currentTheme.colors.cardBackground },
            ]}
          >
            <Text style={[styles.formTitle, { color: currentTheme.colors.text }]}>
              Sign Up
            </Text>

            <TextInput
              style={styles.input}
              placeholder="First name"
              placeholderTextColor={currentTheme.colors.textSecondary}
              value={firstName}
              onChangeText={setFirstName}
            />

            <TextInput
              style={styles.input}
              placeholder="Last name"
              placeholderTextColor={currentTheme.colors.textSecondary}
              value={surname}
              onChangeText={setSurname}
            />

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
              secureTextEntry
              value={password}
              onChangeText={setPassword}
            />

            <TextInput
              style={[
                styles.input,
                ageError && { borderColor: currentTheme.colors.error },
              ]}
              placeholder="Age"
              placeholderTextColor={currentTheme.colors.textSecondary}
              keyboardType="numeric"
              value={age}
              onChangeText={setAge}
            />
            {ageError ? <Text style={styles.errorText}>{ageError}</Text> : null}

            <TextInput
              style={[
                styles.input,
                emergencyContactError && { borderColor: currentTheme.colors.error },
              ]}
              placeholder="Emergency contact (+216 ...)"
              placeholderTextColor={currentTheme.colors.textSecondary}
              keyboardType="phone-pad"
              value={emergencyContact}
              onChangeText={setEmergencyContact}
            />
            {emergencyContactError ? (
              <Text style={styles.errorText}>{emergencyContactError}</Text>
            ) : null}

            <TouchableOpacity
              style={[
                styles.signUpButton,
                { backgroundColor: currentTheme.colors.primary },
              ]}
              onPress={handleSignUp}
            >
              <Text style={styles.signUpText}>Create account</Text>
            </TouchableOpacity>


            <TouchableOpacity
              style={styles.loginLink}
              onPress={() => router.push('/login')}
            >
              <Text style={styles.loginText}>
                Already have an account? <Text style={styles.loginBold}>Sign in</Text>
              </Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  scrollContent: {
    padding: 24,
    paddingBottom: 40,
  },

  header: {
    marginBottom: 16,
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
    textAlign: 'center',
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
    marginBottom: 14,
    backgroundColor: '#f8fafc',
    borderWidth: 1,
    borderColor: '#e2e8f0',
    fontSize: 15,
  },

  signUpButton: {
    height: 56,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 10,
  },
  signUpText: {
    color: '#fff',
    fontWeight: '700',
    fontSize: 16,
  },

  loginLink: {
    marginTop: 18,
    alignItems: 'center',
  },
  loginText: {
    fontSize: 14,
    color: '#64748b',
  },
  loginBold: {
    fontWeight: '700',
    color: '#0f172a',
  },

  errorText: {
    fontSize: 12,
    color: '#ef4444',
    marginBottom: 8,
    marginLeft: 6,
  },
});
