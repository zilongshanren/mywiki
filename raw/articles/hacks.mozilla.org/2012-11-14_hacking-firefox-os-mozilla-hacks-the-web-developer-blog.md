---
title: Hacking Firefox OS – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/11/hacking-firefox-os/
author: Luca Greco
published: '2012-11-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This blog post is written by Luca Greco, a Mozilla community member who loves to hack, especially on JavaScript and other web-related technologies.*

A lot of developers are already creating mobile applications using Web technologies (powered by containers like Phonegap/Cordova as an example),

usually to develop cross platform applications or leverage their current code and/or expertise.

As a consequence Firefox OS is a very intriguing project for quite a few reasons:

- Web apps have first class access to the platform
- Web apps are native (less abstraction levels and better performance)
- Platform itself is web-based (and customizable using web technologies)

Mobile platforms based on web technologies can be the future, and we can now touch it, and even more important, we can help to define it and push it further thanks to a platform (Firefox OS) developed completely in the open. I could not resist the temptation, so I started to dive into Firefox OS code, scrape it using MXR and study [documentation on the wiki](https://developer.mozilla.org/docs/Mozilla/Firefox_OS).

## Hack On Firefox OS

In a couple of weeks I was ready to put together an example app and an unofficial presentation on the topic (presented at the local LinuxDay 2012):

Example App: Chrono for Gaia (user interface of Firefox OS):

During this presentation I tried to highlight an important strength I believe Firefox OS and Firefox have in common:

“It’s not a static build, it’s alive! a truly interactive environment. Like the Web”


I can telnet inside a B2G instance and look around for interesting stuff or run JavaScript snippets to interactively experiment the new WebAPIs. There’s more than one option to get a remote JavaScript shell inside B2G:

[Marionette](https://developer.mozilla.org/docs/Mozilla/Boot_to_Gecko/Setting_Up_Marionette_for_B2G), mainly used for automated tests[B2G Remote JS Shell](http://mxr.mozilla.org/mozilla-central/search?string=b2g.remote-js), a minimal JavaScript shell optionally exposed on a tcp port (which I think will be deprecated in future releases)

Unfortunately these tools currently lack integrated inspection utils (e.g. console.log/console.dir or MozRepl repl.inspect and repl.search), so during the presentation I opted to install [MozRepl](http://github.com/bard/mozrepl) as extension on the B2G simulator, but in the last weeks [Remote WebConsole landed into Firefox Nightly](http://starkravingfinkle.org/blog/2012/10/firefox-for-android-remote-web-console-is-here/).

Obviously RemoteWebConsole isn’t mature yet, so we need to be prepared for bugs and silent errors (e.g. we need to be sure B2G has “remote debugger” enabled or it will fail without errors), but it features objects inspection, network progress logging, JavaScript and CSS errors (like our local Firefox WebConsole).

## Developing for Firefox OS

In my experience, developing an OpenWebApps for Firefox OS isn’t really different from hybrid applications based on Phonegap-like technologies:

We’ll try to code and test major parts of our application on desktop browsers and their development tools, using mockups/shims in place of native functionalities. But during my 2 weeks of studying, I’ve collected an interesting amount of working notes that can be useful to share, so in next sections I’m going to:

- Review development workflow and tools
- Put together a couple of useful tips and tricks
- Release to the public (independently and in the
[Mozilla Marketplace](https://marketplace.mozilla.org/))

As an example app, I’ve chosen to create a simple chronometer:

![](../../assets/27a44444ff5b3801.png)


### Workflow and Tools

During this experience my toolset was composed by:

-
[VoloJS](http://volojs.org)– development server and automated production build (minify js/css, generate manifest.appcache) -
[Firefox Nightly](http://nightly.mozilla.org/)Web Developer Tools – Markup View, Tilt, Responsive Design View and Web Console -
[R2D2B2G](https://hacks.mozilla.org/2012/10/r2d2b2g-an-experimental-prototype-firefox-os-test-environment/)– integrate/interoperate with B2G from a Firefox Addon

Using Volo, I can test my app from volo integrated http server, split JavaScript code into modules using [Require.js](http://requirejs.org/), and finally generate a production version, minified and optionally equipped of an auto-generated manifest.appcache.

During my development cycle I iteratively:

- Make a change
- Reload and inspect changes on desktop browser
- Try changes on b2g-simulator using R2D2B2G
- Debug on desktop browser or remotely on b2g-simulator
- Restart the loop :-)

Using my favorite desktop browser (Firefox, obviously :-P), I have the chance to use very powerful inspection/debugging tools, not usually available on mobile web-runtimes:

- Markup Viewer to inspect and change DOM tree state
- Styles Editor to inspect and change CSS properties
- Tilt to check where offscreen dom elements are located
- Web Console to inspect and change the JavaScript environment

Thanks to new Mozilla projects like “Firefox OS” and “Firefox for Android”, more and more of these tools are now available as “Remote Web Tools” and can be connected to a remote instance.

### Tips and Tricks

#### Gaia UI Building Blocks

Gaia isn’t only a B2G UI implementation, it’s a design style guide and a collection of pre-built CSS styles which implements these guidelines:

-
[Gaia Design Building Blocks – Mozilla Wiki](https://wiki.mozilla.org/Gaia/Design/BuildingBlocks) -
[Gaia Building Blocks – Live Preview](http://mozilla-b2g.github.com/Gaia-UI-Building-Blocks/index.html) -
[Gaia UI Building Blocks – Github Repo](http://github.com/mozilla-b2g/Gaia-UI-Building-Blocks)

We can import components’ styles from the repo above and apply them to our app to achieve a really nice native Look & Feel on Firefox OS. Some components are not stable, which means they can interact badly with other components’ styles or doesn’t work perfectly on all platforms (e.g. Firefox Desktop or Firefox for Android), but usually it’s nothing we can’t fix by using some custom and more specific CSS rules.

It doesn’t feel like a mature and complete CSS framework (e.g. Bootstrap) but it’s promising and I’m sure it will get better.

Using Responsive Design View we can test different resolutions (and orientations), which helps to reach a good and consistent result even without test our app on Firefox OS or Firefox for Android devices, but we should keep an eye on dpi related tweaks, because we currently can’t fully recognize how it will looks using our Desktop browser.

#### App Panels

A lot of apps needs more than one panel, so first I looked inside official Gaia applications to understand how native apps implements this almost mandatory feature. This is how Gaia Clock application appear from a “Tilt” eye:

![](../../assets/1cd4b5ed15e256a0.png)


Panels are simple DOM elements (e.g. a section or a div tag) initially positioned offscreen and moved on screen using a CSS transition:

In the “Chrono” app, you will find this strategy in the Drawer (an unstable Gaia UI Building Block):

![](../../assets/0ac8d7d9f7da0df2.png)


and in the Laps and About panels (combinated with [:target pseudo class](https://developer.mozilla.org/docs/CSS/:target)):

![](../../assets/6c2f02820578f52d.png)


#### The Fascinating -moz-element trick

This is a very fascinating trick, used in the time selector component on Firefox OS:

![](../../assets/e394ce20b1278385.png)


and in the Markup View on Firefox Nightly Desktop (currently disabled):

Thanks to this non-standard CSS feature we can use a DOM Element as background image on another one, e.g. integrating a complex offscreen visual component into the visible space as a single DOM element.

![](../../assets/06f9cf21c932bddb.png)


##### Fragments from index.html



```
...
```




...

##### Fragments from chrono.css



```
...
/* NOTE: set fixed size on empty visible elements
[role="chrono"] > p span {
width: -moz-calc(100% / 3);
height: 100%;
...
}
...
/* NOTE: move real offscreen DOM elements
[role="chrono"] > div {
position: absolute;
left: -moz-calc((100%) + 10px);
...
}
...
```

##### Fragments from chrono.js



```
...
// NOTE: generate seconds, minutes and hours elements
for (var i=0; i<60; i++) {
var txt = i < 10 ? "0"+i : i;
var el = $("
```

Using `-moz-element`

and `-moz-calc`

(compute components size into CSS rules and already included into CSS3 as `calc`

) is really simple, but you can learn more on the subject on MDN:

### Release to the public

#### WebApp Manifest

During our development cycle we install our application into B2G simulator using an R2D2B2G menu option, so we don’t need a real manifest.webapp, but we have to create a real one when ready for a public release or to release it to test users.

Creating a manifest.webapp is not difficult, it’s only a simple and well documented json file format: [App/Manifest on MDN](https://developer.mozilla.org/docs/Apps/Manifest).

Debugging problems related to this manifest file is still an unknown territory, and some tips can be useful:

- If the manifest file contains a syntax error or cannot be downloaded and error will be silently reported into the old Error Console (no, they will not be reported inside the new Web Console)
- If your application is accessible as a subdirectory in its domain, you have to include this path in resources path specified inside the manifest (e.g. launch_path, appcache_path, icons), more on this later
- You can add an uninstall button in your app to help you as a developer (and test users) to uninstall your app in a platform independent way (because “how to uninstall” an installed webapp will be different if you are on Desktop, Android or Firefox OS)

Using OpenWebApps APIs, I added to “Chrono” some code to give users the ability to install itself:

#### Install an app from your browser to your desktop system



```
/* Mozilla/Firefox installation */
var base = location.href.split("#")[0]; // WORKAROUND: remove hash from url
base = base.replace("index.html",""); // WORKAROUND: remove index.html
install.mozillaInstallUrl = base + '/manifest.webapp';
install.mozillaInstall = function () {
var installRequest = navigator.mozApps.install(install.mozillaInstallUrl);
installRequest.onsuccess = function (data) {
triggerChange('installed');
};
installRequest.onerror = function (err) {
install.error = err;
triggerChange('error');
};
};
```

Check if it’s already installed (as a webapp runtime app or a self-service installer in a browser tab):



```
function get_chrono_installed(success,error) {
try1();
// TRY1: get our application management object using getSelf()
// this works correctly when running into the webapp runtime container
function try1() {
req1 = navigator.mozApps.getSelf();
req1.onsuccess = function () {
if (req1.result === null) {
try2();
} else {
success(req1.result);
}
};
req1.onerror = function () {
try2();
}
}
// TRY1: get our application management object using getInstalled()
// this works correctly when running as "self service installer"
// in a Firefox browser tab
function try2() {
req2 = navigator.mozApps.getInstalled();
req2.onsuccess = function () {
var result = null;
var myorigin = window.location.protocol + "//" + window.location.host;
if (req2.result !== null) {
req2.result.forEach(function (app) {
if (app.origin == myorigin)
result = app;
});
}
success(result);
}
req2.onerror = error;
}
}
```

On a Linux Desktop, when you install an OpenWebApp from Firefox, it will create a new launcher (an “.desktop” file) in your “.local/share/applications” hidden directory:

```
$ cat ~/.local/share/applications/owa-http;alcacoop.github.com.desktop
[Desktop Entry]
Name=Chrono
Comment=Gaia Chronometer Example App
Exec="/home/rpl/.http;alcacoop.github.com/webapprt-stub"
Icon=/home/rpl/.http;alcacoop.github.com/icon.png
Type=Application
Terminal=false
Actions=Uninstall;
[Desktop Action Uninstall]
Name=Uninstall App
Exec=/home/rpl/.http;alcacoop.github.com/webapprt-stub -remove
```

As you will notice, current conventions (and implementation) supports only one application per domain, if you give a look inside the hidden directory of our installed webapp you will find a single webapp.json config file:

$ ls /home/rpl/.http;alcacoop.github.com/ Crash Reports icon.png profiles.ini webapp.ini webapp.json webapprt-stub z8dvpe0j.default

Reasons for this limitations are documented on MDN: [FAQs about app manifests](https://developer.mozilla.org/docs/Apps/FAQs/About_app_manifests)

To help yourself debugging problems when you app is running inside the webapp runtime you can run it from command line and enable the old (but still useful) Error Console:

```
$ ~/.http;alcacoop.github.com/webapprt-srt -jsconsole
```

Uninstalling an OpenWebApp is really simple, you can manually removing it using the “wbapprt-stub” executable in the “OpenWebApp hidden directory” (platform dependent method):

```
$ ~/.http;alcacoop.github.com/webapprt-stub -remove
```

Or from JavaScript code, as I’ve done in “Chrono” to give users the ability to uninstall the app from a Firefox Browser tab:



```
function uninstall_error() { $('.install-error').html("UNINSTALL ERROR: retry later."); }
function uninstall_success() {
install.state = "uninstalled";
updateInstallButton();
$('.install-error').html("UNINSTALL: app removed.");
}
function uninstall() {
get_chrono_installed(function (app) {
var req2 = app.uninstall();
req2.onsuccess = uninstall_success;
req2.onerror = uninstall_error;
}, uninstall_error);
return false;
}
```

#### AppCache Manifest

This is a feature integrated a lot of time ago into major browsers, but now, thanks to OpenWebApps, it’s becoming really mandatory: without a manifest.appcache, and proper JavaScript code to handle upgrades, our WebApp will not works offline correctly, and will not feel like a real installed application.

Currently Appcache it’s a kind of black magic and it deserves a “Facts Page” like Chuck Norris: [AppCacheFacts](http://appcachefacts.info).

Thanks to [volo-appcache](https://github.com/volojs/volo-appcache) command, generate a manifest.appcache it’s simple as a single line command:

```
$ volo appache
...
$ ls -l www-build/manifest.appcache
...
$ tar cjvf release.tar.bz2 www-build
...
```

Unfortunately when you need to debug/test your manifest.appcache, you’re on your own, because currently there isn’t any friendly debugging tool integrated into Firefox:

- appcache downloading progress (and errors) are not currently reported into the WebConsole
- appcache errors doesn’t contains an error message/description
- Firefox for Android and Firefox OS doesn’t have an UI to clean your applicationCache

Debug appcache problems can be very tricky, so here a couple of tricks I learned during this experiment:

- Subscribe every window.applicationCache events (‘error’, ‘checking’, ‘noupdate’, ‘progress’, ‘downloading’, ‘cached’, ‘updateready’ etc) and log all received events / error messages during development and debugging
- Add upgrade handling code in your first public release (or prepare yourself to go house by house to help your users to upgrade :-D)
- On Firefox for Desktop you can remove applicationCache from the Preferences dialog
- Analyze server side logs to understand where the “appcache updating” is stuck
-
Activate logging on applicationCache internals when you run Firefox or B2G to understand why it’s stuck

(from https://mxr.mozilla.org/mozilla-central/source/uriloader/prefetch/nsOfflineCacheUpdate.cpp#62):export NSPR_LOG_MODULES=nsOfflineCacheUpdate:5 export NSPR_LOG_FILE=offlineupdate.log firefox -no-remote -ProfileManager & tail -f offlineupdate.log -1614710976[7fc59e91f590]: nsOfflineCacheUpdate::Init [7fc55959ce50] -1614710976[7fc59e91f590]: nsOfflineCacheUpdate::AddObserver [7fc56a9fcc08] to update [7fc55959ce50] -1614710976[7fc59e91f590]: nsOfflineCacheUpdate::AddObserver [7fc55c3264d8] to update [7fc55959ce50] -1614710976[7fc59e91f590]: nsOfflineCacheUpdate::Schedule [7fc55959ce50] -1614710976[7fc59e91f590]: nsOfflineCacheUpdateService::Schedule [7fc57428dac0, update=7fc55959ce50] -1614710976[7fc59e91f590]: nsOfflineCacheUpdateService::ProcessNextUpdate [7fc57428dac0, num=1] -1614710976[7fc59e91f590]: nsOfflineCacheUpdate::Begin [7fc55959ce50] -1614710976[7fc59e91f590]: nsOfflineCacheUpdate::NotifyState [7fc55959ce50, 2] -1614710976[7fc59e91f590]: 7fc559d0df00: Opening channel for http://html5dev:8888/gaia-chrono-app/manifest.appcache -1614710976[7fc59e91f590]: loaded 3981 bytes into offline cache [offset=0] -1614710976[7fc59e91f590]: Update not needed, downloaded manifest content is byte-for-byte identical -1614710976[7fc59e91f590]: done fetching offline item [status=0] -1614710976[7fc59e91f590]: nsOfflineCacheUpdate::LoadCompleted [7fc55959ce50] -1614710976[7fc59e91f590]: nsOfflineCacheUpdate::NotifyState [7fc55959ce50, 3] -1614710976[7fc59e91f590]: nsOfflineCacheUpdate::Finish [7fc55959ce50] -1614710976[7fc59e91f590]: nsOfflineCacheUpdateService::UpdateFinished [7fc57428dac0, update=7fc55959ce50] -1614710976[7fc59e91f590]: nsOfflineCacheUpdateService::ProcessNextUpdate [7fc57428dac0, num=0] -1614710976[7fc59e91f590]: nsOfflineCacheUpdate::NotifyState [7fc55959ce50, 10] -1614710976[7fc59e91f590]: nsOfflineCacheUpdate::RemoveObserver [7fc56a9fcc08] from update [7fc55959ce50] -1614710976[7fc59e91f590]: nsOfflineCacheUpdate::RemoveObserver [7fc55c3264d8] from update [7fc55959ce50]


![](../../assets/788cb4eefd5da5eb.png)


Adding applicationCache support to “Gaia Chrono App”, I used all this tricks to finally discover Firefox didn’t send me an “updateready” event, so I was not able to tell the user to reload the page to start using the new (and already cached) version. With a better understanding of the problem, and searching in the code on MXR and in tickets on Bugzilla, I finally found an existing ticket in the bugtracker: [Bug 683794: onupdateready event not fired when an html5 app cache app is updated](https://bugzilla.mozilla.org/show_bug.cgi?id=683794).

Workaround this bug its really simple (simpler than tracking it down): add a dummy “updateready” listener on applicationCache object in a script tag to be sure it will be fired:



```
...
```

If you are going to start to use this feature (and soon or later you will), be prepared to:

- Implement as suggested from the standard
- Debug reason why it’s not behave as it should
- Search an existent bug or file a bug if it’s not reported (NOTE: this is really important!!! :-D)
- Find a workaround

This is definitely a features that needs more supports into web developer tools, because a regular web developer doesn’t want to debug his webapp from “browser internals” point of view.

#### Port to Firefox for Android

An interesting feature of OpenWebApps is “they can be installed on any supported platform without (almost) any changes”. As an example we can install our “Chrono” App on our Desktop using Firefox Nightly and on Android using Firefox for Android Nightly.

In my own opinion, Firefox for Android can be a strategic platform for the future of OpenWebApps and even Firefox OS: Android is an already popular mobile platform and give developers the option to release their application on Firefox OS and Android from a single codebase is a big plus.

The only problem I faced porting “Chrono” App on Android was related to the different rendering behaviour of Firefox for Android (and as a consequence in the WebAppRT, which contains our application):

A GeckoScreenshot service will force a repaint only when and where it detects changes. This feature interacts badly with the -moz-element trick and it needs some help to understand what really needs to be repainted:



```
// Firefox For Android: force redraw workaround
define(function (require) {
var is_firefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1;
var is_android = navigator.userAgent.toLowerCase().indexOf("android") > -1;
var n = document.createTextNode(' ');
return {
force_redraw: function (element) {
if(is_firefox && is_android) {
rafId = window.mozRequestAnimationFrame(
function(){
element.appendChild(n);
n.parentNode.removeChild(n)
window.mozCancelRequestAnimationFrame(rafId);
}
);
}
}
}
});
```

#### Release to the public

GitHub pages are a rapid and simple option to release our app to the public, even simpler thanks to the [volo-ghdeploy](https://github.com/volojs/volo-ghdeploy) command:

```
$ volo appcache && volo ghdeploy
...
```

When you deploy your OpenWebApp in a subdirectory of a given domain (e.g. using Github Pages) you should take into account that paths from manifest.webapp needs to be relative to your origin (protocol+host+port) and not your current url:



```
{
...
"launch_path": "/gaia-chrono-app/index.html",
"appcache_path": "/gaia-chrono-app/manifest.appcache",
...
"icons": {
"128": "/gaia-chrono-app/icons/chrono-128.png",
"64": "/gaia-chrono-app/icons/chrono-64.png",
"120": "/gaia-chrono-app/icons/chrono-120.png",
"60": "/gaia-chrono-app/icons/chrono-60.png"
},
...
}
```

We can install only a single OpenWebApp from every origin, so if you wants to deploy more than one app from your Github pages you need to configure Github pages to be exposed on a custom domain: [Github Help – Setting up a custom domain with pages](https://help.github.com/articles/setting-up-a-custom-domain-with-pages).

When our app is finally online and public accessible we can [submit it to the Mozilla Marketplace](https://marketplace.mozilla.org/developers/submit/app) and gain more visibility.

During the app submission procedure, your manifest.webapp will be validated and you will be warned if and how you need to tweak it to be able complete your submission:

- Errors related to missing info (e.g. name or icons)
- Errors related to invalid values (e.g. orientation)

As in other mobile marketplaces you should collect and fill into your submission:

- manifest.webapp url (NOTE: it will be read-only in the developer panel and you can’t change it)
- A longer description and feature list
- Short release description
- One or more screenshots

#### Mini Market

Mozilla Marketplace goal is to help OpenWebApps to gain more visibility, as other mobile store currently do for their ecosystem, but Mozilla named this project OpenWebApps for a reason:

Mozilla isn’t the only one that could create a Marketplace for OpenWebApps! Mozilla designed it to give us the same freedom we have on the Web, no more no less.

![](../../assets/f71d70e3c04a8796.png)


This is a very powerful feature because it open to developers a lot of interesting use cases:

- Carrier Apps Market on Firefox OS devices
- Non-Public Apps Installer/Manager
- Intranet Apps Installer/Manager

## Conclusion

Obviously Firefox OS and OpenWebApps aren’t fully completed right now (but improves at an impressive speed), Firefox OS doesn’t have an official released SDK, but the web doesn’t have an official SDK and we already use it everyday to do awesome stuff.

So if you are interested in mobile platforms and you wants to learn how a mobile platform born and grow, or you are a web developer and you wants more and more web technologies into mobile ecosystems…

You should seriously take a look at Firefox OS:

We deserve a more open mobile ecosystem, let’s start to push it now, let’s help OpenWebApps and Firefox OS to became our new powerful tools!

Happy Hacking!

## 12 comments

ArnauNovember 14th, 2012 at 02:49Luca GrecoNovember 14th, 2012 at 04:24Gerard BraadNovember 14th, 2012 at 07:49Luca GrecoNovember 14th, 2012 at 08:20Gerard BraadNovember 14th, 2012 at 08:36HTML5 SpainNovember 14th, 2012 at 09:35Saqib HussainNovember 19th, 2012 at 22:34JarodNovember 24th, 2012 at 07:45SofiNovember 30th, 2012 at 05:49NezDecember 10th, 2012 at 16:24Robert NymanDecember 10th, 2012 at 16:31Gerard BraadDecember 10th, 2012 at 20:12