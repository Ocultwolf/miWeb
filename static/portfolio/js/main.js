const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const isMobile = () => window.innerWidth <= 900;
const lang = document.documentElement.lang === 'es' ? 'es' : 'en';

// ---------- Navegación ----------
const nav = document.getElementById('nav');
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');
addEventListener('scroll', () => nav.classList.toggle('scrolled', scrollY > 40), { passive: true });
function setMenu(open) {
  navToggle.classList.toggle('open', open);
  navMenu.classList.toggle('open', open);
  navToggle.setAttribute('aria-expanded', String(open));
}
navToggle.addEventListener('click', () => setMenu(!navMenu.classList.contains('open')));
navMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
document.addEventListener('click', e => { if (!nav.contains(e.target)) setMenu(false); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });

gsap.registerPlugin(ScrollTrigger);

// ---------- Hero cinematográfico ----------
// Una onda de voz (Neon) que, con el scroll, se deshace en puntos que forman la red de agentes.
(function hero() {
  const home = document.getElementById('home');
  const canvas = document.getElementById('heroCanvas');
  if (!home || !canvas) return;
  const ctx = canvas.getContext('2d');
  const N = 72;
  const NODES = ['voice', 'neon', 'jarvis', 'tools', 'blog', 'web'];
  const LAYOUT = [[0, .5], [.25, .22], [.5, .5], [.78, .2], [.78, .8], [1, .5]];
  const EDGES = [[0, 1], [1, 2], [2, 3], [2, 4], [3, 4], [4, 5]];
  let W = 0, H = 0, progress = 0, t = 0, running = false;
  const seed = Array.from({ length: N }, (_, i) => ({ a: i * 2.399, r: 7 + (i * 7919 % 11) }));

  function size() {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = W * dpr; canvas.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  // Zona donde vive el dibujo: a la derecha del texto en escritorio, abajo en móvil.
  function box() {
    return isMobile()
      ? { x0: W * .1, x1: W * .9, y0: H * .52, y1: H * .86, cy: H * .9 }
      : { x0: W * .5, x1: W * .93, y0: H * .24, y1: H * .76, cy: H * .5 };
  }
  const clamp = v => Math.max(0, Math.min(1, v));
  const ease = v => v < .5 ? 4 * v * v * v : 1 - Math.pow(-2 * v + 2, 3) / 2;
  const nodePos = (k, b) => [b.x0 + LAYOUT[k][0] * (b.x1 - b.x0), b.y0 + LAYOUT[k][1] * (b.y1 - b.y0)];

  function draw() {
    const b = box(), p = progress;
    ctx.clearRect(0, 0, W, H);
    const edgeA = clamp((p - .55) / .2), labelA = clamp((p - .68) / .15);

    // Aristas y pulsos que las recorren
    if (edgeA > 0) {
      ctx.lineWidth = 1;
      EDGES.forEach(([a, c], j) => {
        const [ax, ay] = nodePos(a, b), [cx, cy] = nodePos(c, b);
        ctx.strokeStyle = `rgba(154,151,140,${.35 * edgeA})`;
        ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(cx, cy); ctx.stroke();
        const f = (t * .35 + j * .27) % 1;
        ctx.fillStyle = `rgba(242,181,68,${edgeA})`;
        ctx.beginPath(); ctx.arc(ax + (cx - ax) * f, ay + (cy - ay) * f, 2.2, 0, Math.PI * 2); ctx.fill();
      });
    }

    // Puntos: barra de la onda -> punto orbitando su nodo
    const step = (b.x1 - b.x0) / (N - 1);
    for (let i = 0; i < N; i++) {
      const q = ease(clamp((p - .22 - .2 * (i / N)) / .35));
      const env = Math.exp(-Math.pow((i / N - .5 - .25 * Math.sin(t * .6)) * 3.2, 2));
      const amp = (H * (isMobile() ? .04 : .16)) * env * (.35 + .65 * Math.abs(Math.sin(i * .55 + t * 2.4))) + 2;
      const wx = b.x0 + i * step, wy = b.cy;
      const k = i % NODES.length, [nx, ny] = nodePos(k, b), s = seed[i];
      const ang = s.a + t * .4;
      const tx = nx + Math.cos(ang) * s.r, ty = ny + Math.sin(ang) * s.r;
      const x = wx + (tx - wx) * q, y = wy + (ty - wy) * q;
      const h = amp * (1 - q) + 1.6 * q;
      ctx.fillStyle = `rgba(242,181,68,${.55 + .45 * q})`;
      ctx.fillRect(x - 1.25, y - h, 2.5, h * 2);
    }

    // Nodos y etiquetas
    if (labelA > 0) {
      ctx.font = '500 11px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      NODES.forEach((name, k) => {
        const [nx, ny] = nodePos(k, b);
        ctx.strokeStyle = `rgba(242,181,68,${.6 * labelA})`;
        ctx.beginPath(); ctx.arc(nx, ny, 22, 0, Math.PI * 2); ctx.stroke();
        ctx.fillStyle = `rgba(230,227,218,${labelA})`;
        ctx.fillText(name, nx, ny + (LAYOUT[k][1] > .6 ? 40 : -32));
      });
    }
  }

  function loop() {
    if (!running) return;
    t += 1 / 60;
    draw();
    requestAnimationFrame(loop);
  }
  size(); draw();
  addEventListener('resize', () => { size(); draw(); });

  if (reduceMotion) {
    // Sin animación: imagen fija a medio camino y la historia como lista.
    home.classList.add('no-cine');
    progress = .9; size(); draw();
    return;
  }

  new IntersectionObserver(([e]) => {
    running = e.isIntersecting;
    if (running) requestAnimationFrame(loop);
  }).observe(canvas);

  const tl = gsap.timeline({
    defaults: { ease: 'none' },
    scrollTrigger: {
      trigger: home, start: 'top top', end: '+=240%', pin: true, scrub: .6,
      onUpdate: self => { progress = self.progress; }
    }
  });
  tl.to('.hero-intro', { autoAlpha: 0, y: -60, duration: .16 }, .04)
    .to('.scroll-ind', { autoAlpha: 0, duration: .05 }, 0);
  document.querySelectorAll('.cine-step').forEach((el, i) => {
    const at = .22 + i * .26;
    tl.fromTo(el, { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: .07 }, at);
    if (i < 2) tl.to(el, { autoAlpha: 0, y: -30, duration: .07 }, at + .19);
  });
})();

