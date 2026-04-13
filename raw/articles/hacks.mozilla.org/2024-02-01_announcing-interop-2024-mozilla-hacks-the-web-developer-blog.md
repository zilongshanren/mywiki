---
title: Announcing Interop 2024 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2024/02/announcing-interop-2024/
author: James Graham
published: '2024-02-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The [Interop Project](https://github.com/web-platform-tests/interop#the-interop-project) has become one of the key ways that browser vendors come together to improve the web platform. By working to identify and improve key areas where differences between browser engines are impacting users and web developers, Interop is a critical tool in ensuring the long-term health of the open web.

The web platform is built on interoperability based on common standards. This offers users a degree of choice and control that sets the web apart from proprietary platforms defined by a single implementation. A commitment to ensuring that the web remains open and interoperable forms a fundamental part of Mozilla’s [manifesto](https://www.mozilla.org/about/manifesto/) and [web vision](https://www.mozilla.org/en-US/about/webvision/), and is why we’re so committed to shipping Firefox with our own [Gecko](https://en.wikipedia.org/wiki/Gecko_(software)) engine.

However interoperability requires care and attention to maintain. When implementations ship with differences between the standard and each other, this creates a [pain point](https://2023.stateofcss.com/en-US/usage/#css_pain_points) for web authors; they have to choose between avoiding the problematic feature entirely and coding to specific implementation quirks. Over time if enough authors produce implementation-specific content then interoperability is lost, and along with it user agency.

This is the problem that the Interop Project is designed to address. By bringing browser vendors together to focus on interoperability, the project allows identifying areas where interoperability issues are causing problems, or may do in the near future. Tracking progress on those issues with a public metric provides accountability to the broader web community on addressing the problems.

The project works by identifying a set of high-priority focus areas: parts of the web platform where everyone agrees that making interoperability improvements will be of high value. These can be existing features where we know browsers have slightly different behaviors that are causing problems for authors, or they can be new features which web developer feedback shows is in high demand and which we want to launch across multiple implementations with high interoperability from the start. For each focus area a set of web-platform-tests is selected to cover that area, and the score is computed from the pass rate of these tests.

## Interop 2023

The [Interop 2023](https://hacks.mozilla.org/2023/02/announcing-interop-2023/) project covered high profile features like the new :has() selector, and web-codecs, as well as areas of historically poor interoperability such as pointer events.

![](../../assets/8bbd8efd195193c1.png)


The [results](https://wpt.fyi/interop-2023) of the project speak for themselves: every browser ended the year with scores in excess of 97% for the prerelease versions of their browsers. Moreover, the overall Interoperability score — that is the fraction of focus area tests that pass in all participating browser engines — increased from 59% at the start of the year to 95% now. This result represents a huge improvement in the consistency and reliability of the web platform. For users this will result in a more seamless experience, with sites behaving reliably in whichever browser they prefer.

For the :has() selector — which we know from author feedback has been one of the most in-demand CSS features for a long time — every implementation is [now passing 100%](https://wpt.fyi/results/css/selectors?label=experimental&label=master&product=chrome&product=firefox&product=safari&aligned&view=interop&q=label%3Ainterop-2023-has) of the web-platform-tests selected for the focus area. Launching a major new platform feature with this level of interoperability demonstrates the power of the Interop project to progress the platform without compromising on implementation diversity, developer experience, or user choice.

As well as focus areas, the Interop project also has “investigations”. These are areas where we know that we need to improve interoperability, but aren’t at the stage of having specific tests which can be used to measure that improvement. In 2023 we had two investigations. The first was for accessibility, which covered writing many more tests for ARIA [computed role](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles) and [accessible name](https://developer.mozilla.org/en-US/docs/Glossary/Accessible_name), and ensuring they could be run in different browsers. The second was for mobile testing, which has resulted in both Mobile Firefox and Chrome for Android having their initial [results in wpt.fyi](https://wpt.fyi/runs?label=master&from=2024-01-10T00%3A00&product=firefox_android&product=chrome_android).

## Interop 2024

Following the success of Interop 2023, we are pleased to confirm that the project will continue in 2024 with a new selection of focus areas, representing areas of the web platform where we think we can have the biggest positive impact on users and web developers.

### New Focus Areas

New focus areas for 2024 include, among other things:

[Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API)– This provides a declarative mechanism to create content that always renders in the topmost-layer, so that it overlays other web page content. This can be useful for building features like tooltips and notifications. Support for popover was the #1 author request in the recent State of HTML survey.[CSS Nesting](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_nesting)– This is a feature that’s already shipping, which allows writing more compact and readable CSS files, without the need for external tooling such as preprocessors. However different browsers shipped slightly different behavior based on different revisions of the spec, and Interop will help ensure that everyone aligns on a single, reliable, syntax for this popular feature.- Accessibility – Ensuring that the web is accessible to all users is a critical part of
[Mozilla’s manifesto](https://www.mozilla.org/en-US/about/manifesto/). Our ability to include Accessibility testing in Interop 2024 is a direct result of the success of the Interop 2023 Accessibility Investigation in increasing the test coverage of key accessibility features.

The full list of focus areas is available in the [project README](https://github.com/web-platform-tests/interop/blob/main/2024/README.md).

### Carryover

In addition to the new focus areas, we will carry over some of the 2023 focus areas where there’s still more work to be done. Of particular interest is the Layout focus area, which will combine the previous [Flexbox](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Flexbox), [Grid](https://developer.mozilla.org/en-US/docs/Web/CSS/grid) and [Subgrid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Subgrid) focus area into one area covering all the most important layout primitives for the modern web. On top of that the Custom Properties, URL and Mouse and Pointer Events focus areas will be carried over. These represent cases where, even though we’ve already seen large improvements in Interoperability, we believe that users and web authors will benefit from even greater convergence between implementations.

### Investigations

As well as focus areas, Interop 2024 will also feature a new investigation into improving the integration of WebAssembly testing into web-platform-tests. This will open up the possibility of including WASM features in future Interop projects. In addition we will extend the Accessibility and Mobile Testing investigations, as there is more work to be done to make those aspects of the platform fully testable across different implementations.

## Partner Announcements

**Apple**:[The web just gets better with Interop, now for 2024](https://webkit.org/blog/14955/the-web-just-gets-better-with-interop/)**Bocoup**:[Interop 2024](https://bocoup.com/blog/interop-2024)**Google**:[Interop 2024](https://web.dev/blog/interop-2024)**Igalia**:[Interop 2024 Launches](https://www.igalia.com/2024/interop-2024-launches.html)**Microsoft**:[Microsoft Edge and Interop 2024](https://blogs.windows.com/msedgedev/2024/02/01/microsoft-edge-and-interop-2024/)

## About
[
James Graham ](https://hoppipolla.co.uk)

Software engineer focused on maintaining a healthy open web. Web-platform-tests core team member.