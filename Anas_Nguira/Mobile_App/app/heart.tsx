import { View, Text, StyleSheet, TouchableOpacity, TextInput } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { HeartPulse, Video } from 'lucide-react-native';
import { useApp } from '@/contexts/AppContext';
import { getTheme } from '@/constants/theme';

export default function HeartScreen() {
  const { theme } = useApp();
  const currentTheme = getTheme(theme);

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Heart Health Classification</Text>

      <TouchableOpacity style={styles.uploadBox}>
        <Video />
        <Text>Upload Video</Text>
      </TouchableOpacity>

      <TextInput
        placeholder="Enter value (e.g. heart rate)"
        style={styles.input}
      />

      <TouchableOpacity style={styles.button}>
        <HeartPulse color="#fff" />
        <Text style={styles.buttonText}>Analyze</Text>
      </TouchableOpacity>

      <View style={styles.resultBox}>
        <Text>Result will appear here</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: '800', marginBottom: 20 },
  uploadBox: {
    height: 120,
    borderRadius: 16,
    backgroundColor: '#e2e8f0',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  input: {
    height: 50,
    borderRadius: 12,
    backgroundColor: '#f1f5f9',
    paddingHorizontal: 16,
    marginBottom: 16,
  },
  button: {
    height: 56,
    borderRadius: 16,
    backgroundColor: '#2FB8AC',
    flexDirection: 'row',
    gap: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonText: { color: '#fff', fontWeight: '700' },
  resultBox: {
    marginTop: 24,
    height: 100,
    backgroundColor: '#f8fafc',
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
