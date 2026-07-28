// Signal page chart renderer. Reads window.PLOTLY_DATA (server-rendered JSON),
// draws each dashboard into its container, and swaps the active panel on tab click.

(function () {
  const data = window.PLOTLY_DATA;
  if (!data || typeof Plotly === 'undefined') return;

  const config = { displayModeBar: false, responsive: true };

  function render(key) {
    const block = data[key];
    if (!block) return;
    const primary = document.getElementById(`chart-${key}-primary`);
    const secondary = document.getElementById(`chart-${key}-secondary`);
    if (primary && !primary.dataset.rendered) {
      Plotly.newPlot(primary, block.primary.data, block.primary.layout, config);
      primary.dataset.rendered = '1';
    }
    if (secondary && !secondary.dataset.rendered) {
      Plotly.newPlot(secondary, block.secondary.data, block.secondary.layout, config);
      secondary.dataset.rendered = '1';
    }
  }

  function setActive(key) {
    document.querySelectorAll('[data-signal-panel]').forEach((el) => {
      const visible = el.dataset.signalPanel === key;
      el.classList.toggle('hidden', !visible);
    });
    document.querySelectorAll('[data-signal-tab]').forEach((el) => {
      const active = el.dataset.signalTab === key;
      el.classList.toggle('signal-tab-active', active);
    });
    render(key);
    // Re-layout to make sure newly visible plots size correctly
    const block = data[key];
    if (block) {
      const p = document.getElementById(`chart-${key}-primary`);
      const s = document.getElementById(`chart-${key}-secondary`);
      if (p) Plotly.Plots.resize(p);
      if (s) Plotly.Plots.resize(s);
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-signal-tab]').forEach((el) => {
      el.addEventListener('click', () => setActive(el.dataset.signalTab));
    });
    const initial = document.querySelector('[data-signal-tab]');
    if (initial) setActive(initial.dataset.signalTab);
  });
})();

// Small teaser treemap used on the home page
(function () {
  const el = document.getElementById('signal-teaser');
  if (!el || typeof Plotly === 'undefined' || !window.PLOTLY_TEASER) return;
  Plotly.newPlot(el, window.PLOTLY_TEASER.data, window.PLOTLY_TEASER.layout, { displayModeBar: false, responsive: true });
})();
