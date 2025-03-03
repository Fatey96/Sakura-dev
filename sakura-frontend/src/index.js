import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { ChakraProvider } from '@chakra-ui/react';
import theme from './theme';
import { StixProvider } from './Components/EntitySelector/StixContext';
import { MetricsProvider } from './contexts/MetricsContext';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <MetricsProvider>
        <StixProvider>
          <App />
        </StixProvider>
      </MetricsProvider>
    </ChakraProvider>
  </React.StrictMode>
);