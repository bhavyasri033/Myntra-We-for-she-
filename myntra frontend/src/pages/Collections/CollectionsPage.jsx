import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ChevronRight } from 'lucide-react';

// Layout & Component Imports
import PageContainer from '../../components/layout/PageContainer';
import CompactHero from '../../components/collections/CompactHero';
import DepartmentTabs from '../../components/collections/DepartmentTabs';
import CategoryTabs from '../../components/collections/CategoryTabs';
import FilterToolbar from '../../components/collections/FilterToolbar';
import CatalogProductGrid from '../../components/collections/CatalogProductGrid';
import StickyMobileFilter from '../../components/collections/StickyMobileFilter';

// Data & Route Imports
import { getCollectionsData } from '../../data/mockCollections';
import { getStoreDetailsPath } from '../../constants/routes';

/**
 * CollectionsPage Component (Route: /collections/:storeId)
 * Catalog-first browsing experience for fast product discovery.
 */
export const CollectionsPage = () => {
  const { storeId } = useParams();
  const collectionsData = getCollectionsData(storeId);

  const [activeDepartment, setActiveDepartment] = useState('women');
  const [activeCategory, setActiveCategory] = useState('all');
  const [selectedFabric, setSelectedFabric] = useState(null);
  const [selectedColor, setSelectedColor] = useState(null);
  const [sortBy, setSortBy] = useState('popularity');

  // Scroll to top on store change
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [storeId]);

  // Reset category when department changes
  const handleDepartmentChange = (deptId) => {
    setActiveDepartment(deptId);
    const firstCat = collectionsData.categoriesByDepartment[deptId]?.[0]?.id || 'all';
    setActiveCategory(firstCat);
  };

  const currentCategories = collectionsData.categoriesByDepartment[activeDepartment] || [];
  const currentDept = collectionsData.departments.find((d) => d.id === activeDepartment);
  const currentCatObj = currentCategories.find((c) => c.id === activeCategory);

  return (
    <div className="min-h-screen bg-background text-text-primary">
      {/* 1. Sticky Department Navigation (Top 0) */}
      <DepartmentTabs
        departments={collectionsData.departments}
        activeDepartment={activeDepartment}
        onSelectDepartment={handleDepartmentChange}
      />

      {/* 2. Sticky Category Navigation (Top 49px) */}
      <CategoryTabs
        categories={currentCategories}
        activeCategory={activeCategory}
        onSelectCategory={setActiveCategory}
      />

      {/* Main Page Content */}
      <PageContainer maxWidth="max-w-7xl" padding="px-4 sm:px-6 lg:px-8 py-4 sm:py-6 pb-24 sm:pb-28">
        <div className="space-y-6">
          
          {/* Breadcrumb Navigation */}
          <nav className="flex items-center gap-1.5 text-xs text-text-muted font-medium overflow-x-auto py-1" aria-label="Breadcrumb">
            <Link to="/" className="hover:text-primary transition-colors">Home</Link>
            <ChevronRight className="w-3 h-3 text-border" />
            <Link to="/nearby" className="hover:text-primary transition-colors">Nearby</Link>
            <ChevronRight className="w-3 h-3 text-border" />
            <Link to={getStoreDetailsPath(storeId)} className="hover:text-primary transition-colors">
              {collectionsData.storeName}
            </Link>
            <ChevronRight className="w-3 h-3 text-border" />
            <span className="text-text-primary font-semibold">{currentDept?.label || 'Women'}</span>
            {currentCatObj && currentCatObj.id !== 'all' && currentCatObj.id !== 'all-m' && (
              <>
                <ChevronRight className="w-3 h-3 text-border" />
                <span className="text-primary font-semibold">{currentCatObj.name}</span>
              </>
            )}
          </nav>

          {/* Compact Hero (<50% vertical height) */}
          <CompactHero collectionsData={collectionsData} />

          {/* Filter & Sort Toolbar */}
          <FilterToolbar
            totalCount={collectionsData.products.length}
            sortBy={sortBy}
            onSortChange={setSortBy}
            selectedFabric={selectedFabric}
            onFabricChange={setSelectedFabric}
            selectedColor={selectedColor}
            onColorChange={setSelectedColor}
          />

          {/* Primary Content: Product Catalog Grid */}
          <CatalogProductGrid
            products={collectionsData.products}
            activeDepartment={activeDepartment}
            activeCategory={activeCategory}
            selectedFabric={selectedFabric}
            selectedColor={selectedColor}
            sortBy={sortBy}
          />

        </div>

        {/* Sticky Mobile Filter Button & Sheet */}
        <StickyMobileFilter
          departments={collectionsData.departments}
          activeDepartment={activeDepartment}
          onSelectDepartment={handleDepartmentChange}
          categories={currentCategories}
          activeCategory={activeCategory}
          onSelectCategory={setActiveCategory}
          sortBy={sortBy}
          onSortChange={setSortBy}
        />
      </PageContainer>
    </div>
  );
};

export default CollectionsPage;
