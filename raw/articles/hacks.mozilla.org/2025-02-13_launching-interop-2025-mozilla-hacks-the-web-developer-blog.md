---
title: Launching Interop 2025 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2025/02/interop-2025/
author: James Graham
published: '2025-02-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

# Launching Interop 2025

The Interop Project is a collaboration between browser vendors and other platform implementors to provide users and web developers with high quality implementations of the web platform.

Each year we select a set of focus areas representing key areas where we want to improve interoperability. Encouraging all browser engines to prioritize common features ensures they become usable for web developers as quickly as possible.

Progress in each engine and the overall Interop score are measured by tracking the pass rate of a set of web-platform tests for each focus area using the [Interop dashboard](https://wpt.fyi/interop).

## Interop 2024

Before introducing the new focus areas for this year, we should look at the [successes](https://wpt.fyi/interop-2024) of [Interop 2024](https://hacks.mozilla.org/2024/02/announcing-interop-2024/).

The Interop score, measuring the percentage of tests that pass in all of the major browser engines, has reached 95% in latest browser releases, up from only 46% at the start of the year. In pre-release browsers it’s even higher — over 97%. This is a huge win that shows how effective Interop can be at aligning browsers with the specifications and each other.

Each browser engine individually achieved a test pass score of 98% in stable browser releases and 99% in pre-release, with Firefox finishing slightly ahead with 98.8% in release and 99.1% in Nightly.

For users, this means features such as [requestVideoFrameCallback](https://developer.mozilla.org/en-US/docs/Web/API/HTMLVideoElement/requestVideoFrameCallback), [Declarative Shadow DOM](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM#declaratively_with_html), and [Popover](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API), which a year ago only had limited availability, are now implemented interoperably in all browsers.

## Interop 2025

Building on Interop 2024’s success, we are excited to continue the project into 2025. This year we have 19 focus areas; 17 new and 2 from previous years. A full description of all the focus areas is available [in the Interop repository](https://github.com/web-platform-tests/interop/blob/main/2025/README.md).

From 2024 we’re carrying forward Layout (really “Flexbox and Grid”), and Pointer and Mouse Events. These are important platform primitives where the Interop project has already led to significant interoperability improvements. However, with technologies that are so fundamental to the modern web we think it’s important to set ambitious goals and continue to prioritize these areas, creating rock solid foundations for developers to build on.

The new focus areas represent a broad cross section of the platform. Many of them — like [Anchor Positioning](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_anchor_positioning) and [View Transitions](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API) — have been identified from clear developer demand in surveys such as [State of HTML](https://2024.stateofhtml.com/en-US) and [State of CSS](https://2024.stateofcss.com/en-US). Inclusion in Interop will ensure they’re usable as soon as possible.

In addition to these high profile new features, we’d like to highlight some lesser-known focus areas and explain why we’re pleased to see them in Interop.

### Storage Access

At Mozilla user privacy is a core principle. One of the most common methods for tracking across the web is via [third-party cookies](https://developer.mozilla.org/en-US/docs/Web/Privacy/Third-party_cookies). When sites request data from external services, the service can store data that’s re-sent when another site uses the same service. Thus the service can follow the user’s browsing across the web.

To counter this, Firefox’s “[Total Cookie Protection](https://support.mozilla.org/en-US/kb/introducing-total-cookie-protection-standard-mode)” partitions storage so that third parties receive different cookie data per site and thus reduces tracking. Other browsers have [similar policies](https://developer.mozilla.org/en-US/docs/Web/Privacy/Third-party_cookies#how_do_browsers_handle_third-party_cookies), either by default or in private browsing modes.

However, in some cases, non-tracking workflows such as SSO authentication depend on third party cookies. Storage partitioning can break these workflows, and browsers currently have to ship site-specific workarounds. The [Storage Access API](https://developer.mozilla.org/en-US/docs/Web/API/Storage_Access_API) solves this by letting sites request access to the unpartitioned cookies. Interop here will allow browsers to advance privacy protections without breaking critical functionality.

### Web Compat

The Web Compat focus area is unique in Interop. It isn’t about one specific standard, but focuses on browser bugs known to break sites. These are often in older parts of the platform with long-standing inconsistencies. Addressing these requires either aligning implementations with the standard or, where that would break sites, updating the standard itself.

One feature in the Web Compat focus area for 2025 is [CSS Zoom](https://developer.mozilla.org/en-US/docs/Web/CSS/zoom). Originally a proprietary feature in Internet Explorer, it allowed scaling layout by adjusting the computed dimensions of elements at a time before CSS transforms. WebKit reverse-engineered it, bringing it into Blink, but Gecko never implemented it, due to the lack of a specification and the complexities it created in layout calculations.

Unfortunately, a feature not being standardised doesn’t prevent developers from using it. Use of CSS Zoom led to layout issues on some sites in Firefox, especially on mobile. We tried various workarounds and have had success using [interventions](https://wiki.mozilla.org/Compatibility/System_Addon) to replace `zoom`

with CSS transforms on some affected sites, but an attempt to implement the same approach directly in Gecko broke more sites than it fixed and was abandoned.

The situation seemed to be at an impasse until 2023 when Google investigated [removing CSS Zoom from Chromium](https://groups.google.com/a/chromium.org/g/blink-dev/c/V7q43bgutbo?pli=1). Unfortunately, it turned out that some use cases, such as Microsoft Excel Online’s worksheet zoom, depended on the specific behaviour of CSS Zoom, so removal was not feasible. However, having clarified the use cases, the Chromium team was able to [propose](https://github.com/w3c/csswg-drafts/issues/5623#issuecomment-1644208565) a standardized model for CSS Zoom that was easier to implement without compromising compatibility. This proposal was accepted by the CSS WG and led to the first implementation of CSS Zoom in Firefox 126, 24 years after it was first released in Internet Explorer.

With Interop 2025, we hope to bring the story of CSS Zoom to a close with all engines finally converging on the same behaviour, backed by a real open standard.

### WebRTC

Video conferencing is now an essential feature of modern life, and in-browser video conferencing offers both ease of use and high security, as users are not required to download a native binary. Most web-based video conferencing relies on the [WebRTC API](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API), which offers high level tools for implementing real time communications. However, WebRTC has long suffered from interoperability issues, with implementations deviating from the standards and requiring nonstandard extensions for key features. This resulted in confusion and frustration for users and undermined trust in the web as a reliable alternative to native apps.

Given this history, we’re excited to see WebRTC in Interop for the first time. The main part of the focus area is the [RTCRtpScriptTransform](https://developer.mozilla.org/en-US/docs/Web/API/RTCRtpScriptTransform) API, which enables cross browser end-to-end encryption. Although there’s more to be done in the future, we believe Interop 2025 will be a big step towards making WebRTC a truly interoperable web standard.

### Removing Mutation Events

The focus area for Removing Mutation Events is the first time Interop has been used to coordinate the removal of a feature. [Mutation events](https://developer.mozilla.org/en-US/docs/Web/API/MutationEvent) fire when the DOM changes, meaning the event handlers run on the critical path for DOM manipulation, causing major performance issues, and significant implementation complexity. Despite the fact that they have been implemented in all engines, they’re so problematic that they were never standardised. Instead, [mutation observers](https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver) were developed as a standard solution for the use cases of mutation events without their complexity or performance problems. Almost immediately after mutation observers were implemented, a [Gecko bug was filed](https://bugzilla.mozilla.org/show_bug.cgi?id=769207):

“We now have mutation observers, and we’d really like to kill support for mutation events at some point in the future. Probably not for a while yet.”


That was in 2012. The difficulty is the web’s core [commitment to backwards compatibility](https://www.mozilla.org/en-US/about/webvision/full/#openness). Removing features that people rely on is unacceptable. However, last year Chromium determined that use of mutation events had dropped low enough to allow a “[deprecation trial](https://developer.chrome.com/docs/web-platform/origin-trials#deprecation_trials)“, disabling mutation events by default, but allowing specific sites to re-enable them for a limited time.

This is good news, but long-running deprecation trials can create problems for other browsers. Disabling the feature entirely can break sites that rely on the opt-out. On the other hand we know from experience that some sites actually function better in a browser with mutation events disabled (for example, because they are used for non-critical features, but impact performance).

By including this removal in Interop 2025, we can ensure that mutation events are fully removed in 2025 and end the year with reduced platform complexity and improved web performance.

## Interop Investigations

As well as focus areas, the Interop project also runs investigations aimed at long-term interoperability improvements to areas where we can’t measure progress using test pass rates. For example Interop investigations can be looking to add new test capabilities, or increase the test coverage of platform features.

### Accessibility Investigation

The accessibility testing started as part of Interop 2023. It has added APIs for testing accessible name and computed role, as well as more than 1000 new tests. Those tests formed the Accessibility focus area in Interop 2024, which achieved an Interop score of 99.7%.

In 2025 the focus will be expanding the testability of accessibility features. Mozilla is working on a prototype of [AccessibleNode](https://github.com/WICG/aom/issues/203); an API that enables verifying the shape of the accessibility tree, along with its states and properties. This will allow us to test the effect of features like CSS display: contents or ::before/::after on the accessibility tree.

### Mobile Testing Investigation

Today, all Interop focus areas are scored in desktop browsers. However, some features are mobile-specific or have interoperability challenges unique to mobile.

Improving mobile testing has been part of Interop since 2023, and in that time we’ve made significant progress standing up mobile browsers in web-platform-tests CI systems. Today we have reliable runs of Chrome and Firefox Nightly on Android, and Safari runs on iOS are expected soon. However, some parts of our test framework were written with desktop-specific assumptions in the design, so the focus for 2025 will be on bringing mobile testing to parity with desktop. The goal is to allow mobile-specific focus areas in future Interop projects, helping improve interoperability across all device types.

## Driving the Web Forward

The unique and distinguishing feature of the web platform is its basis in open standards, providing multiple implementations and user choice. Through the Interop project, web platform implementors collaborate to ensure that these core strengths are matched by a seamless user experience across browsers.

With focus areas covering some of the most important new and existing areas of the modern web, Interop 2025 is set to deliver some of the biggest interoperability wins of the project so far. We are confident that Firefox and other browsers will rise to the challenge, providing users and developers with a more consistent and reliable web platform.

## Partner Announcements

## About
[
James Graham ](https://hoppipolla.co.uk)

Software engineer focused on maintaining a healthy open web. Web-platform-tests core team member.