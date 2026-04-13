---
title: 'Interop 2022: Outcomes – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2023/01/interop-2022-outcomes/
author: James Graham
published: '2023-01-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Last March we [announced](https://hacks.mozilla.org/2022/03/interop-2022/) the Interop 2022 project, a collaboration between Apple, Bocoup, Google, Igalia, Microsoft, and Mozilla to improve the quality and consistency of their implementations of the web platform.

Now that it’s 2023 and we’re deep into preparations for the next iteration of Interop, it’s a good time to reflect on how the first year of Interop has gone.

## Interop Wins

Happily, Interop 2022 appears to have been a big success. Every browser has made significant improvements to their test pass rates in the Interop focus areas, and now [all browsers are scoring over 90%](https://wpt.fyi/interop-2022). A particular success can be seen in the Viewport Units focus area, which went from 0% pass rate in all browsers to 100% in all browsers in less than a year. This almost never happens with web platform features!

Looking at the release version of browsers — reflecting what actually ships to users — Firefox started the year with a score of around 60% in Firefox 95 and reached 90% in Firefox 108, which was released in December. This reflects a great deal of effort put into Gecko, both in adding new features and improving the quality of implementation of existing features like CSS containment, which jumped from 85% pass rate to 98% with the improvements that were part of Firefox 103.

One of the big new web-platform features in 2022 was Cascade Layers, which first shipped as part of Firefox 97 in February. This was swiftly followed by implementations shipping in Chrome 99 and Safari 15.4, again showing the power of Interop to rapidly drive a web platform feature from initial implementation to something production-quality and available across browsers.

Another big win that’s worth highlighting was the progress of all browsers to >95% on the “Web Compatibility” focus area. This focus area consisted of a small set of tests from already implemented features where browser differences were known to cause problems for users (e.g. through bug reports to [webcompat.com](https://webcompat.com)). In an environment where it’s easy to fixate on the new, it’s very pleasing to see everyone come together to clean up these longstanding problems that broke sites in the wild.

Other new features that have shipped, or become interoperable, as part of Interop 2022 have been written about in retrospectives by [Apple](https://webkit.org/blog/13591/webkit-features-in-safari-16-2/) and [Google](https://web.dev/interop-2022-wrapup/). There’s a lot of work there to be proud of, and I’d suggest you check out their posts.

## Investigations

Along with the “focus areas” based on counts of passing tests, Interop 2022 had three “investigations”, covering areas where there’s less clarity on what’s required to make the web interoperable, and progress can’t be characterized by a test pass rate.

The Viewport investigation resulted in multiple [spec bugs](https://github.com/web-platform-tests/interop-2022-viewport/issues?q=is%3Aissue+is%3Aclosed+label%3A%22Spec+Issue%22) being filed, as well as [agreement](https://github.com/w3c/csswg-drafts/issues/7590) with the CSSWG to start work on a Viewport Specification. We know that viewport-related differences are a common source of pain, particularly on mobile browsers; so this is very promising for future improvements in this area.

The Mouse and Pointer Events investigation collated a large number of browser differences in the handling of input events. A subset of these issues got tests and formed the basis for a [proposed](https://github.com/web-platform-tests/interop/issues/202) Interop 2023 focus area. There is clearly still more to be done to fix other input-related differences between implementations.

The Editing investigation tackled one of the most historically tricky areas of the platform, where it has long been assumed that complex tasks require the use of libraries that smooth over differences with bespoke handling of each browser engine. One thing that became apparent from this investigation is that IME input (used to input characters that can’t be directly typed on the keyboard) has behavioral differences for which we lack the infrastructure to write automated cross-browser tests. This Interop investigation looks set to catalyze future work in this area.

## Next Steps

All the signs are that Interop 2022 was helpful in aligning implementations of the web and ensuring that users are able to retain a free choice of browser without running into compatibility problems. We plan to build on that success with the forthcoming launch of Interop 2023, which we hope will further push the state of the art for web developers and help web browser developers focus on the most important issues to ensure the future of a healthy open web.

## About
[
James Graham ](https://hoppipolla.co.uk)

Software engineer focused on maintaining a healthy open web. Web-platform-tests core team member.