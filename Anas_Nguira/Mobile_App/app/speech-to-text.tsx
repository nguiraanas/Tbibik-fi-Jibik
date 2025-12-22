import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Mic } from 'lucide-react-native';

export default function SpeechToTextScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Speech to Text</Text>

      <TouchableOpacity style={styles.micButton}>
        <Mic color="#fff" size={32} />
        <Text style={styles.micText}>Start Recording</Text>
      </TouchableOpacity>

      <View style={styles.resultBox}>
        <Text>Transcribed text will appear here</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: '800', marginBottom: 24 },
  micButton: {
    height: 80,
    borderRadius: 20,
    backgroundColor: '#2FB8AC',
    justifyContent: 'center',
    alignItems: 'center',
  },
  micText: { color: '#fff', fontWeight: '700', marginTop: 8 },
  resultBox: {
    marginTop: 32,
    height: 160,
    borderRadius: 16,
    backgroundColor: '#f1f5f9',
    padding: 16,
  },
});
