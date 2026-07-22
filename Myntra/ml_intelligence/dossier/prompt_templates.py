"""
Dossier Prompt Templates Module for ml_intelligence
Defines RAG markdown template strings for Sourcing Dossiers and BD Field Scripts.
"""

DOSSIER_MARKDOWN_TEMPLATE = """# 📑 SOURCING INTELLIGENCE DOSSIER
## Merchant: {canonical_name}
**Location**: {city}, {state} | **Trust Rating**: ⭐ {trust_score}/100 ({badge})

---

### 1. Executive Summary
{executive_summary}

### 2. Verified Trust Evidence
{trust_evidence}

### 3. Strategic Opportunity & Category Fit
• **Target Myntra Category**: {suggested_category}
• **Business Opportunity**: {business_opportunity}

### 4. Tailored BD Field Agent Pitch Script
{bd_pitch_script}

### 5. Objection Handling Strategy
• **Owner Concern**: {objection_concern}
• **BD Response**: {objection_response}
"""
