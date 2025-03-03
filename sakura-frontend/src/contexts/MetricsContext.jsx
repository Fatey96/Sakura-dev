import React, { createContext, useContext, useState } from 'react';

const MetricsContext = createContext(null);

export const useMetrics = () => {
  const context = useContext(MetricsContext);
  if (context === undefined) {
    throw new Error('useMetrics must be used within a MetricsProvider');
  }
  return context;
};

export const MetricsProvider = ({ children }) => {
  const [metrics, setMetrics] = useState(null);
  
  const value = {
    metrics,
    setMetrics
  };

  return (
    <MetricsContext.Provider value={value}>
      {children}
    </MetricsContext.Provider>
  );
};

export default MetricsProvider; 