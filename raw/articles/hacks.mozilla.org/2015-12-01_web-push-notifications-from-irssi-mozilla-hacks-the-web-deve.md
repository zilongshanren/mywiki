---
title: Web Push notifications from Irssi – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/12/web-push-notifications-from-irssi/
author: Marco Castelluccio
published: '2015-12-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Our main communication tool at Mozilla is IRC. I’m running an IRC client called ** Irssi** under

`screen`

on a server constantly connected to the network. It’s a close-to-perfect solution with only two outstanding issues for me. One is the lack of emoji characters (I can live with that). The other is more important: there is no easy way to install a solution to receive notifications. This gave us the idea for a small project — to build a generic server for sending notifications that could work alongside the Irssi client.## Overview of the application

**Mercurius** is a generic push server that lets developers bring Web Push into their own native/web applications. Subscription management is entirely handled by Mercurius; the user registers on the Mercurius website and receives a token that other applications can use to send customized push notifications via a REST API.

Mercurius uses the [web-push](https://github.com/marco-c/web-push/) Node.js library to handle communication with the [push service](https://tools.ietf.org/html/draft-ietf-webpush-protocol-02) and takes care of the necessary payload encryption.

You can [find the code on GitHub](https://github.com/marco-c/mercurius/releases/tag/blog-post).

![irssinotification](../../assets/bde6ac58cf3cec45.gif)


There are four actors in our application:

- The
*user agent (browser)*, which subscribes for push notifications on a push service and sends the subscription information to the application server (Mercurius); - The
*push service*; - The
*Mercurius application server*, which maintains a list of the user subscriptions and sends push notifications to users via the push service; - A
*Mercurius client*(in this case it’s an Irssi plugin), which uses a token (given to the user by the Mercurius server) to send the user push notifications via the Mercurius server.

![Architecture diagram](../../assets/cf4d3440ff8f1a8c.png)


## Subscribing to push notifications

We needed to build a web page to allow users to subscribe for push notifications. The PushManager interface of the [Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API) comes to our aid. It can be accessed through a service worker registration:

```
navigator.serviceWorker.register('service-worker.js')
.then(function(registration) {
// registration.pushManager
```


It provides a function to subscribe the user and a function to get an already existing subscription. We’ll try to get an existing subscription first and, if that fails, we’ll re-register the user:

```
return registration.pushManager.getSubscription()
.then(function(subscription) {
if (subscription) {
return subscription;
}
return registration.pushManager.subscribe({ userVisibleOnly: true })
.then(function(newSubscription) {
return newSubscription;
});
});
```


Once we have the subscription (comprised of an endpoint URL on the push service and a user’s public key), we can send its info to the server, which will then use it to send the user a notification.

The [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) sends the POST request to the server (just to spice up the demo a bit):

```
var key = subscription.getKey ? subscription.getKey('p256dh') : '';
fetch('./register', {
method: 'post',
headers: {
'Content-type': 'application/json'
},
body: JSON.stringify({
endpoint: subscription.endpoint,
key: key ? btoa(String.fromCharCode.apply(null, new Uint8Array(key))) : '',
}),
});
```


## Keeping the subscription up to date

The user’s subscription to the push service is periodically refreshed, or, in some cases invalidated (see the Push Quota recipe in the ServiceWorker Cookbook for an in-depth look), so we need to always keep the server up to date with the user subscription information.

To do so, we’ll add an event listener in the service worker for the ‘**pushsubscriptionchange**‘ event:

```
self.addEventListener('pushsubscriptionchange', function(event) {
// Handle the event by re-subscribing the user and sending the new info to the server
```


This way, when the subscription changes, we notify the server of the new endpoint URL and the new key.

## Showing visual notifications

Once our user is subscribed to the push service and to the Mercurial server, we can send push messages and show visual notifications. The Irssi plugin will send a POST request to the Mercurius server, asking it to send the notification to the user. The Mercurius server sends the notification to the push service, which then delivers the notification to the browser. The payload of the push notification is sent to the endpoint URL with some clever crypto. It provides the actual parameters for displaying the notification. (You can read more here about the encryption: [https://tools.ietf.org/html/draft-thomson-webpush-encryption-01](https://tools.ietf.org/html/draft-thomson-webpush-encryption-01)).

The push notification triggers a ‘**push**‘ event in the service worker registered for the page, re-launching the service worker if it it is no longer active.

So, to show something to the user, we just need to handle the ‘**push**‘ event in our service worker:

```
self.addEventListener('push', function(event) {
var data = event.data ? event.data.json() : null;
var title = data ? data.title : 'Mercurius';
var body = data ? data.body : 'Notification';
event.waitUntil(self.registration.showNotification(title, {
body: body,
}));
});
```


As we mentioned earlier, we’re using the payload of the push message (for reference, see the [Push Payload recipe](https://serviceworke.rs/push-payload.html) in Mozilla’s Service Worker Cookbook) to pass the parameters of the notification from the Irssi plugin (or any other Mercurius client) to the service worker. Here you can see it working from front-end:

## Testing with Mocha

We have implemented a few [BDD](https://en.wikipedia.org/wiki/Behavior-driven_development) tests with the [Mocha framework](http://mochajs.org/) to verify that the Mercurius server works correctly. We’ve also employed [istanbul](http://gotwarlost.github.io/istanbul/) to measure code coverage and guide our test writing activity.

Simply run `npm test`

to see its output.

## Deployment

Deploying the server to [Heroku](https://www.heroku.com/) is really simple. We have chosen to make [Travis CI](https://travis-ci.org/), our continuous integration service, perform the deploy after building Mercurius and a successful test run. Here’s our self-explanatory [YAML](https://en.wikipedia.org/wiki/YAML) configuration file for Travis CI:

```
language: node_js
node_js:
- '0.12'
- '4'
deploy:
provider: heroku
api_key:
secure:
app: mozcurius
skip_cleanup: true
on:
repo: marco-c/mercurius
branch: master
node: '4'
```


We use *skip_cleanup* because we want to publish our build artifacts to Heroku.

The (encrypted) API key is specific to your user account and can be created using the Heroku and Travis CI command line clients:

```
travis encrypt $(heroku auth:token) --add deploy.api_key
```



For more information about integrating Heroku deployment in Travis CI, see [https://docs.travis-ci.com/user/deployment/heroku/](https://docs.travis-ci.com/user/deployment/heroku/).

## Irssi client

The role of the Irssi Mercurius client is to send a notification to the Mercurius server every time the user is mentioned. I’ve modified an existing script, which saves this info to a file, so that it now saves and sends the request to the Mercurius server. After loading the script, a new command is registered in Irssi. It’s called `/mercurius`

, and it sets the token, host (if you decide to run your own), and intensity of the notifications. There is also a method to stop and start again notifications at will.

The plugin is written in Perl. Sending requests to the Mercurius server happens in the *sub notify* using the built-in *HTTP::Tiny* module. I’ve used the *request* method instead of *post* for backwards compatibility with older Perl versions.

The subroutine responsible for sending the notification request is called `notify`

. Description is given here inside the comments.

```
use HTTP::Tiny;
use JSON::PP;
# [...]
sub notify {
if ($enabled) {
my ($text) = @_;
# $host is a global variable set with "set_host" command
my $url = $host . '/notify';
my $http = HTTP::Tiny->new();
my $data = encode_json {
# $token is a global variable set with "set_token" command
"token" => $token,
"payload" => {
"title" => "IRSSI",
"body" => $text
}
};
my $response = $http->request('POST', $url, {
content => $data,
headers => {"Content-Type" => "application/json"}
}
);
# [...]
}
}
```


The plugin is [placed on GitHub along with install instructions](https://github.com/zalun/mercurius-irssi).

### Usage

`/mercurius set_token {TOKEN}`


Use it to set the token. You will receive a notification confirming that it has been set.

`/mercurius set_host {HOST}`


Default value is `"https://mozcurius.herokuapp.com"`

. Please note that the trailing slash has been removed.

`/mercurius set_intense {0/1}`


Switches on/off intense mode (default `0`

). With intense mode (`1`

) all of the notifications are sent. Otherwise (default) if the user is in an active private window only the first message from that window will send a notification.

`/mercurius stop`

and `/mercurius start`

are self explanatory.

## About
[
Marco Castelluccio ](https://marco-c.github.io/)

Marco is a passionate Mozilla hackeneer (a strange hybrid between hacker and engineer), who contributed and keeps contributing to Firefox, PluotSorbet, Open Web Apps. More recently he has been working on using machine learning and data mining techniques for software engineering (testing, crash handling, bug management, and so on).

## About Piotr Zalewa

Piotr Zalewa is a Senior Web Developer at Mozilla's Dev Ecosystem team. Working on web apps. He is the creator of JSFiddle.

## 5 comments

Antoine TurmelDecember 1st, 2015 at 12:46Mikhail KhvoinitskyDecember 3rd, 2015 at 08:49Piotr ZalewaDecember 3rd, 2015 at 09:04Jesús PeralesDecember 15th, 2015 at 16:04Marco CastelluccioDecember 17th, 2015 at 08:48