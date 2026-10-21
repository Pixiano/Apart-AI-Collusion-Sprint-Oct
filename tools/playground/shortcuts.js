// Keyboard shortcuts for the Collusion Playground (llama.cpp web UI copy).
// DOM-driven on purpose: it clicks the UI's own buttons by aria-label instead of patching the minified bundle,
// so it survives bundle changes as long as the labels stay. Press ? for the list.
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const last = (a) => a[a.length - 1];
  // the nav rail labels buttons by aria-label when collapsed and by visible text when expanded
  const btn = (label) => $(`button[aria-label="${label}"]`) || $$('button').find((b) => (b.innerText || '').trim() === label);
  const navToggle = () => $$('button').find((b) => /navigation|sidebar/i.test(b.getAttribute('aria-label') || ''));
  const click = (el) => !!el && (el.click(), true);
  const composer = () => $('textarea[placeholder^="Type a message"]') || last($$('textarea'));
  const cancelEditBtn = () => $$('button').find((b) => (b.innerText || '').trim() === 'Cancel');
  const typing = (t) => !!t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName));
  const dialogOpen = () => !!$('[role="dialog"][data-state="open"]');

  // message action buttons come in groups (copy/edit/[regenerate]/fork/delete); assistant groups have Regenerate
  const group = (b) => { let g = b.parentElement; while (g && !(g.querySelector('[aria-label="Copy"]') && g.querySelector('[aria-label="Delete"]'))) g = g.parentElement; return g; };
  const isAssistant = (b) => !!group(b)?.querySelector('[aria-label="Regenerate"]');
  const lastAction = (label, assistant) => last($$(`button[aria-label="${label}"]`).filter((b) => isAssistant(b) === assistant));
  const stopBtn = () => $$('button').find((b) => /stop/i.test(b.getAttribute('aria-label') || b.innerText || ''));

  // chat tabs strip: anchors layered over each tab
  const tabs = () => $$('a[href^="#/"][aria-label]').filter((a) => a.classList.contains('inset-0'));
  const activeTab = () => tabs().findIndex((a) => a.getAttribute('href') === location.hash);
  const goTab = (i) => { const t = tabs(); if (t.length) location.hash = t[(i + t.length) % t.length].getAttribute('href'); return t.length > 0; };

  const modelPicker = () => last($$('button[data-dropdown-menu-trigger]').filter((b) => !/Add files/.test(b.innerText) && b.getAttribute('aria-label') !== 'Reasoning effort'));

  // scope, keys, label, action, {inInput: also fire while typing, when: extra condition}
  const S = [];
  const def = (scope, keys, label, run, o = {}) => S.push({ scope, keys, label, run, ...o });

  // --- chat ---
  def('Chat', ['/'], 'Focus the message box', () => { composer()?.focus(); return true; });
  def('Chat', ['Escape'], 'Stop generating, else cancel an edit, else leave the message box', () => {
    if (click(stopBtn())) return true;
    if (click(cancelEditBtn())) return true;
    if (document.activeElement === composer()) { composer().blur(); return true; }
    return false;
  }, { inInput: true });
  def('Chat', ['ArrowUp'], 'Edit your last message (message box empty)', () => click(lastAction('Edit', false)), { inInput: true, when: () => document.activeElement === composer() && !composer().value });
  def('Chat', ['y'], 'Copy the last reply', () => click(lastAction('Copy', true)));
  def('Chat', ['r'], 'Regenerate the last reply', () => click(lastAction('Regenerate', true)));
  def('Chat', ['e'], 'Edit your last message', () => click(lastAction('Edit', false)));

  // --- sidebar and tabs ---
  def('Sidebar and tabs', ['n', 'mod+shift+o'], 'New chat', () => click(btn('New chat')), { inInput: (e) => e.ctrlKey || e.metaKey });
  def('Sidebar and tabs', ['s', 'mod+k'], 'Search chats', () => click(btn('Search')), { inInput: (e) => e.ctrlKey || e.metaKey });
  def('Sidebar and tabs', ['b'], 'Expand or collapse the navigation rail', () => click(navToggle()));
  def('Sidebar and tabs', ['[', ']'], 'Previous / next chat tab', (e) => goTab(activeTab() + (e.key === ']' ? 1 : -1)));
  def('Sidebar and tabs', ['1-9'], 'Jump to chat tab 1 to 9', (e) => { const t = tabs(); const i = +e.key - 1; if (!t[i]) return false; location.hash = t[i].getAttribute('href'); return true; }, { match: (e) => /^[1-9]$/.test(e.key) });

  // --- everywhere ---
  def('Everywhere', ['m'], 'Models page (load / unload)', () => click(btn('Models')));
  def('Everywhere', [','], 'Settings', () => click(btn('Settings')));
  def('Everywhere', ['p'], 'Pick model for this chat', () => click(modelPicker()));
  def('Everywhere', ['h'], 'Reasoning effort', () => click(btn('Reasoning effort')));
  def('Everywhere', ['?', 'mod+/'], 'Show or hide this list', () => toggleHelp(), { inInput: (e) => e.ctrlKey || e.metaKey, always: true });

  // --- help overlay ---
  let help;
  const kbd = (k) => `<kbd>${k.replace('mod', 'Ctrl').replace('Escape', 'Esc').replace('ArrowUp', '↑').replace('shift+', 'Shift+').replace(/^(.)$/, (c) => c.toUpperCase())}</kbd>`;
  function toggleHelp() {
    if (help) { help.remove(); help = null; return true; }
    const scopes = [...new Set(S.map((s) => s.scope))];
    help = document.createElement('div');
    help.setAttribute('role', 'note');
    help.style.cssText = 'position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.55)';
    help.innerHTML = `<style>.cp-card{background:var(--background,#161616);color:var(--foreground,#eee);border:1px solid var(--border,#333);border-radius:12px;padding:20px 24px;max-width:560px;width:92%;max-height:86vh;overflow:auto;font:14px system-ui}
.cp-card h2{margin:0 0 12px;font-size:16px}.cp-card h3{margin:14px 0 6px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;opacity:.6}
.cp-row{display:flex;justify-content:space-between;gap:16px;padding:3px 0}.cp-card kbd{border:1px solid var(--border,#444);border-radius:5px;padding:0 6px;margin-left:4px;font:12px ui-monospace,monospace}</style>
<div class="cp-card"><h2>Keyboard shortcuts</h2>${scopes.map((sc) => `<h3>${sc}</h3>` + S.filter((s) => s.scope === sc).map((s) => `<div class="cp-row"><span>${s.label}</span><span>${s.keys.map(kbd).join(' or ')}</span></div>`).join('')).join('')}
<h3>Note</h3><div class="cp-row"><span>Single keys only work when you are not typing. Enter sends, Shift+Enter adds a line.</span></div></div>`;
    help.addEventListener('click', (e) => { if (e.target === help) toggleHelp(); });
    document.body.appendChild(help);
    return true;
  }

  // --- dispatch ---
  const norm = (e) => {
    const p = [];
    if (e.ctrlKey || e.metaKey) p.push('mod');
    if (e.altKey) p.push('alt');
    if (e.shiftKey && (e.key.length > 1 || /[a-z]/i.test(e.key))) p.push('shift');
    p.push(e.key.length === 1 ? e.key.toLowerCase() : e.key);
    return p.join('+');
  };
  addEventListener('keydown', (e) => {
    if (e.isComposing || e.defaultPrevented) return;
    if (help && e.key === 'Escape') { toggleHelp(); e.preventDefault(); return; }
    const k = norm(e);
    const inField = typing(e.target);
    const mod = e.ctrlKey || e.metaKey || e.altKey;
    for (const s of S) {
      if (!(s.match ? s.match(e) && !mod : s.keys.includes(k))) continue;
      const okInField = typeof s.inInput === 'function' ? s.inInput(e) : s.inInput;
      if (inField && !okInField) continue;
      if (!s.always && dialogOpen() && !(inField && okInField && s.keys.includes('Escape'))) continue;
      if (s.when && !s.when(e)) continue;
      if (s.run(e) !== false) { e.preventDefault(); e.stopPropagation(); }
      return;
    }
  }, true);

  window.__collusionShortcuts = S; // for testing in the console
  console.log('[collusion-playground] shortcuts loaded, press ? for the list');
})();
