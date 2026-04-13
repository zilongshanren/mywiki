---
title: Creating Web Things with Python, Node.js, and Java – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2018/05/creating-web-things-with-python-node-js-and-java/
author: Michael Stegeman
published: '2018-05-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The Mozilla IoT team recently released the [Things Framework](https://hacks.mozilla.org/2018/04/build-your-own-web-things-with-the-things-framework/), which allows you to build IoT devices that speak the [Web Thing API](https://iot.mozilla.org/wot/). Last week, James built an [ESP8266 web thing](https://hacks.mozilla.org/2018/04/making-a-web-thing-on-the-esp8266/). This time, I’m going to show you how to build web things with Python, Node.js, or Java. These languages are definitely not optimal for small embedded devices; this tutorial is intended for higher-end devices that can run these languages with ease, or even your own desktop computer.

To demonstrate, we’ll be turning the [Music Player Daemon](https://www.musicpd.org/) (MPD) into a web thing. The libraries we’ll be using here are [webthing-python](https://github.com/mozilla-iot/webthing-python), [webthing-node](https://github.com/mozilla-iot/webthing-node), and [webthing-java](https://github.com/mozilla-iot/webthing-java).

## Intro to the Music Player Daemon (MPD)

The [Music Player Daemon](https://en.wikipedia.org/wiki/Music_Player_Daemon) is an open-source music player that has been around since 2003. MPD operates in a client/server model, and is controllable over TCP with a simple text-based protocol. I won’t cover installation here, but MPD can be installed via your package manager on Linux, Homebrew on Mac OS X, or with [binaries on Windows](https://www.musicpd.org/download.html).

## Some Quick Notes

Although this example is written for MPD, it would be easily portable to other music players with an API, or you could build your own player using this example as a base. More importantly, this example is primarily meant to demonstrate the Things Framework, which can be used to create an endless variety of web things.

The Python, Node.js, and Java web thing libraries all have essentially the same API. While they may not be entirely idiomatic for their respective languages, doing this allows us to maintain all the libraries more easily, which is incredibly valuable while the Web Thing API is still a living draft.

## Getting Started

To start, initialize an empty project for your language of choice. For example, you might create a new project in [IntelliJ IDEA](https://www.jetbrains.com/idea/download/) for Java, or run `npm init`

to start a new Node.js project. You’ll then want to add the webthing library as a dependency. Instructions for doing so can be found on the respective Github project page, or you can [look here](https://iot.mozilla.org/things/).

Now we’re ready to write some code. Essentially we’ll do the following:

- Create a
`Thing`

.- Define its properties.
- Define its actions.
- Define its events.

- Attach the
`Thing`

to a`WebThingServer`

.

## Create a Thing

First off, let’s import our library of choice.

`from webthing import Action, Event, Property, Thing, Value, WebThingServer`


```
const {
Action,
Event,
Property,
Thing,
Value,
WebThingServer,
} = require('webthing');
```


```
import org.mozilla.iot.webthing.Action;
import org.mozilla.iot.webthing.Event;
import org.mozilla.iot.webthing.Property;
import org.mozilla.iot.webthing.Thing;
import org.mozilla.iot.webthing.Value;
import org.mozilla.iot.webthing.WebThingServer;
```


Now, we’ll create a basic subclass of `Thing`

.

```
class MPDThing(Thing):
def __init__(self):
Thing.__init__(self, 'MPD', 'musicPlayer', 'Music Player Daemon')
```


```
class MPDThing extends Thing {
constructor() {
super('MPD', 'musicPlayer', 'Music Player Daemon');
}
}
```


```
public class MPDThing extends Thing {
public MPDThing() {
super("MPD", "musicPlayer", "Music Player Daemon");
}
}
```


## Add Properties

Now that we have our `MPDThing`

, we’ll need to add some properties to it. Obviously, a music player will have quite a few properties. To demonstrate, I will show you how to add one, and I’ll link to the rest of the code at the end of this post.

To add a property, you can do the following inside the `MPDThing`

constructor.

```
status = self.get_status()
self.add_property(
Property(self,
'volume',
Value(self.get_volume(status), self.set_volume),
metadata={
'type': 'number',
'description': 'Playback volume',
'minimum': 0,
'maximum': 100,
}))
```


```
this.getStatus().then((status) => {
this.getVolume(status).then((v) => {
this.addProperty(
new Property(this,
'volume',
new Value(v, this.setVolume.bind(this)),
{
type: 'number',
description: 'Playback volume',
minimum: 0,
maximum: 100,
}));
});
});
```


```
ServerStatus status = this.client.getServerStatus();
Map<String, Object> volumeMetadata = new HashMap<>();
volumeMetadata.put("type", "number");
volumeMetadata.put("description", "Playback volume");
volumeMetadata.put("minimum", 0);
volumeMetadata.put("maximum", 100);
this.volumeValue =
new Value(status.getVolume(), v -> this.setVolume((int)v));
this.addProperty(new Property(this,
"volume",
this.volumeValue,
volumeMetadata));
```


We’ve now created a `Property`

that allows us to GET and PUT the playback volume. The `Value`

piece is an object that essentially stores a cached value and a “value forwarder” callback. When the volume is set via a PUT request, the value forwarder is used to forward the new value to the actual device, which in this case is the MPD server. We’ve also set up some metadata for the property, including a description, value type, and a minimum and maximum value.

## Add Actions

A music player can also have a lot of actions. While the MPD web thing has several basic actions like play, pause, and skip, I’ve added one that takes some additional input, which will queue a series of random songs. Action inputs are verified with a [JSON Schema validator](http://json-schema.org/latest/json-schema-validation.html).

First, let’s create an `Action`

subclass.

```
class QueueRandomAction(Action):
def __init__(self, thing, input_):
Action.__init__(
self, uuid.uuid4().hex, thing, 'queueRandom', input_=input_)
def perform_action(self):
songs = self.thing.list()
if songs:
for _ in range(0, int(self.input['count'])):
self.thing.add(random.choice(songs))
playlist = self.thing.get_playlist()
if playlist is not None:
self.thing.add_event(
PlaylistUpdatedEvent(self.thing, playlist))
```


```
class QueueRandomAction extends Action {
constructor(thing, input) {
super(uuidv4(), thing, 'queueRandom', input);
}
performAction() {
return this.thing.list().then((songs) => {
const promises = [];
if (songs) {
for (let i = 0; i < this.input.count; ++i) {
const uri = songs[Math.floor(Math.random() * songs.length)].file;
promises.push(this.thing.add(uri));
}
promises.push(this.thing.getPlaylist().then((playlist) => {
if (playlist) {
this.thing.addEvent(new PlaylistUpdatedEvent(this.thing, playlist));
}
}));
}
return Promise.all(promises);
});
}
}
```


```
public static class QueueRandomAction extends Action {
public QueueRandomAction(Thing thing, JSONObject input) {
super(UUID.randomUUID().toString(), thing, "queueRandom", input);
}
@Override
public void performAction() {
MPDThing thing = (MPDThing)this.getThing();
Random random = new Random();
List<MPDFile> songs = thing.list();
for (int i = 0; i < this.getInput().getInt("count"); ++i) {
MPDFile file = songs.get(random.nextInt(songs.size()));
thing.add(file);
}
String playlist = thing.getPlaylist();
thing.addEvent(new PlaylistUpdatedEvent(thing, playlist));
}
}
```


`QueueRandomAction`

takes an input, `count`

, queues that number of random songs to the current playlist, and then emits a `PlaylistUpdatedEvent`

(to be defined shortly). To add this new action to our `MPDThing`

, do the following inside the `MPDThing`

constructor:

```
self.add_available_action(
'queueRandom',
{'description': 'Queue a series of random songs',
'input': {
'type': 'object',
'required': [
'count',
],
'properties': {
'count': {
'type': 'number',
'minimum': 1,
},
},
}},
QueueRandomAction)
```


```
this.addAvailableAction(
'queueRandom',
{
description: 'Queue a series of random songs',
input: {
type: 'object',
required: [
'count',
],
properties: {
count: {
type: 'number',
minimum: 1,
},
},
},
},
QueueRandomAction);
```


```
Map<String, Object> queueRandomMetadata = new HashMap<>();
queueRandomMetadata.put("description",
"Queue a series of random songs");
Map<String, Object> queueRandomInputMetadata = new HashMap<<>();
queueRandomInputMetadata.put("type", "object");
queueRandomInputMetadata.put("required", new String[]{"count"});
Map<String, Object> queueRandomInputPropertiesMetadata =
new HashMap<>();
Map<String, Object> queueRandomInputPropertiesCountMetadata =
new HashedMap();
queueRandomInputPropertiesCountMetadata.put("type", "number");
queueRandomInputPropertiesCountMetadata.put("minimum", 1);
queueRandomInputPropertiesMetadata.put("count",
queueRandomInputPropertiesCountMetadata);
queueRandomInputMetadata.put("properties",
queueRandomInputPropertiesMetadata);
queueRandomMetadata.put("input", queueRandomInputMetadata);
this.addAvailableAction("queueRandom",
queueRandomMetadata,
QueueRandomAction.class);
```


## Add Events

The final piece of our `Thing`

is its events. Since MPD is a client/server model, it can be updated externally by any number of other clients. As such, I created an event that will fire when the current playlist is updated.

As with `Thing`

and `Action`

, we’ll create an `Event`

subclass.

```
class PlaylistUpdatedEvent(Event):
def __init__(self, thing, data):
Event.__init__(self, thing, 'playlistUpdated', data=data)
```


```
class PlaylistUpdatedEvent extends Event {
constructor(thing, data) {
super(thing, 'playlistUpdated', data);
}
}
```


```
public static class PlaylistUpdatedEvent extends Event {
public PlaylistUpdatedEvent(Thing thing, String data) {
super(thing, "playlistUpdated", data);
}
}
```


This is a basic `Event`

. The data member will be filled in with a string representation of the current playlist.

To add this `Event`

to our thing, we’ll do the following in the `MPDThing`

constructor:

```
self.add_available_event(
'playlistUpdated',
{'description': 'The current playlist has been updated',
'type': 'string'})
```


```
this.addAvailableEvent(
'playlistUpdated',
{
description: 'The current playlist has been updated',
type: 'string',
});
```


```
Map<String, Object> playlistUpdatedMetadata = new HashMap<>();
playlistUpdatedMetadata.put("description",
"The current playlist has been updated");
playlistUpdatedMetadata.put("type", "string");
this.addAvailableEvent("playlistUpdated", playlistUpdatedMetadata);
```


## Create a WebThingServer

Now that we have a thing with properties, actions, and events, we’ll create a `WebThingServer`

and attach the `MPDThing`

to it.

```
thing = MPDThing()
server = WebThingServer([thing], port=8888)
try:
server.start()
except KeyboardInterrupt:
server.stop()
```


```
const thing = new MPDThing();
const server = new WebThingServer([thing], null, 8888);
process.on('SIGINT', () => {
server.stop();
process.exit();
});
server.start();
```


```
MPDThing thing = new MPDThing();
List<Thing> things = new ArrayList<>();
things.add(thing);
try {
WebThingServer server = new WebThingServer(things, null, 8888);
Runtime.getRuntime()
.addShutdownHook(new Thread(() -> server.stop()));
server.start(false);
} catch (IOException e) {
System.out.println(e);
System.exit(1);
}
```


## Controlling the Web Thing

Our web thing is complete and it’s now controllable via the Web Thing API. Here’s how to add it to the [Things Gateway](https://iot.mozilla.org/gateway/):

- Empty Things Screen

- Add New Thing

- New Thing Displayed

- Expanded Thing UI

The Things Gateway doesn’t currently provide a way to use actions or display events, but those are in the works.

Alternatively, you can control the web thing via cURL or any other HTTP library you choose:

```
$ curl \
-X POST http://127.0.0.1:8888/actions \
-H 'Content-Type: application/json' \
-d '{"play":{}}'
```


## Wrapping Up

Your imagination is really your only limit as to what you can turn into a web thing. If you’d like to see the rest of this example and how the actual MPD controls are implemented, all of the code is [available on Github](https://github.com/mrstegeman/mpd-webthing).

If you have any questions or suggestions, you can head over to [Discourse](https://discourse.mozilla.org/c/iot) or find us in `#iot`

on [irc.mozilla.org](https://wiki.mozilla.org/IRC). Additionally, feel free to create issues, or even better, submit pull requests, to the webthing library repositories!

## About
[
Michael Stegeman ](https://github.com/mrstegeman)

Michael is a software engineer at Mozilla working on WebThings.

## One comment

Arne BabenhauserheideMay 11th, 2018 at 02:46