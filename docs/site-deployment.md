# Documentation site deployment

The site builder creates a static landing page with Schema.org Dataset JSON-LD, an absolute-URL sitemap, robots.txt, a copy of llms.txt, and the generated catalog. It does not copy third-party language data or private conversation history.

## One-time repository setting

The connected GitHub operation can commit repository files and inspect CI, but it cannot change the repository's Pages settings or create the required non-default token. To publish the site:

1. Open **Settings → Pages** for this repository.
2. Under **Build and deployment**, choose **GitHub Actions** as the source.
3. Add repository variable `PAGES_ENABLED` with value `true`.
4. Run the **Build and deploy documentation site** workflow, or push a later commit to `main`.

The workflow builds a preview artifact on every push. The deploy job remains skipped until the variable is set, so it does not falsely claim that a site is live. The Pages deployment action obtains the exact base URL from GitHub's configured Pages metadata; the sitemap is generated from that value rather than a guessed URL.

## Local build

```sh
python scripts/build_site.py --base-url https://your-configured-pages-url --output-dir site
```

Use the exact URL shown in the repository's Pages settings. Do not copy the example URL from tests into a public sitemap.
