import React from 'react';
import { useParams } from 'react-router-dom';
import PageContainer from '../../components/layout/PageContainer';
import SectionContainer from '../../components/layout/SectionContainer';
import SectionHeader from '../../components/common/SectionHeader';

/**
 * Placeholder Shopping Hub Details Page component
 */
export const HubDetailsPage = () => {
  const { hubId } = useParams();

  return (
    <PageContainer>
      <SectionContainer>
        <SectionHeader
          tagline={`Shopping Hub ID: ${hubId}`}
          title="Shopping Hub Details"
          subtitle="Detailed view for iconic shopping markets, store directory, specialties, and visit guides."
        />

        <div className="p-8 bg-surface border border-dashed border-border rounded-3xl text-center text-text-muted space-y-2">
          <p className="text-sm font-semibold">Hub Details Page Placeholder (Hub ID: {hubId})</p>
          <p className="text-xs text-text-muted/80">
            Render hub map, signature crafts, and associated retailer store cards here.
          </p>
        </div>
      </SectionContainer>
    </PageContainer>
  );
};

export default HubDetailsPage;
