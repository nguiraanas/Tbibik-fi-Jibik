import { View, Text, StyleSheet, TextInput, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function AllergyScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Allergy Diagnosis</Text>

      <TextInput
        placeholder="Describe symptoms or ask a question"
        multiline
        style={styles.input}
      />

      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>Ask</Text>
      </TouchableOpacity>

      <View style={styles.resultBox}>
        <Text>Diagnosis / Q&A will appear here</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 24, fontWeight: '800', marginBottom: 20 },
  input: {
    height: 120,
    borderRadius: 16,
    backgroundColor: '#f1f5f9',
    padding: 16,
    marginBottom: 16,
  },
  button: {
    height: 56,
    borderRadius: 16,
    backgroundColor: '#2FB8AC',
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonText: { color: '#fff', fontWeight: '700' },
  resultBox: {
    marginTop: 24,
    height: 120,
    backgroundColor: '#f8fafc',
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
