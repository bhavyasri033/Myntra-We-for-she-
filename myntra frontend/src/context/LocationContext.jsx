import React, { createContext, useState } from 'react';

/**
 * LocationContext
 * State management for frontend location experience (Pure UI & Mock Data).
 * No browser GPS or backend API calls implemented.
 */
export const LocationContext = createContext({
  location: {
    city: 'Hyderabad',
    state: 'Telangana',
    latitude: 17.385044,
    longitude: 78.486671,
  },
  source: 'default', // 'gps' | 'manual' | 'default'
  loading: false,
  permission: 'prompt', // 'prompt' | 'granted' | 'denied'
  requestCurrentLocation: () => {},
  selectCity: () => {},
  changeLocation: () => {},
  clearLocation: () => {},
});

export const LocationProvider = ({ children }) => {
  const [location, setLocationState] = useState({
    city: 'Hyderabad',
    state: 'Telangana',
    latitude: 17.385044,
    longitude: 78.486671,
  });

  const [source, setSource] = useState('default');
  const [loading, setLoading] = useState(false);
  const [permission, setPermission] = useState('prompt');

  // Mock GPS location detection flow (No browser APIs / No backend APIs)
  const requestCurrentLocation = (onSuccess) => {
    setLoading(true);

    // Simulate location discovery
    setTimeout(() => {
      const mockGpsLocation = {
        city: 'Hyderabad',
        state: 'Telangana',
        latitude: 17.385044,
        longitude: 78.486671,
      };
      setLocationState(mockGpsLocation);
      setSource('gps');
      setPermission('granted');
      setLoading(false);

      if (onSuccess) onSuccess(mockGpsLocation);
    }, 1200);
  };

  // Mock manual city selection flow
  const selectCity = (cityData, onSuccess) => {
    const selectedLocation = {
      city: cityData.name || cityData.city,
      state: cityData.state || 'India',
      latitude: cityData.latitude || 17.385044,
      longitude: cityData.longitude || 78.486671,
    };

    setLocationState(selectedLocation);
    setSource('manual');
    setPermission('granted');

    if (onSuccess) onSuccess(selectedLocation);
  };

  // Trigger location change helper
  const changeLocation = () => {
    setPermission('prompt');
  };

  // Reset location state
  const clearLocation = () => {
    setLocationState({
      city: 'Hyderabad',
      state: 'Telangana',
      latitude: 17.385044,
      longitude: 78.486671,
    });
    setSource('default');
    setPermission('prompt');
  };

  return (
    <LocationContext.Provider
      value={{
        location,
        source,
        loading,
        permission,
        requestCurrentLocation,
        selectCity,
        changeLocation,
        clearLocation,
      }}
    >
      {children}
    </LocationContext.Provider>
  );
};

export default LocationProvider;
