import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Resolve static folder
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const publicPath = path.join(__dirname, 'public');

app.use(express.json());
app.use(express.static(publicPath));

// Endpoint to generate product plans
app.post('/api/generate', async (req, res) => {
  const { idea } = req.body;

  if (!idea || idea.trim().length === 0) {
    return res.status(400).json({ error: 'Product idea is required.' });
  }

  const apiKey = process.env.GEMINI_API_KEY;

  if (apiKey && apiKey.trim().length > 0) {
    try {
      const result = await generateWithGemini(idea, apiKey);
      return res.json(result);
    } catch (error) {
      console.error('Gemini API Error:', error);
      // Fallback to mock on API error but log it
      console.log('Falling back to high-quality local generator due to API error.');
    }
  }

  // Fallback to high-quality mock generator
  const plan = generateMockPlan(idea);
  return res.json(plan);
});

// Serve frontend index.html for all client-side routes
app.get('*', (req, res) => {
  res.sendFile(path.join(publicPath, 'index.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`ProductForge AI is running on http://localhost:${PORT}`);
});

/**
 * Call Gemini API using native fetch with structured schema
 */
async function generateWithGemini(idea, apiKey) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;
  
  const systemPrompt = `You are a world-class Product Management expert. Your job is to take a product idea and generate a comprehensive, highly detailed product launch package. 
Your output must be a valid JSON object matching the requested schema. Inside each string property, write detailed, professional, structured Markdown (including headings, subheadings, bullet points, and tables where appropriate) that is highly specific to the user's idea. Do not use generic placeholders. Make the plans ready to present to stakeholders.`;

  const userPrompt = `Generate a complete product plan for the following product idea: "${idea}"`;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      contents: [
        {
          role: 'user',
          parts: [
            { text: systemPrompt },
            { text: userPrompt }
          ]
        }
      ],
      generationConfig: {
        responseMimeType: 'application/json',
        responseSchema: {
          type: 'OBJECT',
          properties: {
            marketResearch: { 
              type: 'STRING',
              description: 'Detailed Market Research in Markdown. Include Market Trends, Target Market & Sizing (TAM/SAM/SOM), Competitor Analysis (at least 3 competitors in a table), and SWOT Analysis.' 
            },
            personas: { 
              type: 'STRING',
              description: 'User Personas in Markdown. Define 2 detailed personas with Name, Role, Goals, Pain Points, and a Scenarios/User Journey.' 
            },
            prd: { 
              type: 'STRING',
              description: 'Product Requirements Document (PRD) in Markdown. Include Executive Summary, Goals, User Stories (format: As a..., I want to..., So that...), Key Features (Functional Requirements), Non-Functional Requirements, and Design Constraints.' 
            },
            roadmap: { 
              type: 'STRING',
              description: 'Product Roadmap in Markdown. Outline a 3-Phase release schedule. Phase 1 (MVP) with core features and timeline, Phase 2 (Growth/Expansion), and Phase 3 (Scale/Advanced AI features).' 
            },
            kpis: { 
              type: 'STRING',
              description: 'Key Performance Indicators (KPIs) in Markdown. List specific, measurable success metrics categorized by Acquisition, Activation, Retention, Engagement, and Revenue/LTV.' 
            }
          },
          required: ['marketResearch', 'personas', 'prd', 'roadmap', 'kpis']
        }
      }
    })
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`Gemini API responded with status ${response.status}: ${errText}`);
  }

  const data = await response.json();
  const textContent = data.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!textContent) {
    throw new Error('Failed to retrieve content parts from Gemini response.');
  }

  return JSON.parse(textContent);
}

/**
 * Generate a high-quality customized mock product plan based on keywords
 */
