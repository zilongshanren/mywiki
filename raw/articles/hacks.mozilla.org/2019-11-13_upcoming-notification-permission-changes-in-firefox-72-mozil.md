---
title: Upcoming notification permission changes in Firefox 72 – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2019/11/upcoming-notification-permission-changes-in-firefox-72/
author: Anne van Kesteren
published: '2019-11-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Notifications. Can you keep count of how many websites or services prompt you daily for permission to send notifications? Can you remember the last time you were thrilled to get one?

Earlier this year we decided to reduce the amount of unsolicited notification permission prompts people receive as they move around the web using the Firefox browser. We see this as an intrinsic part of Mozilla’s commitment to putting people first when they are online.

In preparation, we ran a series of studies and experiments. We wanted to understand how to improve the user experience and reduce annoyance. In response, we’re now making some changes to the workflow for how sites ask users for permission to send them notifications. **Firefox will require explicit user interaction on all notification permission prompts, starting in Firefox 72**.

For the full background story, and details of our analysis and experimentation, please read [Restricting Notification Permission Prompts in Firefox](https://blog.mozilla.org/futurereleases/2019/11/04/restricting-notification-permission-prompts-in-firefox/). Today, we want to be sure web developers are aware of the upcoming changes and share best practices for these two key scenarios:

- How to guide the user toward the prompt.
- How to acknowledge the user changing the permission.

We anticipate that some sites will be impacted by changes to the user flow. We suspect that many sites do not yet deal with the latter in their UX design. Let’s briefly walk through these two scenarios:

## How to guide the user toward the prompt

Ideally, sites that want permission to notify or alert a user already guide them through this process. For example, they ask if the person would like to enable notifications for the site and offer a clickable button.

```
document.getElementById("notifications-button").addEventListener("click", () => {
Notification.requestPermission().then(setupNotifications);
});
```


Starting with Firefox 72, the notification permission prompt is gated behind a user gesture. We will not deliver prompts on behalf of sites that do not follow the guidance above. Firefox will instantly reject the promise returned by [ Notification.requestPermission()](https://developer.mozilla.org/en-US/docs/Web/API/Notification/requestPermission) and

[. However, the user will see a small notification permission icon in the address bar.](https://developer.mozilla.org/en-US/docs/Web/API/PushManager/subscribe)

`PushManager.subscribe()`

Note that because `PushManager.subscribe()`

requires a `ServiceWorkerRegistration`

, Firefox will carry user-interaction flags through promises that return `ServiceWorkerRegistration`

objects. This enables [popular examples](https://developer.mozilla.org/en-US/docs/Web/API/PushManager/subscribe#Example) to continue to work when called from an event handler.

Firefox shows the notification permission icon after a successful prompt. The user can select this icon to make changes to the notification permission. For instance, if they decide to grant the site the permission, or change their preference to no longer receive notifications.

## How to acknowledge the user changing the permission

When the user changes the notification permission through the notification permission icon, this is exposed via the Permissions API:

```
navigator.permissions.query({ name: "notifications" }).then(status => {
status.onchange = () => potentiallyUpdateNotificationPermission(status.state);
potentiallyUpdateNotificationPermission(status.state);
}
```


We believe this improves the user experience and makes it more consistent. And allows to align the site interface with the notification permission. Please note that the code above works in earlier versions of Firefox as well. However, users are unlikely to change the notification permission dynamically in earlier Firefox releases. Why? Because there was no notification permission icon in the address bar.

Our studies show that users are more likely to engage with prompts that they’ve interacted with explicitly. We’ve seen that through *pre-prompting* in the user interface, websites can inform the user of the choice they are making before presenting a prompt. Otherwise, unsolicited prompts are denied in over 99% of cases.

We hope these changes will lead to a better user experience for all and better and healthier engagement with notifications.

## About
[
Anne van Kesteren ](https://annevankesteren.nl/)

Standards person with an interest in privacy & security boundaries, as well as web platform architecture · he/him

## About
[
Johann Hofmann ](http://johannh.me)

Firefox Security & Privacy Engineer

## 9 comments

TrevorNovember 13th, 2019 at 07:45Anne van KesterenNovember 14th, 2019 at 00:02TrevorNovember 15th, 2019 at 15:02Martin BNovember 13th, 2019 at 08:28Anne van KesterenNovember 14th, 2019 at 00:06jr conlinNovember 13th, 2019 at 16:28Anne van KesterenNovember 14th, 2019 at 00:17James BrowningNovember 13th, 2019 at 23:11JordanNovember 14th, 2019 at 05:32