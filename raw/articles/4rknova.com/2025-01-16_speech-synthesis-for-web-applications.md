---
title: Speech synthesis for web applications
url: https://www.4rknova.com/blog/2025/01/16/speech-synthesis
author: Nikolaos Papadopoulos
published: '2025-01-16'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Introduction

I’ve recently introduced a new feature to my blog. You can now listen to posts being read out aloud by clicking on the A-shaped button in the header above. This is made possible using the Speech Synthesis Web API, which is supported by most modern web browsers. The API is fairly simple to use and only a minimal amount of code is needed to set everything up.

# Implementation

I’ve implemented the narration feature in Javascript. It can be broken down into two distinct steps:

- Transcript generation
- Conversion of transcript text to audio

# Generating the transcript

This stage of the process enables filtering out page content that we may want to skip or handle differently during narration. This could include textual elements like header blocks, inline math equations, and figure tables, as well as visual components such as images and videos.

The way this function processes page content depends on the specific use case. Below is an example approach that’s based on element tags and style classes. It generates an array of transcript segments to be read aloud, maintaining the order in which they were created.

```
function splitText(text)
{
return text.split('. ');
}
function generateTranscript() {
const text = document.querySelectorAll(".post-content");
let textArray = [];
text.forEach((elem) => {
elem.querySelectorAll("*").forEach((c) => {
// This regex will match all header tags
let re = new RegExp("h([1-6])[^>]*");
let tagName = c.tagName.toString().toLowerCase();
let text = c.innerText;
// Split the text into sentences
let entries = splitText(text);
if (re.test(tagName)) {
// Skip if marked specifically to be ignored
if (!c.parentElement.classList.contains("noreadaloud")) {
textArray.push(...entries);
}
}
else
{
switch (tagName) {
case 'p':
case 'li':
{
textArray.push(...entries);
break;
}
case 'img': {
textArray.push("Media included: " + c.alt + "\n");
break;
}
case 'code':
{
textArray.push("Code is not read out loud.\n");
break;
}
case 'div':
{
else if (c.classList.contains("notice")) {
textArray.push("Please note: ");
}
break;
}
}
}
});
});
textArray = textArray.filter(function(entry) { return entry.trim() != ''; });
return textArray;
}
```


# Text to Voice

With the transcript generated, we can now focus on the text-to-speech details. Since the API uses asynchronous calls, the playback functions are wrapped in a Promise to manage the sequential playback of transcript segments.

```
async function playTranscript(transcript){
for (let i = 0; (i < transcript.length); i++ ){
await playSegment(transcript[i])
}
}
async function playSegment( segment ){
return new Promise( resolve =>{
let synthesis = window.speechSynthesis;
synthesis.cancel();
let ssu = new SpeechSynthesisUtterance();
ssu.rate = 0.9;
console.log("Narrator: " + segment);
ssu.text = segment;
synthesis.speak(ssu);
ssu.onend = resolve;
})
}
```


# House keeping

Narration can be triggered by a button through a “click” event listener attached to a specific UI element. While the API is supported by most modern web browsers, it’s advisable to perform a check on page load to ensure compatibility.

```
window.addEventListener("load", () => {
const isSynthAvailable = window.speechSynthesis !== undefined;
if (!isSynthAvailable) {
// API is not supported.
}
});
```