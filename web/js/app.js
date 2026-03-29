import { calculateSummary, createModel, createThreadSizes } from "./calculator.js";
import { buildXml, downloadTextFile } from "./xml.js";

const form = document.querySelector("#config-form");
const errorsEl = document.querySelector("#errors");
const summaryEl = document.querySelector("#summary");
const previewEl = document.querySelector("#xmlPreview");
const downloadBtn = document.querySelector("#downloadBtn");
const shareBtn = document.querySelector("#shareBtn");

let generated = null;

hydrateFormFromUrl();

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const parseResult = parseConfig(form);

  if (!parseResult.ok) {
    renderErrors(parseResult.errors);
    return;
  }

  const config = parseResult.config;
  const structure = createModel(config);
  const xml = buildXml(config, structure);
  const summary = calculateSummary(structure);

  generated = {
    filename: config.filename,
    xml,
    summary,
    firstDesignation: structure.model[0]?.designations[0]?.name ?? "n/a",
    lastDesignation:
      structure.model[structure.model.length - 1]?.designations[
        structure.model[structure.model.length - 1]?.designations.length - 1
      ]?.name ?? "n/a",
  };

  renderErrors([]);
  renderOutput(generated);
  writeUrlFromConfig(config);
  downloadBtn.disabled = false;
});

downloadBtn.addEventListener("click", () => {
  if (!generated) {
    return;
  }
  downloadTextFile(generated.filename, generated.xml);
});

shareBtn.addEventListener("click", async () => {
  const parseResult = parseConfig(form);
  if (!parseResult.ok) {
    renderErrors(parseResult.errors);
    return;
  }

  writeUrlFromConfig(parseResult.config);
  const shareUrl = window.location.href;

  try {
    await navigator.clipboard.writeText(shareUrl);
    renderOutput(generated, "Share link copied to clipboard.");
  } catch {
    window.prompt("Copy this share URL:", shareUrl);
  }
});

function parseConfig(formElement) {
  const values = new FormData(formElement);
  const errors = [];

  const pitchStart = parseFloat(values.get("pitchStart"));
  const pitchEnd = parseFloat(values.get("pitchEnd"));
  const pitchStep = parseFloat(values.get("pitchStep"));
  const sizeMin = parseInt(values.get("sizeMin"), 10);
  const sizeMax = parseInt(values.get("sizeMax"), 10);
  const threadAngle = parseFloat(values.get("angle"));
  const threadForm = parseInt(values.get("threadForm"), 10);
  const offsetsRaw = String(values.get("offsets") ?? "");

  if (!(pitchStep > 0)) {
    errors.push("Pitch step must be greater than 0.");
  }

  if (!(pitchEnd >= pitchStart)) {
    errors.push("Pitch end must be greater than or equal to pitch start.");
  }

  if (!(sizeMin > 0 && sizeMax >= sizeMin)) {
    errors.push("Diameter range is invalid. Ensure max >= min and both are positive.");
  }

  if (!(threadAngle > 0)) {
    errors.push("Thread angle must be greater than 0.");
  }

  const toleranceOffsets = offsetsRaw
    .split(",")
    .map((part) => part.trim())
    .filter(Boolean)
    .map((part) => Number(part));

  if (toleranceOffsets.length === 0 || toleranceOffsets.some((value) => Number.isNaN(value))) {
    errors.push("Tolerance offsets must be comma-separated numeric values.");
  }

  if (errors.length > 0) {
    return { ok: false, errors };
  }

  return {
    ok: true,
    config: {
      threadName: String(values.get("threadName") ?? "3D-Printed Metric Threads V3"),
      unit: String(values.get("unit") ?? "mm"),
      filename: ensureXmlFilename(String(values.get("filename") ?? "3DPrintedMetricThreads.xml")),
      threadAngle,
      threadForm,
      pitchStart,
      pitchEnd,
      pitchStep,
      threadSizes: createThreadSizes(sizeMin, sizeMax),
      toleranceOffsets,
    },
  };
}

function renderErrors(errors) {
  errorsEl.innerHTML = "";
  if (errors.length === 0) {
    return;
  }

  for (const error of errors) {
    const item = document.createElement("li");
    item.textContent = error;
    errorsEl.appendChild(item);
  }

  summaryEl.textContent = "Fix the validation errors to generate XML.";
  summaryEl.className = "summary";
  previewEl.textContent = "";
  downloadBtn.disabled = true;
}

function renderOutput(result, notice = "") {
  summaryEl.className = "summary ok";
  const lines = [
    `<strong>Generated:</strong> ${result.filename}`,
    `<strong>Thread Sizes:</strong> ${result.summary.sizeCount}`,
    `<strong>Designations:</strong> ${result.summary.designationCount}`,
    `<strong>Thread Nodes:</strong> ${result.summary.threadCount}`,
    `<strong>Range:</strong> ${result.firstDesignation} to ${result.lastDesignation}`,
  ];

  if (notice) {
    lines.push(`<strong>${notice}</strong>`);
  }

  summaryEl.innerHTML = lines.join("<br>");

  const previewLines = result.xml.split("\n").slice(0, 80).join("\n");
  previewEl.textContent = previewLines;
}

function ensureXmlFilename(filename) {
  const clean = filename.trim() || "3DPrintedMetricThreads.xml";
  return clean.toLowerCase().endsWith(".xml") ? clean : `${clean}.xml`;
}

function hydrateFormFromUrl() {
  const params = new URLSearchParams(window.location.search);
  if (params.size === 0) {
    return;
  }

  setIfPresent("threadName", params.get("threadName"));
  setIfPresent("pitchStart", params.get("pitchStart"));
  setIfPresent("pitchEnd", params.get("pitchEnd"));
  setIfPresent("pitchStep", params.get("pitchStep"));
  setIfPresent("sizeMin", params.get("sizeMin"));
  setIfPresent("sizeMax", params.get("sizeMax"));
  setIfPresent("offsets", params.get("offsets"));
  setIfPresent("unit", params.get("unit"));
  setIfPresent("angle", params.get("angle"));
  setIfPresent("threadForm", params.get("threadForm"));
  setIfPresent("filename", params.get("filename"));
}

function setIfPresent(fieldName, value) {
  if (value === null) {
    return;
  }
  const field = form.querySelector(`[name="${fieldName}"]`);
  if (field) {
    field.value = value;
  }
}

function writeUrlFromConfig(config) {
  const url = new URL(window.location.href);
  url.searchParams.set("threadName", config.threadName);
  url.searchParams.set("pitchStart", String(config.pitchStart));
  url.searchParams.set("pitchEnd", String(config.pitchEnd));
  url.searchParams.set("pitchStep", String(config.pitchStep));
  url.searchParams.set("sizeMin", String(config.threadSizes[0]));
  url.searchParams.set("sizeMax", String(config.threadSizes[config.threadSizes.length - 1]));
  url.searchParams.set("offsets", config.toleranceOffsets.join(","));
  url.searchParams.set("unit", config.unit);
  url.searchParams.set("angle", String(config.threadAngle));
  url.searchParams.set("threadForm", String(config.threadForm));
  url.searchParams.set("filename", config.filename);
  window.history.replaceState({}, "", url);
}
