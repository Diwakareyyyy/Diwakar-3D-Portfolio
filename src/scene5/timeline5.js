// Choreography timeline for Section 5 (Certificates).

const T = {
  wake: [0.0, 0.9],
  glow: [0.4, 1.6],
  floor: [0.7, 1.8],
  deck: [0.9, 2.6],
  labels: [1.8, 3.0],
  live: 2.8,
};

export const T5 = T;

const clamp01 = (v) => Math.min(1, Math.max(0, v));
const span = ([a, b], t) => clamp01((t - a) / (b - a));
const ease = (v) => v * v * (3 - 2 * v);

export function sample5(t) {
  const wake = ease(span(T.wake, t));
  const glow = ease(span(T.glow, t));
  const floor = ease(span(T.floor, t));
  const deck = span(T.deck, t);
  const labels = span(T.labels, t);

  return {
    wake: 0.25 * wake + 0.75 * ease(deck),
    glow,
    floor,
    deck,
    labels,
    live: t >= T.live,
    grain: 0.04 + 0.02 * wake,
  };
}

export function cardIn5(t, rank, total) {
  const stagger = (rank / Math.max(total - 1, 1)) * 0.9;
  const t0 = T.deck[0] + stagger;
  const t1 = t0 + 0.85;
  return ease(span([t0, t1], t));
}
