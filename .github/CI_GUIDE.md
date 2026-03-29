# CI/CD Pipeline Documentation

This document explains the GitHub Actions workflow for automatically generating and releasing XML thread profiles.

## Overview

The automated pipeline ensures that:
1. ✅ XML files are **never committed** to the repository
2. ✅ Every push to `master` triggers a new release
3. ✅ Tests run before each release to ensure quality
4. ✅ Releases are timestamped with UTC datetime
5. ✅ Users always have access to the latest profiles

## Workflow Details

**File:** `.github/workflows/generate-xml-release.yml`

### Trigger Events

The workflow runs on:

```yaml
on:
  push:
    branches:
      - master        # Automatic on every push to master
  workflow_dispatch:  # Manual trigger via GitHub UI
```

### Pipeline Stages

#### 1. Setup (automatic)
- Checkout repository
- Install Python 3.11
- Install Poetry
- Cache dependencies

#### 2. Generate (automatic)
- Generate XML files using `poetry run python -m customthreads.cli`
- Place artifacts in `build/xml/` directory

#### 3. Verify (automatic)
- Run all tests to verify code quality
- Validate generated XML structure

#### 4. Release (automatic)
- Create Git tag with datetime format: `v{YYYY}.{MM}.{DD}-{HHMMSS}-r{RUN_NUMBER}`
- Create GitHub Release with metadata
- Upload XML file as downloadable artifact

### Versioning Scheme

Release versions use **calendar versioning with second precision + run number**:

```
v2026.03.29-124530-r42
 └─ 2026: Year
    └─ 03: Month (March)
       └─ 29: Day
       └─ 124530: Time in UTC (12:45:30 UTC)
         └─ r42: GitHub Actions run number
```

**Advantages:**
- Easy to see when profiles were generated
- No manual version management needed
- Chronological ordering in release history
- Preserves full timestamp accuracy

**Examples:**
- `v2026.03.29-000000-r7` = March 29, 2026 at midnight UTC, run 7
- `v2026.03.29-120000-r12` = March 29, 2026 at noon UTC, run 12
- `v2026.12.31-235959-r128` = December 31, 2026 at 23:59:59 UTC, run 128

## Using Releases

### Download Options

1. **GitHub UI (Recommended)**
   - Visit Repository → Releases page
   - Click on latest release
   - Download `3DPrintedMetricThreads.xml`

2. **Command Line**
   ```bash
   # Get latest release URL
   curl -s https://api.github.com/repos/USERNAME/REPO/releases/latest | \
     grep "browser_download_url" | \
     grep ".xml" | \
     cut -d '"' -f 4 | \
     xargs wget -O
   ```

3. **Direct URL (latest)**
   ```
   https://github.com/USERNAME/REPO/releases/latest/download/3DPrintedMetricThreads.xml
   ```

### Installation

After downloading, place the XML file in your Fusion 360 thread data directory (see README.md for paths).

## Customizing the Workflow

### Change Release Trigger

To manually trigger releases instead of automatic:

Edit `.github/workflows/generate-xml-release.yml`:
```yaml
on:
  workflow_dispatch:  # Manual trigger only (remove 'push' section)
```

Then manually trigger from GitHub UI:
1. Go to Actions → "Generate and Release XML Thread Profiles"
2. Click "Run workflow"
3. Select branch and click "Run workflow"

### Change Release Schedule

To generate profiles on a schedule (e.g., weekly), add:

```yaml
on:
  schedule:
    - cron: '0 0 * * 0'  # Every Sunday at midnight UTC
  workflow_dispatch:      # Plus manual trigger
```

### Customize Generated Profiles

Edit `src/customthreads/cli.py` configuration section:

```python
pitch_start = 1.0        # Starting pitch in mm
pitch_end = 6.0          # Ending pitch in mm
pitch_step = 0.5         # Pitch interval in mm
thread_sizes = list(range(8, 51))  # Diameters 8-50mm
tolerance_offsets = [0.0, 0.1, 0.2, 0.4, 0.8]  # Tolerance classes
```

Then commit and push to trigger a new release with your configuration.

### Modify Release Notes

Edit the `body` section of `create-release` step:

```yaml
- name: Create Release
  with:
    body: |
      Your custom release notes here...
      - Item 1
      - Item 2
```

## Troubleshooting

### Release Not Created

1. Check "Actions" tab for workflow errors
2. Verify branch is `master` (not a feature branch)
3. Ensure `pyproject.toml` is present
4. Check Poetry dependencies are correct

### XML File Invalid

1. Run tests locally: `poetry run pytest -v`
2. Generate locally: `poetry run python -m customthreads.cli`
3. Validate XML: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.xml')"`

### Workflow Not Triggering

1. Verify `.github/workflows/generate-xml-release.yml` is in `master` branch
2. Check repository settings → Actions permissions are enabled
3. Ensure your GitHub token has write access to releases

## Security Considerations

- ✅ Uses only official actions (`actions/checkout`, `actions/setup-python`)
- ✅ Read-only access to repository except for release creation
- ✅ `secrets.GITHUB_TOKEN` automatically provided by GitHub
- ✅ No external secrets or credentials needed

## Performance

- **Runtime:** ~2-3 minutes per release
- **Test Duration:** ~3 seconds
- **XML Generation:** <1 second
- **Total Including Setup:** ~2 minutes

## Future Enhancements

Potential improvements:
- Generate multiple XML variants (different pitch ranges, sizes)
- Create changelog from commit messages
- Upload to GitHub Pages as well
- Multi-architecture testing (Windows, macOS, Linux)
- Code coverage reports

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Poetry CI/CD Integration](https://python-poetry.org/docs/ci-cd/)
