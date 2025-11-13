# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-14

### Fixed
- **Critical**: Fixed incorrect version matching logic that was dismissing alerts when it shouldn't
  - Previously: Alerts were dismissed if a TuxCare patched version existed in VEX, regardless of what version the repository was using
  - Now: Alerts are only dismissed if the repository is actually using the TuxCare patched version (with `.tuxcare` suffix)
  - Example: If repository uses `log4j:1.2.17` and VEX has `log4j:1.2.17.tuxcare.1`, the alert will NOT be dismissed (correct behavior)
  - Example: If repository uses `log4j:1.2.17.tuxcare.1` and VEX has `log4j:1.2.17.tuxcare.1`, the alert WILL be dismissed (correct behavior)

### Added
- Extract actual version from `vulnerableRequirements` field in GitHub alerts
- New version matching function `versions_match()` that checks for TuxCare suffix
- New skip reason `no-actual-version` when version cannot be determined from manifest
- Comprehensive test coverage for new version matching logic

### Changed
- Updated version matching algorithm to require TuxCare suffix in actual version
- Updated skip reason `no-positive-vex-match` message to be more descriptive

## [1.0.0] - 2025-11-13

### Added
- Initial release of TuxCare VEX Auto-Triage GitHub Action
- Support for Java (Maven), Python (pip), JavaScript (npm), and PHP (Composer) ecosystems
- Automatic dismissal of Dependabot alerts based on TuxCare VEX data
- Version range matching for accurate triage
- In-memory caching to avoid redundant VEX downloads
- Comprehensive logging and error handling
- Dry-run mode for testing
- GitHub Actions annotations and step summaries
- Rate limiting for GitHub API
- Retry logic with exponential backoff

