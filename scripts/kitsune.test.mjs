import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import { createHash } from "node:crypto";
import {
  ACTIONS,
  KitsuneDirector,
  DEMO_CUES,
  NEUTRAL,
  layerWeights,
} from "../assets/profile/identity/kitsune-3d/director.mjs";

function advance(director, seconds) {
  for (let i = 0; i < seconds * 60; i++) director.advance(1 / 60);
  return director;
}

test("the same cues produce the same decisions and poses at different frame rates", () => {
  function run(fps) {
    const d = new KitsuneDirector();
    let cue = 0;
    for (let frame = 0; frame < 180 * fps; frame++) {
      const until = (frame + 1) / fps;
      while (cue < DEMO_CUES.length && DEMO_CUES[cue][0] <= until + 1e-8)
        d.signal(DEMO_CUES[cue++][1]);
      d.advance(1 / fps);
    }
    return d;
  }
  const a = run(30),
    b = run(120);
  assert.deepEqual(a.history, b.history);
  assert.deepEqual(a.snapshot(), b.snapshot());
});

test("all 24 actions have a neutral entry/exit and finite bounded facial layers", () => {
  assert.equal(ACTIONS.length, 24);
  assert.equal(new Set(ACTIONS.map((a) => a.id)).size, ACTIONS.length);
  for (const action of ACTIONS) {
    for (const key of Object.keys(NEUTRAL)) {
      assert.equal(action.keys[0][key], NEUTRAL[key]);
      assert.equal(action.keys.at(-1)[key], NEUTRAL[key]);
    }
    const d = new KitsuneDirector({ initialAction: action.id });
    let previous = d.snapshot().pose;
    for (let frame = 0; frame < action.duration * 60; frame++) {
      const pose = d.advance(1 / 60).pose;
      for (const n of Object.values(pose)) assert.ok(Number.isFinite(n));
      for (const weight of Object.values(layerWeights(pose)))
        assert.ok(weight >= 0 && weight <= 1);
      assert.ok(
        Math.abs(pose.roll - previous.roll) < 0.7,
        action.id + " rotation must not snap",
      );
      assert.ok(
        Math.abs(pose.scale - previous.scale) < 0.008,
        action.id + " scale must not snap",
      );
      previous = pose;
    }
  }
});

test("signals wait for a coherent exit, queue is bounded, cooldown blocks repetition", () => {
  const d = new KitsuneDirector();
  for (let i = 0; i < 40; i++) d.signal({ type: "surprise" });
  assert.equal(d.pending.length, 6);
  advance(d, 2);
  assert.equal(d.snapshot().action, "greet");
  advance(d, 25);
  assert.equal(d.history.filter((a) => a.id === "surprise").length, 1);
  assert.ok(d.history[1].start >= 4.8);
});

test("fatigue wins, sleep restores energy and waking takes priority over queued interest", () => {
  const d = new KitsuneDirector({ initialAction: null });
  d.needs.energy = 0.08;
  advance(d, 1);
  assert.equal(d.snapshot().action, "nap");
  d.signal({ type: "attention", x: 1 });
  advance(d, 16);
  assert.equal(d.snapshot().action, "wake");
  assert.ok(d.needs.energy > 0.5);
});

test("an unavailable old cue cannot block a higher priority reaction", () => {
  const d = new KitsuneDirector({ initialAction: null });
  for (const id of ["look-left", "look-right", "look-up", "inspect", "scan"])
    d.last.set(id, 0);
  d.signal({ type: "attention", x: -1 });
  d.signal({ type: "thought" });
  d.signal({ type: "surprise" });
  d.advance(1 / 60);
  assert.equal(d.snapshot().action, "surprise");
  assert.ok(d.pending.some((event) => event.type === "thought"));
});

test("fixation postpones blinking and closed eyes relieve its drive", () => {
  const idle = advance(new KitsuneDirector({ initialAction: null }), 3);
  const focus = advance(new KitsuneDirector({ initialAction: "focus" }), 3);
  const nap = advance(new KitsuneDirector({ initialAction: "nap" }), 8);
  assert.equal(idle.blinkCount, 1);
  assert.equal(focus.blinkCount, 0);
  assert.equal(nap.blinkCount, 0);
  assert.equal(nap.blinkDrive, 0);
});

test("pointer attraction and release are smoothed and clamped", () => {
  const d = new KitsuneDirector({ initialAction: null });
  d.signal({ type: "pointer", x: 999, y: -999 });
  d.advance(1 / 60);
  assert.ok(d.pointer.x > 0 && d.pointer.x < 0.2);
  advance(d, 1);
  const before = d.pointer.strength;
  d.signal({ type: "pointer", strength: 0 });
  d.advance(1 / 60);
  assert.ok(d.pointer.strength > 0 && d.pointer.strength < before);
  advance(d, 2);
  assert.ok(d.pointer.strength < 0.00001);
});

test("long autonomous runs keep needs bounded and do not repeat adjacent actions", () => {
  const d = advance(new KitsuneDirector(), 1200);
  for (const value of Object.values(d.needs))
    assert.ok(value >= 0 && value <= 1);
  assert.ok(d.history.length > 20);
  for (let i = 1; i < d.history.length; i++)
    assert.notEqual(d.history[i].id, d.history[i - 1].id);
  assert.equal(d.signal({ type: "not-a-signal" }), false);
  assert.throws(() => d.advance(Infinity), RangeError);
});

test("README exports loop continuously, are self-contained, and preserve approved art", () => {
  const performance = JSON.parse(
    fs.readFileSync("assets/profile/identity/kitsune-3d/performance.json"),
  );
  assert.equal(performance.duration, 180);
  for (const [key, track] of Object.entries(performance.tracks))
    assert.equal(track[0][1], track.at(-1)[1], key);
  const checksums = JSON.parse(
    fs.readFileSync("assets/profile/identity/kitsune-3d/approved-art.json"),
  );
  for (const [file, hash] of Object.entries(checksums))
    assert.equal(
      createHash("sha256").update(fs.readFileSync(file)).digest("hex"),
      hash,
      file,
    );
  for (const theme of ["light", "dark"])
    for (const mobile of ["", "-mobile"]) {
      const svg = fs.readFileSync(
        `assets/profile/header${mobile}-${theme}.svg`,
        "utf8",
      );
      assert.ok(!svg.includes("<script"));
      assert.ok(!svg.includes("kitsune-divine"));
      assert.ok(!/href="https?:/.test(svg));
      assert.ok(Buffer.byteLength(svg) < 900_000);
      const base = svg.match(
        /<image[^>]+href="data:image\/webp;base64,([^"]+)"/,
      )[1];
      assert.equal(
        createHash("sha256").update(Buffer.from(base, "base64")).digest("hex"),
        checksums["assets/profile/identity/kitsune-3d/open.webp"],
      );
    }
});
