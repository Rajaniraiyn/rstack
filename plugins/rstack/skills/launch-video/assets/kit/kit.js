// Launch-video kit: icons, easing, and time-driven animation primitives.
// Load after icons.js (window.ICONS, window.BRAND). Every helper takes the
// current time t, so a page's render(t) stays a pure function of time.
window.$ = (id) => document.getElementById(id);
window.ic = (name, size = 24, color = "currentColor", sw = 1.75) =>
  `<svg class="ic" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${ICONS[name]}</svg>`;
window.brand = (name, size, color) =>
  `<svg class="ic" width="${size}" height="${size}" viewBox="0 0 24 24"><path d="${BRAND[name]}" fill="${color}"/></svg>`;
// A product's logo: pass its SVG markup once (window.LOGO = "<svg ...>") and
// place it with logo(size). Take the real mark from the product's source.
window.logo = (size) => (window.LOGO || "").replace("<svg", `<svg class="ic" width="${size}" height="${size}"`);

window.clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
window.lerp = (a, b, p) => a + (b - a) * p;
window.eOut = (p) => 1 - Math.pow(1 - p, 3);
window.eOut5 = (p) => 1 - Math.pow(1 - p, 5);
window.eInOut = (p) => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2);
window.eBack = (p) => { const c = 1.25; return 1 + (c + 1) * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); };
window.prog = (t, t0, d) => clamp((t - t0) / d);
window.vis = (el, on) => { el.style.visibility = on ? "visible" : "hidden"; };

// Enter: fade + short travel, no bounce by default.
window.enter = (el, t, t0, d = 0.45, dy = 24, ease = eOut5) => {
  const p = ease(prog(t, t0, d));
  el.style.opacity = clamp(prog(t, t0, d * 0.6));
  el.style.transform = `translateY(${(1 - p) * dy}px)`;
  return p;
};
// Headline line reveal: each .ln child rises out of a mask, staggered.
window.lines = (el, t, t0, stagger = 0.08, d = 0.55) => {
  el.querySelectorAll(".ln > span").forEach((s, i) => {
    const p = eOut5(prog(t, t0 + i * stagger, d));
    s.style.transform = `translateY(${(1 - p) * 105}%)`;
  });
};
// Hard-cut word stamp: appears on the beat at full size with a 2-frame settle.
window.stamp = (el, t, t0) => {
  const on = t >= t0;
  el.style.opacity = on ? 1 : 0;
  const p = eOut5(prog(t, t0, 0.16));
  el.style.transform = `scale(${lerp(1.06, 1, p)})`;
};
// Camera / path keyframes: keys = [[t, a, b, ...], ...]; returns [t, a, b, ...] eased between keys.
// For a camera use [t, scale, focusX, focusY] and apply
// translate(W/2 - fx*s, H/2 - fy*s) scale(s) with transform-origin 0 0.
window.camAt = (t, keys) => {
  if (t <= keys[0][0]) return keys[0];
  if (t >= keys[keys.length - 1][0]) return keys[keys.length - 1];
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i], b = keys[i + 1];
    if (t >= a[0] && t <= b[0]) { const p = eInOut((t - a[0]) / (b[0] - a[0])); return [t, ...a.slice(1).map((v, j) => lerp(v, b[j + 1], p))]; }
  }
};
// Standard readiness promise: fonts and images loaded. Pages set
// window.ready = kitReady().then(() => { /* measure layout */ render(0); });
window.kitReady = () => Promise.all([
  document.fonts.load('600 40px Geist'), document.fonts.load('500 20px "Geist Mono"'), document.fonts.ready,
  ...[...document.images].map((i) => (i.complete ? 1 : new Promise((r) => { i.onload = r; i.onerror = r; }))),
]);
