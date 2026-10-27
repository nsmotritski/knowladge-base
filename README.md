# Knowledge Base

An extensible bilingual field guide, visually adapted from the owner's Data Engineering site. Independent study material; no Anthropic affiliation or claim of complete exam coverage.

## Local build

Requires Python 3.9+; no package installation or external runtime assets.

```sh
python3 build.py
python3 -m http.server 8080 --directory dist
```

Open http://localhost:8080. The root opens the English guide by default, without requiring JavaScript. RU remains available through the language switch. The knowledge catalog is at `catalog.html`. Output: `dist/` (24 HTML pages). The build validates chapter IDs and every local link/asset. Pages work without JavaScript; JS enhances topic filtering and the mobile menu.

## Add or revise a topic

1. Copy a JSON file in `content/` and change its `id` (lowercase URL slug).
2. Fill both `en` and `ru`: `title`, `heading`, `lead`, `flow` (diagram nodes), `sections` (heading/body pairs).
3. Optionally add `diagrams` to each language: a list of `file`, `title`, `caption` objects. Store the corresponding SVG in `assets/diagrams/`; diagrams render after the overview flow. Use separate EN/RU SVGs and a light background.
4. Add its ID to `content/order.json`; rebuild. Navigation, language links and previous/next update automatically.
5. Review sources, examples and both languages before release. Add a separate directory and catalog card for a new subject.

## Content provenance

An independent Cloud Architect learning guide covering AI agents, coordination, context, tools and evidence. Chapters use practical examples and diagrams without test-question numbering or answer keys.

Primary conceptual references:
- https://www.anthropic.com/engineering/multi-agent-research-system
- https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them

The content includes practical architectural recommendations, distinguished from exact API contracts. No specific SDK behavior is assumed.

## GitHub Pages (manual publication)

`.github/workflows/pages.yml` builds and deploys `dist/` only when manually launched (`workflow_dispatch`). Pushes do not publish the site. Publication is managed through the manual workflow; ordinary pushes do not trigger deployment.

Manual publication procedure:
1. Commit and push the source and workflow to `develop` (the current branch). GitHub requires the manual workflow to exist on the repository default branch before it can be run from the Actions UI; confirm that branch or merge it there.
2. In repository **Settings → Pages → Build and deployment**, select **GitHub Actions**. Confirm repository visibility, Pages availability and the `github-pages` environment branch rules.
3. In **Actions → Publish GitHub Pages → Run workflow**, choose the reviewed branch and run it.
4. Use the deployment URL reported by Actions and verify the root opens EN, RU switching works, and chapter assets load.

Expected project URL, provided the owner/repository name and Pages configuration stay unchanged: `https://nsmotritski.github.io/knowladge-base/`. The spelling matches the existing remote. All redirects, navigation and assets use relative paths so the project subpath works without a hardcoded base URL. Do not upload the repository root; the workflow uploads only `dist/`.

Documentation: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
