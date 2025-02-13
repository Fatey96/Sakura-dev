import { extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  config: {
    initialColorMode: 'dark',
    useSystemColorMode: true,
  },
  colors: {
    sakura: {
      50: '#fce7f6',
      100: '#f9c5e8',
      200: '#f5a2d9',
      300: '#f17fcb',
      400: '#ed5cbd',
      500: '#e939af',
      600: '#d633a1',
      700: '#c32d93',
      800: '#b02785',
      900: '#9e2177',
    },
    purple: {
      50: '#f3e8ff',
      100: '#e4ccff',
      200: '#d5afff',
      300: '#c592ff',
      400: '#b675ff',
      500: '#a758ff',
      600: '#9851eb',
      700: '#894ad7',
      800: '#7a43c3',
      900: '#6b3caf',
    },
    cyber: {
      primary: '#00ffff',
      secondary: '#ff00ff',
      background: '#1a1a2e',
      darkBlue: '#16213e',
      accent: '#ffd700',
    }
  },
  fonts: {
    heading: `'Orbitron', sans-serif`,
    body: `'Arial', sans-serif`,
  },
  styles: {
    global: (props) => ({
      body: {
        bg: props.colorMode === 'dark' ? 'cyber.background' : 'gray.50',
        color: props.colorMode === 'dark' ? 'white' : 'gray.800',
      },
    }),
  },
  components: {
    Box: {
      baseStyle: (props) => ({
        bg: props.colorMode === 'dark' ? 'gray.900' : 'gray.50',
      }),
    },
    Button: {
      variants: {
        cyber: {
          bg: 'cyber.primary',
          color: 'cyber.background',
          _hover: {
            bg: '#00cccc',
            transform: 'translateY(-2px)',
            boxShadow: '0 6px 20px rgba(0, 255, 255, 0.4)',
          }
        }
      }
    },
    Tag: {
      variants: {
        cyber: {
          bg: 'rgba(42, 42, 78, 0.6)',
          color: 'white',
          _hover: {
            bg: 'rgba(58, 58, 110, 0.8)',
            transform: 'translateY(-2px)',
          }
        }
      }
    }
  },
});

export default theme; 