// -------------------------------------------------------------
// AETHEL AI FRONTEND CONTROLLER
// -------------------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {
  // Application State
  let generatedPlan = null;
  let activeTab = 'market_research';
  let isGenerating = false;

  // Elements Selection
  const form = document.getElementById('generator-form');
  const ideaTextarea = document.getElementById('product-idea');
  const apiKeyInput = document.getElementById('gemini-api-key');
  const submitBtn = document.getElementById('submit-btn');
  const clearBtn = document.getElementById('clear-input');
  const charCounter = document.getElementById('char-counter');

  // Load saved API key on startup
  if (apiKeyInput) {
    const savedKey = localStorage.getItem('gemini_api_key');
    if (savedKey) {
      apiKeyInput.value = savedKey;
    }
  }
  
  const tabsNav = document.getElementById('tabs-navigation');
  const tabLinks = document.querySelectorAll('.tab-link');
  
  const stateEmpty = document.getElementById('state-empty');
  const stateLoading = document.getElementById('state-loading');
  const stateResult = document.getElementById('state-result');
  const loadingSubtext = document.getElementById('loading-subtext');
  const renderedContent = document.getElementById('rendered-content');
  const sourcesContainer = document.getElementById('sources-container');
  const sourcesList = document.getElementById('sources-list');
  const timelineDrawer = document.getElementById('timeline-drawer');
  const timelineTrack = document.getElementById('timeline-track');
  const pipelineStatusBanner = document.getElementById('pipeline-status-banner');
  const pipelineDuration = document.getElementById('pipeline-duration');
  const btnOpenDrawer = document.getElementById('btn-open-drawer');
  const btnCloseDrawer = document.getElementById('btn-close-drawer');
  const drawerOverlay = document.getElementById('drawer-overlay');
  
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

    // Cache API Key locally
    const apiKey = apiKeyInput ? apiKeyInput.value.trim() : '';
    if (apiKeyInput) {
      if (apiKey) {
        localStorage.setItem('gemini_api_key', apiKey);
      } else {
        localStorage.removeItem('gemini_api_key');
      }
    }

    // Transition States
    isGenerating = true;
    submitBtn.disabled = true;
    submitBtn.querySelector('.btn-text').textContent = 'Forging Plan...';
    
    stateEmpty.classList.add('hidden');
    stateResult.classList.add('hidden');
    pipelineStatusBanner.classList.add('hidden');
    timelineDrawer.classList.remove('open');
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
        body: JSON.stringify({ idea, apiKey })
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
      
      // Render the execution timeline
      renderAgentTimeline(generatedPlan);
      
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
        md += `\n`;
        
        // Append User Stories
        const stories = plan.user_stories;
        if (stories && stories.length) {
          md += `## 5. User Stories\n\n`;
          md += `| Story ID | User Role | Action / Requirement | Value / Outcome |\n`;
          md += `| :--- | :--- | :--- | :--- |\n`;
          stories.forEach(s => {
            md += `| **${s.story_id || ''}** | As a ${s.user_role || ''} | I want to ${s.action || ''} | So that ${s.benefit || ''} |\n`;
          });
          md += `\n`;
        }
        
        // Append Acceptance Criteria
        const acList = plan.acceptance_criteria;
        if (acList && acList.length) {
          md += `## 6. Acceptance Criteria\n\n`;
          acList.forEach(ac => {
            md += `### Story: ${ac.story_id || ''}\n`;
            (ac.scenarios || []).forEach(s => {
              md += `- ${s}\n`;
            });
            md += `\n`;
          });
        }
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
        
        let md = `# Product Roadmap & Risks\n\n`;
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
        
        // Append Risks mitigation matrix
        const risks = plan.risks;
        if (risks && risks.length) {
          md += `\n---\n\n## Project Risks & Mitigation Matrix\n\n`;
          md += `| Risk Description | Category | Impact | Probability | Mitigation Strategy |\n`;
          md += `| :--- | :--- | :--- | :--- | :--- |\n`;
          risks.forEach(r => {
            md += `| **${r.description || ''}** | ${r.category || ''} | ${r.impact || ''} | ${r.probability || ''} | ${r.mitigation || ''} |\n`;
          });
        }
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
      
      case 'evaluation': {
        const evalData = plan.evaluation;
        if (!evalData) return '*No evaluation data available.*';
        
        let md = `# Audit Evaluation Report\n\n`;
        md += `This section reviews the alignment, feasibility, and completeness of the compiled product strategy blueprint and offers high-value recommendations.\n\n`;
        
        const renderCriteria = (title, crit) => {
          if (!crit) return '';
          let critMd = `## ${title} (Score: **${crit.score || 0}/10**)\n\n`;
          critMd += `### Strengths\n`;
          (crit.strengths || []).forEach(s => { critMd += `- ${s}\n`; });
          critMd += `\n### Areas for Improvement\n`;
          (crit.improvement_areas || []).forEach(i => { critMd += `- ${i}\n`; });
          critMd += `\n`;
          return critMd;
        };
        
        md += renderCriteria('Product Alignment', evalData.alignment);
        md += renderCriteria('Technical & Operational Feasibility', evalData.feasibility);
        md += renderCriteria('Blueprint Completeness', evalData.completeness);
        
        md += `## Overall Strategic Recommendations\n`;
        if (evalData.overall_recommendations && evalData.overall_recommendations.length) {
          evalData.overall_recommendations.forEach((r, idx) => {
            md += `* **Recommendation ${idx + 1}**: ${r}\n`;
          });
        } else {
          md += `*No recommendations available.*\n`;
        }
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

    // Render Grounding Sources
    renderGroundingSources(generatedPlan, tabId);
  }

  function getFriendlyUrlName(urlStr) {
    try {
      const url = new URL(urlStr);
      let host = url.hostname.replace('www.', '');
      let pathname = url.pathname;
      if (pathname && pathname !== '/') {
        const segments = pathname.split('/').filter(Boolean);
        if (segments.length > 0) {
          let lastSeg = segments[segments.length - 1];
          lastSeg = lastSeg.replace(/-/g, ' ').replace(/_/g, ' ');
          if (lastSeg.length > 0) {
            lastSeg = lastSeg.charAt(0).toUpperCase() + lastSeg.slice(1);
            return `${host} › ${lastSeg}`;
          }
        }
      }
      return host;
    } catch (e) {
      return urlStr;
    }
  }

  function renderGroundingSources(plan, tabId) {
    if (!sourcesContainer || !sourcesList) return;

    const showSources = (tabId === 'market_research' || tabId === 'competitors');
    const hasSources = (plan.source_attributions && plan.source_attributions.length > 0);

    if (showSources && hasSources) {
      sourcesList.innerHTML = '';
      plan.source_attributions.forEach(url => {
        const badge = document.createElement('a');
        badge.className = 'source-badge';
        badge.href = url;
        badge.target = '_blank';
        badge.rel = 'noopener noreferrer';
        
        // Link SVG icon
        badge.innerHTML = `
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
            <polyline points="15 3 21 3 21 9"></polyline>
            <line x1="10" y1="14" x2="21" y2="3"></line>
          </svg>
          <span>${getFriendlyUrlName(url)}</span>
        `;
        sourcesList.appendChild(badge);
      });
      sourcesContainer.classList.remove('hidden');
    } else {
      sourcesContainer.classList.add('hidden');
    }
  }

  function renderAgentTimeline(plan) {
    if (!timelineDrawer || !timelineTrack) return;

    const trace = plan.execution_trace;
    if (!trace || !trace.length) {
      if (pipelineStatusBanner) pipelineStatusBanner.classList.add('hidden');
      return;
    }

    timelineTrack.innerHTML = '';

    // Regex to parse: "Research Agent execution: status=completed, duration=123ms"
    const regex = /^([^:]+)\s+execution:\s+status=([^,]+),\s+duration=(\d+)ms/;

    const nodes = [];
    trace.forEach(traceStr => {
      const match = traceStr.match(regex);
      if (match) {
        const agentName = match[1].trim();
        const status = match[2].trim().toLowerCase();
        const duration = match[3].trim();
        nodes.push({ agentName, status, duration });
      }
    });

    // Populate duration and show status banner
    const totalMs = nodes.reduce((sum, n) => sum + (parseInt(n.duration) || 0), 0);
    const totalSec = (totalMs / 1000).toFixed(1);
    if (pipelineDuration) {
      pipelineDuration.textContent = totalSec;
    }
    if (pipelineStatusBanner) {
      pipelineStatusBanner.classList.remove('hidden');
    }

    if (nodes.length < 7) {
      // Degrade gracefully to sequential flow if nodes structure is unexpected
      nodes.forEach(n => {
        timelineTrack.appendChild(createTimelineNode(n.agentName, n.status, n.duration));
      });
      return;
    }

    // Build branching structure
    // 1. Linear section (Research, Persona, PRD)
    const linearSection = document.createElement('div');
    linearSection.className = 'timeline-linear-section';
    linearSection.appendChild(createTimelineNode(nodes[0].agentName, nodes[0].status, nodes[0].duration));
    linearSection.appendChild(createTimelineNode(nodes[1].agentName, nodes[1].status, nodes[1].duration));
    linearSection.appendChild(createTimelineNode(nodes[2].agentName, nodes[2].status, nodes[2].duration));

    // 2. Fork Container
    const forkContainer = document.createElement('div');
    forkContainer.className = 'timeline-fork-container';

    // Top Branch (Roadmap, Risk)
    const branchTop = document.createElement('div');
    branchTop.className = 'timeline-branch branch-top';
    branchTop.appendChild(createTimelineNode(nodes[3].agentName, nodes[3].status, nodes[3].duration));
    branchTop.appendChild(createTimelineNode(nodes[4].agentName, nodes[4].status, nodes[4].duration));

    // Bottom Branch (Metrics)
    const branchBottom = document.createElement('div');
    branchBottom.className = 'timeline-branch branch-bottom';
    branchBottom.appendChild(createTimelineNode(nodes[5].agentName, nodes[5].status, nodes[5].duration));
    
    // Add spacer node to align with the top branch's second node
    const spacerNode = document.createElement('div');
    spacerNode.className = 'timeline-node timeline-spacer-node';
    branchBottom.appendChild(spacerNode);

    forkContainer.appendChild(branchTop);
    forkContainer.appendChild(branchBottom);

    // 3. Evaluation Section (Linear again after merge)
    const evaluationSection = document.createElement('div');
    evaluationSection.className = 'timeline-linear-section evaluation-node-wrapper';
    evaluationSection.appendChild(createTimelineNode(nodes[6].agentName, nodes[6].status, nodes[6].duration));

    // Assemble components
    timelineTrack.appendChild(linearSection);
    timelineTrack.appendChild(forkContainer);
    timelineTrack.appendChild(evaluationSection);
  }

  function createTimelineNode(name, status, duration) {
    const node = document.createElement('div');
    node.className = 'timeline-node';

    const dot = document.createElement('div');
    dot.className = `timeline-node-dot ${status}`;
    
    const textWrapper = document.createElement('div');
    textWrapper.className = 'timeline-node-text';

    const nameEl = document.createElement('div');
    nameEl.className = 'timeline-node-name';
    nameEl.textContent = name;

    const durationEl = document.createElement('div');
    durationEl.className = 'timeline-node-duration';
    durationEl.textContent = `${parseInt(duration).toLocaleString()} ms`;

    textWrapper.appendChild(nameEl);
    textWrapper.appendChild(durationEl);

    node.appendChild(dot);
    node.appendChild(textWrapper);

    return node;
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
      { id: 'step-9', text: 'Formulating success KPIs...', delay: 1000 },
      { id: 'step-10', text: 'Auditing launch strategy...', delay: 1000 }
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
    let doc = `% Aethel AI Output Blueprint
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

---

${convertSectionToMarkdown(generatedPlan, 'evaluation')}
`;

    if (generatedPlan.source_attributions && generatedPlan.source_attributions.length) {
      doc += `\n\n---\n\n# Grounding Sources & Attributions\n\n`;
      generatedPlan.source_attributions.forEach(url => {
        doc += `- [${url}](${url})\n`;
      });
    }

    // Download blob file
    const blob = new Blob([doc], { type: 'text/markdown;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    
    // Create sensible file name
    const rawIdea = ideaTextarea.value.trim().toLowerCase();
    const cleanName = rawIdea.replace(/[^a-z0-9]+/g, '-').substring(0, 30) || 'product-plan';
    
    link.href = url;
    link.setAttribute('download', `aethel-${cleanName}.md`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  });

  // 8. Drawer Toggle Control
  if (btnOpenDrawer) {
    btnOpenDrawer.addEventListener('click', () => {
      if (timelineDrawer) timelineDrawer.classList.add('open');
    });
  }
  if (btnCloseDrawer) {
    btnCloseDrawer.addEventListener('click', () => {
      if (timelineDrawer) timelineDrawer.classList.remove('open');
    });
  }
  if (drawerOverlay) {
    drawerOverlay.addEventListener('click', () => {
      if (timelineDrawer) timelineDrawer.classList.remove('open');
    });
  }

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
