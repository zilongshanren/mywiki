---
title: An overview of Containers for add-on developers – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/10/containers-for-add-on-developers/
author: Jonathan Kingston
published: '2017-10-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Containers enable users to log in to multiple accounts on the same site simultaneously, and give users the ability to segregate site data for improved privacy and security. At Firefox, we have been working on [Containers](https://blog.mozilla.org/tanvi/2017/10/03/update-firefox-containers/) for quite some time.

We started with platform work in the browser itself and added a basic user interface, then we moved on to a [Test Pilot experiment](https://testpilot.firefox.com/experiments/containers), in which we expanded the feature in an extension. Now we are graduating from Test Pilot and moving [our extension, Firefox Multi-Account Containers](https://addons.mozilla.org/en-US/firefox/addon/multi-account-containers/) to `addons.mozilla.org`.

In addition, we have updated the Firefox platform so that Containers can be managed by extensions. This means that developers have access to the necessary APIs to create new Container extensions. You can build new extensions on top of Container APIs to meet your needs and use cases! This already happening, with [a number of new extensions popping up on addons.mozilla.org](https://addons.mozilla.org/en-US/firefox/collections/jkt/container-tab-addons/).

This post introduces the [ contextualIdentities API](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/contextualIdentities), and walks through an example Container add-on with developers in mind.

## What are Containers?

Containers work by giving users the ability to place barriers on the flow of data across sites by [isolating cookies, indexedDB, localStorage, and caches](https://wiki.mozilla.org/Security/Contextual_Identity_Project/Containers#What_is_.28and_isn.27t.29_separated_between_Containers) within discrete browsing contexts. For instance, the browser storage associated with a user’s Personal Container is separated from the user’s Work Container. In this way, users can take on different identities depending on the context they are in – we refer to this as * contextual identity*.

The [ Cookie Store](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/cookies/CookieStore) is a key WebExtension API concept that represents storage isolation in the browser. In other browsers, the Cookie Store is used to differentiate private windows from regular windows. In Firefox, the Cookie Store will now also differentiate containers from each other.

Containers are unique to Firefox. These new APIs empower all developers to create new Privacy, Security and Tab management experiences that aren’t available in other browsers today.

## Setting up your manifest

To use the `contextualIdentities`

API, add the `“contextualIdentities”`

and `“cookies”`

permissions to your [ manifest.json](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json) so your extension can create Container Tabs associated with a Cookie Store.

```
"permissions": [
"cookies",
"contextualIdentities"
]
```


## Managing Container Tabs

The cookies permission provides access to the `cookieStoreId`

property needed for container tab management. The `contexualIdentities`

API methods return the `cookieStoreId`

that can be used for methods like `tab.create`

.

```
const containers = await browser.contextualIdentities.query({});
browser.tabs.create({
cookieStoreId: container[0].cookieStoreId,
url: "https://example.com"
});
```


This code creates a new tab that requests `https://example.com` using the `cookieStoreId`

associated with the user’s first container.

We can also use the `cookieStoreId`

to find all open Container Tabs associated with it:

`browser.tabs.query({cookieStoreId});`


## Monitoring for changes

Firefox and Container add-ons have the ability to create, update and remove containers. Extensions can now monitor these changes, alerting them to update their layout or management interfaces when the list of containers has changed.

To monitor for changes an extension can use the `onCreated`

, `onUpdated`

and `onRemoved`

listeners that are passed the modified container object.

```
const rebuildEvent = () => {
this.rebuildMenu();
};
browser.contextualIdentities.onRemoved.addListener((container) => {
this.removeContainer(container.cookieStoreId);
rebuildEvent();
});
browser.contextualIdentities.onUpdated.addListener(rebuildEvent);
browser.contextualIdentities.onCreated.addListener(rebuildEvent);
this.rebuildMenu();
```


Ensure that you use the `onRemoved`

listener to monitor for containers being removed by the user or by other extensions. This is especially important if your extension programmatically creates Container Tabs. For example, an extension may be configured to open a Shopping tab at 5pm every Friday to order beer from the local pub. But, if the user had previously deleted the Shopping tab, then their extension would likely be broken if it did not monitor for the remove event. A sad outcome.

## Keeping a consistent UI with colors & icons

We noticed that some Container add-ons uploaded to addons.mozilla.org were using different icons and looked very different than Firefox. In order to make life a little easier for extension developers, and more harmonious for users, we are now exposing the color code and an icon URL you can use to keep the colors you choose consistent with our palette. We think it’s a win-win.

On Firefox and across our Container extensions, we’ve optimized our color palette. Firefox designers have worked hard to choose colors that are visible within dark and light themes for accessibility reasons. When developers use CSS color keywords like “pink” and “blue” the result looks very different from the native colors Firefox provides.

Our updated APIs provide a public icon URL and Hex color code for the container’s color. Please use the `“colorCode”`

property within your extension, since in the future we may update the color codes to match changes in Firefox.

Consistency across Firefox and Container extensions is important to prevent bugs and provide a pleasing user experience. So, as with the color palette, we also provide URLs for our icons in the `iconUrl`

property. We encourage you to work with our assets to provide an easy-to-navigate user interface as we build together with Containers. And we thank you in advance.

In an extension, you can query for the current active containers like this:

```
const containers = await browser.contextualIdentities.query({});
containers.forEach((container) => {
console.log(container);
/* Object {
name: "Personal",
icon: "fingerprint",
iconUrl: "resource://usercontext-content/fingerprint.svg",
color: "blue",
colorCode: "#37adff",
cookieStoreId: "firefox-container-1"
} */
});
```


## Building an example Container add-on

To demonstrate how the Web Extension APIs for Containers can be used, I’ll now walk you through a [Container extension](https://github.com/jonathanKingston/containers-https) I made. This add-on gives the user the option to automatically redirect HTTP traffic to HTTPS based on a per container preference.

A user may decide to turn on HTTPS for the Banking Container, as seen above. Then when the user is in a Banking tab and visits [ http://example-bank.com](http://example.com), they will see that their tab actually ends up visiting the HTTPS page instead:


`https://example-bank.com`In the extension I wrote, I have the following functions:

```
createIcon(container) {
const icon = document.createElement("div");
icon.classList.add("icon");
const iconUrl = container.iconUrl || "img/blank-tab.svg";
icon.style.mask = `url(${iconUrl}) top left / contain`;
icon.style.background = container.colorCode || "#000";
return icon;
}
async createRow(container) {
const li = document.createElement("li");
li.appendChild(this.createIcon(container));
...
}
async rebuildMenu() {
const containers = await browser.contextualIdentities.query({});
...
containers.unshift({
cookieStoreId: "firefox-default",
name: "Default"
});
const rowPromises = [];
containers.forEach((container) => {
rowPromises.push(this.createRow(container));
});
...
}
```


In my `rebuildMenu`

function I query for all the containers the user has. Then I add an item for default Firefox tabs. When the code calls `createIcon`

with a container object, the `iconUrl`

and `colorCode`

properties can be used to get the associated icon. I use the icon as an SVG mask in CSS for the div, which results in the background color being used for the icon color, as it does in native Firefox menus.

## Making Container APIs reliable

Containers is a platform feature that has been disabled by default in Firefox Beta and general release. Until now, extension developers have had to inform the user to enable Containers in `about:preferences` in order to use the Container APIs. This changes with the release of Firefox Quantum (now in [Developer Edition](https://www.mozilla.org/en-US/firefox/developer/)). In Firefox Quantum, if you are a developer creating a Containers extension, your extension enables Containers. So now, when the user installs your extension, they don’t have that additional step. If they try to disable Containers, they will need to first disable your extension.

This provides an assurance to extension developers that [the Containers APIs will work](https://bugzilla.mozilla.org/show_bug.cgi?id=1397100) when the extension is installed. In the past, users could disable Containers at any point and break all Container-dependent extensions. Now they must disable the extension itself first, in order to disable Container Tabs.

We also made changes to the existing “query”, “get”, “update” and “remove” methods to be more “promise friendly”. Rather than resolving the promise with null or false values, we now reject promises when there are errors. In a situation where a container can’t be found or there is some internal error, we reject the promise of the API, so wrapping API calls in [ try...catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch) blocks allows your code to handle these errors:

```
async getContainer(cookieStoreId) {
let container;
try {
container = await browser.contextualIdentities.get(cookieStoreId);
} catch (e) {
/* Containers may be disabled, the API might have failed
or the container has been deleted. */
this.warnUser(e);
}
return container;
}
```


## Adding containers to existing extensions

Extensions often implement options for their users that aren’t ideal for all browsing activities. Specific extensions may provide privacy, security, or other user interface benefits and enhancements. Maybe the extension is a simple timer to track how often you look at cat gifs in social media during your work day. You might not need it after you’re done with your Work Container. Most extensions require the user to initiate an interaction, and it’s probably not necessary or beneficial for your extension to be “always on.”

Using Containers instead as an indicator of “context” simplifies the user experience of your extension. Extensions that add new features when a specific container is open, are more likely to be actively used because they hook into existing containers. For instance, HTTPS Everywhere’s “always https” option breaks many websites, but it’s always relevant and in context if it’s implemented by default when you’re in the Banking Container.

Whilst extensions can already change their behaviour based on URL, we feel that the security and privacy benefits of containers create new incentive for users to configure settings.

## Ideas for new Container extensions

We’re excited about the possibilities of Container extensions for providing context-based enhancements to browsing. When a user wants to be in a Work tab, an extension might be configured to block *not safe for work* pages. When a user doesn’t want to be reminded of work while at home, an extension may be configured to auto-delete a user’s Work history, but remember the Personal history.

For instance, extensions could:

- Autoload social pages into a Social tab
- Remove cookies on tab close when in a Work tab
- Block key logging scripts when in a Shopping tab
- Create unique containers for pinned tabs
- Load multiple versions of a website for QA testing, whilst still providing history and development tools embedded in the browser (instead of headless browser testing).

For example, we have already seen a number of Container extensions created:

[Containers on the go](https://addons.mozilla.org/en-US/firefox/addon/containers-on-the-go/)– gives users a temporary container that lasts for the lifetime of a tab. The temporary container simulates a private tab as containers are isolated from each other. As soon as the tab is thrown away, the container is deleted, which removes the cookies and other storage associated with it.[Cookie AutoDelete](https://addons.mozilla.org/en-US/firefox/addon/cookie-autodelete/)– has been modified to be progressively enhanced when containers are enabled, giving users the ability to change cookie deletion settings per container.[Conex](https://addons.mozilla.org/en-US/firefox/addon/conex/?)– a containers implementation of the[panorama](https://addons.mozilla.org/en-US/firefox/addon/tab-groups-panorama/)extension[And many more](https://addons.mozilla.org/EN-uS/firefox/collections/jkt/container-tab-addons/)

The Container WebExtension APIs allow developers to rewrite containers themselves. Developers can fork [our extension](https://github.com/mozilla/multi-account-containers/) and build improvements on top of it. If you’re looking for ideas, we have a large list of [open enhancement requests](https://github.com/mozilla/multi-account-containers/issues?q=is%3Aissue+is%3Aopen+sort%3Areactions-%2B1-desc+label%3Aenhancement) that extension developers could solve in their own extension using the provided APIs.

As you can see from all these changes and updates, we truly have [embraced the use of containers for tab management](https://github.com/mozilla/testpilot-containers/issues/336).

## Where next for Container extensions

We have a few more enhancements to make to our APIs. Here’s what’s in the queue:

[Web request to support](https://bugzilla.mozilla.org/show_bug.cgi?id=1391992)`cookieStoreId`

[Neater tab switching API from Container to Container](https://bugzilla.mozilla.org/show_bug.cgi?id=1323873)[Window opening API for](https://bugzilla.mozilla.org/show_bug.cgi?id=1393570)`cookieStoreId`

[Allow extension authors to make](https://bugzilla.mozilla.org/show_bug.cgi?id=1386673)which will allow non-container extensions to prompt the user to enable Container enhancements for their extension.`contextualIdentities`

API optional[Ability for an extension to specify the default tab](https://bugzilla.mozilla.org/show_bug.cgi?id=1403422)`cookieStoreId`


## Publishing your extension

### Terminology

When creating a container extension, we would recommend using “Container Tabs” as a term to explain the add-on instead of using the API name `contextualIdentities`

.

### Privacy best practices

If you’ve built an extension that uses Containers, but does so in a way that compromises user privacy, please disclose this. Let users know that your extension doesn’t meet the [isolation criteria designed for Containers](https://wiki.mozilla.org/Security/Contextual_Identity_Project/Containers#What_is_.28and_isn.27t.29_separated_between_Containers). For example, [moving tabs between containers introduces the risk](https://github.com/mozilla/testpilot-containers/wiki/Moving-between-containers) of exposing the user to additional trackers.

## Fixing issues with existing extensions

For your browser extensions to work in Firefox, please remember to check for the `cookieStoreId`

when creating and querying tabs. Some of the reported extension breakage that we’ve seen is due to extensions that copy tab urls and reopen them later without considering the `cookieStoreId`

the tab pertains to. Here’s an example of [the issue as reported on Github](https://github.com/mozilla/testpilot-containers/issues/831)

I want to thank the countless users, testers, coders and staff that have worked on Containers.

Hit us up with feedback: [containers@mozilla.com](mailto:containers@mozilla.com) or on [Discourse](https://discourse.mozilla.org/c/test-pilot/containers).

## About Jonathan Kingston

Front End Security for Firefox, working on HTTPS adoption, containers and content security.

## 12 comments

gregOctober 3rd, 2017 at 12:03Jonathan KingstonOctober 3rd, 2017 at 12:17Sam AdamsOctober 4th, 2017 at 11:55Jonathan KingstonOctober 4th, 2017 at 14:18WalterKOctober 3rd, 2017 at 18:18Jonathan KingstonOctober 3rd, 2017 at 20:09Graham PerrinOctober 3rd, 2017 at 21:39Jonathan KingstonOctober 4th, 2017 at 02:47glandiumOctober 3rd, 2017 at 22:02Jonathan KingstonOctober 4th, 2017 at 03:00glandiumOctober 4th, 2017 at 03:48Jonathan KingstonOctober 4th, 2017 at 14:12