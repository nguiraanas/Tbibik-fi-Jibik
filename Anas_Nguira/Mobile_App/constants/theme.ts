import { Theme } from '@/types';

export const themes = {
  default: {
    colors: {
      background: '#0f1621',
      cardBackground: '#1a2332',
      primary: '#00ffdd',
      text: '#ffffff',
      textSecondary: '#8a9ba8',
      border: '#2a3a4a',
      error: '#ff4444',
      success: '#00ff88',
    },
    fonts: {
      regular: 16,
      medium: 18,
      large: 24,
      xlarge: 32,
    },
    spacing: {
      xs: 4,
      sm: 8,
      md: 16,
      lg: 24,
      xl: 32,
    },
  },
  elderly: {
    colors: {
      background: '#ffffff',
      cardBackground: '#f5f5f5',
      primary: '#2196F3',
      text: '#000000',
      textSecondary: '#666666',
      border: '#cccccc',
      error: '#ff4444',
      success: '#4caf50',
    },
    fonts: {
      regular: 20,
      medium: 24,
      large: 32,
      xlarge: 40,
    },
    spacing: {
      xs: 8,
      sm: 12,
      md: 20,
      lg: 28,
      xl: 36,
    },
  },
};

export const getTheme = (themeName: Theme) => themes[themeName];
