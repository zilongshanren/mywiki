---
title: Testing that works
url: https://apoorvaj.io/testing-that-works
published: '2025-09-18'
source_blog: apoorvaj.io
source_site: https://apoorvaj.io/
category: graphics
fetched: '2026-04-13'
---

I’m a fast learner, but testing took me years to get right.

Testing determines if your project crumbles. It shapes your team’s culture. It dictates development velocity. It’s the biggest factor in whether AI coding tools help or hurt.

Pragmatism beats dogmatism. Test-driven development and granular unit tests are mostly waste. You won’t screw up vector addition. Bugs happen at integration points between subsystems.

Write subsystems that take plain data and return plain data. Little to no global state This is not exactly a novel idea, but a powerful one nonetheless. If done correctly, you should be able to spoof the input data to a subsystem, and assert against a known output. This means you can test that subsystem in isolation. If you find a bug in the subsystem later, just add a test with the case that fell through the cracks.

So what makes a project well-tested?

Ignore testing at your own peril. Use AI to write tests, then use tests to verify AI’s work. Design subsystems that play well with testing.