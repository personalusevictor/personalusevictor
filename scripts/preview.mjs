import fs from "node:fs";
import path from "node:path";
import http from "node:http";
import { fileURLToPath } from "node:url";
import { marked } from "marked";
import { buildMotionPreview } from "./motion_preview.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "preview");
fs.mkdirSync(output, { recursive: true });
const markdown = fs.readFileSync(path.join(root, "README.md"), "utf8");
marked.use({renderer: {heading({tokens, depth}) {
  const label = this.parser.parseInline(tokens);
  const id = label.replace(/<img\b[^>]*alt="([^"]*)"[^>]*>/g, "$1").replace(/<[^>]*>/g, "").toLowerCase().replace(/[^\p{L}\p{N}\s-]/gu, "").replace(/\s+/g, "-");
  return `<h${depth} id="${id}">${label}</h${depth}>`;
}}});

for (const theme of ["light", "dark"]) {
  const css = fs.readFileSync(
    path.join(
      root,
      `node_modules/github-markdown-css/github-markdown-${theme}.css`,
    ),
    "utf8",
  );
  // Lock the artwork to the preview theme; the delivered README uses GitHub's own theme selection.
  const body = marked
    .parse(markdown)
    .replaceAll('src="assets/', 'src="../assets/')
    .replaceAll('srcset="assets/', 'srcset="../assets/')
    .replace(
      /srcset="([^\"]+)-(light|dark)\.svg"/g,
      (_, stem) => `srcset="${stem}-${theme}.svg"`,
    );
  const html = `<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>personalusevictor — ${theme === "light" ? "Claro" : "Oscuro"}</title><style>
${css}
html,body{margin:0;padding:0;background:${theme === "light" ? "#ffffff" : "#0d1117"};color-scheme:${theme}}
.preview-controls{box-sizing:border-box;max-width:960px;margin:20px auto 0;padding:0 24px;font:13px/1.6 system-ui;color:${theme === "light" ? "#646a78" : "#a6acbd"}}
.preview-controls a{color:inherit;text-underline-offset:3px}.preview-controls span{margin-right:16px}
.profile-preview{box-sizing:border-box;max-width:960px;padding:30px;margin:18px auto 35px;border:1px solid ${theme === "light" ? "#d1d9e0" : "#3d444d"};border-radius:8px}
@media(max-width:650px){.profile-preview{padding:16px;margin:10px 0 0;border:0}.preview-controls{padding:0 16px;font-size:12px}.markdown-body{font-size:14px}}
</style></head><body><nav class="preview-controls" aria-label="Vista previa"><span>README · Vista local</span><a href="light.html">Claro</a> · <a href="dark.html">Oscuro</a></nav><main class="profile-preview markdown-body">${body}</main></body></html>`;
  fs.writeFileSync(path.join(output, `${theme}.html`), html);
}
buildMotionPreview(root, output);
console.log("Vistas generadas: README claro, oscuro y motion.html.");

if (process.argv.includes("--serve")) {
  const port = Number(process.env.PROFILE_PREVIEW_PORT || 8769);
  const types = {
    ".html": "text/html; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".md": "text/plain; charset=utf-8",
    ".mjs": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".webp": "image/webp",
  };
  http
    .createServer((request, response) => {
      try {
        const pathname = decodeURIComponent(
          new URL(request.url, "http://localhost").pathname,
        );
        const target = path.resolve(
          root,
          "." + (pathname === "/" ? "/preview/dark.html" : pathname),
        );
        if (
          !target.startsWith(root + path.sep) ||
          pathname.split("/").some((part) => part.startsWith("."))
        ) {
          response.writeHead(403).end("Forbidden");
          return;
        }
        const contents = fs.readFileSync(target);
        response.writeHead(200, {
          "Content-Type":
            types[path.extname(target)] || "application/octet-stream",
          "Cache-Control": "no-store",
        });
        response.end(contents);
      } catch {
        response.writeHead(404).end("Not found");
      }
    })
    .listen(port, "127.0.0.1", () =>
      console.log(`http://127.0.0.1:${port}/preview/dark.html`),
    );
}
