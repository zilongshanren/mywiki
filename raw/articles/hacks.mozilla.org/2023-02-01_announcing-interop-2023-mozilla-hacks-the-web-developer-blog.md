---
title: Announcing Interop 2023 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2023/02/announcing-interop-2023/
author: James Graham
published: '2023-02-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A key difference between the web and other platforms is that the web puts users in control: people are free to choose whichever browser best meets their needs, and use it with any website. This is *interoperability*: the ability to pick and choose components of a system as long as they adhere to common standards.

For Mozilla, interoperability based on standards is an essential element of what makes the web special and sets it apart from other, proprietary, platforms. Therefore it’s no surprise that maintaining this is a [key part ](https://www.mozilla.org/en-US/about/webvision/full/#openness)of our vision for the web.

However, interoperability doesn’t just happen. Even with precise and well-written standards it’s possible for implementations to have bugs or other deviations from the agreed-upon behavior. There is also a tension between the desire to add new features to the platform, and the effort required to go back and fix deficiencies in already shipping features.

Interoperability gaps can result in sites behaving differently across browsers, which generally creates problems for everyone. When site authors notice the difference, they have to spend time and energy working around it. When they don’t, users suffer the consequences. Therefore it’s no surprise that authors [consider](https://insights.developer.mozilla.org/reports/mdn-web-developer-needs-assessment-2020.html#needs-assessment-top-ten-needs) cross-browser differences to be one of the most significant frustrations when developing sites.

Clearly this is a problem that needs to be addressed at the source. One of the ways we’ve tried to tackle this problem is via [web-platform-tests](http://web-platform-tests.org/). This is a shared testsuite for the web platform that everyone can contribute to. This is run in the Firefox CI system, as well as those of other vendors. Whenever Gecko engineers implement a new feature, the new tests they write are contributed back upstream so that they’re available to everyone.

Having shared tests allows us to find out where platform implementations are different, and gives implementers a clear target to aim for. However, users’ needs are large, and as a result, the web platform is large. That means that simply trying to fix every known test failure doesn’t work: we need a way to prioritize and ensure that we strike a balance between fixing the most important bugs and shipping the most useful new features.

The Interop project is designed to help with this process, and enable vendors to focus their energies in the way that’s most helpful to the long term health of the web. Starting in 2022, the Interop project is a collaboration between Apple, Bocoup, Google, Igalia, Microsoft and Mozilla (and open to any organization implementing the web platform) to set a public metric to measure improvements to interoperability on the web.

[Interop 2022](https://hacks.mozilla.org/2023/01/interop-2022-outcomes/) showed significant improvements in the interoperability of multiple platform features, along with several cross-browser investigations that looked into complex, under-specified, areas of the platform where interoperability has been difficult to achieve. Building on this, we’re pleased to announce [Interop 2023](https://wpt.fyi/interop-2023), the next iteration of the Interop project.

## Interop 2023

Like Interop 2022, Interop 2023 considers two kinds of platform improvement:

**Focus areas** cover parts of the platform where we already have a high quality specification and good test coverage in web-platform-tests. Therefore progress is measured by looking at the pass rate of those tests across implementations. “Active focus areas” are ones that contribute to this year’s scores, whereas “inactive” focus areas are ones from previous years where we don’t anticipate further improvement.

As well as calculating the test pass rate for each browser engine, we’re also computing the “Interop” score: how many tests are passed by all of Gecko, WebKit and Blink. This reflects our goal not just to improve one browser, but to make sure features work reliably across all browsers.

**Investigations** are for areas where we know interoperability is lacking, but can’t make progress just by passing existing tests. These could include legacy parts of the platform which shipped without a good specification or tests, or areas which are hard to test due to missing test infrastructure. Progress on these investigations is measured according to a set of mutually agreed goals.

## Focus Areas

The complete [list of focus areas](https://github.com/web-platform-tests/interop/blob/main/2023/README.md#focus-areas) can be seen in the Interop 2023 readme. This was the result of a consensus based process, with input from web authors, for example using the results of the [State of CSS 2022 survey](https://2022.stateofcss.com/en-US/), and MDN “short surveys”. That process means you can have confidence that all the participants are committed to meaningful improvements this year.

Rather than looking at all the focus areas in detail, I’ll just call out some of the highlights.

## CSS

Over the past several years CSS has added powerful new layout primitives — [flexbox](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Flexbox) and [grid](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Grids), followed by [subgrid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Subgrid) — to allow sophisticated, easy to maintain, designs. These are features we’ve been driving & [championing](https://hacks.mozilla.org/2010/04/the-css-3-flexible-box-model/) for [many](https://hacks.mozilla.org/2017/10/an-introduction-to-css-grid-layout-part-1/) [years](https://hacks.mozilla.org/2019/06/css-grid-level-2-subgrid-is-coming-to-firefox/), and which we were very pleased to see included in Interop 2022. They have been carried forward into Interop 2023, adding additional tests, reflecting the importance of ensuring that they’re totally dependable across implementations.

As well as older features, Interop 2023 also contains some new additions to CSS. Based on feedback from web developers we know that two of these in particular are widely anticipated: [Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Container_Queries) and parent selectors via [:has()](https://developer.mozilla.org/en-US/docs/Web/CSS/:has). Both of these features are currently being implemented in Gecko; Container Queries are already available to try in [prerelease versions of Firefox](https://www.mozilla.org/en-US/firefox/channel/desktop/), and is expected to be released in Firefox 110 later this month, whilst :has() is under active development. We believe that including these new features in Interop 2023 will help ensure that they’re usable cross-browser as soon as they’re shipped.

## Web Apps

Several of the features included in Interop 2023 are those that extend and enhance the capability of the platform; either allowing authors to achieve things that were previously impossible, or [improving the ergonomics of building web applications](https://www.mozilla.org/en-US/about/webvision/full/#site-buildingergonomics).

The [Web Components](https://developer.mozilla.org/en-US/docs/Web/Web_Components) focus area is about ergonomics; components allow people to create and share interactive elements that encapsulate their behavior and integrate into native platform APIs. This is especially important for larger web applications, and success depends on the implementations being rock solid across all browsers.

[Offscreen Canvas](https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas) and [Web Codecs](https://developer.mozilla.org/en-US/docs/Web/API/WebCodecs_API) are focus areas which are really about [extending the capabilities of the platform](https://www.mozilla.org/en-US/about/webvision/full/#newapis); allowing rich video and graphics experiences which have previously been difficult to implement efficiently using web technology.

## Compatibility

Unlike the other focus areas, Web Compatibility isn’t about a specific feature or specification. Instead the tests in this focus area have been written and selected on the basis of observed site breakage, for example from browser bug reports or via [webcompat.com](https://webcompat.com). The fact that these bugs are causing sites to break immediately makes them a very high priority for improving interoperability on the web.

## Investigations

Unfortunately not all interoperability challenges can be simply defined in terms of a set of tests that need to be fixed. In some cases we need to do preliminary work to understand the problem, or to develop new infrastructure that will allow testing.

For 2023 we’re going to concentrate on two areas in which we know that our current test infrastructure is insufficient: mobile platforms and accessibility APIs.

Mobile browsing interaction modes often create web development and interoperability challenges that don’t occur on desktop. For example, the browser viewport is significantly more dynamic and complex on mobile, reflecting the limited screen size. Whilst browser vendors have ways to test their own mobile browsers, we lack shared infrastructure required to run mobile-specific tests in web-platform-tests and include the results in Interop metrics. The Mobile Testing investigation will look at plugging that gap.

Users who make use of assistive technology (e.g., screen readers) depend on parts of the platform that are currently difficult to test in a cross-browser fashion. The Accessibility Testing investigation aims to ensure that accessibility technologies are just as testable as other parts of the web technology stack and can be included in future rounds of Interop as focus areas.

Together these investigations reflect the importance of ensuring that the web works for everyone, irrespective of how they access it.

## Dashboard

To follow progress on Inteop 2023, see the [dashboard](https://wpt.fyi/interop-2023) on wpt.fyi. This gives detailed scores for each focus area, as well as overall progress on Interop and the investigations.

## Mozilla & Firefox

The Interop project is an important part of Mozilla’s vision for a safe & open web where users are in control, and can use any browser on any device. Working with other vendors to focus efforts towards improving cross-browser interoperability is a big part of making that vision a reality. We also know how important it is to lead through our products, and look forward to bringing these improvements to Firefox and into the hands of users.

## Partner Announcements

- Apple –
[Pushing Interop Forward in 2023](https://webkit.org/blog/13706/interop-2023/) - Bocoup –
[Interop 2023 Update](https://bocoup.com/blog/interop-2023) - Google –
[Interop 2023](https://web.dev/interop-2023/) - Igalia –
[Interop 2023](https://www.igalia.com/news/2023/interop2023.html) - Microsoft –
[Microsoft Edge and Interop 2023](https://blogs.windows.com/msedgedev/2023/02/01/microsoft-edge-and-interop-2023/)

## About
[
James Graham ](https://hoppipolla.co.uk)

Software engineer focused on maintaining a healthy open web. Web-platform-tests core team member.

## One comment

voracityFebruary 2nd, 2023 at 04:38