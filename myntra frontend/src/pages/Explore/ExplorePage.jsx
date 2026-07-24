import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { MapPin, ShieldCheck, ArrowRight, Compass, Sparkles } from 'lucide-react';

// Layout & Route Imports
import PageContainer from '../../components/layout/PageContainer';
import SectionHeader from '../../components/common/SectionHeader';
import IndiaBackdrop from '../Landing/IndiaBackdrop';
import { getStateDetailsPath } from '../../constants/routes';
import { STATES_LIST } from '../../data/mockStates';

/**
 * ExplorePage Component (Route: /explore)
 * Explore India destination page mapping state fashion identities to State Details pages (/state/:stateId).
 */
export const ExplorePage = () => {
  const navigate = useNavigate();
  const [selectedRegion, setSelectedRegion] = useState('All');

  // Scroll to top on mount
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  // Filter states by region
  const regions = ['All', 'South India', 'North India', 'West India', 'East India'];
  const filteredStates = selectedRegion === 'All'
    ? STATES_LIST
    : STATES_LIST.filter((s) => s.region === selectedRegion);

  return (
    <PageContainer maxWidth="max-w-7xl" padding="px-4 sm:px-6 lg:px-8 py-6 md:py-10 pb-24 md:pb-28">
      <div className="space-y-12 sm:space-y-16">
        
        {/* Editorial Page Header */}
        <div className="relative rounded-3xl bg-surface border border-border/80 p-8 sm:p-12 shadow-card overflow-hidden text-center space-y-4">
          <IndiaBackdrop />

          <div className="relative z-10 max-w-3xl mx-auto space-y-3">
            <div className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full bg-primary/10 text-primary border border-primary/20 text-xs font-semibold">
              <Compass className="w-3.5 h-3.5" />
              <span>India Fashion Travel Guide</span>
            </div>

            <h1 className="font-editorial text-4xl sm:text-5xl font-bold text-text-primary tracking-tight leading-tight">
              Explore Regional Fashion Across India
            </h1>

            <p className="text-sm sm:text-base text-text-muted font-normal leading-relaxed">
              Select a state to uncover its iconic shopping hubs, master weaving heritage, and verified Regional Fashion Icons.
            </p>
          </div>
        </div>

        {/* Region Selector Pills */}
        <div className="flex items-center justify-center gap-2 overflow-x-auto custom-scrollbar no-scrollbar py-1">
          {regions.map((region) => (
            <button
              key={region}
              type="button"
              onClick={() => setSelectedRegion(region)}
              className={`px-4 py-2 rounded-full text-xs font-semibold transition-all shrink-0 cursor-pointer ${
                selectedRegion === region
                  ? 'bg-primary text-white shadow-subtle'
                  : 'bg-surface border border-border/80 text-text-primary hover:border-primary/40 hover:bg-background'
              }`}
            >
              {region}
            </button>
          ))}
        </div>

        {/* State Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          {filteredStates.map((state, index) => (
            <motion.div
              key={state.id}
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35, delay: index * 0.06 }}
              whileHover={{ y: -6 }}
              className="group bg-surface border border-border/80 rounded-3xl overflow-hidden shadow-card hover:shadow-elevated hover:border-primary/40 transition-all duration-300 flex flex-col justify-between"
            >
              {/* Cover Image */}
              <div className="relative h-60 w-full overflow-hidden bg-slate-950">
                <img
                  src={state.image}
                  alt={state.name}
                  className="w-full h-full object-cover opacity-85 transition-transform duration-700 group-hover:scale-105"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/20 to-transparent" />

                {/* Region Tag */}
                <span className="absolute top-4 left-4 px-3 py-1 rounded-full bg-surface/90 backdrop-blur-md text-[11px] font-semibold text-primary shadow-subtle">
                  {state.region}
                </span>

                {/* Hub Count Overlay */}
                <span className="absolute top-4 right-4 px-3 py-1 rounded-full bg-slate-950/70 backdrop-blur-md text-[11px] font-semibold text-white border border-white/20">
                  {state.hubCount} Shopping Hubs
                </span>

                {/* Title Overlay */}
                <div className="absolute bottom-4 left-4 right-4 text-white z-10">
                  <h3 className="font-editorial text-3xl font-bold tracking-tight">
                    {state.name}
                  </h3>
                </div>
              </div>

              {/* Card Details */}
              <div className="p-6 space-y-4 flex-1 flex flex-col justify-between">
                <p className="text-xs sm:text-sm text-text-muted font-normal leading-relaxed line-clamp-2">
                  {state.tagline}
                </p>

                {/* Key Metrics & Crafts */}
                <div className="space-y-3 pt-2 border-t border-border/60">
                  <div className="flex items-center justify-between text-xs font-semibold text-text-primary">
                    <span className="flex items-center gap-1 text-primary">
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>{state.storeCount} Verified Stores</span>
                    </span>
                    <span className="text-accent">{state.craftCount} Crafts</span>
                  </div>

                  <div className="flex flex-wrap gap-1">
                    {state.crafts.map((craft, i) => (
                      <span
                        key={i}
                        className="px-2 py-0.5 rounded-md bg-background border border-border/60 text-[10px] font-semibold text-text-muted"
                      >
                        {craft}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Direct CTA to State Details Page */}
                <div className="pt-2">
                  <Link
                    to={getStateDetailsPath(state.id)}
                    className="w-full py-3 px-4 rounded-2xl bg-primary text-white text-xs font-semibold hover:bg-primary-hover shadow-subtle transition-all duration-200 flex items-center justify-center gap-2 group/btn"
                  >
                    <span>Explore {state.name} Heritage</span>
                    <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover/btn:translate-x-1" />
                  </Link>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

      </div>
    </PageContainer>
  );
};

export default ExplorePage;
