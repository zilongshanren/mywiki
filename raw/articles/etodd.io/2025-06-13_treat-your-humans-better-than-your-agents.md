---
title: Treat Your Humans Better Than Your Agents
url: https://etodd.io/2025/06/13/treat-your-humans-better-than-your-agents/
published: '2025-06-13'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Treat Your Humans Better Than Your Agents

Folks are starting to [figure out](https://lucumr.pocoo.org/2025/6/12/agentic-coding/) what kind of environment AI agents need to be [productive](https://crawshaw.io/blog/programming-with-agents).
The gist is:

- Agents need clear guidelines in a markdown file at the root of the repository explaining how to contribute to the project.
- Agents need a clean, isolated, reproducible environment in which they can run tests and go wild without breaking stuff and getting stuck.
- If the environments are sufficiently isolated, you can run them in parallel and allow multiple agents to work concurrently.
- Agents need fast tools so they can get feedback quickly. Tests should run fast. Speed of the iteration loop is everything.
- Documentation and code comments help agents figure out what’s going on.
- Agents work best with small contained tasks which can be reviewed and deployed continuously, rather than in huge risky chunks.

What’s maddening is, if you replace the word “agents” with “humans”, all these sentences are equally true, if not more so.

We’re suddenly rushing to accommodate these agents and make them productive, yet we’ve never felt the need to do the same for humans. It’s always been a struggle to fund projects to make humans more productive. But now, we’re going to measure every human’s performance based on how well they unblock and guide these agents. Can you imagine if we had been measuring performance all these years based on how well humans unblocked and guided other humans?

Our industry is about to spend an enormous amount of money building ideal development experiences for agents. I’m glad these changes are happening.

But do it for your humans, not your agents.