---
title: 'A web testing deep dive: The MDN web testing report – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2021/04/a-web-testing-deep-dive-the-mdn-web-testing-report/
author: Chris Mills
published: '2021-04-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

For the last couple of years, we’ve run the MDN Web Developer Needs Assessment (DNA) Report, which aims to highlight the key issues faced by developers building web sites and applications. This has proved to be an invaluable source of data for browser vendors and other organizations to prioritize improvements to the web platform. This year we did a deep dive into web testing, and we are delighted to be able to announce the publication of this follow-on work, available at our [insights.developer.mozilla.org](https://insights.developer.mozilla.org/) site along with our other Web DNA publications.

## Why web testing?

In the Web DNA studies for [2019](https://insights.developer.mozilla.org/reports/mdn-web-developer-needs-assessment-2019.html) and [2020](https://insights.developer.mozilla.org/reports/mdn-web-developer-needs-assessment-2020.html), developers ranked the need “Having to support specific browsers, (e.g., IE11)” as the most frustrating aspect of web development, among 28 needs. The 2nd and 3rd rankings were also related to browser compatibility:

- Avoiding or removing a feature that doesn’t work across browsers
- Making a design look/work the same across browsers

In 2020, we released our [browser compatibility research results](https://insights.developer.mozilla.org/reports/mdn-browser-compatibility-report-2020.html) — a deeper dive into identifying specific issues around browser compatibility and pinpointing what can be done to mitigate these issues.

This year we decided to follow up with another deep dive focused on the 4th most frustrating aspect of developing for the web, “Testing across browsers.” It follows on nicely from the previous deep dive, and also concerns much-sought-after information.

You can download this report directly — see the [Web Testing Report (PDF, 0.6MB)](https://insights.developer.mozilla.org/reports/pdf/MDN-Web-Testing-Report-2021.pdf).

## A new question for 2020

Based on the 2019 ranking of “testing across browsers”, we introduced a new question to the DNA survey in 2020: “What are the biggest pain points for you when it comes to web testing?” We wanted to understand more about this need and what some of the underlying issues are.

Respondents could choose one or more of the following answers:

- Time spent on manual testing (e.g. due to lack of automation).
- Slow-running tests.
- Running tests across multiple browsers.
- Test failures are hard to debug or reproduce.
- Lack of debug tooling support (browser dev tools or IDE integration).
- Difficulty diagnosing performance issues.
- Tests are difficult to write.
- Difficult to set up an adequate test environment.
- No pain points.
- Other.

## Results summary

7.5% of respondents (out of 6,645) said they don’t have pain points with web testing. For those who did, the biggest pain point is the time spent on manual testing.

To better understand the nuances behind these results, we ran a qualitative study on web testing. The study consisted of twenty one-hour interviews with web developers who took the 2020 DNA survey and agreed to participate in follow-up research.

The results will help browser vendors understand whether to accelerate work on [WebDriver Bidirectional Protocol (BiDi) ](https://w3c.github.io/webdriver-bidi/)or if the unmet needs lie elsewhere. Our analysis on WebDriver BiDi is based on the assumption that the feature gap between single-browser test tooling and cross-browser test tooling is a source of pain. Future research on the struggles developers have will be able to focus the priorities and technical design of that specification to address the pain points.

### Key Takeaways

- In the 2020 Web DNA report, we included the results of a segmentation study. One of the seven segments that emerged was “Testing Technicians”. The name implies that the segment does testing and therefore finds frustration while doing tests. This is correct, but what’s also true is that developers commonly see a high entry barrier to testing, which contributes to their frustration.
- Defining a testing workflow, choosing tools, writing tests, and running tests all take time. Many developers face pressure to develop and launch products under tight deadlines. Testing or not testing is a tradeoff between the perceived value that testing adds compared to the time it will take to implement.
- Some developers are aware of testing but limited by their lack of knowledge in the area. This lack of knowledge is a barrier to successfully implementing a testing strategy. Other developers are aware of what testing is and how to do it, but they still consider it frustrating. Rather than lacking knowledge, this second group lacks the time and resources to run tests to the degree that they’d ideally like.
- For some developers, what constitutes a test type is unclear. Additionally, the line between coding and testing can be blurry.
- For developers who have established a testing workflow, the best way to describe how that came to be is
*evolutionary*. The evolutionary workflow is generally being continuously improved. - Browser vendors assumed unit testing to be a common type of testing and that it’s a well-developed space without a lot of pain points. However, what we learned is that there are more challenges with unit testing code that runs in the browser than anticipated, and there’s the same time pressure as elsewhere, meaning it doesn’t happen as frequently as expected.
- In the most general of summaries, one could conclude that testing should take less time than it does.
- Stakeholders had assumed that developers want to test their code in as many browsers as they can and they’re just limited by the browsers their tools support. What we learned is that the decision of which browsers they support does not depend on the tools they use. Conversely, what browsers they support drives the decisions for which tools they use.8

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.