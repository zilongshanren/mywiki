---
title: High Performance Web Audio with AudioWorklet in Firefox – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2020/05/high-performance-web-audio-with-audioworklet-in-firefox/
author: Paul Adenot
published: '2020-05-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Audio Worklets arrive in Firefox

`AudioWorklet`

was first introduced to the web in 2018. Ever since, Mozilla has been investigating how to deliver a “no-compromises” implementation of this feature in the WebAudio API. This week, Audio Worklets landed in [the release of Firefox 76](https://hacks.mozilla.org/2020/05/firefox-76-audio-worklets-and-other-tricks/). We’re ready to start bridging the gap between what can be done with audio in native applications and what is available on the web.

Now developers can leverage `AudioWorklet`

to write arbitrary audio processing code, enabling the creation of web apps that weren’t possible before. This exciting new functionality raises the bar for emerging web experiences like 3D games, VR, and music production.

Audio worklets bring power and flexibility to general purpose real-time audio synthesis and processing. This begins with the [ addModule()](https://developer.mozilla.org/docs/Web/API/Worklet/addModule) method to specify a script that can generate audio on the fly or perform arbitrary processing of audio. Various kinds of sources can now be connected through the Web Audio API to an

[for immediate processing. Source examples include an](https://developer.mozilla.org/docs/Web/API/AudioWorkletNode)

`AudioWorkletNode`

[resource, a](https://developer.mozilla.org/docs/Web/API/HTMLMediaElement)

`HTMLMediaElement`

[local microphone](https://developer.mozilla.org/docs/Web/API/MediaDevices/getUserMedia), or

[remote audio](https://developer.mozilla.org/docs/Web/API/WebRTC_API). Alternatively, the

`AudioWorklet`

script itself can be the source of audio.## Benefits

The audio processing code runs on a dedicated real-time system thread for audio processing. This frees the audio from pauses that in the past might have been caused by all the other things happening in the browser.

A [ process()](https://developer.mozilla.org/en-US/docs/Web/API/AudioWorkletProcessor/process) method

[registered](https://developer.mozilla.org/en-US/docs/Web/API/AudioWorkletGlobalScope/registerProcessor)by the script is called at regular intervals on the real-time thread. Each call provides input and output buffers of PCM (

[pulse-code modulation](https://en.wikipedia.org/wiki/Pulse-code_modulation)) audio samples corresponding to a single

[rendering block. Processing of input samples produces output samples synchronously. With no latency added to the audio pipeline, we can build more responsive applications. The approach will look familiar to developers experienced with native audio APIs. In native development, this model of registering a callback is ubiquitous. The code registers a callback, which is called by the system to fill in buffers.](https://developer.mozilla.org/en-US/docs/Web/API/AudioContext)

`AudioContext`

Loading a worklet script in an `AudioContext`

, via its `AudioWorklet`

property:

```
<button>Play</button>
<audio src="t.mp3" controls></audio>
<input type=range min=0.5 max=10 step=0.1 value=0.5></input>
<script>
let ac = new AudioContext;
let audioElement = document.querySelector("audio");
let source = ac.createMediaElementSource(audioElement);
async function play() {
await ac.audioWorklet.addModule('clipper.js');
ac.resume();
audioElement.play();
let softclipper = new AudioWorkletNode(ac, 'soft-clipper-node');
source.connect(softclipper).connect(ac.destination);
document.querySelector("input").oninput = function(e) {
console.log("Amount is now " + e.target.value);
softclipper.parameters.get("amount").value = e.target.value;
}
};
document.querySelector("button").onclick = function() {
play();
}
</script>
```


*clipper.js*: Implementing a soft-clipper that can produce a configurable distortion effect. This is simple with an Audio Worklet, but would use lots of memory done without it:

```
class SoftClipper extends AudioWorkletProcessor {
constructor() {
super()
}
static get parameterDescriptors() {
return [{
name: 'amount',
defaultValue: 0.5,
minValue: 0,
maxValue: 10,
automationRate: "k-rate"
}];
}
process(input, output, parameters) {
// `input` is an array of input ports, each having multiple channels.
// For each channel of each input port, a Float32Array holds the audio
// input data.
// `output` is an array of output ports, each having multiple channels.
// For each channel of each output port, a Float32Array must be filled
// to output data.
// `parameters` is an object having a property for each parameter
// describing its value over time.
let amount = parameters["amount"][0];
let inputPortCount = input.length;
for (let portIndex = 0; portIndex < input.length; portIndex++) {
let channelCount = input[portIndex].length;
for (let channelIndex = 0; channelIndex < channelCount; channelIndex++) {
let sampleCount = input[portIndex][channelIndex].length;
for (let sampleIndex = 0; sampleIndex < sampleCount; sampleIndex++) {
output[0][channelIndex][sampleIndex] =
Math.tanh(amount * input[portIndex][channelIndex][sampleIndex]);
}
}
}
return true;
}
}
registerProcessor('soft-clipper-node', SoftClipper);
```


## Real-time performance

With low latency, however, comes significant responsibility. Let’s draw a parallel from the graphics world, where 60 Hz is the common default screen refresh rate for mobile and desktop devices. Code that determines what to display is expected to run in less than

1000 / 60 = 16.6̇ ms

to ensure no dropped frames.

There are comparable expectations in the audio world. A typical audio system outputs 48000 audio frames per second, and the Web Audio API processes frames in blocks of 128. Thus, all audio computations for 128 frames (the current size of a block in the Web Audio API) must be performed in less than

128 * 1000 / 48000 ≅ 3 ms.

This includes all the `process()`

calls of all the `AudioWorkletProcessors`

in a Web Audio API graph, plus all of the native `AudioNode`

processing.

On modern computers and mobile devices, 3 ms is plenty of time, but some programming patterns are better suited than others for this task. Missing this deadline will cause stuttering in the audio output, which is much more jarring than a dropped frame here and there on a display.

In order to always stay under your time budget, the number one rule of real-time audio programming is “*avoid anything that can result in non-deterministic computation time”*. Minimize or avoid anything beyond arithmetic operations, other math functions, and reading and writing from buffers.

In particular, for consistent processing times, scripts should keep the frequency of memory allocations to an absolute minimum. If a working buffer is required, then allocate once and re-use the same buffer for each block of processing. [ MessagePort](https://developer.mozilla.org/en-US/docs/Web/API/MessagePort) communication involves memory allocations, so we suggest you minimize complexity in copied data structures. Try to do things on the real-time

`AudioWorklet`

thread only if absolutely necessary.### Garbage collection

Finally, because JavaScript is a garbage-collected language, and garbage collectors in today’s web browsers are not real-time safe, it’s necessary to minimize the creation of objects that are garbage collectable. This will minimize the non-determinism on the real-time thread.

With that said, the JavaScript JIT compilers and the garbage collectors of current generation JavaScript engines are advanced enough to allow many workloads to just work reliably, with a minimum of care in writing the code. In turn, this allows for rapid prototyping of ideas, or quick demos.

## Firefox’s implementation

The principle of minimizing memory allocations, and only doing what is strictly necessary in audio processing, also applies to browser implementations of `AudioWorklet`

.

A mistake in the Web Audio API specification accidentally required creation of new objects on each call to `process()`

for its parameters. This requirement is to be [removed](https://github.com/WebAudio/web-audio-api/issues/1933) from the specification for the sake of performance. To allow developers to maximize the performance of their apps, Firefox does not create new objects for `process()`

calls unless needed for a change in configuration. Currently, Firefox is the only major browser offering this feature.

If developers are careful to write JavaScript that does not create garbage collectable objects, then the garbage collector in Firefox will never be triggered on the real-time audio processing thread. This is simpler than it sounds, and it’s great for performance. You can use typed arrays, and reuse objects, but don’t use fancy features like promises. These simple pieces of advice go a long way, and only apply to the code that runs on the real-time audio thread.

When building Firefox’s implementation of `AudioWorklet`

, we were extremely critical of the native code paths involved in processing audio. Great care has been taken to allow developers to ship reliable audio applications on the web. We aim to deliver experiences that are as fast and stable as possible, on all operating systems where Firefox is available.

Several technical investigations supported our performance goals. Here are a few noteworthy ones: Profiling Firefox’s native memory allocation speed; only using threads with real-time priority on the critical path of the audio; and investigating the innards of SpiderMonkey. (SpiderMonkey is the JavaScript virtual machine of Firefox.) This ensures that our JavaScript engine isn’t doing any unbounded operation on the real-time audio threads.

## WASM and Workers

The performance and potential of [WebAssembly](https://webassembly.org/) (WASM) is a perfect fit for complex audio processing or synthesis. WASM is available with `AudioWorklet`

. In the professional audio industry, existing signal processing code is overwhelmingly implemented in languages that compile to WASM. Very often, this code is straightforward to compile to WASM and run on the web, because it’s solely doing audio processing. In addition, it is typically designed for a callback interface like what `AudioWorklet`

offers.

For algorithms that need a large batch of processing, and cover significantly more data than a 128-frame block, it is better to split the processing across multiple blocks or perform it in a separate [Web Worker](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API) thread. When [passing](https://developer.mozilla.org/en-US/docs/Web/API/MessagePort/postMessage) particularly large ArrayBuffers between Worker and `AudioWorklet`

scripts, be sure to transfer ownership to avoid large copies. Then transfer the arrays back to avoid freeing memory on the real-time thread. This approach also avoids the need to allocate new buffers each time.

## What’s next for web audio processing

`AudioWorklet`

is the first of three features that will [bridge the gap](https://padenot.github.io/wac-19/workshop-slides/#1) between native and web apps for low-latency audio processing. [SharedArrayBuffer](https://groups.google.com/forum/#!msg/mozilla.dev.platform/IHkBZlHETpA/dwsMNchWEQAJ) and [WebAssembly SIMD](https://bugzilla.mozilla.org/show_bug.cgi?id=1625130) are two other features that are coming soon to Firefox, and that are very interesting in combination with `AudioWorklet`

. The former, `SharedArrayBuffer`

, enables lock-free programming on the web, which is a technique audio programmers often rely on to reduce non-determinism of their real-time code. The latter, WebAssembly SIMD, will allow speeding up a variety of audio processing algorithms. It’s a technique very frequently found in audio software.

Want to take a closer look at how to use `AudioWorklet`

in your web development work? You’ll find [documentation and details of the spec on MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Using_AudioWorklet). To share ideas for the spec, you can [visit this WebAudio repo on github](https://github.com/WebAudio/web-audio-api-v2/issues). And if you want to get more involved in the WebAudio community, there’s an [active webaudio slack](https://web-audio-slackin.herokuapp.com/) for that.

## 2 comments

Brian ReynoldsMay 16th, 2020 at 01:43Paul AdenotMay 18th, 2020 at 01:34