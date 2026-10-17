# Documentation site deployment

The site builder generates a static landing page, Schema.org Dataset JSON-LD, an absolute-URL sitemap, robots.txt, a copy of llms.txt, and the current catalog. It does not copy third-party language data or private conversation history.

## Observed deployment state

As of the latest checked run, [Pages workflow run 38994178661](https://github.com/Francois-EF-WebOps/BabelGlobalKreole/actions/runs/38994178661), the preview build succeeded but the `deploy` job was skipped. Therefore the site is **not yet verified live**, even if Pages settings have since been changed. The deployment URL and generated absolute URLs must be checked after a successful deploy run.

## Owner-only settings

1. Open **Settings → Pages** for this repository.
2. Under **Build and deployment**, choose **GitHub Actions** as the source.
3. Under **Settings → Secrets and variables → Actions → Variables**, ensure repository variable `PAGES_ENABLED` is exactly `true`.
4. Run the **Build and deploy documentation site** workflow again.
5. Confirm the run's `deploy` job succeeded and use the exact URL shown by the GitHub Pages environment/deployment.

The build preview runs on pushes even when deployment is disabled. A green preview-only run is not evidence that the site is published.

## URL integrity checks after deployment

Compare the exact configured base URL against the deployed `sitemap.xml`, `robots.txt`, `llms.txt`, `CITATION.cff`, and Dataset JSON-LD. The sitemap and robots files are generated into the site artifact by `scripts/build_site.py`; they are not necessarily tracked at repository root. Do not add a live-site link to the README or claim that URLs are verified until the deployment URL loads and the generated files agree.

## Local build

```sh
python scripts/build_site.py --base-url https://your-configured-pages-url --output-dir site
```

Use the exact URL shown in repository Pages settings. The preview artifact uses the repository URL only for validation; the deploy job rebuilds with the configured Pages URL. Do not publish the preview artifact.
