---
title: Announcing Interop 2022 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2022/03/interop-2022/
author: Anne van Kesteren
published: '2022-03-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A key benefit of the web platform is that it’s defined by standards, rather than by the code of a single implementation. This creates a shared platform that isn’t tied to specific hardware, a company, or a business model.

Writing high quality standards is a necessary first step to an interoperable web platform, but ensuring that browsers are consistent in their behavior requires an ongoing process. Browsers must work to ensure that they have a shared understanding of web standards, and that their implementation matches that understanding.

## Interop 2022

Interop 2022 is a cross-browser initiative to find and address the most important interoperability pain points on the web platform. The end result is a public metric that will assess progress toward fixing these interoperability issues.

In order to identify the areas to include, we looked at two primary sources of data:

- Web developer feedback (e.g., through developer facing surveys including
[MDN’s Web DNA Report](https://insights.developer.mozilla.org/)) on the most common pain points they experience. - End user bug reports (e.g., via
[webcompat.com](https://webcompat.com/)) that could be traced back to implementation differences between browsers.

During the process of collecting this data, it became clear there are two principal kinds of interoperability problems which affect end users and developers:

- Problems where there’s a relatively clear and widely accepted standard, but where implementations are incomplete or buggy.
- Problems where the standard is missing, unclear, or doesn’t match the behavior sites depend on.

Problems of the first kind have been termed “focus areas”. For these we use [web-platform-tests](https://web-platform-tests.org/): a large, shared testsuite that aims to ensure web standards are implemented consistently across browsers. It accepts contributions from anyone, and browsers, including Firefox, contribute tests as part of their process for fixing bugs and shipping new features.

The path to improvement for these areas is clear: identify or write tests in web-platform-tests that measure conformance to the relevant standard, and update implementations so that they pass those tests.

Problems of the second kind have been termed “investigate areas”. For these it’s not possible to simply write tests as we’re not really sure what’s necessary to reach interoperability. Such unknown unknowns turn out to be extremely common sources of developer and user frustration!

We’ll make progress here through investigation. And we’ll measure progress with more qualitative goals, e.g., working out what exact behavior sites depend on, and what can be implemented in practice without breaking the web.

In all cases, the hope is that we can move toward a future in which we know how to make these areas interoperable, update the relevant web standards for them, and measure them with tests as we do with focus areas.

### Focus areas

Interop 2022 has ten new focus areas:

- Cascade Layers
- Color Spaces and Functions
- Containment
- Dialog Element
- Forms
- Scrolling
- Subgrid
- Typography and Encodings
- Viewport Units
- Web Compat

Unlike the others the Web Compat area doesn’t represent a specific technology, but is a group of specific known problems with already shipped features, where we see bugs and deviations from standards cause frequent site breakage for end users.

There are also five additional areas that have been adopted from Google and Microsoft’s “Compat 2021” effort:

- Aspect Ratio
- Flexbox
- Grid
- Sticky Positioning
- Transforms

A browser’s test pass rate in each area contributes 6% — totaling at 90% for fifteen areas — of their score of Interop 2022.

We believe these are areas where the standards are in good shape for implementation, and where improving interoperability will directly improve the lives of developers and end users.

### Investigate areas

Interop 2022 has three investigate areas:

- Editing, contentEditable, and execCommand
- Pointer and Mouse Events
- Viewport Measurement

These are areas in which we often see complaints from end users, or reports of site breakage, but where the path toward solving the issues isn’t clear. Collaboration between vendors is essential to working out how to fix these problem areas, and we believe that Interop 2022 is a unique opportunity to make progress on historically neglected areas of the web platform.

The overall progress in this area will contribute 10% to the overall score of Interop 2022. This score will be the same across all browsers. This reflects the fact that progress on the web platform requires browsers to collaborate on new or updated web standards and accompanying tests, to achieve the best outcomes for end users and developers.

## Contributions welcome!

Whilst the focus and investigate areas for 2022 are now set, there is still much to do. For the investigate areas, the detailed targets need to be set, and the complex work of understanding the current state of the art, and assessing the options to advance it, are just starting. Additional tests for the focus areas might be needed as well to address particular edge cases.

If this sounds like something you’d like to get involved with, follow the instructions on the [Interop 2022 Dashboard](https://wpt.fyi/interop-2022).

Finally, it’s also possible that Interop 2022 is missing an area you consider to be a significant pain point. It won’t be possible to add areas this year, but, if the effort is a success we may end up running further iterations. Feedback on browser differences that are making your life hard as developer or end user are always welcome and will be helpful for identifying the correct focus and investigate areas for any future edition.

## Partner announcements

Bringing Interop 2022 to fruition was a collaborative effort and you might be interested in the other announcements:

- Apple’s
[Working together on Interop 2022](https://webkit.org/blog/12288/working-together-on-interop-2022/) [Bocoup and Interop 2022](https://bocoup.com/blog/interop-2022)- Google’s
[Interop 2022: browsers working together to improve the web for developers](https://web.dev/interop-2022) [Igalia and Interop 2022](https://www.igalia.com/news/interop2022.html)[Microsoft and Interop 2022](https://aka.ms/microsoft-interop2022)

## About
[
Anne van Kesteren ](https://annevankesteren.nl/)

Standards person with an interest in privacy & security boundaries, as well as web platform architecture · he/him

## About
[
James Graham ](https://hoppipolla.co.uk)

Software engineer focused on maintaining a healthy open web. Web-platform-tests core team member.