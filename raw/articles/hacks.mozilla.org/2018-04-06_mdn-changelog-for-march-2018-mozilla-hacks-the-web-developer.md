---
title: MDN Changelog for March 2018 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/04/mdn-changelog-for-march-2018/
author: John Whitlock
published: '2018-04-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s note:** *A changelog is “a log or record of all notable changes made to a project. [It] usually includes records of changes such as bug fixes, new features, etc.”
*

*Publishing a changelog is kind of a tradition in open source, and a long-time practice on the web. We thought readers of Hacks and folks who use and contribute to MDN Web Docs would be interested in learning more about the work of the MDN engineering team, and the impact they have in a given month. We’ll also introduce code contribution opportunities, interesting projects, and new ways to participate.*

## Done in March

Here’s what happened in March to the [code, data, and tools](https://github.com/mdn/) that support [MDN Web Docs](https://developer.mozilla.org):

[Improved compatibility data at the](https://hacks.mozilla.org#bcd-mar-18)[Hack on MDN event](https://hacks.mozilla.org/2018/03/hack-on-mdn-building-useful-tools-with-browser-compatibility-data/)[Experimented with brotli compression](https://hacks.mozilla.org#brotli-mar-18)[Shipped tweaks and fixes](https://hacks.mozilla.org#tweaks-mar-18)by merging 370 pull requests, including 137 pull requests from 48 new contributors.

Here’s the plan for April:

[Get HTML interactive examples ready for production](https://hacks.mozilla.org#ie-mar-18)[Ship the CDN and Django 1.11](https://hacks.mozilla.org#cdn-mar-18)[Improve the front-end developer experience](https://hacks.mozilla.org#frontend-mar-18)

In March, the MDN team focused on the Browser Compatibility Data project, meeting in Paris with dozens of collaborators for the “Hack on MDN” event. The work resulted in [221 Pull Requests in the BCD repo](https://github.com/mdn/browser-compat-data/pulls?utf8=%E2%9C%93&q=is%3Apr+label%3A%22HackOnMDNParis2018+%3Afr%3A%22+), as well as additional work in other repos. See Jean-Yves Perrier’s [Hack on MDN article](https://hacks.mozilla.org/2018/03/hack-on-mdn-building-useful-tools-with-browser-compatibility-data/) for details about the tools created and data updated during the week.

We reviewed and merged over 250 PRs in March. The compatibility data conversion jumped from 57% to 63% complete. [Jeremie Patonnier](https://github.com/JeremiePat) led the effort to convert SVG data ([BCD PR 1371](https://github.com/mdn/browser-compat-data/pull/1371)). API data was also a focus, both converting the existing MDN tables and using other data sources to fill out missing APIs.

There’s now [264 open PRs](https://github.com/mdn/browser-compat-data/pulls?q=is%3Aopen+is%3Apr) in the BCD repo, about a month’s worth, and the contributions keep coming in. BCD is one of the most active GitHub repositories at Mozilla this year by pull requests (880) and by authors (95), only second to [rust](https://github.com/rust-lang/rust) (1268 PRs, 267 authors). The rate of contributions continue to increase, so BCD may be #1 for Q2 2018.

[Brotli](https://en.wikipedia.org/wiki/Brotli) is a Google-developed compression algorithm designed for serving web assets, which can outperform the widely used [gzip](https://en.wikipedia.org/wiki/Gzip) algorithm. By the end of 2017, all major browsers support the `br`

content-encoding method, and Florian requested a test of brotli on MDN in [bug 1412891](https://bugzilla.mozilla.org/show_bug.cgi?id=1412891). [Maton Anthony](https://github.com/MatonAnthony) wrote a Python-2 compatible brotli middleware in [PR 4686](https://github.com/mozilla/kuma/pull/4686), with the default compression level of 11. This went live on March 7th.

Brotli does compress our content better than gzip. The homepage goes from 36k uncompressed to 9.5k with gzip to 7k with brotli. The results are better on wiki pages like [CSS display page](https://developer.mozilla.org/en-US/docs/Web/CSS/display), which goes from 144k uncompressed to 20k with gzip and 15k with brotli.

However, brotli was a net-negative for MDN performance. Average response time measured at the server was slower, going from 75 ms to 120 ms, due to the increased load of the middleware. Google Analytics showed a 6% improvement in page download time (1 ms better), but a 23% decline in average server response time (100 ms worse). We saw no benefit in static assets, because CloudFront handles gzip compression and ignores brotli.

Antony adjusted to compression level 5 ([Kuma PR 4712](https://github.com/mozilla/kuma/pull/4712)), which a [State of Brotli article](https://samsaffron.com/archive/2016/06/15/the-current-state-of-brotli-compression) tested to be comparable to gzip 9 in compression time but still results in smaller assets. When this went live on March 26th, we saw similar results, with our response time returning to pre-brotli levels, but with a slight improvement in HTML size when `br`

was used.

When we ship CloudFront in April, the CDN will take care of compression, and brotli will go away again. It looks like a promising technology, but requires a CDN that supports it, and works best with a “pre-compress” workflow rather than a “when requested” middleware workflow, which means it won’t be a good fit for MDN for a while.

There were 370 PRs merged in March:

[255 mdn/browser-compat-data PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22)[52 mdn/interactive-examples PRs](https://github.com/mdn/interactive-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22)[39 mozilla/kuma PRs](https://github.com/mozilla/kuma/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22)[5 mdn/kumascript PRs](https://github.com/mdn/kumascript/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22)[4 mdn/learning-area PRs](https://github.com/mdn/learning-area/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22)[4 mdn/webextensions-examples PRs](https://github.com/mdn/webextensions-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22)[4 mdn/bob PRs](https://github.com/mdn/bob/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22)[2 mdn/browser-compat-toolkit PRs](https://github.com/mdn/browser-compat-toolkit/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22)[2 mdn/pwa-examples PRs](https://github.com/mdn/pwa-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22)[1 mdn/webassembly-examples PR](https://github.com/mdn/webassembly-examples/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22)[1 mdn/pab PR](https://github.com/mdn/pab/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22)[1 mdn/mdn-fiori PR](https://github.com/mdn/mdn-fiori/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22)

137 of these were from first-time contributors:

- SpeechGrammar API (
[BCD PR 976](https://github.com/mdn/browser-compat-data/pull/976)), from[Jeremy Wilken](https://github.com/gnomeontherun). - Add UC (international and Chinese) for Android as a browsers (
[PR 1077](https://github.com/mdn/browser-compat-data/pull/1077)), Add QQ browser identifier (qq_android) ([PR 1078](https://github.com/mdn/browser-compat-data/pull/1078)), and[2 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22+author:foolip)to BCD from[Philip Jägenstedt](https://github.com/foolip). - Adds DOMTokenList compat data (
[BCD PR 1121](https://github.com/mdn/browser-compat-data/pull/1121)), from[Jared Fowler](https://github.com/jafow). - Add URL API (
[BCD PR 1122](https://github.com/mdn/browser-compat-data/pull/1122)), from[Jeremy Karlsson](https://github.com/enjikaka). - Add compat data for DocumentFragment (
[BCD PR 1184](https://github.com/mdn/browser-compat-data/pull/1184)), from[Juang, Yi-Lin](https://github.com/frankyjuang). - Add compat data for MediaRecorder (
[PR 1186](https://github.com/mdn/browser-compat-data/pull/1186)), Add compat data for Slotable api ([PR 1232](https://github.com/mdn/browser-compat-data/pull/1232)), and[4 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22+author:lucian95)to BCD from[Lucian Condrea](https://github.com/lucian95). - Adding compat data for MediaStream (
[PR 1212](https://github.com/mdn/browser-compat-data/pull/1212)), Add compat data for MediaStreamContraints ([PR 1244](https://github.com/mdn/browser-compat-data/pull/1244)), and[4 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22+author:mec)to BCD from[Mec](https://github.com/mec). - Add compat data for SVGAnimateElement (
[BCD PR 1236](https://github.com/mdn/browser-compat-data/pull/1236)), from[Djam Saidmuradov](https://github.com/djamshed). - Prevent tag auto-closing and correctly syntax highlight (
[BCD PR 1246](https://github.com/mdn/browser-compat-data/pull/1246)), from[Scott Buchanan](https://github.com/scottsb). - Update display: contents compat table (
[BCD PR 1271](https://github.com/mdn/browser-compat-data/pull/1271)), from[Guylian](https://github.com/gpgekko). - Add Safari and Node WebAssembly results (
[BCD PR 1280](https://github.com/mdn/browser-compat-data/pull/1280)), from[Sergey Rubanov](https://github.com/chicoxyzzy). - Added mandatory applicationServerKey for chrome (
[PR 1281](https://github.com/mdn/browser-compat-data/pull/1281)), from[Safwan Rahman](https://github.com/safwanrahman)(first contribution to BCD). - Add compat data for AnimationEffectTimingProperties (
[BCD PR 1299](https://github.com/mdn/browser-compat-data/pull/1299)), from[Terry](https://github.com/Teamop). - Adding compat data for PerformanceLongTaskTiming (
[BCD PR 1316](https://github.com/mdn/browser-compat-data/pull/1316)), from[Matthieu Bergel](https://github.com/mlbrgl). - Add compat data for :scope selector: Not supported in Edge (
[BCD PR 1323](https://github.com/mdn/browser-compat-data/pull/1323)), from[Bert Verhelst](https://github.com/bertyhell). - Update PerformanceResourceTiming support since safari(mac/ios) 11 (
[BCD PR 1334](https://github.com/mdn/browser-compat-data/pull/1334)), from[Mike Li](https://github.com/29decibel). - Updates css.property.display compat for Edge for Grid value (
[BCD PR 1340](https://github.com/mdn/browser-compat-data/pull/1340)), from[Bryan Robinson](https://github.com/brob). - Fix note about “defer” attribute in IE (
[BCD PR 1341](https://github.com/mdn/browser-compat-data/pull/1341)), from[vlakoff](https://github.com/vlakoff). - Trailing arrow function parameter commas do work in node (
[BCD PR 1365](https://github.com/mdn/browser-compat-data/pull/1365)), from[coolreader18](https://github.com/coolreader18). - Opera support (
[PR 1366](https://github.com/mdn/browser-compat-data/pull/1366)), and Opera 36 supports default parameters ([PR 1639](https://github.com/mdn/browser-compat-data/pull/1639)), to BCD from[Andrea Giammarchi](https://github.com/WebReflection). - Create version_name (
[BCD PR 1380](https://github.com/mdn/browser-compat-data/pull/1380)), from[Vitaly Zdanevich](https://github.com/vitaly-zdanevich). - Update structure of BCD data for WebRTC interfaces (
[PR 1397](https://github.com/mdn/browser-compat-data/pull/1397)), Update structure of BCD data for Service Worker interfaces ([PR 1398](https://github.com/mdn/browser-compat-data/pull/1398)), and[27 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22+author:dontcallmedom)from[Dominique Hazael-Massieux](https://github.com/dontcallmedom)(first contributions to BCD). - Add compat data for SVG <feBlend> (
[PR 1420](https://github.com/mdn/browser-compat-data/pull/1420)), Add compat data for SVG <feColorMatrix> ([PR 1423](https://github.com/mdn/browser-compat-data/pull/1423)), and[35 more PRs](https://github.com/mdn/browser-compat-data/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22+author:solfen)to BCD from[maximelore](https://github.com/solfen). - Fixed Windows issue related to schema validation of browser info (
[PR 1433](https://github.com/mdn/browser-compat-data/pull/1433)), from[Sebastian Zartner](https://github.com/SebastianZ)(first contribution to BCD). - Update to Edge browser release dates (
[PR 1482](https://github.com/mdn/browser-compat-data/pull/1482)), and Add release dates for Edge Mobile browser ([PR 1483](https://github.com/mdn/browser-compat-data/pull/1483)), to BCD from[Matt Wojciakowski](https://github.com/mattwojo). - Update Edge support data based on MicrosoftEdge-Documentation (
[BCD PR 1518](https://github.com/mdn/browser-compat-data/pull/1518)), from[Mark Dittmer](https://github.com/mdittmer). - Update Edge data (
[PR 1619](https://github.com/mdn/browser-compat-data/pull/1619)), and Update set-cookie info for Edge and IE ([PR 1642](https://github.com/mdn/browser-compat-data/pull/1642)), from[patrick kettner](https://github.com/patrickkettner)(first contributions to BCD). - Rewrite the Object.create example. (
[Interactive Examples PR 634](https://github.com/mdn/interactive-examples/pull/634)), from[Mathias Arens](https://github.com/tatellos). - Use console.error() method to display errors (
[Interactive Examples PR 638](https://github.com/mdn/interactive-examples/pull/638)), from[Rudz Boy](https://github.com/rudzboy). - Better example for
`sort`

use case ([Interactive Examples PR 642](https://github.com/mdn/interactive-examples/pull/642)), from[Marek Pepke](https://github.com/pepkin88). - Update justify-content.html (
[Interactive Examples PR 649](https://github.com/mdn/interactive-examples/pull/649)), from[Clément P](https://github.com/yukulele). - Update: add calc() values in grid-gap demo (
[Interactive Examples PR 665](https://github.com/mdn/interactive-examples/pull/665)), from[一丝](https://github.com/yisibl). - Fix no-wrap (
[Interactive Examples PR 666](https://github.com/mdn/interactive-examples/pull/666)), from[Nikolay Puzyrev](https://github.com/npuzyrev). - Add example for CSS font-kerning property (
[Interactive Examples PR 667](https://github.com/mdn/interactive-examples/pull/667)), from[Ian Sanders](https://github.com/iansan5653). - More illustrative example for
`Proxy.apply`

([Interactive Examples PR 677](https://github.com/mdn/interactive-examples/pull/677)), from[Patrick Lienau](https://github.com/rozzzly). - Update object-assign.html (
[Interactive Examples PR 678](https://github.com/mdn/interactive-examples/pull/678)), from[Abhishek](https://github.com/Abhicoding). - Fixed typo (
[Interactive Examples PR 687](https://github.com/mdn/interactive-examples/pull/687)), from[Simon Wörner](https://github.com/SWW13). - Fix: ArrayBuffer.byteLength() => byteLength (
[Interactive Examples PR 689](https://github.com/mdn/interactive-examples/pull/689)), from[Martijn Thé](https://github.com/martijnthe). - Upgrade bleach to 2.1.3 (
[Kuma PR 4697](https://github.com/mozilla/kuma/pull/4697)), from[Greg Guthe](https://github.com/g-k). - Switch to node.js 8.10.0 (
[PR 640](https://github.com/mdn/kumascript/pull/640)), from[Maton Anthony](https://github.com/MatonAnthony)(first contribution to KumaScript). - Added Spanish translation (
[KumaScript PR 642](https://github.com/mdn/kumascript/pull/642)), from[Sergio González Collado](https://github.com/sergiocollado). - Update URL structure for IETF RFCs for HTTPS (
[KumaScript PR 647](https://github.com/mdn/kumascript/pull/647)), from[David Beitey](https://github.com/davidjb). - Update main.js (
[learning-area PR 62](https://github.com/mdn/learning-area/pull/62)), from[Ann Cascarano](https://github.com/redrambles). - Replace bgtile.png (
[PR 63](https://github.com/mdn/learning-area/pull/63)), can-store patches ([PRR65](https://github.com/mdn/learning-area/pull/65)), and nytimes patches ([PR 66](https://github.com/mdn/learning-area/pull/66)), to learning-area from[Adilson Sandoval](https://github.com/2alin). - First complete version of bob (
[PR 2](https://github.com/mdn/bob/pull/2)), Small update to README ([PR 3](https://github.com/mdn/bob/pull/3)), and[2 more PRs](https://github.com/mdn/bob/pulls?page=1&utf8=✓&q=is:pr+is:closed+merged:%222018-03-01..2018-03-31%22+author:schalkneethling)from[Schalk Neethling](https://github.com/schalkneethling)(first contributions to bob). - Eslint + Webpack + Travis CI setup (
[PR 1](https://github.com/mdn/browser-compat-toolkit/pull/1)), and Revert ES2015 modules configuration ([PR 2](https://github.com/mdn/browser-compat-toolkit/pull/2)), from[Maton Anthony](https://github.com/MatonAnthony)(first contributions to browser-compat-toolkit). - js13kPWA (
[PR 1](https://github.com/mdn/pwa-examples/pull/1)), and Fixes and icons ([PR 2](https://github.com/mdn/pwa-examples/pull/2)), to pwa-examples from[Andrzej Mazur](https://github.com/end3r). - Fixed function call when opening database fails (
[webassembly-examples PR 12](https://github.com/mdn/webassembly-examples/pull/12)), from[Dan McCarthy](https://github.com/Daniel-McCarthy). - Web for all link demos (
[pab PR 18](https://github.com/mdn/pab/pull/18)), from[r12a](https://github.com/r12a). - Updates to licenses as well as README and index page (
[PR 3](https://github.com/mdn/mdn-fiori/pull/3)), from[Schalk Neethling](https://github.com/schalkneethling)(first contribution to mdn-fiori).

Other significant PRs:

- Standardize signal handlers and apps (
[Kuma PR 4689](https://github.com/mozilla/kuma/pull/4689)), from[me](https://github.com/jwhitlock). - Upgrade node.js in our KS image to 8.10.0 (
[Kuma PR 4692](https://github.com/mozilla/kuma/pull/4692)), from[Maton Anthony](https://github.com/MatonAnthony). - Update feeder app, allow calling as task (
[Kuma PR 4694](https://github.com/mozilla/kuma/pull/4694)), from[me](https://github.com/jwhitlock). - Fix checkbox labels in Edit Profile (
[Kuma PR 4696](https://github.com/mozilla/kuma/pull/4696)), from[Donovan Glover](https://github.com/GloverDonovan). - Remove font observer lib, replace with font-display (
[Kuma PR 4699](https://github.com/mozilla/kuma/pull/4699)), from - Preload title and body fonts for improved performance (
[Kuma PR 4709](https://github.com/mozilla/kuma/pull/4709)), from[Schalk Neethling](https://github.com/schalkneethling). - Make lang preference cookie persistent (
[Kuma PR 4718](https://github.com/mozilla/kuma/pull/4718)), from[Maton Anthony](https://github.com/MatonAnthony). - Show error message to users on 500 internal server error (
[Kuma PR 4720](https://github.com/mozilla/kuma/pull/4720)), from[Schalk Neethling](https://github.com/schalkneethling). - Replaced hard-coded strings with translatable ones (
[Kuma PR 4722](https://github.com/mozilla/kuma/pull/4722)), from[Віталій Крутько](https://github.com/asmforce).

## Planned for April

We’ll be busy in April with [the output of the Hack on MDN event](https://hacks.mozilla.org/2018/03/hack-on-mdn-building-useful-tools-with-browser-compatibility-data/), reviewing PRs and turning prototypes into production code. We’ll continue working on our other projects as well.

The interactive examples are transitioning from rapid experimentation to a shipping feature. Will Bamberg published [Bringing interactive examples to MDN](https://hacks.mozilla.org/2018/03/bringing-interactive-examples-to-mdn/) in March, which details how this project went from idea to implementation.

The interactive examples team will firm up the code and processes, to build a better foundation for contributors and for future support. At the same time, they will firm up the design for HTML examples, which often require a mix of CSS and HTML to illustrate usage.

[Ryan Johnson](https://github.com/escattone) finished up caching headers for the 60 or so MDN endpoints, and he and [Dave Parfitt](https://github.com/metadave) added [CloudFront](https://aws.amazon.com/cloudfront/) in front of the staging site. We’ll spend some time with automated and manual testing, and then reconfigure production to also be behind a CDN.

We’ve missed the April 1 deadline for the Django 1.11 update. We plan to focus on the minimum tasks needed to update in April, and will defer other tasks, like updating out-of-date but compatible 3rd-party libraries, until later.

Schalk Neethling has had some time to get familiar with the front-end code of MDN, using tools like [Sonarwhal](https://sonarwhal.com/) and Chrome devtools’ performance and network panels to find performance issues faced by Chrome visitors to MDN. He’s put together a list of changes that he think will improve development and performance.

One quick win is to replace [FontAwesome’s](https://fontawesome.com/) custom font face with [SVG icons](https://fontawesome.com/how-to-use/svg-with-js). Instead of loading all the icons in a single file, only the icons used by a page will be loaded. The SVG will be included in the HTML, avoiding additional HTTP requests. SVG icons are automatically scaled, so they will look good on all devices. This should also improve the development experience. It’s easy to make mistakes when using character encodings like `"\f108\0020\eae6"`

, and much clearer to use names like `"icon-ie icon-mobile"`

.

Schalk is thinking about other challenges to front-end development, and how to bring in current tools and techniques. He’s cleaning up code to make it more consistent, and formalizing the rules in [MDN Fiori](https://github.com/mdn/mdn-fiori), a front-end style guide and pattern library. This may be the first step to switching to a UI component structure, such as [React](https://reactjs.org/).

A bigger improvement would be updating the front-end build pipeline. MDN’s build system was developed years ago (by Python developers) when JavaScript was less mature, and the system hasn’t kept up. [Webpack](https://webpack.js.org/) is widely used to bundle code and assets for deployment, and a new pipeline could allow developers to use a broader ecosystem of tools like [Babel](https://babeljs.io/) to write modern JavaScript.

Finally, we continue to look for the right way to test JavaScript. We’re currently using [Selenium](https://docs.seleniumhq.org/) to automate testing in a browser environment. We’ve had [issues](https://github.com/mozilla/kuma/pull/4195) getting a stable set of tools for consistent Selenium testing, and it has proven to be too heavy for unit testing of JavaScript. Schalk has had good experiences with [Jest](https://facebook.github.io/jest/), and wants to start testing MDN Javascript with Jest in April.

## About John Whitlock

John is a web developer working on the engine of MDN Web Docs

## One comment

Benny PowersApril 16th, 2018 at 07:28