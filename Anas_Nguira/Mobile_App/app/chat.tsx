import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useApp } from "@/contexts/AppContext";
import { getTheme } from "@/constants/theme";
import { askLloydRAG } from "../services/api";

export default function ChatScreen() {
  const { theme } = useApp();
  const currentTheme = getTheme(theme);

  const [messages, setMessages] = useState<{ role: string; text: string }[]>([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);

    // 🟢 Effacer immédiatement l’input
    setInput("");

    const answer = await askLloydRAG(input, "mobile_session_01");

    const botMsg = { role: "bot", text: answer };
    setMessages((prev) => [...prev, botMsg]);
  };


  return (
    <SafeAreaView
      style={[
        styles.container,
        { backgroundColor: currentTheme.colors.background },
      ]}
    >
      {/* HEADER */}
      <View
        style={[
          styles.header,
          { backgroundColor: currentTheme.colors.cardBackground },
        ]}
      >
        <Text style={[styles.headerTitle, { color: currentTheme.colors.text }]}>
          🤖 Lloyd Assistant
        </Text>
      </View>

      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === "ios" ? "padding" : undefined}
      >
        {/* MESSAGES */}
        <ScrollView style={styles.chatBox}>
          {messages.map((m, i) => (
            <View
              key={i}
              style={[
                styles.msg,
                m.role === "user"
                  ? {
                      ...styles.userMsg,
                      backgroundColor: currentTheme.colors.primary,
                    }
                  : {
                      ...styles.botMsg,
                      backgroundColor: currentTheme.colors.cardBackground,
                      borderWidth: 1,
                      borderColor: currentTheme.colors.border,
                    },
              ]}
            >
              <Text
                style={[
                  styles.msgText,
                  {
                    color:
                      m.role === "user"
                        ? currentTheme.colors.background
                        : currentTheme.colors.text,
                  },
                ]}
              >
                {m.text}
              </Text>
            </View>
          ))}
        </ScrollView>

        {/* INPUT */}
        <View style={[styles.inputContainer]}>
          <TextInput
            value={input}
            onChangeText={setInput}
            placeholder="Pose une question à Lloyd…"
            placeholderTextColor={currentTheme.colors.textSecondary}
            style={[
              styles.input,
              {
                backgroundColor: currentTheme.colors.cardBackground,
                color: currentTheme.colors.text,
                borderColor: currentTheme.colors.border,
              },
            ]}
          />
          <TouchableOpacity
            onPress={sendMessage}
            style={[
              styles.btn,
              { backgroundColor: currentTheme.colors.primary },
            ]}
          >
            <Text style={{ color: currentTheme.colors.background, fontWeight: "700" }}>
              Envoyer
            </Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },

  header: {
    padding: 18,
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,
    alignItems: "center",
  }, 

  headerTitle: {
    fontSize: 20,
    fontWeight: "800",
  },

  chatBox: {
    flex: 1,
    paddingHorizontal: 12,
    marginTop: 10,
  },

  msg: {
    marginVertical: 6,
    padding: 12,
    maxWidth: "80%",
    borderRadius: 16,
  },

  userMsg: {
    alignSelf: "flex-end",
    borderTopRightRadius: 0,
  },

  botMsg: {
    alignSelf: "flex-start",
    borderTopLeftRadius: 0,
  },

  msgText: {
    fontSize: 16,
    lineHeight: 22,
  },

  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    padding: 12,
    gap: 10,
  },

  input: {
    flex: 1,
    borderWidth: 1,
    padding: 10,
    borderRadius: 14,
    fontSize: 16,
  },

  btn: {
    paddingVertical: 12,
    paddingHorizontal: 18,
    borderRadius: 14,
  },
});
