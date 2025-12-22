import React, { useEffect, useRef, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { CameraView, useCameraPermissions } from 'expo-camera';

import { useApp } from '@/contexts/AppContext';
import { getTheme } from '@/constants/theme';
import { predictSignLanguage } from '@/services/api';

export default function SignLanguageScreen() {
  const { theme } = useApp();
  const currentTheme = getTheme(theme);

  const cameraRef = useRef<CameraView>(null);
  const [permission, requestPermission] = useCameraPermissions();

  const [prediction, setPrediction] = useState<string>('—');
  const [loading, setLoading] = useState(false);

  // 📸 Capture périodique
  useEffect(() => {
    if (!permission?.granted) return;

    const interval = setInterval(async () => {
      if (!cameraRef.current || loading) return;

      try {
        setLoading(true);

        const photo = await cameraRef.current.takePictureAsync({
          quality: 0.4,
          skipProcessing: true,
        });

        const result = await predictSignLanguage(photo.uri);

        if (result?.prediction) {
          setPrediction(result.prediction);
        }

      } catch (err) {
        console.log('Prediction error:', err);
      } finally {
        setLoading(false);
      }
    }, 600); // ⏱️ toutes les 600 ms

    return () => clearInterval(interval);
  }, [permission, loading]);

  if (!permission) {
    return <View />;
  }

  if (!permission.granted) {
    return (
      <SafeAreaView style={styles.center}>
        <Text>Camera permission required</Text>
        <Text onPress={requestPermission} style={styles.link}>
          Grant permission
        </Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <CameraView
        ref={cameraRef}
        style={styles.camera}
        facing="front"
      />

      <View style={styles.overlay}>
        <Text style={styles.label}>Recognized sign</Text>
        <Text style={styles.prediction}>{prediction}</Text>
        {loading && <ActivityIndicator color="#fff" />}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  camera: { flex: 1 },
  overlay: {
    position: 'absolute',
    bottom: 40,
    alignSelf: 'center',
    backgroundColor: 'rgba(0,0,0,0.6)',
    padding: 20,
    borderRadius: 20,
    alignItems: 'center',
  },
  label: {
    color: '#fff',
    fontSize: 14,
    marginBottom: 6,
  },
  prediction: {
    color: '#00ffcc',
    fontSize: 28,
    fontWeight: '800',
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  link: {
    color: '#2563eb',
    marginTop: 12,
  },
});
