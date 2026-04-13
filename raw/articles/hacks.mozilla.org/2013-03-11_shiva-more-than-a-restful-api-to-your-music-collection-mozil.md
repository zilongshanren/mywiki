---
title: Shiva – More than a RESTful API to your music collection – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2013/03/shiva-more-than-a-restful-api-to-your-music-collection/
author: Alvaro Mouriño
published: '2013-03-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Music for me is not only part of my daily life, it is an essential part. It helps me concentrate, improves my mood, distracts me and/or helps me relax. This is true for most (if not all) people.The lack of music or the wrong selection of tunes can have the complete opposite effect, it has a strong influence on how we feel. It also plays a key role in shaping our identity. Music, like most (if not all) types of culture, is not an accessory, is not something we can choose to ignore, it is a need that we have as human beings.

The Internet has become the most efficient medium ever in culture distribution. Today it’s easier than ever to have access to a huge diversity of culture, from any place in the world. At the same time you can reach the whole world with your music, instantly, with just signing up at one of the many websites you can find for music distribution. Just as “travel broadens the mind”, music sharing enriches culture, and thanks to the Internet, culture is nowadays more alive than ever.

Not too long ago record labels were the judges of what was good music (by their standards) and what was not. They controlled the only global-scale distribution channel, so to make use of it you would need to come to an agreement with them, which usually meant giving up most of the rights over your cultural pieces. Creating and maintaining such a channel was neither easy nor cheap, there was a need for the service they provided, and even though their goal was not to distribute culture but to be profitable (as every company) both parties, industry and society, benefited from this.

