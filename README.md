# CustomThreads - 3D-Printed Metric Threads Generator

Generate standardized ISO metric thread profiles optimized for 3D printing in XML format.

## Quick Start

### Use the Web Generator

The browser generator is in [web/index.html](web/index.html) and is deployed through GitHub Pages.

- Live URL: [https://eckphi.github.io/CustomThreads/](https://eckphi.github.io/CustomThreads/)

- Local preview:

```bash
cd web
python3 -m http.server 8080
```

- Open `http://localhost:8080`
- Generate and download `3DPrintedMetricThreads.xml`
- Use Copy Share Link to share a prefilled generator configuration via URL

### Download Pre-Generated XML Files

The latest XML thread profiles are automatically generated and available as GitHub Releases:

👉 **[Download Latest Release](../../releases/latest)**

Simply download the `3DPrintedMetricThreads.xml` file and follow the installation instructions below.

### Install in Fusion 360

1. Download `3DPrintedMetricThreads.xml` from the latest release
2. Save it to your Fusion 360 thread data directory:
	 - **Windows:** `%localappdata%\Autodesk\webdeploy\Production\<version>\Fusion\Server\Fusion\Configuration\ThreadData`
	 - **macOS:** `~/Library/Application Support/Autodesk/Webdeploy/production/<version>/Autodesk Fusion 360/Contents/Libraries/Applications/Fusion/Fusion/Server/Fusion/Configuration/ThreadData`
3. Restart Fusion 360
4. When creating threads, select **"3D-Printed Metric Threads V3"** from the thread type dropdown

> **Note:** You can automate this installation with the [ThreadKeeper](https://github.com/thomasa88/ThreadKeeper) plugin, which reinstalls profiles automatically after each Fusion 360 update.

## Project Structure

```
.
├── .github/workflows/          # CI/CD pipeline
│   ├── generate-xml-release.yml
│   └── deploy-pages.yml
├── src/customthreads/          # Python package (core logic)
│   ├── __init__.py
│   ├── models.py               # Thread model classes
│   ├── generator.py            # XML generation utilities
│   └── cli.py                  # Command-line interface
├── tests/                      # Test suite
│   └── test_main.py
├── web/                        # GitHub Pages generator app
├── pyproject.toml              # Poetry configuration
├── README.md
└── .gitignore
```

## Development

### Installation

Install dependencies with Poetry:

```bash
poetry install
```

### Generate XML Locally

Run the thread generator:

```bash
poetry run python -m customthreads.cli
```

This creates `3DPrintedMetricThreads.xml` with:
- **Diameters:** 8-50mm
- **Pitches:** 1.0mm to 6.0mm (0.5mm steps)
- **Tolerance Classes:** O.0, O.1, O.2, O.4, O.8

### Customize Configuration

Edit `src/customthreads/cli.py` to customize parameters:
- Pitch range (pitch_start, pitch_end, pitch_step)
- Thread sizes (thread_sizes)
- Tolerance offsets (tolerance_offsets)
- Output filename (output_filename)
- Thread metadata (thread_name, unit, thread_angle, thread_form)

### Run Tests

```bash
poetry run pytest -v
```

All 12 tests should pass ✓

### Use as a Library

```python
from customthreads import generate_xml

# Generate custom thread profiles
generate_xml(
		output_filename="custom_threads.xml",
		thread_name="My Custom Threads",
		unit="mm",
		thread_angle=60.0,
		thread_form=8,
		pitch_start=1.0,
		pitch_end=6.0,
		pitch_step=0.5,
		thread_sizes=list(range(8, 51)),
		tolerance_offsets=[0.0, 0.1, 0.2, 0.4, 0.8],
)
```

## Automated Release Pipeline

### How It Works

This project uses **GitHub Actions** to automatically generate and publish thread profiles as releases.

**Workflow File:** `.github/workflows/generate-xml-release.yml`

**Trigger Events:**
- ✅ Every push to `master` branch
- ✅ Manual trigger via GitHub Actions UI (workflow_dispatch)

**Pipeline Steps:**
1. Set up Ubuntu environment with Python 3.11
2. Install dependencies using Poetry
3. Run test suite to verify code quality
4. Generate XML thread profiles
5. Create a GitHub Release with datetime-based version
6. Upload XML file as release artifact

### Release Versioning

- **Format:** `v{YYYY}.{MM}.{DD}-{HHMMSS}-r{RUN_NUMBER}` (UTC time + workflow run number)
- **Examples:** 
	- `v2026.03.29-100000-r5` = March 29, 2026 at 10:00:00 UTC, run 5
	- `v2026.03.29-124530-r9` = March 29, 2026 at 12:45:30 UTC, run 9

### Key Features

- ✅ **No committed XML files** — generated automatically on every push
- ✅ **Version history** — easy to compare profiles across releases
- ✅ **Quality assured** — tests run before each release
- ✅ **One-click downloads** — users get latest profiles from Releases page

### Disable Auto-Release (Optional)

To switch to manual-only releases:

1. Edit `.github/workflows/generate-xml-release.yml`
2. Change the trigger to:
	 ```yaml
	 on:
		 workflow_dispatch:  # Manual trigger only
	 ```
3. Commit and push
4. Releases can now be triggered manually from the Actions tab

## Thread Specifications

### Tolerance Classes

These offset values from nominal dimensions allow fine-tuning for different printing conditions:

| Class | Offset | Use Case |
|-------|--------|----------|
| O.0 | 0.0mm | Tightest fit, best accuracy |
| O.1 | +0.1mm | Standard fit, most prints |
| O.2 | +0.2mm | Loose fit, easier to print |
| O.4 | +0.4mm | Very loose, coarse prints |
| O.8 | +0.8mm | Safety margin, worst-case prints |

### Generated Profile Range

| Parameter | Value |
|-----------|-------|
| **Diameters** | 8-50mm (all integer values) |
| **Pitches** | 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0mm |
| **Thread Type** | ISO Metric (60° flank angle) |
| **Optimized for** | FDM 3D printing (0.2-0.3mm layer height) |

## GitHub Pages Deployment

The web app is deployed by [.github/workflows/deploy-pages.yml](.github/workflows/deploy-pages.yml).

- Trigger: push to `master` when files under [web](web) change
- Source artifact: [web](web)
- Publish target: GitHub Pages environment

If Pages is not enabled yet in repository settings, enable it once and keep source as GitHub Actions.

## License

See LICENSE file for details

## References

- [Fusion 360 Custom Threads Documentation](https://knowledge.autodesk.com/support/fusion-360/learn-explore/caas/sfdcarticles/sfdcarticles/Custom-Threads-in-Fusion-360.html)
- [ISO Metric Screw Thread (Wikipedia)](https://en.wikipedia.org/wiki/ISO_metric_screw_thread)
- [ThreadKeeper - Fusion 360 Plugin](https://github.com/thomasa88/ThreadKeeper)
