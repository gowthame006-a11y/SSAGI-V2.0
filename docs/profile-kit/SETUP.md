# Profile dashboard setup

1. Create a public repository named `gowthame006-a11y` under the account `gowthame006-a11y`.
2. Copy `docs/PROFILE_README.md` from this repository to `README.md` at the new repository root.
3. Copy `docs/metrics.svg` to `metrics.svg` at the new root as an initial preview.
4. Copy this kit's `scripts/profile_metrics.py` to `scripts/profile_metrics.py` and `.github/workflows/profile-metrics.yml` to `.github/workflows/profile-metrics.yml` in the new repository.
5. Run **Refresh profile metrics** from the Actions tab. It refreshes daily thereafter.

The workflow uses the built-in GitHub Actions token; no personal access token is required. It reads public account and repository metadata only. Language bars count primary languages of public non-fork repositories, not code-byte percentages. The workflow template has not been executed yet. It assumes the profile repository default branch is `main` and permits workflow commits.

GitHub's native contribution calendar remains on the profile. A 3D calendar, coding-hour chart, and PageSpeed scores are not included because those need separate data sources and setup.
