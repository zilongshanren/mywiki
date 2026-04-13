---
title: How to implement SRI in your build process – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2016/04/how-to-implement-sri-into-your-build-process/
author: Justin Dorfman
published: '2016-04-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Imagine getting a call from a customer who says your website is serving malware. Your heart drops, you start sweating, and then the tweets start pouring in. Something is up. You find out your systems have **not** been tampered with.

In fact, it was your CDN provider that got hacked, and the scripts you included on your website have become malicious. You tell your customers what happened and they don’t care. You failed to provide a secure product, now trust is lost. If this happened 2 years ago, I would feel bad for you. But if it happened to you today I would sigh and say,*“You should have used SRI*.”

[Subresource Integrity](https://www.maxcdn.com/one/visual-glossary/subresource-integrity/) (SRI) is a new-ish web application security standard and [W3C spec](https://www.w3.org/TR/SRI/) that helps prevent situations like the one above. Think of SRI as a safety net or rock-climbing rope for website content security. It is simply an attribute named `integrity`

with a SHA-2 hash as the value within a `<script>`

or `<link>`

tag. For example:

```
<script src="http://code.jquery.com/jquery-2.2.3.min.js"
integrity="sha256-a23g1Nt4dtEYOj7bR+vTu7+T8VP13humZFBJNIYoEJo="
crossorigin="anonymous">
</script>
```


In order for SRI to work, the CDN needs [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS) enabled. That (and more) is explained in detail in a [previous Hacks post introducing SRI](https://hacks.mozilla.org/2015/09/subresource-integrity-in-firefox-43/).

## Support

#### File types

The first version of the SRI standard was designed to address the biggest attack vectors caused by subresource hijacking on CDNs prevalent in Cascading Style Sheets (CSS) and JavaScript (JS) files. Other file types such as Flash, image, and video are not currently supported, but may be added in a future revision of the spec.

#### Browsers

As of April 2016 [CanIUse.com reports](http://caniuse.com/#feat=subresource-integrity) that ~52% of browsers (mobile + desktop) globally support SRI. The desktop user-agents that support SRI are Firefox (44+), Chrome(47+) & Opera (36+). The following Android-only mobile browsers also support SRI: Chrome (49+), Android Browser (49+), Opera (36+) & Firefox (45+).

Please note, SRI will still not work with browsers such as [Firefox for iOS](https://www.mozilla.org/en-US/firefox/ios/). This is because Apple requires all apps (including browsers & in-app browsing) to use the WebKit web browser engine. It would be nice to see a [status update](https://twitter.com/freddyb/status/717277170192801792)…

## SRI in your build process

There’s more than one way to get SRI into your build process. A number of tools already have plugins, for example: [Grunt](https://github.com/neftaly/grunt-sri), [Gulp](https://www.npmjs.com/package/gulp-sri), [Broccoli](https://github.com/jonathanKingston/broccoli-sri-hash), [Webpack](https://www.npmjs.com/package/webpack-subresource-integrity), [Ember CLI](https://github.com/jonathanKingston/ember-cli-sri) & [Handlebars](https://github.com/neftaly/handlebars-helper-sri).

We decided to show a real world example of SRI in a build process. We used a Grunt plugin called [grunt-sri](https://www.npmjs.com/package/grunt-sri) to generate the hashes.

#### How we did it for jQuery:

When looking at including SRI integrity for [code.jquery.com](https://code.jquery.com), we took a fairly simple approach compared to previous implementations. The code base was already using [Grunt](http://gruntjs.com/), and as such, it was pretty straightforward to include a target using the popular `grunt-sri`

node module. `grunt-sri`

traverses a specified list of files and generates a JSON payload including all the metadata required for implementing SRI in a code base. Once generated, the output file can easily be used as the base datasource when building out an application. Here’s a simple example of implementing a base generator using `grunt-sri`

:

```
// Gruntfile.js
grunt.loadNpmTasks("grunt-sri");
grunt.initConfig({
sri: {
generate: {
src: [ 'public/**/*.js', 'public/**/*.css' ],
options: { algorithms: [ 'sha256' ] }
}
}
});
```


Once implemented, running `grunt sri:generate`

will output `./payload.json`

for requiring in your application, or another Grunt task. The SRI SHA can then be accessed from the payload file from your code as shown in the `grunt-sri`

documentation:

```
// ES6 from https://github.com/neftaly/grunt-sri#javascript
var payload = require("./payload.json");
var sri = (id) => payload.payload[id];
var element = `<link
href='/style.css?cache=${ sri("@cssfile1").hashes.sha256 }'
integrity='${ sri("@cssfile1").integrity }'
rel='stylesheet'>`;
```


For additional implementation details see [https://github.com/neftaly/grunt-sri](https://github.com/neftaly/grunt-sri) or peruse [our pull request](https://github.com/jquery/codeorigin.jquery.com/pull/22/files) to code.jquery.com, specifically [this diff](https://github.com/jquery/codeorigin.jquery.com/pull/22/files#diff-35b4a816e0441e6a375cd925af50752cR281).

#### Beyond JavaScript / Node.js

If you prefer to keep it old school with a `Makefile`

, no problem. Assuming you are using a unix-like environment, you can skip using node modules and do something like this:

```
# Makefile
generate:
cat FILENAME.js | openssl dgst -sha256 -binary \
| openssl enc -base64 -A
```


For examples of generating SRI SHAs in various other platforms, see [this Gist](https://gist.github.com/jmervine/ae1bace0fe37dce75b90ec3e9592771c).

#### Conclusion

Subresource Integrity is a very simple way to secure static assets hosted on servers you have no control over. There are several tools that allow you to easily integrate SRI support into your build process(es). Modern website/application developers should not only do their part in implementing SRI, but discuss it with their peers explaining the benefits.

Big thanks to [Frederik Braun](https://twitter.com/freddyb), [Jonathan Kingston](https://twitter.com/kingstontime), [Francois Marier](https://twitter.com/fmarier) & [Havi Hoffman](https://twitter.com/freshelectrons) for their help reviewing this article.

## About
[
Justin Dorfman ](https://www.justindorfman.com)

Justin is [MaxCDN](https://www.maxcdn.com)’s Director of Developer Relations and is responsible for evangelizing the company’s technologies and championing the needs of developers who use the network. He started [BootstrapCDN](https://www.bootstrapcdn.com/) in 2012 and is heavily involved with the FOSS community contributing to Bootstrap, Font Awesome, Grunt, Ionic, jQuery Foundation, Twemoji, Nginx & GNU Bash.

## About
[
Joshua Mervine ](http://www.mervine.net)

Joshua is an SRE at Heroku with over 20 years of experience Development and Systems Engineering. He took over the lead developer role on BootstrapCDN in 2013 and is heavily involved in open source and the community, both through his own projects and his contributions to others.

## 11 comments

oxdefApril 12th, 2016 at 12:48Jonathan KingstonApril 12th, 2016 at 14:16AndersApril 12th, 2016 at 13:25Jonathan KingstonApril 12th, 2016 at 14:08AndersApril 12th, 2016 at 14:19Jonathan KingstonApril 12th, 2016 at 14:43AndersApril 13th, 2016 at 15:25Jonathan KingstonApril 14th, 2016 at 02:49FrederikApril 13th, 2016 at 05:16AndersApril 13th, 2016 at 15:38Jonathan KingstonApril 14th, 2016 at 02:55