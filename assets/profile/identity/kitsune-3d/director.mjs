/** Deterministic character director. No DOM, timers, network or random numbers. */
export const STEP = 1 / 60;
export const NEUTRAL = Object.freeze({
  x: 0,
  y: 0,
  roll: 0,
  scale: 1,
  gx: 0,
  gy: 0,
  lid: 0,
  wink: 0,
  neutral: 0,
  think: 0,
  laugh: 0,
  surprise: 0,
});
const clamp = (n, a = 0, b = 1) => Math.max(a, Math.min(b, n));
const smooth = (t) => t * t * (3 - 2 * t);
const frame = (at, values = {}) => ({ at, ...NEUTRAL, ...values });
const clip = (id, label, state, duration, cooldown, keys, effects = {}) => ({
  id,
  label,
  state,
  duration,
  cooldown,
  keys: [frame(0), ...keys.map(([t, p]) => frame(t, p)), frame(duration)],
  effects,
});

export const ACTIONS = Object.freeze([
  clip(
    "greet",
    "Saludar",
    "social",
    4.8,
    60,
    [
      [0.45, { y: -0.25, scale: 1.025 }],
      [1, { roll: -4, gy: -0.3 }],
      [1.6, { roll: 2, y: 0.18 }],
      [2.15, { y: -0.35 }],
      [2.7, { y: 0.2 }],
      [3.5, { roll: -2 }],
    ],
    { social: -0.45 },
  ),
  clip(
    "listen",
    "Escuchar",
    "atento",
    7.2,
    20,
    [
      [0.65, { neutral: 1, roll: -2 }],
      [2.3, { neutral: 1, roll: -2.8, gx: -0.25 }],
      [4.2, { neutral: 1, roll: -1.8, gy: 0.2 }],
      [5.8, { neutral: 0.5, y: 0.12 }],
    ],
    { social: -0.1, strain: 0.02 },
  ),
  clip(
    "slow-blink",
    "Parpadear con calma",
    "tranquilo",
    5.4,
    26,
    [
      [0.7, { neutral: 0.65, roll: -1 }],
      [1.2, { neutral: 0.65, lid: 0.35, roll: -1 }],
      [1.6, { neutral: 0.65, lid: 1, roll: -1, y: 0.08 }],
      [2, { neutral: 0.65, lid: 1, roll: -1, y: 0.08 }],
      [2.6, { neutral: 0.65, lid: 0.3, roll: -1 }],
      [3.8, {}],
    ],
    { strain: -0.12, social: -0.08 },
  ),
  clip(
    "look-left",
    "Mirar a la izquierda",
    "curioso",
    5.6,
    18,
    [
      [0.25, { gx: -1 }],
      [0.9, { gx: -1, x: -0.13, roll: -3.4 }],
      [2.4, { gx: -0.8, roll: -3.4 }],
      [3.4, { gx: -0.45, roll: -1.5 }],
      [4.7, {}],
    ],
    { curiosity: -0.18, strain: 0.04 },
  ),
  clip(
    "look-right",
    "Mirar a la derecha",
    "curioso",
    5.8,
    18,
    [
      [0.3, { gx: 1 }],
      [1, { gx: 1, x: 0.13, roll: 3.2 }],
      [2.6, { gx: 0.85, roll: 3.2 }],
      [3.7, { gx: 0.4, roll: 1.2 }],
      [4.9, {}],
    ],
    { curiosity: -0.18, strain: 0.04 },
  ),
  clip(
    "scan",
    "Explorar el entorno",
    "curioso",
    9.2,
    35,
    [
      [0.45, { gx: -1 }],
      [1.2, { gx: -1, roll: -2.2 }],
      [2.8, { gx: -0.7, roll: -2.2 }],
      [3.8, { gx: 0.15, gy: -0.5 }],
      [4.6, { gx: 0.9, roll: 2.2 }],
      [6.4, { gx: 0.7, roll: 2.2 }],
      [7.9, {}],
    ],
    { curiosity: -0.38, strain: 0.08 },
  ),
  clip(
    "inspect",
    "Acercarse a mirar",
    "concentrado",
    7.8,
    25,
    [
      [0.5, { gy: 0.8, neutral: 0.7 }],
      [1.2, { scale: 1.055, y: 0.25, gy: 1, neutral: 1, roll: -3 }],
      [3.5, { scale: 1.055, y: 0.25, gy: 0.8, neutral: 1, roll: -3 }],
      [5.3, { scale: 1.02, neutral: 0.7, gy: 0.2 }],
      [6.7, {}],
    ],
    { curiosity: -0.3, strain: 0.1 },
  ),
  clip(
    "look-up",
    "Seguir algo arriba",
    "curioso",
    6.4,
    24,
    [
      [0.25, { gy: -1 }],
      [1, { gy: -1, y: -0.3, roll: 1.6, neutral: 0.7 }],
      [3.2, { gy: -0.8, y: -0.3, roll: 1.6, neutral: 0.7 }],
      [4.9, {}],
    ],
    { curiosity: -0.22, strain: 0.04 },
  ),
  clip(
    "think",
    "Pensar",
    "pensativo",
    9.4,
    28,
    [
      [0.6, { think: 1, gx: -0.5 }],
      [1.5, { think: 1, gy: -0.7, roll: -4 }],
      [4.4, { think: 1, gy: -0.7, roll: -4, lid: 0.12 }],
      [5.9, { think: 1, gx: 0.45, roll: -2 }],
      [7.4, { think: 0.4, roll: 1 }],
      [8.2, {}],
    ],
    { curiosity: -0.2, strain: 0.13 },
  ),
  clip(
    "focus",
    "Concentrarse",
    "concentrado",
    10.4,
    32,
    [
      [0.7, { neutral: 1, gy: 0.5, scale: 1.02 }],
      [2, { neutral: 1, gy: 0.65, scale: 1.02, lid: 0.12 }],
      [4.5, { neutral: 1, gx: -0.3, gy: 0.4, scale: 1.02 }],
      [6.5, { neutral: 1, gx: 0.3, gy: 0.5 }],
      [8.7, { neutral: 0.5 }],
    ],
    { curiosity: -0.3, strain: 0.2, energy: -0.06 },
  ),
  clip(
    "nod",
    "Asentir",
    "social",
    4.3,
    14,
    [
      [0.55, { y: 0.3, neutral: 0.65 }],
      [0.95, { y: -0.3, neutral: 0.65 }],
      [1.4, { y: 0.23, neutral: 0.65 }],
      [1.85, { y: -0.2, neutral: 0.4 }],
      [2.4, {}],
      [3.2, { roll: 1 }],
    ],
    { social: -0.12 },
  ),
  clip(
    "reconsider",
    "Negar suavemente",
    "pensativo",
    5.6,
    23,
    [
      [0.6, { neutral: 1, x: -0.2, roll: -3 }],
      [1.25, { neutral: 1, x: 0.2, roll: 3 }],
      [1.95, { neutral: 1, x: -0.15, roll: -2 }],
      [2.7, { neutral: 0.8, roll: 1 }],
      [4, { think: 0.6 }],
    ],
    { strain: 0.04 },
  ),
  clip(
    "question",
    "Preguntar con la mirada",
    "curioso",
    6.2,
    26,
    [
      [0.6, { neutral: 0.8, roll: 4, gx: 0.4 }],
      [2, { think: 0.65, roll: 5, gx: 0.5 }],
      [3.4, { think: 0.65, roll: 5, lid: 0.15 }],
      [4.7, { neutral: 0.5 }],
    ],
    { curiosity: -0.15 },
  ),
  clip(
    "wink",
    "Guiñar un ojo",
    "juguetón",
    4.8,
    35,
    [
      [0.55, { roll: -2 }],
      [1, { wink: 0.3, roll: -3 }],
      [1.15, { wink: 1, roll: -3 }],
      [1.55, { wink: 1, roll: -3 }],
      [1.9, { wink: 0, roll: -2 }],
      [3.3, {}],
    ],
    { social: -0.25, energy: -0.02 },
  ),
  clip(
    "mischief",
    "Sonreír con complicidad",
    "juguetón",
    6.6,
    40,
    [
      [0.6, { gx: 0.7, roll: -2, neutral: 0.3 }],
      [1.7, { gx: 0.6, roll: -3, wink: 0.45, neutral: 0.3 }],
      [3.3, { gx: 0.5, roll: -3, wink: 0.45 }],
      [4.8, { roll: 1 }],
    ],
    { social: -0.24, energy: -0.02 },
  ),
  clip(
    "laugh",
    "Reír",
    "alegre",
    5.8,
    28,
    [
      [0.5, { laugh: 0.6 }],
      [1, { laugh: 1, lid: 0.65, y: -0.25, roll: -2 }],
      [1.4, { laugh: 1, lid: 0.75, y: 0.15, roll: -1 }],
      [1.8, { laugh: 1, lid: 0.55, y: -0.2, roll: 1 }],
      [2.2, { laugh: 1, lid: 0.65, y: 0.12, roll: 2 }],
      [2.7, { laugh: 0.85, lid: 0.4, y: -0.1 }],
      [3.8, { laugh: 0.4, roll: 1 }],
      [4.9, {}],
    ],
    { social: -0.35, strain: -0.15, energy: -0.04 },
  ),
  clip(
    "surprise",
    "Sorprenderse",
    "alerta",
    4.9,
    22,
    [
      [0.2, { surprise: 1, scale: 1.035, y: -0.25 }],
      [0.65, { surprise: 1, gy: -0.5, scale: 1.035, y: -0.25 }],
      [1.7, { surprise: 0.8, gy: -0.3, roll: 2 }],
      [2.7, { neutral: 0.6, roll: 2 }],
      [3.8, {}],
    ],
    { curiosity: 0.2, energy: -0.03 },
  ),
  clip(
    "proud",
    "Celebrar algo pequeño",
    "alegre",
    5.5,
    30,
    [
      [0.65, { scale: 1.025, y: -0.2, roll: -2 }],
      [1.3, { laugh: 0.7, lid: 0.3, y: -0.4, roll: 2 }],
      [2.1, { laugh: 0.7, lid: 0.3, y: -0.2, roll: 2 }],
      [3.1, { neutral: 0.5, gy: -0.3 }],
      [4.4, {}],
    ],
    { social: -0.25, strain: -0.1 },
  ),
  clip(
    "stretch",
    "Estirarse",
    "descansando",
    7.4,
    45,
    [
      [0.9, { neutral: 1, y: -0.35, scale: 1.015, lid: 0.4 }],
      [2.1, { neutral: 1, y: -0.6, scale: 1.02, lid: 0.85, roll: -3 }],
      [3.1, { neutral: 1, y: -0.5, lid: 0.85, roll: 3 }],
      [4.3, { neutral: 1, lid: 0.4, y: 0.2 }],
      [5.9, {}],
    ],
    { strain: -0.5, energy: 0.06 },
  ),
  clip(
    "sigh",
    "Respirar y soltar",
    "descansando",
    7.6,
    35,
    [
      [1.3, { neutral: 1, scale: 1.025, y: -0.12, lid: 0.25 }],
      [2.9, { neutral: 1, scale: 1.025, y: -0.12, lid: 0.7 }],
      [4.8, { neutral: 1, scale: 0.99, y: 0.2, lid: 0.45 }],
      [6.1, { neutral: 0.6 }],
    ],
    { strain: -0.4, energy: 0.03 },
  ),
  clip(
    "drowsy",
    "Vencer al sueño",
    "somnoliento",
    9.8,
    35,
    [
      [1, { neutral: 1, lid: 0.35, roll: 2 }],
      [2.9, { neutral: 1, lid: 0.7, y: 0.2, roll: 3 }],
      [4.2, { neutral: 1, lid: 0.92, y: 0.45, roll: 3 }],
      [4.8, { neutral: 1, lid: 0.15, y: -0.25 }],
      [6.2, { neutral: 1, lid: 0.5, y: 0.15 }],
      [8.2, { neutral: 0.5, lid: 0.2 }],
    ],
    { energy: 0.06, strain: -0.2 },
  ),
  clip(
    "nap",
    "Echar una cabezada",
    "dormido",
    14,
    80,
    [
      [1.2, { neutral: 1, lid: 0.7, y: 0.15 }],
      [2.4, { neutral: 1, lid: 1, y: 0.45, roll: 3 }],
      [5, { neutral: 1, lid: 1, y: 0.5, roll: 3 }],
      [8, { neutral: 1, lid: 1, y: 0.45, roll: 2.5 }],
      [10.8, { neutral: 1, lid: 1, y: 0.4, roll: 2 }],
      [12.5, { neutral: 0.8, lid: 0.4, y: 0.1 }],
    ],
    { energy: 0.55, strain: -0.65 },
  ),
  clip(
    "wake",
    "Despertarse",
    "recuperándose",
    6.2,
    45,
    [
      [0.55, { neutral: 1, lid: 0.55, y: 0.15 }],
      [1.1, { neutral: 1, lid: 0.1, gy: -0.3, y: -0.25 }],
      [1.7, { neutral: 1, lid: 0.65 }],
      [2.3, { neutral: 0.7, lid: 0, gy: 0.4 }],
      [3.5, { gx: -0.6, roll: -2 }],
      [4.8, {}],
    ],
    { energy: 0.1, curiosity: 0.2 },
  ),
  clip(
    "farewell",
    "Despedirse",
    "social",
    5.8,
    80,
    [
      [0.6, { roll: 3 }],
      [1.2, { y: 0.3, roll: 2 }],
      [1.8, { y: -0.2, roll: 1 }],
      [2.7, { wink: 1, roll: -2 }],
      [3.2, { wink: 0, roll: -2 }],
      [4.5, {}],
    ],
    { social: -0.3 },
  ),
]);
export const ACTION_MAP = new Map(ACTIONS.map((action) => [action.id, action]));
export const SIGNALS = Object.freeze({
  greeting: ["greet"],
  attention: ["look-left", "look-right", "look-up", "inspect", "scan"],
  thought: ["think", "question", "focus"],
  agreement: ["nod", "proud"],
  doubt: ["reconsider", "question"],
  humor: ["laugh", "mischief", "wink"],
  surprise: ["surprise"],
  quiet: ["sigh", "drowsy", "nap"],
  return: ["wake", "greet"],
  farewell: ["farewell"],
});

