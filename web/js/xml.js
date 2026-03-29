import { format4g } from "./calculator.js";

export function buildXml(config, structure) {
  const lines = [];
  lines.push("<?xml version='1.0' encoding='UTF-8'?>");
  lines.push("<ThreadType>");
  lines.push(`  <Name>${escapeXml(config.threadName)}</Name>`);
  lines.push(`  <CustomName>${escapeXml(config.threadName)}</CustomName>`);
  lines.push(`  <Unit>${escapeXml(config.unit)}</Unit>`);
  lines.push(`  <Angle>${escapeXml(String(config.threadAngle))}</Angle>`);
  lines.push(`  <ThreadForm>${escapeXml(String(config.threadForm))}</ThreadForm>`);
  lines.push("  <SortOrder>3</SortOrder>");

  for (const sizeItem of structure.model) {
    lines.push("  <ThreadSize>");
    lines.push(`    <Size>${sizeItem.size}</Size>`);

    for (const designation of sizeItem.designations) {
      lines.push("    <Designation>");
      lines.push(`      <ThreadDesignation>${escapeXml(designation.name)}</ThreadDesignation>`);
      lines.push(`      <CTD>${escapeXml(designation.name)}</CTD>`);
      lines.push(`      <Pitch>${designation.pitch}</Pitch>`);

      for (const thread of designation.threads) {
        lines.push("      <Thread>");
        lines.push(`        <Gender>${thread.gender}</Gender>`);
        lines.push(`        <Class>${thread.clazz}</Class>`);
        lines.push(`        <MajorDia>${format4g(thread.majorDia)}</MajorDia>`);
        lines.push(`        <PitchDia>${format4g(thread.pitchDia)}</PitchDia>`);
        lines.push(`        <MinorDia>${format4g(thread.minorDia)}</MinorDia>`);
        if (thread.tapDrill != null) {
          lines.push(`        <TapDrill>${format4g(thread.tapDrill)}</TapDrill>`);
        }
        lines.push("      </Thread>");
      }

      lines.push("    </Designation>");
    }

    lines.push("  </ThreadSize>");
  }

  lines.push("</ThreadType>");
  return lines.join("\n");
}

export function downloadTextFile(filename, text) {
  const blob = new Blob([text], { type: "application/xml;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

function escapeXml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}