Times have changed and this model is obsolete now; the king is dead, so there are companies fighting to occupy this vacancy. What also changed was the business model. Now it is not just the music – it is also about restricting access to it and collecting (and selling) private information about the listeners. In other words, [DRM](http://drm.info/en/what-is-drm) and privacy. Here is where Shiva comes into play.

## What is Shiva?

Shiva is, technically speaking, a RESTful API to your music collection. It indexes your music and exposes an API with the metadata of your files so you can then perform queries on it and organize it as you wish.

On a higher level, however, Shiva aims to be a free (as in freedom and beer) alternative to popular music services. It was born with the goal of giving back the control over their music and privacy to the users, protecting them from the industry’s obsession with control.

It’s not intended to compete directly with online music services, but to be an alternative that you can install and modify to your needs. You will own the music in your server. Nobody but you (or whoever you give permission) will be able to delete files or modify the files’ metadata to correct it when it’s wrong. And of course, it will all be available to any device with Internet connection.

You will also have a clean, RESTful API to your music without restrictions. You can grant access to your friends and let them use the service or, if they have their own Shiva instances, let both servers talk to each other and share the music transparently.

To sum up, Shiva is a distributed social network for sharing music.

## Your own music server

[Shiva-Server](https://github.com/tooxie/shiva-server) is the component that indexes your music and exposes a RESTful API. These are the available resources:

- /artists
- /artists/shows

- /albums
- /tracks
- /tracks/lyrics


It’s built in python, using SQLAlchemy as ORM and Flask for HTTP communication.

### Indexing your music

The installation process is quite simple. There’s a very complete [guide](https://github.com/tooxie/shiva-server#installation) in the README file, but I’ll summarize it here:

- Get the source
- Install dependencies from the requirements.pip file
- Copy /shiva/config/local.py.example to /shiva/config/local.py
- Edit it and configure the directories to scan
- Create the database (sqlite by default)
- Run the indexer
- Run the development server

For details on any of the steps, check the documentation.

Once the music has been indexed, all the metadata is stored in the database and queried from it. Files are only accessed by the file server for streaming. Lyrics are scraped the first time they are requested and then cached. Given the changing nature of the shows resource, this is the only one that is not cached; instead is queried every time. At the moment of this writing is using only one source, the [BandsInTown API](http://www.bandsintown.com/api/overview).

Once the server is running you have all you need to start playing with Shiva. Point to a resource, like /artists, to see it in action.

### Scraping lyrics

As mentioned, lyrics are scraped, and you can create your own scrapers for specific websites that have the lyrics you want. All you need is to create a python file with a class inheriting from LyricScraper in the /shiva/lyrics directory. The following template makes clear how easy it is. Let’s say we have a file /shiva/lyrics/mylyrics.py:

From `shiva.lyrics import LyricScraper`

:

```
class MyLyricsScraper(LyricScraper):
“““ Fetches lyrics from mylyrics.com ”””
def fetch(self, artist, title):
# Magic happens here
if not lyrics:
return False
self.lyrics = lyrics
self.source = lyrics_url
return True
```

After this you need add your brand new scraper to the scrapers list, in your local.py config file:

```
SCRAPERS = {
‘lyrics’: (
‘mylyrics.MyLyricScraper’,
)
}
```

Shiva will instantiate your scraper and call the fetch() method. If it returns True, it will then proceed to look for the lyrics in the lyrics attribute, and the URL from which they were scraped in the source attribute:

```
if scraper.fetch():
lyrics = Lyrics(text=scraper.lyrics, source=scraper.source,
track=track)
g.db.session.add(lyrics)
g.db.session.commit()
return lyrics
```

Check the [existing scrapers](https://github.com/tooxie/shiva-server/tree/master/shiva/lyrics) for real world examples.

Lyrics will only be fetched when you request one specific tracks, not when retrieving more than one. The reason behind this is that each track’s lyrics may require two or more requests, and we don’t want to DoS the website when retrieving an artist’s discography. That would not be nice.

### Setting up a file server

The development server, as its name clearly states, should not be used for production. In fact it is almost impossible because can only serve one request at a time, and the audio element will keep the connection open as long as the file is playing, ergo, blocking completely the API.

Shiva provides a way to delegate the file serving to a dedicated server. For this you have to edit your /shiva/config/local.py file, and edit the MEDIA_DIRS setting. This option expects a tuple of MediaDir objects, which provide the mechanism to define directories to scan and a socket to serve the files through:

```
MediaDir(‘/srv/music’, url=’http://localhost:8080’)
```

This way doesn’t matter in which socket your application runs, files in the /src/music directory will be served through the URL defined in the url attribute. This object also allows to define subdirectories to be scanned. For example:

```
MediaDir(‘/srv/music’, dirs=(‘/pop’, ‘/rock’), url=’http://localhost:8080’)
```

In this case only the directories /srv/music/pop and /srv/music/rock will be scanned. You can define as many MediaDir objects as you need. Suppose you have the file /srv/music/rock/nofx-dinosaurs_will_die.mp3, once this is in place the track’s download_uri attribute will be:

```
{
"slug": "dinosaurs-will-die",
"title": "Dinosaurs Will Die",
"uri": "/track/510",
"id": 510,
"stream_uri": "http://localhost:8080/nofx-dinosaurs_will_die.mp3"
}
```

## Your own music player

Once you have your music scanned and the API running, you need a client that consumes those services and plays your music, like [Shiva-Client](https://github.com/tooxie/shiva-client). Built as a single page application with AngularJS and HTML5 technologies, like Audio and Drag and Drop, this client will allow you to browse through your catalog, add files to a playlist and play them.

Due to the [Same-Origin-Policy](http://en.wikipedia.org/wiki/Same_origin_policy) you will need a server that acts as proxy between the web app and the API. For this you will find a server.py file in the repo that will do this for you. The only dependency for this file is Flask, but I assume you have that installed already. Now just execute it:

`python server.py`

This will run the server on `http://localhost:9001/`


Access that URI and check the server output, you will see not only the media needed by the app (like images and javascript files) but also a /api/artists call. That’s the proxy. Any call to /api/ will be redirected by the server to http://localhost:9002/

If you open a console, like firebug, you will see a Shiva object in the global namespace. Inside of it you will find 2 main attributes, Player and Playlist. Those objects encapsulate all the logic for queueing and playing music. The Player only holds the current track, acts as a wrapper around HTML5’s Audio element. What may not seem natural at first is that normally you won’t interact with the Player, but with the Playlist, which acts as a façade because it knows all the tracks and instructs the Player which track to load and play next.

The source for those objects is in the js/controllers.js file. There you will also find the AngularJS controllers, which perform the actual calls to the API. It consists of just 2 calls, one to get the list of artists and another one to get the discography for an artist. Check the code, is quite simple.

So once tracks are added to the playlist, you can do things like play it:

```
Shiva.Playlist.play()
```

Stop it:

```
Shiva.Playlist.stop()
```

Or skip the track:

```
Shiva.Playlist.next()
```

Some performance optimizations were made in order to lower the processing as much as possible. For example, you will see a progress bar when playing music, that will only be updated when it has to be shown. The events will be removed when not needed to avoid any unnecessary DOM manipulation of non-visible elements:

```
Shiva.Player.audio.removeEventListener('timeupdate', Shiva.Player.audio.timeUpdateHandler, false);
```

## Present and future

At the time of this writing, Shiva is in a usable state and provides the core functionality but is still young and lacks some important features. That’s also why this article doesn’t dig too much into the code, because it will rapidly change. To know the current status please check the [documentation](https://github.com/tooxie/shiva-server).

If you want to contribute, there are many ways you can help the project. First of all, fork both the server and the client, play with them and send your improvements back to upstream.

Request features. If you think “seems nice, but I wouldn’t use it” write down why and send those thoughts and ideally some ideas on how to tackle them. There is a long list of lacking features; your help is vital in order to prioritize them.

But most importantly; build your own client. You know what you like about your favourite music player and you know what sucks. Fork and modify the existing client or create your own from scratch, bring new ideas to the old world of music players. Give new and creative uses to the API.

There’s a lot of work to be done, in many different fronts. Some of the plans for the future are:

**Shiva-jslib:**An easy to use javascript library that encapsulates the API calls, so you can focus only on building the GUI and forget about the protocol.**Shiva2Shiva communication:**Let two (or more) Shiva instances talk to each other to allow for transparent sharing of music between servers.**Shiva-FXOS:**A Shiva client for Firefox OS.

And anything else you can think of. Code, send ideas, code your clients.

Happy hacking!

## About
[
Alvaro Mouriño ](http://twitter.com/tuxie_)

Alvaro is a Free Software hacktivist from Uruguay, currently living in Berlin. Has been involved in Free Software groups for years as an active member, organizing many local events and attending many more in the Southern Cone region.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 26 comments

ant cosentinoMarch 11th, 2013 at 10:31mikekijMarch 11th, 2013 at 11:37Alvaro MouriñoMarch 13th, 2013 at 11:04KaiMarch 11th, 2013 at 12:22Alvaro MouriñoMarch 14th, 2013 at 02:22R. Kyle MurphyMarch 11th, 2013 at 13:36Alvaro MouriñoMarch 13th, 2013 at 11:24ucuzmuzikaletiMarch 11th, 2013 at 14:17oneknlrMarch 11th, 2013 at 14:59Alvaro MouriñoMarch 13th, 2013 at 14:33TheSisbMarch 11th, 2013 at 18:10DimitrisMarch 11th, 2013 at 23:35h00dyMarch 12th, 2013 at 02:38Alvaro MouriñoMarch 13th, 2013 at 11:45AlexMarch 12th, 2013 at 07:21jasonxuMarch 12th, 2013 at 19:46FresoMarch 13th, 2013 at 10:03Alvaro MouriñoMarch 13th, 2013 at 14:08M7700March 13th, 2013 at 20:56AgresvigMarch 14th, 2013 at 01:54Alvaro MouriñoMarch 14th, 2013 at 02:21silopolisMarch 14th, 2013 at 03:43FresoMarch 14th, 2013 at 07:44TomMarch 14th, 2013 at 15:08RudolfMarch 18th, 2013 at 09:13Sonicjar MusicApril 2nd, 2013 at 09:40