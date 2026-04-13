---
title: Vibe-coding a tax calculator
url: https://apoorvaj.io/vibe-coding-a-tax-calculator
published: '2026-02-13'
source_blog: apoorvaj.io
source_site: https://apoorvaj.io/
category: graphics
fetched: '2026-04-13'
---

I live in Denmark. Danish tax is complicated. I was doing some
financial planning to buy an apartment, and wanted an online tax
calculator that properly accounted for interest payments and pension
contributions. I couldn’t find one that did a good job of it, so I built
my own: [taxman.dk](https://taxman.dk).

I vibe-coded the whole thing in two evenings with [Claude Code](https://docs.anthropic.com/en/docs/claude-code). I
have some thoughts about the experience.

Even with Opus 4.6, AI is remarkably good at some things and remarkably bad at others. It can scaffold an entire web app in minutes, but will occasionally lack common sense in ways that surprise you. I had to stay engaged throughout. I was thinking less about syntax and implementation details, and more about architecture and correctness.

I used Claude Code’s plan mode to describe the feature I wanted at a
high level, and let it produce a rough draft all in one go. The first
version of the tax calculation engine was loose and and that was fine.
In subsequent prompts, I requested refinements, and worked with it to
write a lot of tests. I tightened the engine up with a combination of
manual QA and automated testing. This is the same approach I described
in [Testing that works](https://apoorvaj.io/testing-that-works): start with a
working system, find bugs, add test cases that catch them, and
iterate.

When the model has just diagnosed a bug and understands the root cause, have it write the test right there, in the same session. If you lose that context, you end up re-explaining what went wrong, and you can’t always reconstruct the same diagnostic context.

Claude Code has a built-in sandbox
mode. Sandboxing
is a [deep
and important subject](https://www.luiscardoso.dev/blog/sandboxes-for-ai), but here we’re just using Claude Code’s
built-in sandbox. I turned on auto-allow and let it run. In
agentic development, unless I’m hitting a jagged edge of the model’s
intelligence, the bottleneck is my time and attention. I could optimize
this by reviewing code once per PR, not once per commit. I let it build
an entire feature, then review the result as a whole.

The whole project took two evenings. The tax engine has over 25,000 test cases and matches my pay slips at least. I wouldn’t have built it without AI, not because it was hard, but because the effort wouldn’t have been worth the payoff. That calculus has changed.