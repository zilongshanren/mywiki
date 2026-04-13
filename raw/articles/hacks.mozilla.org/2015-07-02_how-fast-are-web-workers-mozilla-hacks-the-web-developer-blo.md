---
title: How fast are web workers? – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/07/how-fast-are-web-workers/
author: Guillaume Cedric Marty
published: '2015-07-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The next version of Firefox OS, the mobile operating system, will unleash the power of devices by taking full advantage of their multi-core processors. Classically, JavaScript has been executed on a single thread, but web workers offer a way to execute code in parallel. Doing so frees the browser of anything that may get in the way of the main thread so that it can smoothly animate the UI.

## A brief introduction to web workers

There are several types of web workers:

They each have specific properties, but share a similar design. The code running in a worker is executed in its own separate thread and runs in parallel with the main thread and other workers. The different types of workers all share a common interface.

### Web workers

Dedicated web workers are instantiated by the main process and they can communicate only with it.

### Shared workers

Shared workers can be reached by all processes running on the same origin (different browser tabs, iframes or other shared workers).

### Service workers

Service workers have gained a lot of attention recently. They make it possible to proxy a web server programmatically to deliver specific content to the requester (e.g. the main thread). One use case for service workers is to serve content while offline. Service workers are a very new API, not fully implemented in all browsers, and are not covered in this article.

In order to verify that web workers make Firefox OS run faster, we need to validate their speed by benchmarking them.

## The cost of creating web workers

This article focuses on Firefox OS. All measurement are made on a [Flame device](https://developer.mozilla.org/en-US/Firefox_OS/Phone_guide/Flame), powered by middle-end hardware.

The first set of benchmarks will look at the time it takes to create web workers. To do that, we set up a script that instantiates a web worker and sends a minimal message, to which the worker replies immediately. Once the response is received by the main thread, the time that the operation takes is calculated. The web worker is destroyed and the operation is repeated enough times to get a good idea of how long it takes on average to get a functional web worker. Instantiating a web worker is as easy as:

```
// Start a worker.
var worker = new Worker('worker-script.js');
// Terminate a worker.
worker.terminate();
```

The same method is applied to the creation of broadcast channel:

```
// Open a broadcast channel.
var channel = new window.BroadcastChannel('channel-name');
// Close a broadcast channel.
channel.close();
```

Shared workers can’t really be benchmarked here because once they are created, the developer can’t destroy them. The browser is entirely responsible for their lifetime. For that reason, we can’t create and destroy shared workers at will to get a meaningful benchmark.

Web workers take about **40 ms** to be instantiated. Also, this time is pretty stable with variations of only a few milliseconds. Setting up a broadcast channel is usually done within **1 ms**.

Under normal circumstances, the browser UI is refreshed at a rate of 60 frames per second. This means that no JavaScript code should run longer than the time needed by a frame, i.e., 16.66ms (60 frames per second). Otherwise, you may introduce jankiness and lag in your application.

Instantiating web workers is pretty efficient, but still may not fit in the time allocated for a single frame. That’s why it’s important to create as few web workers as possible and reuse them.

## Message latency

A critical aspect of web workers is having fast communication between your main thread and the workers. There are two different ways the main browser thread can communicate with a web worker.

### postMessage

This API is the default and preferred way to send and receive messages from a web worker. [postMessage()](https://developer.mozilla.org/en-US/docs/Web/API/Worker/postMessage) is easy to use:

```
// Send a message to the worker.
worker.postMessage(myMessage);
// Listen to messages from the worker.
worker.onmessage = evt => {
var message = evt.data;
};
```

### Broadcast Channel

This is a [newly implemented API](https://hacks.mozilla.org/2015/02/broadcastchannel-api-in-firefox-38/), only available in Firefox at the time of this writing. It lets us broadcast messages to all contexts sharing the same origin. All browser tabs, iframes, or workers served from the same origin can emit and receive messages:

```
// Send a message to the broadcast channel.
channel.postMessage(myMessage);
// Listen to messages from the broadcast channel.
channel.onmessage = evt => {
var message = evt.data;
};
```

To benchmark this, we use a script similar to the one described above, except that the web worker is not destroyed and reused at each operation. The time to get a round trip response should be divided by two.

As you might expect, the simple postMessage is fast. It usually takes between **0 to 1 ms** to send a message, whether to a web or shared worker. Broadcast channel API takes about **1 to 2 ms**.

Under normal circumstances, exchanging messages with workers is fast and you should not feel too concerned about speed here. However, larger messages can take longer.

## The size of messages

There are 2 ways to send messages to web workers:

- Copying the message
- Transferring the message

In the first case, the message is serialized, copied, and sent over. In the latter, the data is transferred. This means that the original sender can no longer use it once sent. Transferring data is almost instantaneous, so there is no real point in benchmarking that. However, only ArrayBuffer is transferable.

As expected, serializing, copying, and de-serializing data adds significant overhead to the message transmission. The bigger the message, the longer it takes to be sent.

The benchmark here sends a typed array to a web worker. Its size is progressively increased at each iteration. There is a linear correlation between size of the message and transfer time. For each measurement, we can divide the size (in kilobytes) by the time (in milliseconds) to get the transfer speed in kb/ms.

Typically, on a Flame, the transfer speed is **80 kB/ms** for postMessage and **12 kB/ms** using broadcast channel. This means that if you want your message to fit in a single frame, you should keep it under **1,300 kB** with postMessage and under **200 kB** when using the broadcast channel. Otherwise, it may introduce frame drop in your application.

In this benchmark, we use typed arrays, because it makes it possible to determine their size in kilobytes precisely. You can also transfer JavaScript objects, but due to the serialization process, they take longer to post. For small objects, this doesn’t really matter, but if you need to send huge objects, you may as well serialize them to a binary format. You can use something similar to [Protocol Buffer](https://developers.google.com/protocol-buffers/).

## Web workers are fast if used correctly

Here is a quick summary of various benchmarks related to web workers, as measured on a Flame:

| Operation | Value |
| Instantiation of a web worker | 40 ms |
|---|---|
| Instantiation of a broadcast channel | 1 ms |
| Communication latency with postMessage | 0.5 ms |
| Communication latency with broadcast channel | 1.5 ms |
| Communication speed with postMessage | 80 kB/ms |
| Communication speed with broadcast channel | 12 kB/ms |
| Maximum message size with postMessage | 1,300 kB |
| Maximum message size with broadcast channel | 200 kB |

Benchmarking is the only way to make sure that the solution you are implementing is fast. This process takes much of the guesswork out of web development.

If you want to run these benchmarks on a specific device, the app I built to make these measurements, [web workers benchmark](https://github.com/gmarty/web-workers-benchmark), is open source. You are also welcome to contribute by submitting new types of benchmarks.

## About
[
Guillaume Cedric Marty ](http://gu.illau.me)

Guillaume has been working in the web industry for more than a decade. He's passionate about web technologies and contributes regularly to open source projects, which he writes about on his [technical blog](http://gu.illau.me/). He's also fascinated by video games, animation, and, as a Japanese speaker, foreign languages.

## 9 comments

Fernando MontoyaJuly 2nd, 2015 at 23:40LukeJuly 3rd, 2015 at 00:26Guillaume Cedric MartyJuly 3rd, 2015 at 01:57smaugJuly 3rd, 2015 at 12:043y3July 3rd, 2015 at 04:05Robert O’CallahanJuly 3rd, 2015 at 22:21Gervase MarkhamJuly 4th, 2015 at 08:54Guillaume Cedric MartyJuly 6th, 2015 at 04:07El GoopoJuly 8th, 2015 at 17:33