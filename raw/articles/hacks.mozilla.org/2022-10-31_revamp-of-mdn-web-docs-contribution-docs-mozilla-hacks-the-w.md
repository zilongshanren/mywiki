---
title: Revamp of MDN Web Docs Contribution Docs – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2022/10/revamp-of-mdn-web-docs-contribution-docs/
author: Dipika Bhattacharya
published: '2022-10-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The MDN Web Docs team recently undertook a project to revamp and reorganize the “[Contribution Docs](https://developer.mozilla.org/en-US/docs/MDN)”. These are all the pages on MDN that describe what’s what – the templates and page structures, how to perform a task on MDN, how to contribute to MDN, and the community guidelines to follow while contributing to this massive open source project.

The contribution docs are an essential resource that help authors navigate the MDN project. Both the community as well as the partner and internal teams reference it regularly whenever we want to cross-check our policies or how-tos in any situation. Therefore, it was becoming important that we spruce up these pages to keep them relevant and up to date.

## Cleanup

This article describes the updates we made to the “Contribution Docs”.

### Reorganization

To begin with, we grouped and reorganized the content into two distinct buckets – Community guidelines and Writing guidelines. This is how the project outline looks like now:

- You’ll now find all the information about open source etiquette, discussions, process flows, users and teams, and how to get in touch with the maintainers in the
[Community guidelines](https://developer.mozilla.org/en-US/docs/MDN/Community)section. - You’ll find the information about how to write for MDN, what we write, what we regard as experimental, and so on in the
[Writing guidelines](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines)section.

Next, we shuffled the information around a bit so that logically similar pieces sit together. We also collated information that was scattered across multiple pages into more logical chunks.

For example, the [Writing style guide](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Writing_style_guide) now also includes information about “Write with SEO in mind”, which was earlier a separate page elsewhere.

We also restructured some documents, such as the [Writing style guide](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Writing_style_guide). This document is now divided into the sections “General writing guidelines”, “Writing style”, and “Page components”. In the previous version of the style guide, everything was grouped under “Basics”.

### Updates and rewrites

In general, we reviewed and removed outdated as well as repeated content. The cleanup effort also involved doing the following:

- Removing and redirecting common procedural instructions, such as setting up Git and using Github, to Github docs, instead of repeating the steps on MDN.
- Moving some repository-specific information to the respective repository. For example, a better home for the content about “Matching web features to browser release version numbers” is in the
[mdn/browser-compat-data](https://github.com/mdn/browser-compat-data)repository. - Rewriting a few pages to make them relevant to the currently followed guidelines and processes.
- Documenting our process flows for issues and pull requests on mdn/content vs other repositories on mdn. This is an ongoing task as we tweak and define better guidelines to work with our partners and community.

## New look

As a result of the cleanup effort, the new “Contributor Docs” structure looks like this:

### Community guidelines

### Writing guidelines


## Comparing the old with the new

The list below will give you an idea of the new home for some of the content in the previous version:

- “Contributing to MDN”
- New home: Community guidelines > Contributing to MDN Web Docs


- “Get started on MDN”
- New home: Community guidelines > Contributing to MDN Web Docs > Getting started with MDN Web Docs


- “Basic etiquette for open source projects”
- New home: Community guidelines > Contributing to MDN Web Docs > Open source etiquette


- “Where is everything on MDN”
- New home: Community guidelines > Contributing to MDN Web Docs > MDN Web Docs Repositories


- “Localizing MDN”
- New home: Community guidelines > Contributing to MDN Web Docs > Translated content


- “Does this belong on MDN Web Docs”, “Editorial policies”, “Criteria for inclusion”, “Process for selection”, “Project guidelines”
- New home: Writing guidelines > What we write


- “Criteria for inclusion”, “Process for selection”, “Project guidelines”
- New home: Writing guidelines > What we write > Criteria for inclusion on MDN Web Docs


- “MDN conventions and definitions”
- New home for definitions: Writing guidelines > Experimental, deprecated and obsolete
- New home for conventions: Writing guidelines > What we write


- “Video data on MDN”
- New home: Writing guidelines > How-to guides > How to add images and media


- “Structured data on MDN”
- New home: Writing guidelines > How-to guides > How to use structured data


- “Content structures”
- New home: Writing guidelines > Page structures


## Summary

The Contribution Docs are working documents — they are reviewed and edited regularly to keep them up to date with editorial and community policies. Giving them a good spring clean allows easier maintenance for us and our partners.