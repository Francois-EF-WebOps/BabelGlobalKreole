# Documentation site deployment

The site builder generates a static landing page, Schema.org Dataset JSON-LD, an absolute-URL sitemap, robots.txt, a copy of llms.txt, and the current catalog. It does not copy third-party language data or private conversation history.

## Observed deployment state

The most recent deployment attempt reviewed for this note is [Pages workflow run 38994770664](https://github.com/Francois-EF-WebOps/BabelGlobalKreole/actions/runs/38994770664), commit `e6fa4578893b9c36b2b36d7bddc8d06781613422`. Its preview build succeeded using the proposed Pages base URL, but the `deploy` job was skipped. The proposed site address is `https://francois-ef-webops.github.io/BabelGlobalKreole/`; it is not verified as live. The web verifier reported `DisabledError` while attempting to fetch the page and generated files, which is not an HTTP 404 and does not independently establish their HTTP status.

A skipped `deploy` job means this workflow did not publish the current build. Check the repository variable `PAGES_ENABLED` and Pages configuration; do not infer that a successful preview means deployment succeeded.

## Owner-only settings

1. Open **Settings → Pages** for this repository.
2. Under **Build and deployment**, choose **GitHub Actions** as the source.
3. Under **Settings → Secrets and variables → Actions → Variables**, ensure repository variable `PAGES_ENABLED` is exactly `true`.
4. Run the **Build and deploy documentation site** workflow again.
5. Confirm the run's `deploy` job succeeded and use the exact URL shown by the GitHub Pages environment/deployment.

The build preview runs on pushes even when deployment is disabled. It now uses the proposed Pages base URL and asserts that the HTML canonical URL, Dataset JSON-LD `url`, all three sitemap locations and the robots Sitemap directive match that base. A green preview-only run verifies generated output, not public availability. GitHub repository links in `llms.txt`, `CITATION.cff`'s `repository-code`, and the Dataset JSON-LD `identifier`/catalog `contentUrl` remain GitHub URLs intentionally: they point to the authoritative source repository and data, not the landing page.

## URL integrity checks after deployment

After a successful deployment, compare the exact configured base URL against site-referencing URLs in the deployed `sitemap.xml`, `robots.txt`, copied `llms.txt`, and Dataset JSON-LD. In `CITATION.cff`, keep `repository-code` pointing to the GitHub repository; only site URL fields, if present, should match the live site. External license and repository links must not be rewritten to the site address. The sitemap and robots files are generated into the site artifact by `scripts/build_site.py`; they are not necessarily tracked at repository root. Do not add a live-site link to the README or claim that URLs are verified until the deployment URL loads and the generated files agree.

## Local build

```sh
python scripts/build_site.py --base-url https://your-configured-pages-url --output-dir site
```

Use the exact URL shown in repository Pages settings. The preview artifact is built against the proposed Pages URL only for URL-integrity validation; the deploy job rebuilds with the configured Pages URL. Do not publish the preview artifact.