function generateMockPlan(idea) {
  // Extract a sensible product name or default
  let productName = 'ProductForge Innovation';
  const cleanIdea = idea.replace(/['"]/g, '').trim();
  
  // Try to find a good name from the first sentence or keywords
  const nameMatch = cleanIdea.match(/called\s+([A-Za-z0-9\s_-]+)/i) || 
                    cleanIdea.match(/name[d]?\s+([A-Za-z0-9\s_-]+)/i) ||
                    cleanIdea.match(/^([A-Za-z0-9\s_-]{3,20})/i);
                    
  if (nameMatch && nameMatch[1]) {
    productName = nameMatch[1].trim();
  } else {
    // Take the first 3 words
    const words = cleanIdea.split(/\s+/).slice(0, 3);
    if (words.length > 0) {
      productName = words.map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ') + ' App';
    }
  }

  // Detect category
  const ideaLower = cleanIdea.toLowerCase();
  let category = 'SaaS Platform';
  let targetAudience = 'Business Professionals';
  let keyProblem = 'inefficient workflows and lack of centralized collaboration tools';
  let competitorA = 'Atlassian Jira';
  let competitorB = 'Monday.com';
  let competitorC = 'ClickUp';

  if (ideaLower.includes('ai') || ideaLower.includes('gpt') || ideaLower.includes('llm') || ideaLower.includes('model') || ideaLower.includes('intelligence')) {
    category = 'AI-Powered System';
    targetAudience = 'Developers, Enterprises, and Creators';
    keyProblem = 'time-consuming content generation, manual analysis, and high cognitive load';
    competitorA = 'OpenAI Enterprise';
    competitorB = 'Anthropic Claude';
    competitorC = 'Copy.ai / Jasper';
  } else if (ideaLower.includes('food') || ideaLower.includes('restaurant') || ideaLower.includes('cook') || ideaLower.includes('delivery')) {
    category = 'FoodTech Service';
    targetAudience = 'Busy Urban Dwellers & Families';
    keyProblem = 'difficulty finding healthy meal options, long preparation times, and high delivery fees';
    competitorA = 'Uber Eats';
    competitorB = 'HelloFresh';
    competitorC = 'DoorDash';
  } else if (ideaLower.includes('finance') || ideaLower.includes('money') || ideaLower.includes('budget') || ideaLower.includes('invest') || ideaLower.includes('crypto')) {
    category = 'Fintech Application';
    targetAudience = 'Retail Investors & Budget-Conscious Individuals';
    keyProblem = 'complex portfolio management, hidden transaction fees, and lack of financial literacy';
    competitorA = 'Robinhood';
    competitorB = 'Mint / Copilot';
    competitorC = 'Acorns';
  } else if (ideaLower.includes('fit') || ideaLower.includes('health') || ideaLower.includes('gym') || ideaLower.includes('workout') || ideaLower.includes('pet')) {
    category = 'Health & Wellness Platform';
    targetAudience = 'Health Enthusiasts and Daily Active Individuals';
    keyProblem = 'fragmented fitness trackers, lack of personalized workout/nutrition plans, and low motivation';
    competitorA = 'MyFitnessPal';
    competitorB = 'Strava';
    competitorC = 'Whoop / Apple Health';
  } else if (ideaLower.includes('educat') || ideaLower.includes('school') || ideaLower.includes('learn') || ideaLower.includes('course') || ideaLower.includes('student')) {
    category = 'EdTech Platform';
    targetAudience = 'Students, Lifelong Learners, and Educators';
    keyProblem = 'rigid course structures, lack of interactive feedback, and expensive tuition rates';
    competitorA = 'Duolingo';
    competitorB = 'Coursera';
    competitorC = 'Quizlet / Udemy';
  } else if (ideaLower.includes('e-commerce') || ideaLower.includes('shop') || ideaLower.includes('store') || ideaLower.includes('sell') || ideaLower.includes('marketplace')) {
    category = 'E-commerce Marketplace';
    targetAudience = 'Online Vendors and Convenience Seekers';
    keyProblem = 'complex checkout flows, high transaction charges, and poor supplier transparency';
    competitorA = 'Shopify';
    competitorB = 'Etsy';
    competitorC = 'Amazon Seller Central';
  }

  // Create the tailored sections
  const marketResearch = `# Market Research Report: ${productName}

## Executive Summary
**${productName}** is entering the market as a disruptive **${category}** designed to address a critical friction point: ${keyProblem}. The target market represents a high-growth segment demanding modern UI/UX and seamless integration.

## Market Trends & Indicators
1. **Self-Service & AI Integration**: Customers are shifting towards platforms that offer automated insights rather than raw dashboard data.
2. **Privacy First**: Strong regulatory headwinds (GDPR, CCPA) require encryption and transparent data governance.
3. **Hyper-Personalization**: Users expect interfaces and algorithms tailored exactly to their work behaviors.

## Target Sizing (TAM, SAM, SOM)
- **Total Addressable Market (TAM)**: $12.5 Billion globally (representing the entire ${category} sector).
- **Serviceable Addressable Market (SAM)**: $2.4 Billion (representing modern web-first solutions targeting ${targetAudience}).
- **Serviceable Obtainable Market (SOM)**: $85 Million (initial target captured within 3 years of product launch).

## Competitor Analysis
Below is a comparative breakdown of key competitors relative to **${productName}**:

| Competitor | Strengths | Weaknesses | ${productName} Advantage |
| :--- | :--- | :--- | :--- |
| **${competitorA}** | Massive user base, established brand trust. | Legacy code, slow onboarding, complex configurations. | 10x faster setup, zero-configuration defaults. |
| **${competitorB}** | Robust integrations, flexible workflow engines. | High license costs, bloated desktop applications. | Modular pricing model, light-weight client UI. |
| **${competitorC}** | Extensive feature set, aggressive marketing. | Steep learning curve, poor mobile usability. | Fluid mobile responsive design, AI-driven guidance. |

## SWOT Analysis
- **Strengths**: Built on modern web architecture; highly performant; AI-first interface design.
- **Weaknesses**: Lower initial brand recognition; dependent on third-party cloud APIs.
- **Opportunities**: Rapidly growing adoption of automated toolchains in the **${targetAudience}** demographic.
- **Threats**: Rapid imitation by entrenched giants; downward pricing pressures.
`;

  const personas = `# Target User Personas: ${productName}

We have identified two distinct primary user segments that experience the core problems solved by **${productName}**.

---

## Persona 1: Sarah, The Hustler (Primary User)

\`\`\`
  Name: Sarah Jenkins
  Age: 29
  Role: Operations Specialist / Digital Lead
  Tech Savviness: High
\`\`\`

### Background
Sarah manages day-to-day operations and coordinates cross-functional projects. She is constantly switching between multiple dashboards, spreadsheet lists, and chat groups.

### Goals
- Centralize workflow tracking to eliminate manual reports.
- Decrease time spent on repetitive tasks by at least 40%.
- Share project statuses instantly with external stakeholders.

### Pain Points
- Current software tools are bloated, loading slowly on mobile.
- Pricing plans charge heavily for read-only user access.
- Confusing onboarding interfaces require training new hires.

### User Scenario
Sarah is travelling to a client meeting. She receives a message asking for an update on product specs. She opens **${productName}** on her phone, accesses the dashboard in under two seconds, copies a shareable secure URL, and drops it into the chat immediately.

---

## Persona 2: Marcus, The Technical Director (Buyer / Advisor)

\`\`\`
  Name: Marcus Chen
  Age: 42
  Role: VP of Product & Tech
  Tech Savviness: Expert
\`\`\`

### Background
Marcus is responsible for selecting software, managing data compliance, and approving software budgets. He values safety, security, and developer ergonomics.

### Goals
- Secure the organization's IP and satisfy audit compliance requirements.
- Standardize on collaborative tools that integrate with existing APIs.
- Keep licensing overhead predictable.

### Pain Points
- Vendors lock data into proprietary formats, preventing data exports.
- Complicated API limits break internal reporting.
- Lack of granular role-based permissions (RBAC).

### User Scenario
Marcus is auditing software packages before a quarterly board review. He logs into **${productName}**, downloads a standard compliance audit report in PDF, reviews the security settings, and easily creates credentials for his external security auditor.
`;

  const prd = `# Product Requirements Document (PRD)

## 1. Document Control & Purpose
This document outlines the requirements for the initial launch of **${productName}**. It defines scope, user stories, and technical parameters to guide design and development teams.

## 2. Core Value Proposition & Objectives
- **Objective 1**: Build a highly performant **${category}** optimized for speed (page load < 1.5s).
- **Objective 2**: Reduce friction in setup, targeting less than 3 clicks to produce the first core output.
- **Objective 3**: Implement a modern dark-mode interface centered around clean data tables and visualizations.

## 3. User Stories

| Story ID | User Role | Action | Value / Outcome |
| :--- | :--- | :--- | :--- |
| **US-01** | Sarah | Enter my product idea in plain text | Immediately receive a modular, structured execution outline |
| **US-02** | Sarah | Filter outputs by category or timeline | Focus only on immediately actionable items without clutter |
| **US-03** | Marcus | View security settings and exports | Download system states to PDF/Markdown for executive reports |
| **US-04** | Developer | Access standard API keys and endpoints | Integrate the platform inputs into automated pipelines |

## 4. Functional Requirements (MVP Scope)

### 4.1 Input Console
- Rich text editor or high-contrast text area with character counts.
- Dynamic input validation notifying users of empty states before submissions.
- Quick templates to auto-populate sample ideas.

### 4.2 Dashboard & Tabs Panel
- Layout separating inputs from generated plan components.
- Modern tabs with active underlines and smooth transitions to switch sections.
- Markdown rendering support (bullet points, tables, code blocks).

### 4.3 Export Systems
- "Copy Section" buttons that copy clean plain text to the clipboard.
- "Export Markdown" button downloading the entire comprehensive plan.

## 5. Non-Functional Requirements
- **Performance**: High Core Web Vitals (LCP < 2.0s, INP < 150ms).
- **Accessibility**: Full compliance with WCAG 2.1 AA standards (color contrasts, keyboard-accessible tabs, semantic HTML labels).
- **Stack Compatibility**: Client-side execution degrades gracefully if scripts or styles fail to load.
`;

  const roadmap = `# Product Implementation Roadmap

This roadmap outlines the launch timeline for **${productName}**, divided into three distinct phases to ensure validation before scaling.

\`\`\`mermaid
gantt
    title Product Release Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1 (MVP)
    Design & Wireframing :a1, 2026-06-01, 10d
    Core Features Build  :after a1, 15d
    section Phase 2 (Growth)
    Auth & Collaboration:2026-07-01, 20d
    Advanced Reporting   :10d
    section Phase 3 (Scale)
    AI Recommendations   :2026-08-01, 30d
\`\`\`

---

## Phase 1: Minimum Viable Product (MVP) - *Months 1-2*
- **Focus**: Core content generator engine, sleek responsive dashboard UI, and basic text exports.
- **Milestones**:
  - Launch internal beta testing program (50 participants).
  - Implement full keyboard accessibility and semantic document structure.
  - Setup local client caching to prevent data loss on page refreshes.

## Phase 2: Collaboration & Advanced Analytics - *Months 3-4*
- **Focus**: User accounts, team collaboration workspace, and customizable strategy templates.
- **Milestones**:
  - Integrate user authentication (Social login, magic links).
  - Add "Share Plan" secure links allowing view-only access to managers.
  - Deliver dynamic Gantt chart visualizers for the Product Roadmap section.

## Phase 3: AI-Driven Insights & Custom Integrations - *Months 5-6*
- **Focus**: Deep generative AI integration, automated competitor feed ingestion, and API endpoints.
- **Milestones**:
  - Release native extensions for Slack and Jira.
  - Implement AI chat assistant side panel to modify individual PRD lines.
  - Roll out localized translation supporting 6 languages (Spanish, German, French, Japanese, Mandarin, Portuguese).
`;

  const kpis = `# Key Performance Indicators (KPIs)

To monitor the performance and business viability of **${productName}**, we track specific, actionable metrics rather than vanity indicators.

## Success Metrics Framework

### 1. Acquisition & Reach
- **Conversion Rate**: Percentage of landing page visitors who complete their first strategy generation (Target: **> 12%**).
- **CAC (Customer Acquisition Cost)**: Keeping marketing expenses below **$18** per registered user.
- **Organic Traffic Share**: Percentage of traffic generated via SEO blogs and peer recommendations (Target: **> 45%**).

### 2. Activation & First Value
- **Time to Value (TTV)**: Average duration from landing page entry to strategy rendering (Target: **< 90 seconds**).
- **First-Day Export Rate**: Percentage of active sign-ups that copy or export their plan immediately (Target: **> 60%**).
- **Onboarding Completion**: Percentage of users who complete the initial 3-step feature tour (Target: **> 85%**).

### 3. Retention & Engagement
- **Weekly Active Users (WAU)**: Count of active product managers logging back in to review or update plans.
- **1-Month Retention (M1)**: Percentage of users returning in Month 2 to create a second product forge (Target: **> 28%**).
- **Core Session Duration**: Time spent editing and interacting with PRD lines (Target: **> 8 minutes**).

### 4. Revenue & Value Capture (Future Focus)
- **ARPU (Average Revenue Per User)**: target subscription pricing of **$29/month** for Pro features.
- **LTV/CAC Ratio**: Ratio of customer lifetime value to cost of acquisition (Target: **> 3.5x**).
- **Expansion Rate**: Percentage of users adding more than 3 seat licenses in their organization (Target: **> 15%**).
`;

  return {
    marketResearch,
    personas,
    prd,
    roadmap,
    kpis
  };
}

