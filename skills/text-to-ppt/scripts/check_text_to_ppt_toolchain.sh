#!/usr/bin/env bash
set -u

if command -v node >/dev/null 2>&1; then
  printf 'ok: node -> %s\n' "$(command -v node)"
else
  echo 'missing: node'
fi

node - <<'JS'
try {
  require("pptxgenjs");
  console.log("ok: pptxgenjs");
} catch (error) {
  const path = require("path");
  if (process.env.NODE_PATH) {
    try {
      require(path.join(process.env.NODE_PATH, "pptxgenjs"));
      console.log("ok: pptxgenjs via NODE_PATH");
      process.exit(0);
    } catch (_) {}
  }
  console.log(`missing: pptxgenjs (${error.message})`);
}
JS
