# Documentation site deployment

The site builder generates a static landing page, Schema.org Dataset JSON-LD, an absolute-URL sitemap, robots.txt, a copy of llms.txt, and the current catalog. It does not copy third-party language data or private conversation history.

## Observed deployment state

The latest checked run is [Pages workflow run 38994355957](https://github.com/Francois-EF-WebOps/BabelGlobalKreole/actions/runs/38994355957), commit `956f3f3359f159fa4c9b131c19d698b8df713e03`. Its preview build succeeded, but the `deploy` job was skipped. The proposed site address is `https://francois-ef-webops.github.io/BabelGlobalKreole/`; it is not verified as live. The web verifier reported `DisabledError` while attempting to fetch the page and generated files, which is not an HTTP 404 and does not independently establish their HTTP status.

A skipped `deploy` job means this workflow did not publish the current build. Check the repository variable `PAGES_ENABLED` and Pages configuration; do not infer that a successful preview means deployment succeeded.

## Owner-only settings

1. Open **Settings → Pages** for this repository.
2. Under **Build and deployment**, choose **GitHub Actions** as the source.
3. Under **Settings → Secrets and variables → Actions → Variables**, ensure repository variable `PAGES_ENABLED` is exactly `true`.
4. Run the **Build and deploy documentation site** workflow again.
5. Confirm the run's `deploy` job succeeded and use the exact URL shown by the GitHub Pages environment/deployment.

The build preview runs on pushes even when deployment is disabled. A green preview-only run is not evidence that the site is published.

## URL integrity checks after deployment

After a successful deployment, compare the exact configured base URL against site-referencing URLs in the deployed `sitemap.xml`, `robots.txt`, copied `llms.txt`, and Dataset JSON-LD. In `CITATION.cff`, keep `repository-code` pointing to the GitHub repository; only site URL fields, if present, should match the live site. External license and repository links must not be rewritten to the site address. The sitemap and robots files are generated into the site artifact by `scripts/build_site.py`; they are not necessarily tracked at repository root. Do not add a live-site link to the README or claim that URLs are verified until the deployment URL loads and the generated files agree.

## Local build

```sh
python scripts/build_site.py --base-url https://your-configured-pages-url --output-dir site
```

Use the exact URL shown in repository Pages settings. The preview artifact uses the repository URL only for validation; the deploy job rebuilds with the configured Pages URL. Do not publish the preview artifact.
