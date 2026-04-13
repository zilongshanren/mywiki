---
title: The Poor Man's Voice Acting
url: https://etodd.io/2016/04/30/poor-mans-voice-acting/
published: '2016-04-30'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# The Poor Man's Voice Acting

Allow me to regale you with an exciting tale: the birth of a janky dialogue and voice system.

I have a JSON file with all the localized strings in my game, like this:

```
{
"danger": "Danger",
"level": "Level %d",
...
}
```


A preprocessor takes this and generates a header file with integer constants for each string, like this:

```
namespace strings
{
const int danger = 0;
const int level = 1;
// ...
```


At runtime, it loads the JSON file and hooks up the integer IDs to localized strings. A function called "_" takes an integer ID and returns the corresponding localized string. I use it like this:

`draw_string(_(strings::danger), position);`


This all worked (and still works) pretty well for UI strings. Not so much for dialogue.

To write dialogue, I had to come up with a unique ID for each line, then add it to the strings file, like this:

```
{
"hello_penelope": "Hello! I am Penelope.",
"nice_meet_you": "Nice to meet you.",
...
}
```


Yes, the preprocessor generated a new integer ID in the header file every time I added a line of dialogue. Gross.

I construct dialogue trees in [Dialogger](https://github.com/etodd/dialogger). With this setup, I had to use IDs like "hello_penelope" rather than actual English strings. Also gross.

### A better way

I keep the string system, but extend it to support "dynamic" strings loaded at runtime that do not have integer IDs in the header file.

Now I can write plain English in the dialogue trees. The preprocessor goes through all of them and extracts the strings into a separate JSON file, using the SHA-1 hash of each string for its ID. Once everything is loaded, I discard all string IDs in favor of integer IDs.

I couldn't find a simple straightforward SHA-1 implementation that worked on plain C strings, so [here's one for you](https://github.com/etodd/sha1).

The point of all this is: I now have a single JSON file containing all the dialogue in the game. Ripe for automation...

### Speak and spell

Penelope is an AI character. I'm using text-to-speech for her voice, at least for now. I don't want to integrate a text-to-speech engine in the game; that's way too much work. And I don't want to manually export WAVs from a text-to-speech program. Also too much work.

I create a free [IBM Bluemix](http://www.ibm.com/cloud-computing/bluemix/) account. They have a dead simple text-to-speech API: make an HTTP request with basic HTTP authentication, get a WAV file back.

I write an [82-line Python script](https://github.com/etodd/yearning/blob/35745430125677afe55b86103e82cc48e85eaf7c/assets/script/text_to_speech.py) that goes through all the dialogue strings and makes an HTTP request for each one. It keeps track of which strings have previously been voiced, to facilitate incremental updates.

Now I have a folder of WAV files, each one named after a SHA-1 hash. I'm using [Wwise](https://www.audiokinetic.com/products/wwise/) for audio, so the next step requires a bit of manual involvement. I drag all the WAVs into the project and batch create events for them.

![](../../assets/8dac72a4edcffa82.png)

Now when I display a dialogue string, I just have to look up the SHA-1 hash and play the audio event. Easy.

### Disaster strikes

I don't hear anything. All signs indicate the audio is playing correctly, but nothing comes out of my speakers.

I look at one of the audio files in Wwise.

![](../../assets/4d4b18012e077ce9.png)

Looks like the file is corrupted. I play the WAV in a number of different programs. Some play it fine, others don't play it at all.

I edit my text-to-speech script to use Python's [wave](https://docs.python.org/3.5/library/wave.html) library to load the WAV file after downloading it from IBM. Sure enough, the library doesn't know what to make of it.

Too lazy to care, I edit the wave library in-place in my Python distribution. YOLO.

After a bit of printf debugging, I pinpoint the issue. The WAV format is based on [RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format), a binary format which breaks the file into "chunks". According to Wikipedia, the format of each chunk is as follows:

- 4 bytes: an ASCII identifier for this chunk (examples are "fmt " and "data"; note the space in "fmt ").
- 4 bytes: an unsigned, little-endian 32-bit integer with the length of this chunk (except this field itself and the chunk identifier).
- variable-sized field: the chunk data itself, of the size given in the previous field.
- a pad byte, if the chunk's length is not even.

Turns out, IBM's text-to-speech API generates streaming WAV files, which means it sets the "length" field to 0. Some WAV players can handle it, while others choke. Wwise falls in the latter category.

Fortunately, I can easily figure out the chunk length based on the file size, modify it using the wave library, and write it back out to the WAV file. [Like so](https://github.com/etodd/yearning/blob/2b087235242781962de0f8cb1b31b83a7455755b/assets/script/text_to_speech.py#L60).

Problem solved. Wwise is happy. Next I set up some Wwise callbacks to detect the current volume of Penelope's voice, and when she's done speaking.

Here's the result, along with some rope physics in the background being destroyed by the wonky framerate caused by my GIF recorder:

If you want to hear it, check out the IBM text-to-speech demo [here](https://text-to-speech-demo.mybluemix.net/).

If you enjoyed this article, try these:

Thanks for reading!