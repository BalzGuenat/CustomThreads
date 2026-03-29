export function generatePitchList(start, end, step) {
  const pitches = [];
  let current = start;

  while (current <= end + 1e-9) {
    pitches.push(roundTo(current, 4));
    current += step;
  }

  return pitches;
}

export function formatNumber(value) {
  return Number.isInteger(value) ? String(value) : String(value);
}

export function format4g(value) {
  return parseFloat(Number(value).toPrecision(4)).toString();
}

export function createThreadSizes(minSize, maxSize) {
  const sizes = [];
  for (let size = minSize; size <= maxSize; size += 1) {
    sizes.push(size);
  }
  return sizes;
}

export function createModel(config) {
  const pitches = generatePitchList(config.pitchStart, config.pitchEnd, config.pitchStep);
  const model = [];

  for (const size of config.threadSizes) {
    const designations = [];
    for (const pitch of pitches) {
      const designation = {
        nominalDiameter: size,
        pitch,
        name: `M${formatNumber(size)}x${formatNumber(pitch)}`,
        threads: calculateThreads(size, pitch, config.threadAngle, config.toleranceOffsets),
      };
      designations.push(designation);
    }

    model.push({
      size,
      designations,
    });
  }

  return { pitches, model };
}

export function calculateSummary(structure) {
  const sizeCount = structure.model.length;
  const designationCount = structure.model.reduce((sum, item) => sum + item.designations.length, 0);
  const threadCount = structure.model.reduce(
    (sum, item) =>
      sum + item.designations.reduce((inner, des) => inner + des.threads.length, 0),
    0
  );

  return { sizeCount, designationCount, threadCount };
}

function calculateThreads(diameter, pitch, threadAngle, toleranceOffsets) {
  const threads = [];

  const h = (1 / Math.tan(toRadians(threadAngle / 2))) * (pitch / 2);
  const pitchDiaBase = diameter - 2 * ((3 * h) / 8);
  const minorDiaBase = diameter - 2 * ((5 * h) / 8);

  for (const offset of toleranceOffsets) {
    const classLabel = `O.${String(offset).split(".")[1] ?? "0"}`;

    threads.push({
      gender: "external",
      clazz: classLabel,
      majorDia: diameter - offset,
      pitchDia: pitchDiaBase - offset,
      minorDia: minorDiaBase - offset,
      tapDrill: null,
    });

    threads.push({
      gender: "internal",
      clazz: classLabel,
      majorDia: diameter + offset,
      pitchDia: pitchDiaBase + offset,
      minorDia: minorDiaBase + offset,
      tapDrill: diameter - pitch,
    });
  }

  return threads;
}

function toRadians(value) {
  return (Math.PI / 180) * value;
}

function roundTo(value, places) {
  const scale = 10 ** places;
  return Math.round(value * scale) / scale;
}
