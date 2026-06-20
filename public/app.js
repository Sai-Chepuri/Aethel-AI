// -------------------------------------------------------------
// PRODUCTFORGE AI FRONTEND CONTROLLER
// -------------------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {
  // Application State
  let generatedPlan = null;
  let activeTab = 'market_research';
  let isGenerating = false;

  // Elements Selection
  const form = document.getElementById('generator-form');
  const ideaTextarea = document.getElementById('product-idea');
  const submitBtn = document.getElementById('submit-btn');
  const clearBtn = document.getElementById('clear-input');
  const charCounter = document.getElementById('char-counter');
  
  const tabsNav = document.getElementById('tabs-navigation');
  const tabLinks = document.querySelectorAll('.tab-link');
  
  const stateEmpty = document.getElementById('state-empty');
  const stateLoading = document.getElementById('state-loading');
  const stateResult = document.getElementById('state-result');
  const loadingSubtext = document.getElementById('loading-subtext');
  const renderedContent = document.getElementById('rendered-content');
  
  const btnCopyTab = document.getElementById('btn-copy-tab');
  const btnExportAll = document.getElementById('btn-export-all');
  const apiStatus = document.getElementById('api-status');

  // Quick Template Content Maps
  const templates = {
    SaaS: "A subscription-based mobile application for pet health tracking that integrates with smart collars, tracks daily exercise, calculates calorie needs, and allows pet owners to instantly export health reports to veterinarians.",
    AI: "An automated AI code reviewer extension for developers that scans pull requests for security vulnerabilities, memory leaks, and performance bottlenecks, offering automated inline refactored fixes.",
    FoodTech: "An eco-friendly local food delivery marketplace connecting urban households with organic home cooks. Meals are delivered in zero-waste, heat-insulated, reusable containers that are collected on the next order.",
    Fintech: "A personal micro-budgeting app that auto-links bank accounts, categorizes expenses using machine learning, alerts users of upcoming subscription rate changes, and round-ups spare change into micro-investments."
  };

  // 1. Textarea Event Listeners
  ideaTextarea.addEventListener('input', () => {
    const len = ideaTextarea.value.length;
    charCounter.textContent = `${len.toLocaleString()} character${len === 1 ? '' : 's'}`;
  });

  clearBtn.addEventListener('click', () => {
    ideaTextarea.value = '';
    charCounter.textContent = '0 characters';
    ideaTextarea.focus();
  });

  // 2. Quick Template Tags Selection
  document.querySelectorAll('.tag-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const type = btn.getAttribute('data-template');
      if (templates[type]) {
        ideaTextarea.value = templates[type];
        // Trigger input event to update character count
        ideaTextarea.dispatchEvent(new Event('input'));
        ideaTextarea.focus();
      }
    });
  });

  // 3. Form Submit Action
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (isGenerating) return;

    const idea = ideaTextarea.value.trim();
    if (!idea) return;

    // Transition States
    isGenerating = true;
    submitBtn.disabled = true;
    submitBtn.querySelector('.btn-text').textContent = 'Forging Plan...';
    
    stateEmpty.classList.add('hidden');
    stateResult.classList.add('hidden');
    stateLoading.classList.remove('hidden');
    
    // Lock tab navigation during loading
    tabsNav.setAttribute('inert', '');
    tabsNav.style.opacity = '0.4';

    // Start Checklist Animation Flow
    const animationController = startChecklistAnimation();

    try {
      // Trigger API Request
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ idea })
      });

      if (!response.ok) {
        throw new Error(`Server returned error: ${response.statusText}`);
      }

      const data = await response.json();
      
      // Complete remaining checklist steps quickly
      await animationController.completeAllSteps();
      
      // Save data to state
      generatedPlan = data.result || data;
      isGenerating = false;
      
      // Update UI state
      submitBtn.disabled = false;
      submitBtn.querySelector('.btn-text').textContent = 'Forge Product Plan';
      
      stateLoading.classList.add('hidden');
      stateResult.classList.remove('hidden');
      
      // Unlock tab navigation
      tabsNav.removeAttribute('inert');
      tabsNav.style.opacity = '1';
      
      // Render first tab
      switchTab('market_research');

    } catch (err) {
      console.error(err);
      animationController.failSteps();
      
      loadingSubtext.textContent = 'Generation failed. Please check backend logs or try again.';
      isGenerating = false;
      submitBtn.disabled = false;
      submitBtn.querySelector('.btn-text').textContent = 'Forge Product Plan';
    }
  });

  // 4. Tab Switching Control
  tabLinks.forEach(link => {
    link.addEventListener('click', () => {
      const tabId = link.getAttribute('data-tab');
      switchTab(tabId);
    });
  });

  // 4.5 Structured JSON to Markdown Converter
  function convertSectionToMarkdown(plan, section) {
    if (!plan) return '*No content generated.*';
    
    switch(section) {
      case 'market_research': {
        const mr = plan.market_research;
        if (!mr) return '*No market research data.*';
        
        let md = `# Market Research Report\n\n`;
        md += `## Executive Summary\n${mr.executive_summary || ''}\n\n`;
        
        md += `## Market Trends & Indicators\n`;
        if (mr.market_trends && mr.market_trends.length) {
          mr.market_trends.forEach(t => { md += `1. ${t}\n`; });
        } else {
          md += `*No trends available.*\n`;
        }
        md += `\n`;
        
        md += `## Market Sizing (TAM / SAM / SOM)\n`;
        if (mr.market_sizing) {
          md += `| Metric | Value | Scope | Rationale |\n| :--- | :--- | :--- | :--- |\n`;
          md += `| **TAM** | ${mr.market_sizing.tam || ''} | Entire global sector | ${mr.market_sizing.rationale || ''} |\n`;
          md += `| **SAM** | ${mr.market_sizing.sam || ''} | Target web segment | ${mr.market_sizing.rationale || ''} |\n`;
          md += `| **SOM** | ${mr.market_sizing.som || ''} | Target capture (3yr) | ${mr.market_sizing.rationale || ''} |\n`;
        }
        md += `\n`;
        
        md += `## SWOT Analysis\n`;
        if (mr.swot) {
          md += `### Strengths\n`;
          (mr.swot.strengths || []).forEach(s => { md += `- ${s}\n`; });
          md += `\n### Weaknesses\n`;
          (mr.swot.weaknesses || []).forEach(w => { md += `- ${w}\n`; });
          md += `\n### Opportunities\n`;
          (mr.swot.opportunities || []).forEach(o => { md += `- ${o}\n`; });
          md += `\n### Threats\n`;
          (mr.swot.threats || []).forEach(t => { md += `- ${t}\n`; });
        }
        return md;
      }
      
      case 'competitors': {
        const comps = plan.competitors;
        if (!comps || !comps.length) return '*No competitors list.*';
        
        let md = `# Competitor Analysis\n\n`;
        md += `| Competitor | Strengths | Weaknesses | Product Advantage |\n`;
        md += `| :--- | :--- | :--- | :--- |\n`;
        comps.forEach(c => {
          const str = (c.strengths || []).join(', ');
          const weak = (c.weaknesses || []).join(', ');
          md += `| **${c.name || ''}** | ${str} | ${weak} | ${c.differentiation || ''} |\n`;
        });
        return md;
      }
      
      case 'personas': {
        const personas = plan.personas;
        if (!personas || !personas.length) return '*No personas list.*';
        
        let md = `# User Personas\n\n`;
        personas.forEach((p, idx) => {
          md += `## Persona ${idx + 1} — ${p.name || ''}\n\n`;
          md += `\`\`\`\nAge   : ${p.age || ''}\nRole  : ${p.role || ''}\n\`\`\`\n\n`;
          
          md += `### Goals\n`;
          (p.goals || []).forEach(g => { md += `- ${g}\n`; });
          md += `\n`;
          
          md += `### Pain Points\n`;
          (p.pain_points || []).forEach(pp => { md += `- ${pp}\n`; });
          md += `\n`;
          
          md += `### Scenario & Journey\n${p.user_scenario || ''}\n\n---\n\n`;
        });
        return md;
      }
      
      case 'prd': {
        const prd = plan.prd;
        if (!prd) return '*No PRD data.*';
        
        let md = `# Product Requirements Document\n\n`;
        md += `## 1. Purpose & Scope\n${prd.purpose_scope || ''}\n\n`;
        
        md += `## 2. Goals & Success Criteria\n`;
        if (prd.goals_success_criteria && prd.goals_success_criteria.length) {
          md += `| Objective | Measurable Target |\n| :--- | :--- |\n`;
          prd.goals_success_criteria.forEach(g => {
            md += `| ${g.objective || ''} | ${g.measurable_target || ''} |\n`;
          });
        }
        md += `\n`;
        
        md += `## 3. Functional Requirements\n`;
        (prd.functional_requirements || []).forEach(fr => { md += `- ${fr}\n`; });
        md += `\n`;
        
        md += `## 4. Non-Functional Requirements\n`;
        (prd.non_functional_requirements || []).forEach(nfr => { md += `- ${nfr}\n`; });
        return md;
      }
      
      case 'user_stories': {
        const stories = plan.user_stories;
        if (!stories || !stories.length) return '*No user stories list.*';
        
        let md = `# User Stories\n\n`;
        md += `| Story ID | User Role | Action / Requirement | Value / Outcome |\n`;
        md += `| :--- | :--- | :--- | :--- |\n`;
        stories.forEach(s => {
          md += `| **${s.story_id || ''}** | As a ${s.user_role || ''} | I want to ${s.action || ''} | So that ${s.benefit || ''} |\n`;
        });
        return md;
      }
      
      case 'acceptance_criteria': {
        const acList = plan.acceptance_criteria;
        if (!acList || !acList.length) return '*No acceptance criteria.*';
        
        let md = `# Acceptance Criteria\n\n`;
        acList.forEach(ac => {
          md += `## Story: ${ac.story_id || ''}\n`;
          (ac.scenarios || []).forEach(s => {
            md += `- ${s}\n`;
          });
          md += `\n`;
        });
        return md;
      }
      
      case 'roadmap': {
        const rm = plan.roadmap;
        if (!rm) return '*No roadmap data.*';
        
        let md = `# Product Roadmap\n\n`;
        if (rm.mermaid_gantt) {
          md += `\`\`\`mermaid\n${rm.mermaid_gantt}\n\`\`\`\n\n`;
        }
        
        (rm.phases || []).forEach(p => {
          md += `## Phase: ${p.phase_name || ''} (${p.timeline || ''})\n`;
          md += `**Focus**: ${p.focus || ''}\n\n`;
          md += `### Milestones & Deliverables\n`;
          (p.milestones || []).forEach(m => { md += `- ${m}\n`; });
          md += `\n`;
        });
        return md;
      }
      
      case 'risks': {
        const risks = plan.risks;
        if (!risks || !risks.length) return '*No risks list.*';
        
        let md = `# Product Risks & Mitigation Matrix\n\n`;
        md += `| Risk Description | Category | Impact | Probability | Mitigation Strategy |\n`;
        md += `| :--- | :--- | :--- | :--- | :--- |\n`;
        risks.forEach(r => {
          md += `| **${r.description || ''}** | ${r.category || ''} | ${r.impact || ''} | ${r.probability || ''} | ${r.mitigation || ''} |\n`;
        });
        return md;
      }
      
      case 'kpis': {
        const kpis = plan.kpis;
        if (!kpis) return '*No KPIs data.*';
        
        let md = `# Key Performance Indicators (KPIs)\n\n`;
        
        const renderKpiTable = (title, list) => {
          if (!list || !list.length) return '';
          let sectionMd = `## ${title}\n\n`;
          sectionMd += `| Metric | Target | Notes |\n| :--- | :--- | :--- |\n`;
          list.forEach(item => {
            sectionMd += `| **${item.metric || ''}** | ${item.target || ''} | ${item.notes || ''} |\n`;
          });
          sectionMd += `\n`;
          return sectionMd;
        };
        
        md += renderKpiTable('Acquisition', kpis.acquisition);
        md += renderKpiTable('Activation', kpis.activation);
        md += renderKpiTable('Retention', kpis.retention);
        md += renderKpiTable('Revenue', kpis.revenue);
        return md;
      }
      
      default:
        return '*Invalid section.*';
    }
  }

  function switchTab(tabId) {
    if (!generatedPlan || isGenerating) return;
    
    activeTab = tabId;
    
    // Update active visual classes
    tabLinks.forEach(lnk => {
      if (lnk.getAttribute('data-tab') === tabId) {
        lnk.classList.add('active');
      } else {
        lnk.classList.remove('active');
      }
    });

    // Render Tab Markdown
    const markdownContent = convertSectionToMarkdown(generatedPlan, tabId);
    
    // Render using marked library
    renderedContent.innerHTML = marked.parse(markdownContent);
    renderedContent.focus();
  }

  // 5. Loading Animation Engine
  function startChecklistAnimation() {
    const steps = [
      { id: 'step-0', text: 'Analyzing product concept...', delay: 800 },
      { id: 'step-1', text: 'Forging market insights...', delay: 1000 },
      { id: 'step-2', text: 'Inspecting competitor landscape...', delay: 1000 },
      { id: 'step-3', text: 'Outlining user personas...', delay: 1000 },
      { id: 'step-4', text: 'Drafting functional PRD...', delay: 1000 },
      { id: 'step-5', text: 'Detailing user stories...', delay: 1000 },
      { id: 'step-6', text: 'Defining acceptance criteria...', delay: 1000 },
      { id: 'step-7', text: 'Sequencing milestones roadmap...', delay: 1000 },
      { id: 'step-8', text: 'Assessing project risks...', delay: 1000 },
      { id: 'step-9', text: 'Formulating success KPIs...', delay: 1000 }
    ];

    // Reset all list elements to pending
    steps.forEach(s => {
      const el = document.getElementById(s.id);
      el.className = 'pending';
    });

    let currentStepIndex = 0;
    let timeoutId = null;

    function runNextStep() {
      if (currentStepIndex >= steps.length) return;
      
      const step = steps[currentStepIndex];
      const el = document.getElementById(step.id);
      
      // Make active
      el.className = 'active';
      loadingSubtext.textContent = step.text;

      // Mark previous completed
      if (currentStepIndex > 0) {
        const prevStep = steps[currentStepIndex - 1];
        document.getElementById(prevStep.id).className = 'completed';
      }

      timeoutId = setTimeout(() => {
        currentStepIndex++;
        runNextStep();
      }, step.delay);
    }

    // Begin loop
    runNextStep();

    // Controllers returned for backend coordination
    return {
      completeAllSteps: async () => {
        clearTimeout(timeoutId);
        
        // Fast-forward all remaining steps to completed
        for (let i = 0; i < steps.length; i++) {
          const el = document.getElementById(steps[i].id);
          el.className = 'completed';
          await new Promise(resolve => setTimeout(resolve, 150));
        }
        loadingSubtext.textContent = 'Blueprints forged successfully!';
        await new Promise(resolve => setTimeout(resolve, 400));
      },
      failSteps: () => {
        clearTimeout(timeoutId);
        // Turn active or pending steps to pending but stop process
        steps.forEach(s => {
          const el = document.getElementById(s.id);
          if (el.className === 'active' || el.className === 'pending') {
            el.className = 'pending';
          }
        });
      }
    };
  }

  // 6. Copying Tab Source Code
  btnCopyTab.addEventListener('click', () => {
    if (!generatedPlan || !activeTab) return;
    
    const content = convertSectionToMarkdown(generatedPlan, activeTab);
    navigator.clipboard.writeText(content).then(() => {
      const originalText = btnCopyTab.innerHTML;
      btnCopyTab.innerHTML = `✓ Copied!`;
      btnCopyTab.style.borderColor = 'var(--accent-emerald)';
      btnCopyTab.style.color = 'var(--accent-emerald)';
      
      setTimeout(() => {
        btnCopyTab.innerHTML = originalText;
        btnCopyTab.style.borderColor = '';
        btnCopyTab.style.color = '';
      }, 2000);
    }).catch(err => {
      console.error('Failed to copy text: ', err);
    });
  });

  // 7. Export Entire Document
  btnExportAll.addEventListener('click', () => {
    if (!generatedPlan) return;

    // Combine all sections into a single markdown file
    const doc = `% ProductForge AI Output Blueprint
% Target Concept: ${ideaTextarea.value.trim().substring(0, 100)}...

${convertSectionToMarkdown(generatedPlan, 'market_research')}

---

${convertSectionToMarkdown(generatedPlan, 'competitors')}

---

${convertSectionToMarkdown(generatedPlan, 'personas')}

---

${convertSectionToMarkdown(generatedPlan, 'prd')}

---

${convertSectionToMarkdown(generatedPlan, 'user_stories')}

---

${convertSectionToMarkdown(generatedPlan, 'acceptance_criteria')}

---

${convertSectionToMarkdown(generatedPlan, 'roadmap')}

---

${convertSectionToMarkdown(generatedPlan, 'risks')}

---

${convertSectionToMarkdown(generatedPlan, 'kpis')}
`;

    // Download blob file
    const blob = new Blob([doc], { type: 'text/markdown;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    
    // Create sensible file name
    const rawIdea = ideaTextarea.value.trim().toLowerCase();
    const cleanName = rawIdea.replace(/[^a-z0-9]+/g, '-').substring(0, 30) || 'product-plan';
    
    link.href = url;
    link.setAttribute('download', `productforge-${cleanName}.md`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  });

  // Check if API key is set in backend
  async function checkApiStatus() {
    try {
      // Just check if we can reach the server, but for our status indicator,
      // let's do a simple inspection or leave it as Local Engine Active.
      // We can also check if the server environment has a GEMINI_API_KEY.
      // But keeping it as standard active is clean.
    } catch (e) {}
  }
  checkApiStatus();
});