// ---------- Proyectos: fila horizontal fijada (solo escritorio) ----------
const track = document.getElementById('track');
if (track && !isMobile() && !reduceMotion) {
  const dist = () => Math.max(0, track.scrollWidth - track.parentElement.clientWidth + 48);
  gsap.to(track, {
    x: () => -dist(), ease: 'none',
    scrollTrigger: { trigger: '#projects', pin: true, scrub: .5, start: 'top top', end: () => '+=' + dist(), invalidateOnRefresh: true }
  });
}

// Inclinación sutil de las tarjetas (escritorio)
if (!isMobile() && !reduceMotion) {
  document.querySelectorAll('[data-tilt]').forEach(card => {
    card.addEventListener('mousemove', e => {
      const r = card.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      card.style.transform = `perspective(800px) rotateY(${x * 8}deg) rotateX(${-y * 5}deg)`;
    });
    card.addEventListener('mouseleave', () => { card.style.transform = ''; });
  });
}

addEventListener('load', () => ScrollTrigger.refresh());

// ---------- Copiar email ----------
document.querySelectorAll('.copy-email-btn').forEach(btn => {
  btn.addEventListener('click', e => {
    if (!navigator.clipboard) return; // sin portapapeles, que actúe el mailto
    e.preventDefault();
    navigator.clipboard.writeText('pablodominguezviera@gmail.com').then(() => {
      let toast = document.querySelector('.copy-toast');
      if (!toast) {
        toast = document.createElement('div');
        toast.className = 'copy-toast';
        toast.setAttribute('role', 'status');
        document.body.appendChild(toast);
      }
      toast.textContent = btn.dataset.copied || 'Email copied';
      requestAnimationFrame(() => toast.classList.add('show'));
      setTimeout(() => toast.classList.remove('show'), 2500);
    }, () => { location.href = btn.href; });
  });
});

