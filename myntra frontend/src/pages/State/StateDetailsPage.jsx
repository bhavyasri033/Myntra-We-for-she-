import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';

// Layout & Component Imports
import PageContainer from '../../components/layout/PageContainer';
import StateBreadcrumb from '../../components/state/StateBreadcrumb';
import StateHero from '../../components/state/StateHero';
import FashionHeritage from '../../components/state/FashionHeritage';
import RegionalSpecialties from '../../components/state/RegionalSpecialties';
import ShoppingHubsSection from '../../components/state/ShoppingHubsSection';
import FeaturedStoresSection from '../../components/state/FeaturedStoresSection';
import StateHighlights from '../../components/state/StateHighlights';
import ExploreCTA from '../../components/state/ExploreCTA';

// Data Provider
import { getStateData } from '../../data/mockStates';

/**
 * StateDetailsPage Component (Route: /state/:stateId)
 * Editorial fashion travel guide introducing the state's fashion identity & shopping hubs.
 */
export const StateDetailsPage = () => {
  const { stateId } = useParams();
  const stateData = getStateData(stateId);

  // Scroll to top on state ID change
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [stateId]);

  const handleScrollToHubs = () => {
    const section = document.getElementById('primary-shopping-hubs');
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <PageContainer maxWidth="max-w-7xl" padding="px-4 sm:px-6 lg:px-8 py-6 md:py-10 pb-24 md:pb-28">
      <div className="space-y-16 sm:space-y-20 md:space-y-24">
        
        {/* 1. Breadcrumb & 2. State Hero */}
        <div className="space-y-6">
          <StateBreadcrumb stateName={stateData.name} />
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
          >
            <StateHero stateData={stateData} />
          </motion.div>
        </div>

        {/* 3. Fashion Heritage */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <FashionHeritage heritage={stateData.heritage} stateName={stateData.name} />
        </motion.section>

        {/* 4. Regional Specialties */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <RegionalSpecialties specialties={stateData.specialties} />
        </motion.section>

        {/* 5. Popular Shopping Hubs (PRIMARY VISUAL FOCUS) */}
        <motion.section
          id="primary-shopping-hubs"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <ShoppingHubsSection hubs={stateData.shoppingHubs} stateName={stateData.name} />
        </motion.section>

        {/* 6. Featured Regional Fashion Icons */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <FeaturedStoresSection stores={stateData.featuredStores} stateName={stateData.name} />
        </motion.section>

        {/* 7. State Highlights */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <StateHighlights stats={stateData.stats} stateName={stateData.name} />
        </motion.section>

        {/* 8. Explore Shopping Hubs CTA */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <ExploreCTA stateName={stateData.name} onScrollToHubs={handleScrollToHubs} />
        </motion.section>

      </div>
    </PageContainer>
  );
};

export default StateDetailsPage;
