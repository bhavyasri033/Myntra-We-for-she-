import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';

// Layout & Component Imports
import PageContainer from '../../components/layout/PageContainer';
import ProductBreadcrumb from '../../components/product/ProductBreadcrumb';
import ProductHero from '../../components/product/ProductHero';
import ProductStory from '../../components/product/ProductStory';
import MeetTheStore from '../../components/product/MeetTheStore';
import CraftDetails from '../../components/product/CraftDetails';
import ProductOptions from '../../components/product/ProductOptions';
import WhyLoveSection from '../../components/product/WhyLoveSection';
import Specifications from '../../components/product/Specifications';
import SimilarProducts from '../../components/product/SimilarProducts';
import MoreFromStore from '../../components/product/MoreFromStore';
import HeritagePromise from '../../components/product/HeritagePromise';
import StickyPurchaseBar from '../../components/product/StickyPurchaseBar';

// Data Provider
import { getProductData } from '../../data/mockProducts';

/**
 * ProductDetailsPage Component (Route: /product/:productId)
 * Storytelling-first luxury product details page for authentic regional fashion creations.
 */
export const ProductDetailsPage = () => {
  const { productId } = useParams();
  const product = getProductData(productId);

  const [selectedColor, setSelectedColor] = useState(product.options?.colors?.[0]?.name || 'Crimson Red & Gold');
  const [selectedSize, setSelectedSize] = useState(product.options?.sizes?.[0] || 'Unstitched Saree (6.3m)');
  const [selectedQuantity, setSelectedQuantity] = useState(1);

  // Scroll to top on product change
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (product.options) {
      if (product.options.colors?.[0]) setSelectedColor(product.options.colors[0].name);
      if (product.options.sizes?.[0]) setSelectedSize(product.options.sizes[0]);
      setSelectedQuantity(1);
    }
  }, [productId]);

  return (
    <PageContainer maxWidth="max-w-7xl" padding="px-4 sm:px-6 lg:px-8 py-6 md:py-10 pb-24 md:pb-28">
      <div className="space-y-16 sm:space-y-20 md:space-y-24">
        
        {/* 1. Breadcrumb & 2. Product Hero */}
        <div className="space-y-6">
          <ProductBreadcrumb product={product} />
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
          >
            <ProductHero
              product={product}
              selectedColor={selectedColor}
              selectedSize={selectedSize}
              onSelectColor={setSelectedColor}
              onSelectSize={setSelectedSize}
            />
          </motion.div>
        </div>

        {/* 3. Product Story */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <ProductStory story={product.story} />
        </motion.section>

        {/* 4. Meet The Store */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <MeetTheStore store={product.store} />
        </motion.section>

        {/* 5. Craft Details */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <CraftDetails craftDetails={product.craftDetails} />
        </motion.section>

        {/* 6. Select Options */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <ProductOptions
            options={product.options}
            selectedColor={selectedColor}
            selectedSize={selectedSize}
            selectedQuantity={selectedQuantity}
            onSelectColor={setSelectedColor}
            onSelectSize={setSelectedSize}
            onSelectQuantity={setSelectedQuantity}
          />
        </motion.section>

        {/* 7. Why You'll Love It */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <WhyLoveSection features={product.whyLove} />
        </motion.section>

        {/* 8. Specifications */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <Specifications specifications={product.specifications} />
        </motion.section>

        {/* 9. Similar Products */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <SimilarProducts products={product.similarProducts} />
        </motion.section>

        {/* 10. More From This Store */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <MoreFromStore products={product.moreFromStore} store={product.store} />
        </motion.section>

        {/* 11. Heritage Promise */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <HeritagePromise />
        </motion.section>

      </div>

      {/* 12. Sticky Purchase Bar */}
      <StickyPurchaseBar product={product} selectedSize={selectedSize} />
    </PageContainer>
  );
};

export default ProductDetailsPage;
