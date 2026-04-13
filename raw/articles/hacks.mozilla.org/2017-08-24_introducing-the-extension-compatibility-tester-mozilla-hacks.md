---
title: Introducing the Extension Compatibility Tester – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/08/introducing-the-extension-compatibility-tester/
author: Sergi Mansilla
published: '2017-08-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

With Firefox’s move to a [modern web-style browser extension API](https://developer.mozilla.org/en-US/Add-ons/WebExtensions), it’s now possible to maintain one codebase and ship an extension in multiple browsers. However, since different browsers can have different capabilities, some extensions may require modification to be truly portable. With this in mind, we’ve built the [Extension Compatibility Tester](https://www.extensiontest.com/) to give developers a better sense of whether their existing extensions will work in Firefox.

The tool currently supports Chrome extension bundle (.crx) files, but we’re working on expanding the types of extensions you can check. The tool generates a report showing any potential uses of APIs or permissions incompatible with Firefox, along with next steps on how to distribute a compatible extension to Firefox users.

We will continue to participate in the [Browser Extensions Community Group](https://www.w3.org/community/browserext/) and support its goal of finding a common subset of extensible points in browsers and APIs that developers can use. We hope you give the tool a spin and let us know what you think!

### “The tool says my extension may not be compatible“

Not to worry! Our analysis only shows API and permission usage, and doesn’t have the full context. If the incompatible functionality is non-essential to your extension you can use capability testing to only use the API when available:

```
<span class="sf_code_syntax_comment">// Causes an Error
</span>browser.unavailableAPI(...);
<span class="sf_code_syntax_comment">
// Capability Testing FTW!
</span><span class="sf_code_syntax_keyword">if</span><span class="sf_code_syntax_comment"> (</span><span class="sf_code_syntax_string">'unavailableAPI'</span><span class="sf_code_syntax_comment"> </span><span class="sf_code_syntax_keyword">in</span><span class="sf_code_syntax_comment"> browser) {</span>
browser.unavailableAPI(...);<span class="sf_code_syntax_comment">
</span>}
```


Additionally, we’re constantly expanding the [available extension APIs](https://developer.mozilla.org/en-US/Add-ons/WebExtensions), so your missing functionality may be only a few weeks away!

### “The tool says my extension is compatible!”

Hooray! That said, definitely [try your extension out in Firefox](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Temporary_Installation_in_Firefox) before submitting to make sure things work as you expect. Common APIs may still have different effects in different browsers.

### “I don’t want to upload my code to a 3rd party website.”

Understood! The compatibility testing is available as part of our [extension development command-line tool](https://www.npmjs.com/package/web-ext) or as a [standalone module](https://github.com/mozilla/addons-linter).

If you have any issues using the tool, please [file an issue](https://github.com/mozilla/webext-compat-tool/issues) or leave a comment here. The hope is that this tool is a useful first step in helping developers port their extensions, and we get a healthier, more interoperable extension ecosystem.

**Happy porting!**

## One comment

PeterAugust 24th, 2017 at 08:11