import {
  KitsuneDirector,
  ACTIONS,
  DEMO_DURATION,
  applyDemoCues,
  renderPose,
} from "./director.mjs";

const $ = (id) => document.getElementById(id);
const svg = document.querySelector(".stage svg");
const stage = document.querySelector(".stage");
const reduced = matchMedia("(prefers-reduced-motion:reduce)");
let director = new KitsuneDirector(),
  cursor = 0,
  mode = "score",
  paused = false,
  slow = false,
  last = 0,
  readoutAt = -1,
  historyCount = -1;
for (const action of ACTIONS) {
  const option = document.createElement("option");
  option.value = action.id;
  option.textContent = action.label;
  $("gesture").append(option);
}
const stamp = (t) =>
  String(Math.floor(t / 60)).padStart(2, "0") +
  ":" +
  String(Math.floor(t % 60)).padStart(2, "0");

function refresh(force = false) {
  const snapshot = director.snapshot();
  if (!reduced.matches) renderPose(svg, snapshot.pose);
  if (!force && snapshot.time - readoutAt < 0.12) return;
  readoutAt = snapshot.time;
  $("action").textContent = snapshot.label;
  $("reason").textContent = snapshot.reason;
  $("time").textContent = stamp(snapshot.time);
  $("timeline").max =
    mode === "audition"
      ? ACTIONS.find((a) => a.id === $("gesture").value).duration
      : 179.9;
  $("timeline").value = Math.min(Number($("timeline").max), snapshot.time);
  $("timeline").disabled = mode === "free" || reduced.matches;
  $("mode").textContent =
    mode === "score"
      ? "Actuación del README · 3 minutos"
      : mode === "audition"
        ? "Prueba de un comportamiento"
        : "Director autónomo · " + snapshot.state;
  for (const [key, value] of Object.entries(snapshot.needs)) {
    $(key).value = value;
    $(key + "-value").textContent = Math.round(value * 100) + "%";
  }
  if (historyCount !== director.history.length || force) {
    historyCount = director.history.length;
    $("history").replaceChildren(
      ...director.history.slice(-6).map((event) => {
        const li = document.createElement("li");
        li.textContent =
          stamp(event.start) + " · " + event.label + " — " + event.reason;
        return li;
      }),
    );
  }
}
function buttons() {
  $("pause").textContent = paused ? "Reanudar" : "Pausar";
  $("pause").setAttribute("aria-pressed", paused);
  $("slow").setAttribute("aria-pressed", slow);
  $("autonomous").setAttribute("aria-pressed", mode === "free");
}
function reset(initialAction = "greet") {
  director = new KitsuneDirector({ initialAction });
  cursor = 0;
  last = 0;
  readoutAt = -1;
  historyCount = -1;
  paused = false;
  buttons();
  refresh(true);
}
function seek(time) {
  const audition = mode === "audition";
  mode = audition ? "audition" : "score";
  reset(audition ? $("gesture").value : "greet");
  for (let tick = 0; tick < Math.floor(time * 60); tick++) {
    if (!audition)
      cursor = applyDemoCues(director, director.time + 1 / 60, cursor);
    director.advance(1 / 60);
  }
  paused = true;
  buttons();
  refresh(true);
}
$("pause").onclick = () => {
  paused = !paused;
  last = 0;
  buttons();
};
$("slow").onclick = () => {
  slow = !slow;
  buttons();
};
$("restart").onclick = () => {
  mode = "score";
  reset();
};
$("autonomous").onclick = () => {
  mode = "free";
  director.pending = [];
  buttons();
  refresh(true);
};
$("timeline").addEventListener("input", (event) =>
  seek(Number(event.target.value)),
);
$("audition").onclick = () => {
  mode = "audition";
  reset($("gesture").value);
};
$("signals").addEventListener("click", (event) => {
  const button = event.target.closest("button[data-signal]");
  if (!button) return;
  if (mode === "score") {
    mode = "free";
    director.pending = [];
  }
  director.signal({
    type: button.dataset.signal,
    x: Number(button.dataset.x || 0),
    y: Number(button.dataset.y || 0),
  });
  paused = false;
  buttons();
  refresh(true);
});
stage.addEventListener("pointermove", (event) => {
  if (reduced.matches || mode === "score" || mode === "audition") return;
  const box = stage.getBoundingClientRect();
  director.signal({
    type: "pointer",
    x: ((event.clientX - box.left) / box.width) * 2 - 1,
    y: ((event.clientY - box.top) / box.height) * 2 - 1,
  });
});
stage.addEventListener("pointerleave", () =>
  director.signal({ type: "pointer", strength: 0 }),
);
function accessibility() {
  for (const element of document.querySelectorAll("button,select,input"))
    element.disabled = reduced.matches;
  if (reduced.matches) {
    paused = true;
    svg.querySelector(".fox-head").removeAttribute("transform");
    for (const el of svg.querySelectorAll("[data-fox-layer]"))
      el.style.opacity = 0;
  } else {
    paused = false;
  }
  last = 0;
  buttons();
  refresh(true);
}
reduced.addEventListener("change", accessibility);
accessibility();
document.addEventListener("visibilitychange", () => {
  last = 0;
});
function loop(now) {
  if (!document.hidden && !paused && !reduced.matches) {
    const elapsed = last
      ? Math.min(0.1, (now - last) / 1000) * (slow ? 0.22 : 1)
      : 0;
    const steps = Math.max(1, Math.ceil(elapsed * 60));
    for (let step = 0; step < steps; step++) {
      if (mode === "score")
        cursor = applyDemoCues(
          director,
          director.time + elapsed / steps,
          cursor,
        );
      director.advance(elapsed / steps);
      if (mode === "score" && director.time >= DEMO_DURATION) {
        reset();
        break;
      }
    }
    refresh();
  }
  last = now;
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
