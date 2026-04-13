---
title: Inspecting Security and Privacy Settings of a Website – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2015/10/inspecting-security-and-privacy-settings-of-a-website/
author: Christoph Kerschbaumer
published: '2015-10-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

### Inspecting the Content Security Policy of a Website

Starting in Firefox 41, Mozilla provides a developer tool that allows users to inspect the security settings of a website. Using [GCLI (Graphic Command Line Interface)](https://developer.mozilla.org/en-US/docs/Tools/GCLI) a user can inspect the [Content Security Policy (CSP)](http://www.w3.org/TR/CSP/) of a website. CSP is a security concept that allows websites to protect themselves against cross-site scripting (XSS) and related attacks. CSP allows website authors to whitelist approved sources from which content can be loaded safely. Browsers enforce that Content Security Policy header and only allow whitelisted resources to be loaded into that website. The CSP inspection tool `» security csp` lists all whitelisted sources.

The main intention behind CSP is to protect websites against XSS attacks, but the protection needs to be deployed in a way that allows support for legacy code on these sites. For example, the keyword ‘unsafe-inline’ was originally introduced to support legacy inline scripts while transitioning sites to use CSP. This keyword whitelists all inline scripts for a site, but it also allows attacker-injected scripts to execute, making CSP ineffective against most XSS attacks. Hence, the CSP devtool not only lists all whitelisted sources, but also provides a rating for each whitelisted source, to indicate the level of protection.

### Inspecting the referrer policy of a website

Starting in Firefox 43, Mozilla exposes more website privacy settings and also allows users to inspect the

[Referrer Policy](http://www.w3.org/TR/referrer-policy/)

`» security referrer`. The referrer policy allows websites to exercise more control over the browser’s referrer header. Specifically it allows website authors to instruct the browser to strip the referrer completely, reveal it only when navigating within the same origin, etc. The referrer devtool provides an example of what referrer will be used when visiting different websites, allowing the user and developer to inspect what information is sent when following a link.

Inspecting the Content Security Policy as well as the Referrer Policy is only the starting point to providing end users with more feedback about the security and privacy settings a web page uses. We hope to add more tools in the future to give users more transparency and control over the security and privacy of the websites they visit.

## About
[
Christoph Kerschbaumer ](https://christophkerschbaumer.com/)

Christoph has over two decades of experience in software engineering and computer security. His expertise includes designing secure systems with fail-safe defaults, mitigating cross-site scripting vulnerabilities, preventing machine-in-the-middle attacks, and advancing security foundations for trustworthy AI systems. He earned his Ph.D. in Computer Science from the University of California, Irvine, where his research focused on information flow tracking techniques in web browsers.

## About Kate McKinley

Security ◆ Privacy