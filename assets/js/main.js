(() => {
  const d = document, w = window;
  const reduce = w.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Header + progress */
  const hdr = d.querySelector('.hdr'), bar = d.querySelector('.progress');
  const onScroll = () => {
    const y = w.scrollY, h = d.documentElement.scrollHeight - innerHeight;
    hdr && hdr.classList.toggle('is-solid', y > 20);
    bar && (bar.style.transform = `scaleX(${h > 0 ? y / h : 0})`);
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* Burger */
  const burger = d.querySelector('.burger');
  burger && burger.addEventListener('click', () => {
    const open = d.body.classList.toggle('menu-open');
    burger.setAttribute('aria-expanded', open);
  });
  d.querySelectorAll('.mnav a').forEach(a => a.addEventListener('click', () => d.body.classList.remove('menu-open')));

  /* Dropdown keyboard / touch */
  d.querySelectorAll('.dd>button').forEach(b => b.addEventListener('click', () => {
    const dd = b.parentElement, o = dd.classList.toggle('open'); b.setAttribute('aria-expanded', o);
  }));
  d.addEventListener('click', e => d.querySelectorAll('.dd.open').forEach(dd => !dd.contains(e.target) && dd.classList.remove('open')));
  d.addEventListener('keydown', e => { if (e.key === 'Escape') { d.querySelectorAll('.dd.open').forEach(dd => dd.classList.remove('open')); d.body.classList.remove('menu-open'); } });


  /* Route en perspective (canvas) : les marquages filent vers l'emblème */
  d.querySelectorAll('canvas.road').forEach(cv => {
    const ctx = cv.getContext('2d'), host = cv.parentElement, target = host.querySelector('.emblem .badge');
    let W, H, vp, run = true, t0 = performance.now(), dpr = Math.min(devicePixelRatio || 1, 2);
    const fit = () => {
      const r = host.getBoundingClientRect(); W = r.width; H = r.height;
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      if (target && innerWidth > 767) { const e = target.getBoundingClientRect(); vp = { x: e.left + e.width / 2 - r.left, y: e.top + e.height / 2 - r.top }; }
      else vp = { x: W * (innerWidth > 767 ? .78 : .7), y: H * (target ? .2 : .32) };
      draw(0);
    };
    const P = (xw, z) => { const k = 1 / z; return [vp.x + (xw - vp.x) * k, vp.y + (H + 40 - vp.y) * k]; };
    const draw = time => {
      ctx.clearRect(0, 0, W, H);
      const cx = vp.x - W * .08, half = Math.max(W * .55, 420), Z = 40;
      const L1 = P(cx - half, 1), R1 = P(cx + half, 1), L2 = P(cx - half, Z), R2 = P(cx + half, Z);
      const g = ctx.createLinearGradient(0, vp.y, 0, H);
      g.addColorStop(0, 'rgba(22,22,25,0)'); g.addColorStop(1, 'rgba(24,24,28,.9)');
      ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(...L1); ctx.lineTo(...L2); ctx.lineTo(...R2); ctx.lineTo(...R1); ctx.fill();
      [cx - half * .92, cx + half * .92].forEach(xw => {
        const a = P(xw, 1), b = P(xw, Z), lg = ctx.createLinearGradient(...a, ...b);
        lg.addColorStop(0, 'rgba(255,255,255,.35)'); lg.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.strokeStyle = lg; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(...a); ctx.lineTo(...b); ctx.stroke();
      });
      const off = (time / 1000 * 2.2) % 4, dw = half * .035;
      for (let k = 0; k < 15; k++) {
        const z1 = k * 4 - off, z2 = z1 + 2.3; if (z2 < .15) continue;
        const zn = Math.max(z1, .15);
        const a = P(cx - dw, zn), b = P(cx + dw, zn), c = P(cx + dw, z2), e = P(cx - dw, z2);
        ctx.fillStyle = `rgba(251,194,12,${Math.min(.95, 2.2 / Math.sqrt(Math.max(z1, 0) + 1)).toFixed(3)})`;
        ctx.beginPath(); ctx.moveTo(...a); ctx.lineTo(...b); ctx.lineTo(...c); ctx.lineTo(...e); ctx.fill();
      }
    };
    const loop = now => { if (!run) return; draw(now - t0); requestAnimationFrame(loop); };
    new IntersectionObserver(([en]) => { run = en.isIntersecting && !reduce; if (run) requestAnimationFrame(loop); }).observe(host);
    addEventListener('resize', fit); d.fonts && d.fonts.ready.then(fit); setTimeout(fit, 1200); fit();
  });

  /* Reveal on scroll */
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -12% 0px', threshold: .08 });
  d.querySelectorAll('.rv,.steps').forEach(el => io.observe(el));

  /* Service card spotlight */
  d.querySelectorAll('.svc').forEach(c => c.addEventListener('pointermove', e => {
    const r = c.getBoundingClientRect();
    c.style.setProperty('--mx', `${e.clientX - r.left}px`); c.style.setProperty('--my', `${e.clientY - r.top}px`);
  }));

  /* Gallery: pinned horizontal scroll */
  const gal = d.querySelector('.gal');
  if (gal && !reduce) {
    const track = gal.querySelector('.gal-track'), shots = [...track.children];
    const fill = gal.querySelector('.gal-bar i'), cnt = gal.querySelector('.gal-count b');
    let dist = 0;
    const size = () => {
      dist = Math.max(0, track.scrollWidth - innerWidth);
      gal.style.height = `${dist + innerHeight}px`;
      tick();
    };
    const tick = () => {
      const top = gal.getBoundingClientRect().top;
      const p = dist ? Math.min(1, Math.max(0, -top / dist)) : 0;
      track.style.transform = `translate3d(${-p * dist}px,0,0)`;
      fill && (fill.style.transform = `scaleX(${p})`);
      const mid = innerWidth / 2;
      let best = 0, bd = 1e9;
      shots.forEach((s, i) => {
        const r = s.getBoundingClientRect(), c = r.left + r.width / 2, off = (c - mid) / innerWidth;
        s.style.setProperty('--s', (1 - Math.min(Math.abs(off) * .12, .08)).toFixed(3));
        s.style.setProperty('--px', `${(-off * 40).toFixed(1)}px`);
        if (Math.abs(c - mid) < bd) { bd = Math.abs(c - mid); best = i; }
      });
      cnt && (cnt.textContent = String(best + 1).padStart(2, '0'));
    };
    addEventListener('resize', size); addEventListener('scroll', () => requestAnimationFrame(tick), { passive: true });
    addEventListener('load', size); size();
  }
  d.querySelectorAll('.shot img').forEach(img => {
    const ok = () => img.closest('.shot').classList.add('has-img');
    const ko = () => img.remove();
    if (img.complete) { img.naturalWidth ? ok() : ko(); } else { img.addEventListener('load', ok); img.addEventListener('error', ko); }
  });

  /* Parallaxe du bandeau photo */
  const pbs = [...d.querySelectorAll('.photoband')];
  if (pbs.length && !reduce) {
    const par = () => pbs.forEach(b => {
      const r = b.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) return;
      const p = (r.top + r.height / 2 - innerHeight / 2) / (innerHeight + r.height);
      b.querySelector('.pb-img').style.setProperty('--py', `${(p * -160).toFixed(1)}px`);
    });
    addEventListener('scroll', () => requestAnimationFrame(par), { passive: true }); par();
  }

  /* Radar map */
  const radar = d.querySelector('.radar');
  const data = d.getElementById('towns-data');
  if (radar && data) {
    const T = JSON.parse(data.textContent), NS = 'http://www.w3.org/2000/svg';
    const R = 270, C = 300, focus = radar.dataset.focus || '';
    const rad = km => R * Math.sqrt(km / 25), pos = t => { const k = t.km ? rad(t.km) / Math.hypot(t.x, t.y) : 0; return [C + t.x * k, C - t.y * k]; };
    const svg = d.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 600 600'); svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Carte radar de la zone d’intervention : 25 km autour de Ris-Orangis');
    const el = (n, a, p = svg) => { const e = d.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); p.appendChild(e); return e; };
    const defs = el('defs', {});
    const g = el('radialGradient', { id: 'rg' }, defs);
    el('stop', { offset: '0', 'stop-color': '#FBC20C', 'stop-opacity': '.10' }, g);
    el('stop', { offset: '1', 'stop-color': '#FBC20C', 'stop-opacity': '0' }, g);
    el('circle', { cx: C, cy: C, r: R, fill: 'url(#rg)' });
    [2, 5, 10, 15, 25].forEach(k => {
      el('circle', { cx: C, cy: C, r: rad(k), fill: 'none', stroke: k === 25 ? 'rgba(251,194,12,.55)' : 'rgba(255,255,255,.09)', 'stroke-width': k === 25 ? 1.5 : 1, 'stroke-dasharray': k === 25 ? '6 6' : '' });
      const t = el('text', { x: C + 4, y: C - rad(k) - 5, class: 'ringtxt' }); t.textContent = `${k} km`;
    });
    el('line', { x1: C, y1: C - R - 10, x2: C, y2: C + R + 10, stroke: 'rgba(255,255,255,.06)' });
    el('line', { x1: C - R - 10, y1: C, x2: C + R + 10, y2: C, stroke: 'rgba(255,255,255,.06)' });
    [['N', C, C - R - 16], ['S', C, C + R + 26], ['O', C - R - 22, C + 4], ['E', C + R + 14, C + 4]].forEach(([s, x, y]) => { const t = el('text', { x, y, class: 'ringtxt', 'text-anchor': 'middle' }); t.textContent = s; });
    const card = d.createElement('div'); card.className = 'rcard'; card.setAttribute('role', 'status'); radar.appendChild(card);
    const nodes = {};
    const show = (t, node) => {
      Object.values(nodes).forEach(n => n.classList.remove('on')); node.classList.add('on');
      d.querySelectorAll('.towns a').forEach(a => a.classList.toggle('on', a.dataset.slug === t.slug));
      const [px, py] = pos(t), x = px / 6, y = py / 6;
      card.style.left = `${x}%`; card.style.top = `${y}%`;
      card.innerHTML = `<b>${t.n}</b><span>${t.cp} · ${t.km.toString().replace('.', ',')} km de Ris-Orangis</span>` + (t.url ? `<a href="${t.url}">Dépannage à ${t.n} →</a>` : `<a href="tel:+33607945798">Appeler le 06 07 94 57 98</a>`);
      card.classList.add('show');
    };
    T.forEach(t => {
      const [x, y] = pos(t), ang = (Math.atan2(t.x, t.y) * 180 / Math.PI + 360) % 360;
      if (t.hq) {
        const h = el('g', { class: 'hq' });
        el('circle', { cx: x, cy: y, r: 16, class: 'halo' }, h); el('circle', { cx: x, cy: y, r: 7 }, h);
        const tx = el('text', { x: x + 12, y: y - 12, class: 'ringtxt', style: 'fill:#FBC20C;font-weight:700;font-size:12px' }, h); tx.textContent = 'Ris-Orangis · base';
        return;
      }
      const n = el('g', { class: 'c' + (t.major || t.slug === focus ? ' major' : ''), tabindex: 0, role: 'button', 'aria-label': `${t.n}, ${t.km} km` });
      n.style.setProperty('--dl', `${(ang / 36).toFixed(2)}s`);
      el('circle', { cx: x, cy: y, r: 5, class: 'ping' }, n);
      el('circle', { cx: x, cy: y, r: 4, class: 'dot' }, n);
      el('circle', { cx: x, cy: y, r: 14, fill: 'transparent' }, n);
      const lb = el('text', { x: x + (t.x < 0 ? -9 : 9), y: y + 4, 'text-anchor': t.x < 0 ? 'end' : 'start' }, n); lb.textContent = t.n;
      n.addEventListener('mouseenter', () => show(t, n)); n.addEventListener('focus', () => show(t, n));
      n.addEventListener('click', () => { show(t, n); });
      n.addEventListener('keydown', e => { if (e.key === 'Enter' && t.url) location.href = t.url; });
      nodes[t.slug] = n;
    });
    radar.prepend(svg);
    const sw = radar.querySelector('.sweep'); if (sw) { sw.style.animation = 'none'; sw.offsetWidth; sw.style.animation = ''; }
    d.querySelectorAll('.towns a[data-slug]').forEach(a => {
      const t = T.find(x => x.slug === a.dataset.slug);
      if (t) a.addEventListener('mouseenter', () => show(t, nodes[t.slug]));
    });
    radar.addEventListener('mouseleave', () => card.classList.remove('show'));
    if (focus && nodes[focus]) { const t = T.find(x => x.slug === focus); setTimeout(() => show(t, nodes[focus]), 600); }
  }

  /* Form */
  const form = d.getElementById('quoteForm');
  if (form) form.addEventListener('submit', async e => {
    e.preventDefault();
    let bad = null;
    form.querySelectorAll('[required]').forEach(f => {
      const wrap = f.closest('.field'), err = wrap.querySelector('.err');
      const ok = f.value.trim() && (f.type !== 'tel' || f.value.replace(/\D/g, '').length >= 10);
      wrap.classList.toggle('bad', !ok); err.textContent = ok ? '' : (f.type === 'tel' ? 'Indiquez un numéro à 10 chiffres pour qu’on vous rappelle.' : 'Ce champ est nécessaire pour vous rappeler.');
      if (!ok && !bad) bad = f;
    });
    if (bad) { bad.focus(); return; }
    const btn = form.querySelector('button[type=submit]'), label = btn.innerHTML;
    btn.disabled = true; btn.innerHTML = 'Envoi en cours…';
    const fd = new FormData(form), obj = Object.fromEntries(fd.entries());
    try {
      const r = await fetch(form.action, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(obj) });
      if (!r.ok) throw 0;
      form.classList.add('sent');
    } catch {
      const body = `Demande de devis - ${obj.nom} (${obj.telephone}) - ${obj.ville || ''} - ${obj.prestation || ''} : ${obj.message || ''}`;
      location.href = `sms:+33607945798?&body=${encodeURIComponent(body)}`;
      btn.disabled = false; btn.innerHTML = label;
    }
  });
})();
