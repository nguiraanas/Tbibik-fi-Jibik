import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { ImagePlus, Camera, FileText } from 'lucide-react-native';

import { useApp } from '@/contexts/AppContext';
import { getTheme } from '@/constants/theme';

import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system/legacy';
import * as Sharing from 'expo-sharing';

import { analyzeWoundImage } from '@/services/api';

export default function WoundScreen() {
  const { theme } = useApp();
  const currentTheme = getTheme(theme);

  const [imageUri, setImageUri] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // 📁 Choisir depuis la galerie
  const pickFromGallery = async () => {
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permission.granted) {
      alert('Gallery permission denied');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      quality: 1,
    });

    if (!result.canceled) {
      setImageUri(result.assets[0].uri);
    }
  };

  // 📸 Prendre une photo en temps réel
  const takePhoto = async () => {
    const permission = await ImagePicker.requestCameraPermissionsAsync();
    if (!permission.granted) {
      alert('Camera permission denied');
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      quality: 1,
    });

    if (!result.canceled) {
      setImageUri(result.assets[0].uri);
    }
  };

  // 🧠 Analyse + PDF
  const handleAnalyze = async () => {
    if (!imageUri) {
      alert('Please select or take an image');
      return;
    }

    try {
      setLoading(true);

      // 1️⃣ Appel API → PDF (Blob)
      const pdfBlob = await analyzeWoundImage(imageUri);

      // 2️⃣ Blob → Base64 (méthode sûre)
      const base64 = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader();
        reader.onerror = reject;
        reader.onload = () => {
          const dataUrl = reader.result as string;
          resolve(dataUrl.split(',')[1]);
        };
        reader.readAsDataURL(pdfBlob);
      });

      // 3️⃣ Sauvegarde locale
      const pdfUri = FileSystem.documentDirectory + 'wound_report.pdf';

      await FileSystem.writeAsStringAsync(pdfUri, base64, {
        encoding: 'base64',
      });

      // 4️⃣ Ouverture / partage
      await Sharing.shareAsync(pdfUri);

    } catch (error) {
      console.error(error);
      alert('Error generating report');
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView
      style={[
        styles.container,
        { backgroundColor: currentTheme.colors.background },
      ]}
    >
      <Text style={[styles.title, { color: currentTheme.colors.text }]}>
        Wound Analysis
      </Text>

      {/* Choix image */}
      <View style={styles.choiceContainer}>
        <TouchableOpacity style={styles.card} onPress={takePhoto}>
          <Camera size={32} color={currentTheme.colors.primary} />
          <Text style={styles.cardText}>Take photo</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.card} onPress={pickFromGallery}>
          <ImagePlus size={32} color={currentTheme.colors.primary} />
          <Text style={styles.cardText}>Choose from gallery</Text>
        </TouchableOpacity>
      </View>

      {imageUri && (
        <Text style={styles.selectedText}>Image selected ✓</Text>
      )}

      {/* Analyse */}
      <TouchableOpacity
        style={[
          styles.button,
          { backgroundColor: currentTheme.colors.primary },
        ]}
        onPress={handleAnalyze}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <>
            <FileText color="#fff" />
            <Text style={styles.buttonText}>Generate PDF Report</Text>
          </>
        )}
      </TouchableOpacity>

      <View style={styles.resultBox}>
        <Text style={styles.resultText}>
          The generated PDF will open automatically
        </Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: '800',
    marginBottom: 24,
  },
  choiceContainer: {
    flexDirection: 'row',
    gap: 16,
    marginBottom: 24,
  },
  card: {
    flex: 1,
    height: 140,
    borderRadius: 20,
    borderWidth: 1,
    borderStyle: 'dashed',
    justifyContent: 'center',
    alignItems: 'center',
  },
  cardText: {
    marginTop: 10,
    fontWeight: '600',
  },
  selectedText: {
    marginBottom: 16,
    fontWeight: '600',
    color: '#16a34a',
    textAlign: 'center',
  },
  button: {
    height: 56,
    borderRadius: 16,
    flexDirection: 'row',
    gap: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: '700',
  },
  resultBox: {
    marginTop: 32,
    height: 120,
    borderRadius: 16,
    backgroundColor: '#f1f5f9',
    justifyContent: 'center',
    alignItems: 'center',
  },
  resultText: {
    color: '#64748b',
    textAlign: 'center',
  },
});
