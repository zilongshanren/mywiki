---
title: How to Quit Spotify
url: https://benui.ca/blog/quitting-spotify/
published: '2026-01-01'
source_blog: ben🌱ui
source_site: https://benui.ca/
category: unreal engine
fetched: '2026-04-13'
---

It's ~~2025~~ 2026, if you're like me, you've been using Spotify for way too long.

You think about quitting, but it seems like a *whole thing*. There are many reasons you might have:

- Spotify's CEO
[invests hundreds of millions in an AI weapons company](https://techcrunch.com/2025/06/16/spotifys-daniel-ek-just-bet-bigger-on-helsing-europes-defense-tech-darling/). - Spotify pays practically nothing to artists.
[$0.003 per stream](https://www.headphonesty.com/2025/03/qobuz-exposed-streaming-secret/) - Spotify pays $250M to
[a toxic masc-thumb](https://variety.com/2024/digital/news/joe-rogan-renews-spotify-deal-not-exclusive-1235895424/). - Artists you like
[are leaving](https://www.loudersound.com/news/massive-attack-removing-music-spotify-2025)

## Getting out of Spotify

First, the escape.

### Request Your Data

First, before you close your account, you should request your data from Spotify. It should be under the [Account Privacy](https://www.spotify.com/account/privacy/) page. They will take a few days, and then email you when your download is ready.

What you get doesn't seem to include your favourited tracks. Be forewarned.

## What next

Now you add to or start building your musical library. You own it, it's yours. Forever.

Don't go back into some other streaming service. Amazon, Tidal, Apple Music, Youtube Music, Qobuz, they all pay next-to-nothing to artists.

### Where to get music

#### Ripping your own CDs

If you're an aging millennial you probably own a few of these coasters. To convert them into MP3s or FLACs:

- Download
[Exact Audio Copy](https://www.exactaudiocopy.de/). - Follow a
[much better tutorial](https://flemmingss.com/perfect-cd-ripping-to-flac-with-exact-audio-copy/)on how to set up EAC. - Rip a bunch of stuff.
- After ripping, use
[MP3Tag](https://docs.mp3tag.de/)to tag your files because EAC's tagging is not that great.

#### Buying Music

You can get second-hand CDs from local record stores for pretty cheap. The money won't go to the original artists, but you're helping the local economy and not supporting a foreign billionaire. I would recommend that for artists that are plenty rich already or are already dead.

For supporting living artists who deserve your hard-earned ₡, there's:

[Bandcamp](https://bandcamp.com/)takes a 10-15% cut of sales which seems relatively low?[7Digital](https://ca.7digital.com/)seems to only have very large artists.[Faircamp](https://faircamp.webr.ing/directory.html)is like a webring of individual artists.[Steam](https://store.steampowered.com/search/?category1=990&ndl=1)has soundtracks did you know?

If you really have to, iTunes and Amazon offer DRM-free stuff but try to avoid them like the plague.

### Transferring your music

The easiest way I've found to sync my music files from my PC to my MP3 player is to use Windows's [robocopy](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy) command.

I take out the micro-SD card that my MP3 player uses and put it into the card reader that's attached to my PC.

Attaching the player by USB means that files are transferred by some super-slow Android connection thing, so this is much better.

For example if your music is stored in `C:\Music\`

and your micro-SD is `G:\`

, you can use a command like the following to back up all of your files to `G:\`

.

```
robocopy c:\Music\ G:\Music\ /mir /R:2 /W:5 /s /zb /log:C:\Music\music-backup.log
```


### Playing Music

#### Desktop

[foobar2000](https://www.foobar2000.org/)- I'm a sucker for software that looks like it hasn't been changed since Windows 95.[MusicBee](https://www.getmusicbee.com/)- exists

#### Android

[Musicolet](https://play.google.com/store/apps/details?id=in.krosbits.musicolet)is my favourite.

#### iOS

- i have no idea

#### Devices

There are a bunch of devices out there, mostly available through AliExpress. I picked the [HiBy M300](https://www.aliexpress.com/item/1005006219815444.html) because it runs Android, which I'm used to.

### Protecting Your Collection

- Get a cheap external hard-drive. Depending on your collection, 256gb may be plenty.
- Use something like
[Arq](https://www.arqbackup.com/)to back up your music folder to an external hard-drive or cloud (the cloud costs money).

### Shameless Music Recommendations

I like these artists so they're automatically good.