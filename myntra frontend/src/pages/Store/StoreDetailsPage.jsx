import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';

// Sub-components Imports
import PageContainer from '../../components/layout/PageContainer';
import StoreHero from '../../components/store/StoreHero';
import StoreStory from '../../components/store/StoreStory';
import HeritageTimeline from '../../components/store/HeritageTimeline';
import HeritageMetrics from '../../components/store/HeritageMetrics';
import TrustSection from '../../components/store/TrustSection';
import RegionalSpecialties from '../../components/store/RegionalSpecialties';
import RegionalHeritageBanner from '../../components/store/RegionalHeritageBanner';
import FeaturedCollections from '../../components/store/FeaturedCollections';
import SignatureProducts from '../../components/store/SignatureProducts';
import StoreGallery from '../../components/store/StoreGallery';
import StoreInformation from '../../components/store/StoreInformation';
import CustomerMoments from '../../components/store/CustomerMoments';
import NearbyStores from '../../components/store/NearbyStores';
import StickyActionBar from '../../components/store/StickyActionBar';

// Data Provider
import { getStoreData } from '../../data/mockStores';

/**
 * StoreDetailsPage Component (Route: /store/:storeId)
 * Award-winning digital storytelling experience for regional fashion destinations.
 */
export const StoreDetailsPage = () => {
  const { storeId } = useParams();
  const store = getStoreData(storeId);

  // Scroll to top on store ID change
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [storeId]);

  return (
    <PageContainer maxWidth="max-w-7xl" padding="px-4 sm:px-6 lg:px-8 py-6 md:py-10 pb-24 md:pb-28">
      <div className="space-y-16 sm:space-y-20 md:space-y-24">
        
        {/* 1. Hero Section (Clickable Shopping Hub) */}
        <motion.section
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <StoreHero store={store} />
        </motion.section>

        {/* 2. Our Story & Heritage Timeline */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className="space-y-16"
        >
          <StoreStory story={store.story} />
          <HeritageTimeline timeline={store.timeline} />
        </motion.section>

        {/* 3. Heritage Metrics */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <HeritageMetrics metrics={store.metrics} />
        </motion.section>

        {/* 4. Why Shoppers Trust This Store */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <TrustSection trustHighlights={store.trustHighlights} />
        </motion.section>

        {/* 5. Regional Specialties */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <RegionalSpecialties specialties={store.specialties} />
        </motion.section>

        {/* 6. Regional Heritage Banner */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <RegionalHeritageBanner banner={store.heritageBanner} />
        </motion.section>

        {/* 7. Featured Collections */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <FeaturedCollections collections={store.collections} />
        </motion.section>

        {/* 8. Signature Products */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <SignatureProducts products={store.signatureProducts} />
        </motion.section>

        {/* 9. Store Experience Gallery */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <StoreGallery gallery={store.gallery} />
        </motion.section>

        {/* 10. Location Experience */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <StoreInformation location={store.location} information={store.information} />
        </motion.section>

        {/* 11. Customer Moments */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <CustomerMoments moments={store.customerMoments} />
        </motion.section>

        {/* 12. Continue Your Heritage Journey */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <NearbyStores nearbyStores={store.nearbyStores} />
        </motion.section>

      </div>

      {/* Sticky Action Bar */}
      <StickyActionBar store={store} />
    </PageContainer>
  );
};

export default StoreDetailsPage;
