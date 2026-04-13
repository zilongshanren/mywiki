---
title: Firefox and the Web Speech API – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/01/firefox-and-the-web-speech-api/
author: Chris Mills
published: '2016-01-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Speech Synthesis and recognition are powerful tools to have available on computers, and they have become quite widespread in this modern age — look at tools like Cortana, Dictation and Siri on popular modern OSes, and accessibility tools like screenreaders.

But what about the Web? To be able to issue voice commands directly to a web page and have the browser read text content directly would be very useful.

Fortunately, some intelligent folk have been at work on this. The [Web Speech API](https://dvcs.w3.org/hg/speech-api/raw-file/tip/webspeechapi.html) has been around for quite some time, the spec having been written in around 2014, with no significant changes made since. As of late 2015, Firefox (44+ behind a pref, and Firefox OS 2.5+) has implemented Web Speech, with Chrome support available too!

In this article we’ll explore how this API works, and what kind of fun you can already have.

## How does it work?

You might be thinking “functionality like Speech Synthesis is pretty complex to implement.” Well, you’d be right. Browsers tend to use the speech services available on the operating system by default, so for example you’ll be using the Mac Speech service when accessing speech synthesis on Firefox or Chrome for OS X.

The recognition and synthesis parts of the Web Speech API sit in the same spec, but operate independently to one another. There is nothing to stop you from implementing an app that recognizes an inputted voice command and then speaks it back to the user, but apart from that their functionality is separate.

Each one has a series of interfaces defining their functionality, at the center of which sits a controller interface — called (predictably) [SpeechRecognition](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition) and [SpeechSynthesis](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis). In the coming sections we’ll explore how to use these interfaces to build up speech-enabled apps.

## Browser support in more detail

As mentioned above, the two browsers that have implemented Web Speech so far are Firefox and Chrome. Chrome/Chrome mobile have supported synthesis and recognition since version 33, the latter with webkit prefixes.

Firefox on the other hand has support for both parts of the API without prefixes, although there are some things to bear in mind:

- Even through recognition is implemented in Gecko, it is not currently usable in desktop/Android because the UX/UI to allow users to grant an app permission to use it is not yet implemented.
- Speech synthesis does not work in Android yet.
- To use the recognition and synthesis parts of the spec in Firefox (desktop/Android), you’ll need to enable the
`media.webspeech.recognition.enable`

and`media.webspeech.synth.enabled`

flags in about:config. -
In Firefox OS, for an app to use speech recognition it needs to be privileged, and include the audio-capture and speech-recognition permission (see here for a suitable manifest
[example](https://github.com/mdn/web-speech-api/blob/master/speech-color-changer/manifest.webapp)) - Firefox does not currently support the
[continuous property](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition/continuous) - The
[onnomatch event handler](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition/onnomatch)is currently of limited use — it doesn’t fire because the speech recognition engine Gecko has integrated, Pocketsphinx, does not support a confidence measure for each recognition. So it doesn’t report back “sorry that’s none of the above” — instead it says “of the choices you gave me, this looks the best”.

Note: Chrome does not appear to deal with specific grammars; instead it just returns all results, and you can deal with them as you want. This is because Chrome’s server-side speech recognition has more processing power available than the client-side solution Firefox uses. There are advantages to each approach.

## Demos

We have written two simple demos to allow you to try out speech recognition and synthesis: Speech color changer and Speak easy synthesis. You can [find both of these on Github](https://github.com/mdn/web-speech-api).

To run them live:

## Speech Recognition

Let’s look quickly at the JavaScript powering the [Speech color changer demo](https://github.com/mdn/web-speech-api/tree/master/speech-color-changer).

### Chrome support

As mentioned earlier, Chrome currently supports speech recognition with prefixed properties, so we start our code with this, to make sure each browser gets fed the right object (nom nom.)

```
var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent
```


### The grammar

The next line defines the grammar we want our app to recognize:

```
var grammar = '#JSGF V1.0; grammar colors; public <color> = aqua | azure | beige | bisque | black | [LOTS MORE COLOURS] ;'
```


The grammar format used is [JSpeech Grammar Format](https://www.w3.org/TR/jsgf/) (JSGF).

### Plugging the grammar into our speech recognition

The next thing to do is define a speech recognition instance to control the recognition for our application. This is done using the `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition/SpeechRecognition">SpeechRecognition()</a>`

constructor. We also create a new speech grammar list to contain our grammar, using the `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechGrammarList/SpeechGrammarList" target="_blank">SpeechGrammarList()</a>`

constructor.

```
var recognition = new SpeechRecognition();
var speechRecognitionList = new SpeechGrammarList();
```


We add our grammar to the list using the `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechGrammarList/addFromString" target="_blank">SpeechGrammarList.addFromString()</a>`

method. Its parameters are the grammar we want to add, plus optionally a weight value that specifies the importance of this grammar in relation of other grammars available in the list (can be from 0 to 1 inclusive.) The added grammar is available in the list as a [ SpeechGrammar](https://developer.mozilla.org/en-US/docs/Web/API/SpeechGrammar) object instance.

```
speechRecognitionList.addFromString(grammar, 1);
```


We then add the SpeechGrammarList to the speech recognition instance by setting it to the value of the SpeechRecognition `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition/grammars" target="_blank">grammars</a>`

property.

### Starting the speech recognition

Now we implement an `onclick`

handler so that when the screen is tapped/clicked, the speech recognition service will start. This is achieved by calling `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition/start" target="_blank">SpeechRecognition.start()</a>`

.

```
var diagnostic = document.querySelector('.output');
var bg = document.querySelector('html');
document.body.onclick = function() {
recognition.start();
console.log('Ready to receive a color command.');
}
```


### Receiving and handling results

Once the speech recognition is started, there are many event handlers than can be used to retrieve results and other pieces of surrounding information (see the [SpeechRecognition event handlers list](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition#Event_handlers).) The most common one you’ll probably use is `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition/onresult" target="_blank">SpeechRecognition.onresult</a>`

, which is fired once a successful result is received:

```
recognition.onresult = function(event) {
var color = event.results[0][0].transcript;
diagnostic.textContent = 'Result received: ' + color + '.';
bg.style.backgroundColor = color;
console.log('Confidence: ' + event.results[0][0].confidence);
}
```


The second line here is a bit complex-looking, so let’s explain it step by step. The `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognitionEvent/results" target="_blank">SpeechRecognitionEvent.results</a>`

property returns a `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognitionResultList" target="_blank">SpeechRecognitionResultList</a>`

object containing one or more `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognitionResult">SpeechRecognitionResult</a>`

objects. It has a getter so it can be accessed like an array — so the first [0] returns the `SpeechRecognitionResult`

at position 0.

Each `SpeechRecognitionResult`

object contains `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognitionAlternative" target="_blank">SpeechRecognitionAlternative</a>`

objects that contain individual recognized words. These also have getters so they can be accessed like arrays — the second [0] therefore returns the `SpeechRecognitionAlternative`

at position 0. We then return its `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognitionAlternative/transcript" target="_blank">transcript</a>`

property to get a string containing the individual recognized result as a string, set the background color to that color, and report the color recognized as a diagnostic message in the UI.

You can find more detail about this demo on [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API#Speech_recognition).

## Speech Synthesis

Now let’s quickly review how the Speak easy synthesis [demo](https://github.com/mdn/web-speech-api/tree/master/speak-easy-synthesis) works

### Setting variables

First of all, we capture a reference to `<a href="https://developer.mozilla.org/en-US/docs/Web/API/Window/speechSynthesis" target="_blank">Window.speechSynthesis</a>`

. This is API’s entry point — it returns an instance of `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis" target="_blank">SpeechSynthesis</a>`

, the controller interface for web speech synthesis. We also create an empty array to store the available system voices (see the next step.)

```
var synth = window.speechSynthesis;
...
var voices = [];
```


### Populating the select element

To populate the `<select>`

element with the different voice options the device has available, we’ve written a `populateVoiceList()`

function. We first invoke [ SpeechSynthesis.getVoices()](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis/getVoices), which returns a list of all the available voices, represented by

`<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisVoice" target="_blank">SpeechSynthesisVoice</a>`

objects. We then loop through this list — for each voice we create an `<option>`

element, set its text content to display the name of the voice (grabbed from `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisVoice/name" target="_blank">SpeechSynthesisVoice.name</a>`

), the language of the voice (grabbed from `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisVoice/lang" target="_blank">SpeechSynthesisVoice.lang</a>`

), and — DEFAULT if the voice is the default voice for the synthesis engine (checked by seeing if `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisVoice/default" target="_blank">SpeechSynthesisVoice</a>`

.default returns true.)```
function populateVoiceList() {
voices = synth.getVoices();
for(i = 0; i < voices.length ; i++) {
var option = document.createElement('option');
option.textContent = voices[i].name + ' (' + voices[i].lang + ')';
if(voices[i].default) {
option.textContent += ' -- DEFAULT';
}
option.setAttribute('data-lang', voices[i].lang);
option.setAttribute('data-name', voices[i].name);
voiceSelect.appendChild(option);
}
}
```


When we come to run the function, we do the following. This is because Firefox doesn’t support `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis/onvoiceschanged" target="_blank">SpeechSynthesis.onvoiceschanged</a>`

, and will just return a list of voices when `SpeechSynthesis.getVoices()`

is fired. With Chrome however, you have to wait for the event to fire before populating the list, hence the if statement seen below.

```
populateVoiceList();
if (speechSynthesis.onvoiceschanged !== undefined) {
speechSynthesis.onvoiceschanged = populateVoiceList;
}
```


### Speaking the entered text

Next, we create an event handler to start speaking the text entered into the text field. We are using an `onsubmit`

handler on the form so that the action happens when Enter/Return is pressed. We first create a new `SpeechSynthesisUtterance()`

instance using its [constructor](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance) — this is passed the text input’s value as a parameter.

Next, we need to figure out which voice to use. We use the `HTMLSelectElement selectedOptions`

property to return the currently selected `<option>`

element. We then use this element’s `data-name`

attribute, finding the `SpeechSynthesisVoice`

object whose name matches this attribute’s value. We set the matching voice object to be the value of the `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/voice" target="_blank">SpeechSynthesisUtterance.voice</a>`

property.

Finally, we set the `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/pitch" target="_blank">SpeechSynthesisUtterance.pitch</a>`

and `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/rate">SpeechSynthesisUtterance.rate</a>`

to the values of the relevant range form elements. Then, with all necessary preparations made, we start the utterance being spoken by invoking `<a href="https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis/speak" target="_blank">SpeechSynthesis.speak()</a>`

, passing it the `SpeechSynthesisUtterance`

instance as a parameter.

```
inputForm.onsubmit = function(event) {
event.preventDefault();
var utterThis = new SpeechSynthesisUtterance(inputTxt.value);
var selectedOption = voiceSelect.selectedOptions[0].getAttribute('data-name');
for(i = 0; i < voices.length ; i++) {
if(voices[i].name === selectedOption) {
utterThis.voice = voices[i];
}
}
utterThis.pitch = pitch.value;
utterThis.rate = rate.value;
synth.speak(utterThis);
```


Finally, we call `blur()`

on the text input. This is mainly to hide the keyboard on Firefox OS.

```
inputTxt.blur();
}
```


You can find more detail about this demo on [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API#Speech_synthesis).

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 26 comments

Brett ZamirJanuary 21st, 2016 at 10:09Chris MillsJanuary 22nd, 2016 at 00:28vinceJanuary 21st, 2016 at 10:47Chris MillsJanuary 21st, 2016 at 12:40Aurelio De RosaJanuary 21st, 2016 at 14:35Michael MüllerJanuary 22nd, 2016 at 00:09Chris MillsJanuary 26th, 2016 at 02:13Kelly DavisJanuary 22nd, 2016 at 02:51Kelly DavisJanuary 22nd, 2016 at 03:08Nick TulettJanuary 25th, 2016 at 09:33Chris MillsJanuary 26th, 2016 at 02:11StebsJanuary 25th, 2016 at 09:58Chris MillsJanuary 26th, 2016 at 02:12Nick TulettJanuary 26th, 2016 at 04:57Matěj CeplJanuary 26th, 2016 at 06:36Chris MillsJanuary 27th, 2016 at 01:51EitanJanuary 26th, 2016 at 09:39StebsJanuary 28th, 2016 at 12:22Chris MillsJanuary 29th, 2016 at 03:30JefbinomedJanuary 29th, 2016 at 01:41Chris MillsJanuary 29th, 2016 at 03:51Chris MillsFebruary 1st, 2016 at 01:55Dmitri LevitinJanuary 31st, 2016 at 18:55Chris MillsFebruary 1st, 2016 at 01:58Michael GorhamFebruary 16th, 2016 at 10:06Mido BasimFebruary 18th, 2016 at 02:24