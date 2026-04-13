---
title: Version 100 in Chrome and Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2022/02/version-100-in-chrome-and-firefox/
author: Karl Dubost
published: '2022-02-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Chrome and Firefox will reach version 100 in a [couple](https://developer.chrome.com/blog/force-major-version-to-100/) of [months](https://www.otsukare.info/2021/04/20/ua-three-digits-get-ready). This has the potential to cause breakage on sites that rely on identifying the browser version to perform business logic. This post covers the timeline of events, the strategies that Chrome and Firefox are taking to mitigate the impact, and how you can help.

## User-Agent string

[User-Agent (UA)](https://www.rfc-editor.org/rfc/rfc7231.html#section-5.5.3) is a string that browsers send in HTTP headers, so servers can identify the browser. The string is also accessible through JavaScript with [navigator.userAgent](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/userAgent). It’s usually formatted as follows:

`browserName/majorVersion.minorVersion`


For example, the latest release versions of browsers at the time of publishing this post are:

`Chrome: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36`

`Firefox: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0`

`Safari: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15`


## Major version 100—three-digit version number

Major version 100 is a big milestone for both Chrome and Firefox. It also has the potential to cause breakage on websites as we move from a two-digit to a **three-digit version number**. Web developers use all kinds of techniques for parsing these strings, from custom code to using User-Agent parsing libraries, which can then be used to determine the corresponding processing logic. The User-Agent and any other version reporting mechanisms will soon report a three-digit version number.

### Version 100 timelines

Version 100 browsers will be first released in experimental versions (Chrome Canary, Firefox Nightly), then beta versions, and then finally on the stable channel.

| Chrome (
|

[Release Schedule](https://wiki.mozilla.org/Release_Management/Calendar))## Why can a three-digit version number be problematic?

When browsers first reached version 10 a little over 12 years ago, [many issues were discovered](https://maqentaer.com/devopera-static-backup/http/dev.opera.com/articles/view/opera-ua-string-changes/index.html) with User-Agent parsing libraries as the major version number went from one digit to two.

Without a single specification to follow, [different browsers have different formats](https://developer.mozilla.org/docs/Web/HTTP/Headers/User-Agent) for the User-Agent string, and site-specific User-Agent parsing. It’s possible that some parsing libraries may have hard-coded assumptions or bugs that don’t take into account three-digit major version numbers. Many libraries improved the parsing logic when browsers moved to two-digit version numbers, so hitting the three-digit milestone is expected to cause fewer problems. Mike Taylor, an engineer on the Chrome team, has done a survey of common UA parsing libraries which didn’t uncover any issues. Running Chrome experiments in the field has surfaced some issues, which are being worked on.

## What are browsers doing about it?

Both Firefox and Chrome have been running experiments where current versions of the browser report being at major version 100 in order to detect possible website breakage. This has led to a few [reported](https://github.com/webcompat/web-bugs/labels/version100) [issues](https://bugs.chromium.org/p/chromium/issues/detail?id=1273958), some of which have already been fixed. These experiments will continue to run until the release of version 100.

There are also backup mitigation strategies in place, in case version 100 release to stable channels causes more damage to websites than anticipated.

## Firefox mitigation

In Firefox, the strategy will depend on how important the breakage is. Firefox has a [site interventions mechanism](https://wiki.mozilla.org/Compatibility/Interventions_Releases). Mozilla webcompat team can hot fix broken websites in Firefox using this mechanism. If you type `about:compat`

in the Firefox URL bar, you can see what is currently being fixed. If a site breaks with the major version being 100 on a specific domain, it is possible to fix it by sending version 99 instead.

If the breakage is widespread and individual site interventions become unmanageable, Mozilla can temporarily freeze Firefox’s major version at 99 and then test other options.

## Chrome mitigation

In Chrome, the backup plan is to use a flag to freeze the major version at 99 and report the real major version number in the minor version part of the User-Agent string (the code has already [landed](https://chromium-review.googlesource.com/c/chromium/src/+/3341658)).

The Chrome version as reported in the User-Agent string follows the pattern <major_version>.<minor_version>.<build_number>.<patch_number>.

If the backup plan is employed, then the User-Agent string would look like this:

`99.101.4988.0`


Chrome is also running experiments to ensure that reporting a three-digit value in the minor version part of the string does not result in breakage, since the minor version in the Chrome User-Agent string has reported 0 for a very long time. The Chrome team will decide on whether to resort to the backup option based on the number and severity of the issues reported.

## What can you do to help?

Every strategy that adds complexity to the User-Agent string has a strong impact on the ecosystem. Let’s work together to avoid yet another quirky behavior. In Chrome and Firefox Nightly, you can configure the browser to report the version as 100 right now and report any issues you come across.

### Configure Firefox Nightly to report the major version as 100

- Open Firefox Nightly’s Settings menu.
- Search for “Firefox 100” and then check the “Firefox 100 User-Agent String” option.

### Configure Chrome to report the major version as 100

- Go to chrome://flags/#force-major-version-to-100
- Set the option to `Enabled`.

### Test and file reports

**If you are a website maintainer**, test your website with Chrome and Firefox 100. Review your User-Agent parsing code and libraries, and ensure they are able to handle three-digit version numbers. We have compiled some of the[patterns that are currently breaking](https://www.otsukare.info/2022/01/14/broken-ua-detection).**If you develop a User-Agent parsing library**, add tests to parse versions greater than and equal to 100. Our early tests show that recent versions of libraries can handle it correctly. But the Web is a legacy machine, so if you have old versions of parsing libraries, it’s probably time to check and eventually upgrade.**If you are browsing the web**and notice any issues with the major version 100,[file a report on webcompat.com](https://webcompat.com/issues/new?label=version100).

## About
[
Karl Dubost ](http://www.otsukare.info/)

## About
[
Chris Peterson ](http://www.cpeterso.com/blog/)

Chris is a developer on Mozilla's Firefox for Android team.

## About Ali Beyad

Ali Beyad is a Staff Software Engineer at Google