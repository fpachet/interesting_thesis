(() => {
  const navToggle = document.querySelector('.nav-toggle');
  const siteNav = document.querySelector('.site-nav');
  if (navToggle && siteNav) {
    navToggle.addEventListener('click', () => {
      const open = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!open));
      siteNav.classList.toggle('is-open', !open);
    });
  }

  const catalogForm = document.querySelector('[data-catalog-form]');
  if (catalogForm) {
    const cards = [...document.querySelectorAll('[data-card]')];
    const count = document.querySelector('[data-result-count]');
    const empty = document.querySelector('[data-empty-state]');
    const reset = document.querySelector('[data-reset-filters]');
    const fields = {
      search: catalogForm.elements.recherche,
      family: catalogForm.elements.famille,
      level: catalogForm.elements.niveau,
      kind: catalogForm.elements.forme,
    };

    const normalize = (value) => value
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .trim();

    const filter = () => {
      const query = normalize(fields.search.value);
      let visible = 0;
      cards.forEach((card) => {
        const haystack = normalize(`${card.dataset.title} ${card.dataset.text}`);
        const matches = (!query || haystack.includes(query))
          && (!fields.family.value || card.dataset.family === fields.family.value)
          && (!fields.level.value || card.dataset.level === fields.level.value)
          && (!fields.kind.value || card.dataset.kind === fields.kind.value);
        card.hidden = !matches;
        if (matches) visible += 1;
      });
      count.textContent = String(visible);
      empty.hidden = visible !== 0;
      const params = new URLSearchParams();
      if (fields.search.value) params.set('q', fields.search.value);
      if (fields.family.value) params.set('famille', fields.family.value);
      if (fields.level.value) params.set('niveau', fields.level.value);
      if (fields.kind.value) params.set('forme', fields.kind.value);
      const url = `${window.location.pathname}${params.size ? `?${params}` : ''}`;
      window.history.replaceState(null, '', url);
    };

    const params = new URLSearchParams(window.location.search);
    fields.search.value = params.get('q') || '';
    fields.family.value = params.get('famille') || '';
    fields.level.value = params.get('niveau') || '';
    fields.kind.value = params.get('forme') || '';
    catalogForm.addEventListener('input', filter);
    catalogForm.addEventListener('change', filter);
    catalogForm.addEventListener('submit', (event) => event.preventDefault());
    reset.addEventListener('click', () => {
      catalogForm.reset();
      filter();
      fields.search.focus();
    });
    filter();
  }

  const graph = document.querySelector('[data-idea-graph]');
  const graphDataElement = document.querySelector('#graph-data');
  if (graph && graphDataElement) {
    const data = JSON.parse(graphDataElement.textContent);
    const nodes = [...graph.querySelectorAll('.graph-node')];
    const edges = [...graph.querySelectorAll('.graph-edge')];
    const detail = document.querySelector('[data-graph-detail]');
    const search = document.querySelector('[data-graph-search]');
    const family = document.querySelector('[data-graph-family]');
    const relation = document.querySelector('[data-graph-relation]');
    const reset = document.querySelector('[data-graph-reset]');
    let selected = '';

    const escapeHtml = (value) => String(value)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;');

    const relationsFor = (cardId) => data.relations.filter(
      (item) => item.source === cardId || item.target === cardId,
    );

    const renderDetail = (cardId) => {
      const card = data.cards[cardId];
      const linked = relationsFor(cardId);
      const list = linked.map((item) => {
        const outgoing = item.source === cardId;
        const otherId = outgoing ? item.target : item.source;
        const other = data.cards[otherId];
        const relationLabel = outgoing
          ? data.labels[item.kind]
          : `est ${data.labels[item.kind]} par`;
        return `<li><span>${escapeHtml(relationLabel)}</span><button type="button" data-select-card="${otherId}">${escapeHtml(other.title)}</button></li>`;
      }).join('');
      detail.innerHTML = `
        <p class="eyebrow">${escapeHtml(cardId)}</p>
        <h2>${escapeHtml(card.title)}</h2>
        <div class="graph-detail__meta"><span class="badge">${escapeHtml(card.family)}</span><span class="badge">${escapeHtml(card.level)}</span></div>
        <p>${linked.length} relation${linked.length > 1 ? 's' : ''} forte${linked.length > 1 ? 's' : ''} directement connectée${linked.length > 1 ? 's' : ''}.</p>
        <ul class="graph-detail__relations">${list || '<li>Aucune relation forte enregistrée.</li>'}</ul>
        <a class="button" href="${card.href}">Lire la carte complète</a>
      `;
      detail.querySelectorAll('[data-select-card]').forEach((button) => {
        button.addEventListener('click', () => selectCard(button.dataset.selectCard));
      });
    };

    const applyFilters = () => {
      const currentRelations = new Set();
      edges.forEach((edge) => {
        const familyMatch = !family.value
          || data.cards[edge.dataset.source].family === family.value
          || data.cards[edge.dataset.target].family === family.value;
        const relationMatch = !relation.value || edge.dataset.relation === relation.value;
        const selectionMatch = !selected
          || edge.dataset.source === selected
          || edge.dataset.target === selected;
        const focused = familyMatch && relationMatch && selectionMatch;
        edge.classList.toggle('is-focus', focused && Boolean(selected || family.value || relation.value));
        edge.classList.toggle('is-muted', !focused && Boolean(selected || family.value || relation.value));
        if (focused) {
          currentRelations.add(edge.dataset.source);
          currentRelations.add(edge.dataset.target);
        }
      });

      nodes.forEach((node) => {
        const familyMatch = !family.value || node.dataset.family === family.value;
        const selectedNode = node.dataset.id === selected;
        const neighbor = currentRelations.has(node.dataset.id);
        const visible = familyMatch || neighbor || (!family.value && !selected && !relation.value);
        node.classList.toggle('is-focus', selectedNode);
        node.classList.toggle('is-neighbor', neighbor && !selectedNode);
        node.classList.toggle('is-muted', !visible || (selected && !neighbor));
      });
    };

    function selectCard(cardId) {
      if (!data.cards[cardId]) return;
      selected = cardId;
      search.value = cardId;
      renderDetail(cardId);
      applyFilters();
    }

    nodes.forEach((node) => {
      node.addEventListener('click', () => selectCard(node.dataset.id));
      node.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          selectCard(node.dataset.id);
        }
      });
    });

    const resolveGraphSearch = () => {
      const value = search.value.trim();
      if (data.cards[value]) {
        selectCard(value);
        return;
      }
      const found = Object.entries(data.cards).find(([, card]) => (
        card.title.toLowerCase().includes(value.toLowerCase())
      ));
      if (found) selectCard(found[0]);
    };
    search.addEventListener('input', () => {
      if (data.cards[search.value.trim()]) resolveGraphSearch();
    });
    search.addEventListener('change', resolveGraphSearch);
    family.addEventListener('change', applyFilters);
    relation.addEventListener('change', applyFilters);
    reset.addEventListener('click', () => {
      selected = '';
      search.value = '';
      family.value = '';
      relation.value = '';
      nodes.forEach((node) => node.classList.remove('is-focus', 'is-neighbor', 'is-muted'));
      edges.forEach((edge) => edge.classList.remove('is-focus', 'is-muted'));
      window.location.reload();
    });
  }
})();