function poseAt(action, age) {
  const keys = action.keys;
  let i = 1;
  while (i < keys.length - 1 && keys[i].at < age) i++;
  const a = keys[i - 1],
    b = keys[i],
    t = smooth(clamp((age - a.at) / (b.at - a.at)));
  return Object.fromEntries(
    Object.keys(NEUTRAL).map((key) => [key, a[key] + (b[key] - a[key]) * t]),
  );
}

export class KitsuneDirector {
  constructor({ initialAction = "greet" } = {}) {
    this.time = 0;
    this.accumulator = 0;
    this.active = null;
    this.history = [];
    this.pending = [];
    this.needs = { energy: 0.84, curiosity: 0.24, social: 0.5, strain: 0 };
    this.last = new Map();
    this.blinkStart = -100;
    this.lastBlink = 0;
    this.blinkDrive = 0.45;
    this.blinkCount = 0;
    this.nextDecision = 0;
    this.pointer = { x: 0, y: 0, strength: 0 };
    this.pointerTarget = { ...this.pointer };
    this.lastSignal = 0;
    this.ticks = 0;
    if (initialAction !== null) {
      if (!ACTION_MAP.has(initialAction))
        throw new RangeError("Gesto inicial desconocido.");
      this.start(
        initialAction,
        initialAction === "greet"
          ? "Primera presencia: saluda antes de explorar."
          : "Prueba explícita: " + ACTION_MAP.get(initialAction).label + ".",
      );
    }
  }
  signal({ type, x = 0, y = 0, strength = 1 } = {}) {
    if (type === "pointer") {
      this.pointerTarget = {
        x: clamp(Number(x) || 0, -1, 1),
        y: clamp(Number(y) || 0, -1, 1),
        strength: clamp(Number(strength) || 0),
      };
      return true;
    }
    if (!Object.hasOwn(SIGNALS, type)) return false;
    this.pending.push({
      type,
      x: clamp(Number(x) || 0, -1, 1),
      y: clamp(Number(y) || 0, -1, 1),
      at: this.time,
    });
    this.pending = this.pending.slice(-6);
    this.lastSignal = this.time;
    return true;
  }
  perform(id) {
    if (!ACTION_MAP.has(id) || this.active) return false;
    this.start(id, "Prueba explícita de este gesto.");
    return true;
  }
  start(id, reason) {
    const action = ACTION_MAP.get(id);
    this.active = { action, start: this.time, reason };
    this.last.set(id, this.time);
    this.history.push({
      id,
      label: action.label,
      state: action.state,
      start: +this.time.toFixed(4),
      duration: action.duration,
      reason,
    });
    if (this.history.length > 128) this.history.shift();
  }
  choose() {
    this.pending = this.pending.filter((e) => this.time - e.at < 18);
    const available = (action) =>
      this.time - (this.last.get(action.id) ?? -1000) > action.cooldown &&
      this.history.at(-1)?.id !== action.id;
    if (this.needs.energy < 0.15 && available(ACTION_MAP.get("nap"))) {
      this.start(
        "nap",
        "La fatiga tiene prioridad: necesita recuperarse antes de seguir.",
      );
      return;
    }
    const priorities = {
      return: 100,
      surprise: 90,
      farewell: 70,
      greeting: 65,
    };
    const event = [...this.pending]
      .filter((e) =>
        SIGNALS[e.type].some((id) => available(ACTION_MAP.get(id))),
      )
      .sort(
        (a, b) =>
          (priorities[b.type] ?? 40) - (priorities[a.type] ?? 40) ||
          a.at - b.at,
      )[0];
    if (event) {
      const candidates = SIGNALS[event.type]
        .map((id) => ACTION_MAP.get(id))
        .filter(available);
      if (candidates.length) {
        let chosen;
        if (event.type === "attention") {
          const preferred =
            event.y < -0.5
              ? "look-up"
              : event.y > 0.5
                ? "inspect"
                : event.x < -0.3
                  ? "look-left"
                  : event.x > 0.3
                    ? "look-right"
                    : "scan";
          chosen = candidates.find((a) => a.id === preferred);
        }
        if (event.type === "quiet")
          chosen = candidates.find(
            (a) => a.id === (this.needs.energy < 0.5 ? "nap" : "sigh"),
          );
        chosen ??= candidates.sort(
          (a, b) =>
            (this.last.get(a.id) ?? -1000) - (this.last.get(b.id) ?? -1000),
        )[0];
        this.pending.splice(this.pending.indexOf(event), 1);
        this.start(
          chosen.id,
          `Señal «${event.type}»; gesto disponible y fuera de su descanso.`,
        );
        return;
      }
    }
    const n = this.needs;
    const scores = {
      nap: (0.42 - n.energy) * 5,
      drowsy: (0.64 - n.energy) * 3,
      stretch: n.strain * 1.5,
      sigh: n.strain * 1.3,
      scan: n.curiosity,
      inspect: n.curiosity * 0.8,
      "look-left": n.curiosity * 0.7,
      "look-right": n.curiosity * 0.7,
      "look-up": n.curiosity * 0.65,
      think: n.curiosity * 0.6,
      listen: n.social * 0.9,
      wink: n.social * 0.65,
      mischief: n.social * 0.65,
    };
    const ranked = ACTIONS.filter(available)
      .map((a) => ({
        a,
        score:
          (scores[a.id] ?? -1) +
          Math.min(0.12, (this.time - (this.last.get(a.id) ?? 0)) * 0.0008),
      }))
      .sort((a, b) => b.score - a.score);
    if (ranked[0]?.score > 0.58) {
      const { a } = ranked[0];
      this.start(
        a.id,
        `Prioridad interna: energía ${Math.round(n.energy * 100)}%, curiosidad ${Math.round(n.curiosity * 100)}%, atención social ${Math.round(n.social * 100)}%, esfuerzo ${Math.round(n.strain * 100)}%.`,
      );
    } else this.nextDecision = this.time + 1.2;
  }
  tick() {
    this.ticks++;
    this.time = this.ticks * STEP;
    const n = this.needs;
    n.energy = clamp(n.energy - STEP * 0.0025);
    n.curiosity = clamp(n.curiosity + STEP * 0.006);
    n.social = clamp(n.social + STEP * 0.003);
    n.strain = clamp(n.strain - STEP * 0.0008);
    this.pointerTarget.strength *= Math.exp(-STEP * 0.6);
    for (const key of ["x", "y", "strength"])
      this.pointer[key] +=
        (this.pointerTarget[key] - this.pointer[key]) *
        (1 - Math.exp(-STEP * 10));
    if (
      this.active &&
      this.time - this.active.start >= this.active.action.duration
    ) {
      const finished = this.active.action;
      for (const [key, value] of Object.entries(finished.effects))
        n[key] = clamp(n[key] + value);
      if (["focus", "think", "surprise"].includes(finished.id))
        this.blinkDrive = Math.max(this.blinkDrive, 0.85);
      this.active = null;
      this.nextDecision = this.time + 1.1 + Math.min(2, n.strain * 3);
      if (finished.id === "nap")
        this.pending.unshift({ type: "return", x: 0, y: 0, at: this.time });
    }
    if (!this.active && this.time >= this.nextDecision) this.choose();
    const age = this.active ? this.time - this.active.start : 0;
    const p = this.active ? poseAt(this.active.action, age) : NEUTRAL;
    const focused = this.active?.action.state === "concentrado";
    const startled = this.active?.action.id === "surprise" && age < 1.8;
    // Eye closure relieves the drive; fixation postpones blinking until attention relaxes.
    this.blinkDrive =
      p.lid > 0.75 ? 0 : this.blinkDrive + STEP * (0.23 + n.strain * 0.04);
    if (
      this.blinkDrive >= (focused ? 1.35 : 1) &&
      !startled &&
      p.lid < 0.2 &&
      p.wink < 0.1
    ) {
      this.blinkStart = this.time;
      this.lastBlink = this.time;
      this.blinkCount++;
      this.blinkDrive = 0;
    }
  }
  advance(seconds) {
    if (!Number.isFinite(seconds) || seconds < 0 || seconds > 60)
      throw new RangeError("advance admite entre 0 y 60 segundos.");
    this.accumulator += seconds;
    while (this.accumulator + 1e-9 >= STEP) {
      this.tick();
      this.accumulator -= STEP;
    }
    return this.snapshot();
  }
  snapshot() {
    const age = this.active ? this.time - this.active.start : 0;
    const p = this.active ? poseAt(this.active.action, age) : { ...NEUTRAL };
    const b = this.time - this.blinkStart;
    const blink =
      b < 0 || b > 0.29
        ? 0
        : b < 0.09
          ? smooth(b / 0.09)
          : b < 0.13
            ? 1
            : 1 - smooth((b - 0.13) / 0.16);
    p.lid = Math.max(p.lid, blink);
    const tracking =
      this.active?.action.state === "dormido" ? 0 : this.pointer.strength;
    p.gx = clamp(p.gx + this.pointer.x * tracking * 0.65, -1, 1);
    p.gy = clamp(p.gy + this.pointer.y * tracking * 0.65, -1, 1);
    p.roll += this.pointer.x * tracking * 1.3;
    // Small continuous breathing bridges the pauses without changing the face.
    p.y -= Math.sin((this.time * Math.PI * 2) / 5.6) * 0.045;
    p.scale += Math.sin((this.time * Math.PI * 2) / 5.6) * 0.003;
    return {
      time: this.time,
      pose: p,
      state: this.active?.action.state ?? "tranquilo",
      action: this.active?.action.id ?? "rest",
      label: this.active?.action.label ?? "Descansar sin perder la atención",
      reason:
        this.active?.reason ??
        "Pausa entre acciones; no hay una necesidad urgente.",
      needs: { ...this.needs },
      progress: this.active ? clamp(age / this.active.action.duration) : 0,
    };
  }
}

