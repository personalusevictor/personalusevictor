import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  KitsuneDirector,
  NEUTRAL,
  LAYERS,
  layerWeights,
  applyDemoCues,
  DEMO_DURATION,
} from "../assets/profile/identity/kitsune-3d/director.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const director = new KitsuneDirector();
const samples = [];
let cursor = 0;
for (let index = 0; index <= DEMO_DURATION * 30; index++) {
  const time = index / 30;
  cursor = applyDemoCues(director, time, cursor);
  if (index) director.advance(1 / 30);
  const { pose } = director.snapshot();
  // A quiet neutral tail makes the exported loop continuous, including all expression layers.
  const fade = Math.max(0, Math.min(1, (DEMO_DURATION - time) / 2));
  for (const key of Object.keys(pose))
    pose[key] = NEUTRAL[key] + (pose[key] - NEUTRAL[key]) * fade;
  samples.push({ time, pose, weights: layerWeights(pose) });
}

function simplify(points, tolerance) {
  if (points.length <= 2) return points;
  const keep = new Set([0, points.length - 1]);
  const stack = [[0, points.length - 1]];
  while (stack.length) {
    const [a, b] = stack.pop();
    let largest = tolerance,
      index = -1;
    for (let i = a + 1; i < b; i++) {
      const ratio =
        (points[i][0] - points[a][0]) / (points[b][0] - points[a][0]);
      const error = Math.abs(
        points[i][1] - (points[a][1] + (points[b][1] - points[a][1]) * ratio),
      );
      if (error > largest) {
        largest = error;
        index = i;
      }
    }
    if (index !== -1) {
      keep.add(index);
      stack.push([a, index], [index, b]);
    }
  }
  return [...keep].sort((a, b) => a - b).map((i) => points[i]);
}

const tracks = {};
for (const key of ["x", "y", "roll", "scale"]) {
  tracks[key] = simplify(
    samples.map((s) => [s.time, s.pose[key]]),
    key === "scale" ? 0.0004 : key === "roll" ? 0.025 : 0.006,
  );
}
for (const key of LAYERS)
  tracks[key] = simplify(
    samples.map((s) => [s.time, s.weights[key]]),
    0.018,
  );
const performance = {
  version: 1,
  duration: DEMO_DURATION,
  fps: 30,
  actions: director.history,
  tracks,
};
fs.writeFileSync(
  path.join(root, "assets/profile/identity/kitsune-3d/performance.json"),
  JSON.stringify(performance),
);
console.log(
  `Actuación: ${performance.actions.length} acciones, ${Object.values(tracks).reduce((n, t) => n + t.length, 0)} claves, ${DEMO_DURATION}s.`,
);
