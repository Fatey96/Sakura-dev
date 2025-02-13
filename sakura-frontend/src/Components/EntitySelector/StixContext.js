import React, { createContext, useState, useContext } from 'react';

const StixContext = createContext();

export const StixProvider = ({ children }) => {
  const [stixBundle, setStixBundle] = useState(null);

  return (
    <StixContext.Provider value={{ stixBundle, setStixBundle }}>
      {children}
    </StixContext.Provider>
  );
};

export const useStix = () => useContext(StixContext);