export const DEMO_DURATION = 180;
// A directed performance, not simulated mouse tracking. Decisions still respect recovery and cooldowns.
export const DEMO_CUES = Object.freeze([
  [7, { type: "attention", x: -1 }],
  [15, { type: "attention", y: 1 }],
  [25, { type: "thought" }],
  [37, { type: "agreement" }],
  [44, { type: "humor" }],
  [53, { type: "attention", y: -1 }],
  [62, { type: "doubt" }],
  [71, { type: "surprise" }],
  [79, { type: "humor" }],
  [89, { type: "thought" }],
  [101, { type: "agreement" }],
  [110, { type: "quiet" }],
  [122, { type: "attention", x: 1 }],
  [132, { type: "humor" }],
  [143, { type: "quiet" }],
  [161, { type: "return" }],
  [171, { type: "farewell" }],
]);

export function applyDemoCues(director, until, cursor = 0) {
  while (cursor < DEMO_CUES.length && DEMO_CUES[cursor][0] <= until + 1e-8) {
    director.signal(DEMO_CUES[cursor][1]);
    cursor++;
  }
  return cursor;
}

export const LAYERS = Object.freeze([
  "left",
  "right",
  "up",
  "down",
  "quarter",
  "half",
  "near",
  "closed",
  "wink-quarter",
  "wink-half",
  "wink-near",
  "wink-closed",
  "mouth-neutral",
  "mouth-think",
  "mouth-laugh",
  "mouth-surprise",
]);
export function layerWeights(pose) {
  const w = Object.fromEntries(LAYERS.map((layer) => [layer, 0]));
  const horizontal = Math.abs(pose.gx),
    vertical = Math.abs(pose.gy),
    total = Math.max(1, horizontal + vertical);
  w[pose.gx < 0 ? "left" : "right"] = horizontal / total;
  w[pose.gy < 0 ? "up" : "down"] = vertical / total;
  // Successive overlays are cumulative: the top frame becomes opaque, covering previous poses.
  for (const [i, layer] of ["quarter", "half", "near", "closed"].entries()) {
    w[layer] = clamp((pose.lid - i * 0.25) / 0.25);
    w["wink-" + layer] = clamp((pose.wink - i * 0.25) / 0.25);
  }
  for (const key of ["neutral", "think", "laugh", "surprise"])
    w["mouth-" + key] = pose[key];
  return w;
}

const renderers = new WeakMap();
export function renderPose(svg, pose) {
  if (!renderers.has(svg))
    renderers.set(svg, {
      head: svg.querySelector(".fox-head"),
      layers: [...svg.querySelectorAll("[data-fox-layer]")],
    });
  const { head, layers } = renderers.get(svg);
  head.setAttribute(
    "transform",
    `translate(${pose.x} ${pose.y}) rotate(${pose.roll} 0 6) translate(0 6) scale(${pose.scale}) translate(0 -6)`,
  );
  const weights = layerWeights(pose);
  for (const element of layers)
    element.style.opacity = weights[element.dataset.foxLayer] ?? 0;
}