// ---------- Actividad de GitHub: solo con datos reales ----------
(async function contributions() {
  const section = document.getElementById('activity');
  const canvas = document.getElementById('contribCanvas');
  if (!section || !canvas) return;
  let data;
  try {
    const res = await fetch('https://github-contributions-api.jogruber.de/v4/Ocultwolf?y=last');
    if (!res.ok) return;
    data = (await res.json()).contributions.map(d => ({ date: d.date, count: d.count }));
  } catch { return; }
  if (!data || !data.length) return;
  section.hidden = false;

  const ctx = canvas.getContext('2d');
  const tooltip = document.getElementById('contribTooltip');
  const WEEKS = 53, DAYS = 7, GAP = 3;
  const total = data.reduce((s, d) => s + d.count, 0);
  document.getElementById('contribCount').textContent = lang === 'es'
    ? `${total.toLocaleString('es')} contribuciones en el último año`
    : `${total.toLocaleString('en')} contributions in the last year`;
  const byDate = new Map(data.map(d => [d.date, d.count]));
  const start = new Date(); start.setDate(start.getDate() - start.getDay() - (WEEKS - 1) * 7);
  const cells = [];
  for (let w = 0; w < WEEKS; w++) for (let d = 0; d < DAYS; d++) {
    const date = new Date(start); date.setDate(start.getDate() + w * 7 + d);
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    cells.push({ w, d, date, count: byDate.get(key) || 0 });
  }
  const color = c => c === 0 ? 'rgba(242,181,68,.07)' : c <= 2 ? 'rgba(242,181,68,.25)' : c <= 5 ? 'rgba(242,181,68,.5)' : c <= 10 ? 'rgba(242,181,68,.75)' : 'rgba(242,181,68,1)';
  let CELL = 10;
  function draw() {
    const dpr = devicePixelRatio || 1;
    CELL = Math.max(8, Math.floor((canvas.parentElement.clientWidth - (WEEKS - 1) * GAP) / WEEKS));
    const w = WEEKS * CELL + (WEEKS - 1) * GAP, h = DAYS * CELL + (DAYS - 1) * GAP;
    canvas.width = w * dpr; canvas.height = h * dpr; canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cells.forEach(c => { ctx.fillStyle = color(c.count); ctx.fillRect(c.w * (CELL + GAP), c.d * (CELL + GAP), CELL, CELL); });
  }
  draw();
  addEventListener('resize', draw);
  canvas.addEventListener('mousemove', e => {
    const r = canvas.getBoundingClientRect();
    const w = Math.floor((e.clientX - r.left) / (CELL + GAP)), d = Math.floor((e.clientY - r.top) / (CELL + GAP));
    const cell = cells[w * DAYS + d];
    if (!cell || d >= DAYS) { tooltip.style.opacity = '0'; return; }
    const when = cell.date.toLocaleDateString(lang, { day: 'numeric', month: 'short', year: 'numeric' });
    tooltip.textContent = `${cell.count} · ${when}`;
    tooltip.style.opacity = '1';
    tooltip.style.left = Math.min(e.clientX - r.left + 12, r.width - 140) + 'px';
    tooltip.style.top = Math.max(e.clientY - r.top - 34, 0) + 'px';
  });
  canvas.addEventListener('mouseleave', () => { tooltip.style.opacity = '0'; });
})();
