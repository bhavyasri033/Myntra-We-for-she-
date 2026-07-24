import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { MapPin, Navigation, Compass } from 'lucide-react';
import PageContainer from '../../components/layout/PageContainer';
import LocationCard from '../../components/location/LocationCard';
import LocationIllustration from '../../components/location/LocationIllustration';
import LocationButton from '../../components/location/LocationButton';
import IndiaBackdrop from '../Landing/IndiaBackdrop';
import { ROUTES } from '../../constants/routes';
import { LocationContext } from '../../context/LocationContext';

/**
 * LocationPermissionPage Component (Route: /location-permission)
 * Onboarding screen prompting user to choose between auto-location discovery or manual city selection.
 */
export const LocationPermissionPage = () => {
  const navigate = useNavigate();
  const { requestCurrentLocation } = useContext(LocationContext);

  const handleUseCurrentLocation = () => {
    // Trigger mock location request and navigate to loading screen
    requestCurrentLocation(() => {
      navigate(ROUTES.LOCATING);
    });
  };

  const handleChooseCity = () => {
    navigate(ROUTES.CHOOSE_CITY);
  };

  return (
    <PageContainer maxWidth="max-w-4xl" padding="px-4 py-8 md:py-16 flex items-center justify-center min-h-[calc(100vh-5rem)]">
      <IndiaBackdrop />

      <div className="relative z-10 w-full flex flex-col items-center justify-center my-auto py-6">
        <LocationCard maxWidth="max-w-[520px]">
          {/* Animated Pin Illustration */}
          <LocationIllustration />

          {/* Heading */}
          <h1 className="font-editorial text-3xl sm:text-4xl font-bold text-text-primary tracking-tight leading-tight mb-3">
            Find Fashion Near You
          </h1>

          {/* Subtitle */}
          <p className="text-xs sm:text-sm text-text-muted font-normal max-w-md mx-auto leading-relaxed mb-8">
            Allow location access to discover trusted regional fashion stores, iconic shopping hubs, and authentic collections around you.
          </p>

          {/* Actions */}
          <div className="space-y-3 max-w-sm mx-auto">
            <LocationButton
              onClick={handleUseCurrentLocation}
              variant="primary"
              icon={Navigation}
            >
              Use Current Location
            </LocationButton>

            <LocationButton
              onClick={handleChooseCity}
              variant="secondary"
              icon={Compass}
            >
              Choose City Instead
            </LocationButton>
          </div>
        </LocationCard>
      </div>
    </PageContainer>
  );
};

export default LocationPermissionPage;
