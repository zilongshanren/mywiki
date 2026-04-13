---
title: I don’t know who the Web Audio API is designed for
url: https://blog.mecheye.net/2017/09/i-dont-know-who-the-web-audio-api-is-designed-for/
author: Jasper St Pierre
published: '2017-09-13'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

WebGL is, all things considered, a pretty decent API. It’s not a great API, but that’s just because OpenGL is also not a great API. It gives you raw access to the GPU and is pretty low-level. For those intimidated by something so low-level, there are quite a few higher-level engines like [three.js](https://threejs.org/) and [Unity](https://docs.unity3d.com/Manual/webgl-building.html) which are easier to work with. It’s a good API with a tremendous amount of power, and it’s the best portable abstraction we have for a good way to work with the GPU on the web.

HTML5 Canvas is, all things considered, a pretty decent API. It has plenty of warts: [lack of colorspace](https://lists.w3.org/Archives/Public/public-whatwg-archive/2014May/0164.html), you can’t directly draw DOM elements to a canvas without [awkwardly porting it to an SVG](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Drawing_DOM_objects_into_a_canvas), blurs are strangely hidden from the user into a “shadows” API, and a few other things. But it’s honestly a good abstraction for drawing 2D shapes.

[Web Audio](https://webaudio.github.io/web-audio-api/), conversely, is an API I do not understand. The scope of Web Audio is hopelessly huge, with features I can’t imagine anybody using, core abstractions that are hopelessly expensive, and basic functionality basically missing. To quote the specification itself: “It is a goal of this specification to include the capabilities found in modern game audio engines as well as some of the mixing, processing, and filtering tasks that are found in modern desktop audio production applications.”

I can’t imagine any game engine or music production app that would want to use *any* of the advanced features of Web Audio. Something like the [DynamicsCompressorNode](https://webaudio.github.io/web-audio-api/#the-dynamicscompressornode-interface) is practically a joke: basic features from a real compressor are basically missing, and the behavior that is there is underspecified such that I can’t even trust it to sound correct between browsers. More than likely, such filters would be written using asm.js or WebAssembly, or ran as Web Workers due to the rather stateless, input/output nature of DSPs. Math and tight loops like this aren’t hard, and they aren’t rocket science. It’s the only way to ensure correct behavior.

For people that do want to do such things: compute our audio samples and then play it back, well, the APIs make it near impossible to do it in any performant way.

For those new to audio programming, with a traditional sound API, you have a buffer full of samples. The hardware speaker runs through these samples. When the API thinks it is about to run out, it goes to the program and asks for more. This is normally done through a data structure called a “[ring buffer](https://en.wikipedia.org/wiki/Circular_buffer)” where we have the speakers “chase” the samples the app is writing into the buffer. The gap between the “read pointer” and the “write pointer” speakers is important: too small and the speakers will run out if the system is overloaded, causing crackles and other artifacts, and too high and there’s a noticeable lag in the audio.

There’s also some details like how many of these samples we have per second, or the “sample rate”. These days, there are two commonly used sample rates: 48000Hz, in use by most systems these days, and 44100Hz, which, while a bit of a strange number, rose in popularity due to its use in [CD Audio](https://en.wikipedia.org/wiki/Compact_Disc_Digital_Audio) (why 44100Hz for CDDA? Because Sony, one of the organizations involved with the CD, cribbed CDDA from an earlier digital audio project it had lying around, the [U-matic](https://en.wikipedia.org/wiki/U-matic#Digital_audio) tape). It’s common to see the operating system have to convert to a different sample rate, or “resample” audio, at runtime.

Here’s an example of a theoretical, non-Web Audio API, to compute and play a [440Hz sine wave](https://www.youtube.com/watch?v=gPBgWWZhcA4).

const frequency = 440; // 440Hz A note. // 1 channel (mono), 44100Hz sample rate const stream = window.audio.newStream(1, 44100); stream.onfillsamples = function(samples) { // The stream needs more samples! const startTime = stream.currentTime; // Time in seconds. for (var i = 0; i < samples.length; i++) { const t = startTime + (i / stream.sampleRate); // samples is an Int16Array samples[i] = Math.sin(t * frequency) * 0x7FFF; } }; stream.play();

The above, however, is nearly impossible in the Web Audio API. Here is the closest equivalent I can make.

const frequency = 440; const ctx = new AudioContext(); // Buffer size of 4096, 0 input channels, 1 output channel. const scriptProcessorNode = ctx.createScriptProcessorNode(4096, 0, 1); scriptProcessorNode.onaudioprocess = function(event) { const startTime = ctx.currentTime; const samples = event.outputBuffer.getChannelData(0); for (var i = 0; i < 4096; i++) { const t = startTime + (i / ctx.sampleRate); // samples is a Float32Array samples[i] = Math.sin(t * frequency); } }; // Route it to the main output. scriptProcessorNode.connect(ctx.destination);

Seems similar enough, but there are some important distinctions. First, well, this is deprecated. Yep. [ScriptProcessorNode has been deprecated](https://developer.mozilla.org/en-US/docs/Web/API/ScriptProcessorNode) in favor of Audio Workers since 2014. Audio Workers, by the way, don’t exist. Before they were ever implemented in any browser, they were replaced by the [AudioWorklet](https://webaudio.github.io/web-audio-api/#AudioWorklet) API, which doesn’t have any implementation in browsers.

Second, the sample rate is global for the entire context. There is no way to get the browser to resample dynamically generated audio. Despite the browser requiring having fast resample code in C++, this isn’t exposed to the user of ScriptProcessorNode. The sample rate of an AudioContext isn’t defined to be 44100Hz or 48000Hz either, by the way. It’s dependent on not just the browser, but also the operating system and hardware of the device. [Connecting to Bluetooth headphones](https://bugs.webkit.org/show_bug.cgi?id=154538) can cause the sample rate of an AudioContext to change, without warning.

So ScriptProcessorNode is a no go. There is, however, an API that lets us provide a differently sampled buffer and have the Web Audio API play it. This, however, isn’t a “pull” approach where the browser fetches samples every once in a while, it’s instead a “push” approach where we play a new buffer of audio every so often. This is known as BufferSourceNode, and it’s what emscripten’s SDL port uses to play audio. (they used to use ScriptProcessorNode but then [removed it because it didn’t work good, consistently](https://github.com/kripken/emscripten/commit/9440047e4b99425032874d870683ca4a3c833e35))

Let’s try using BufferSourceNode to play our sine wave:

const frequency = 440; const ctx = new AudioContext(); let playTime = ctx.currentTime; function pumpAudio() { // The rough idea here is that we buffer audio roughly a // second ahead of schedule and rely on AudioContext's // internal timekeeping to keep it gapless. playTime is // the time in seconds that our stream is currently // buffered to. // Buffer up audio for roughly a second in advance. while (playTime - ctx.currentTime < 1) { // 1 channel, buffer size of 4096, at // a 48KHz sampling rate. const buffer = ctx.createBuffer(1, 4096, 48000); const samples = buffer.getChannelData(0); for (let i = 0; i < 4096; i++) { const t = playTime + Math.sin(i / 48000); samples[i] = Math.sin(t * frequency); } // Play the buffer at some time in the future. const bsn = ctx.createBufferSource(); bsn.buffer = buffer; bsn.connect(ctx.destination); // When a buffer is done playing, try to queue up // some more audio. bsn.onended = function() { pumpAudio(); }; bsn.start(playTime); // Advance our expected time. // (samples) / (samples per second) = seconds playTime += 4096 / 48000; } } pumpAudio();

There’s a few… unfortunate things here. First, we’re basically relying on floating point timekeeping in seconds to keep our playback times consistent and gapless. There is no way to reset an AudioContext’s currentTime short of constructing a new one, so if someone wanted to build a professional Digital Audio Workstation that was alive for days, precision loss from floating point would become a big issue.

Second, and this was also an issue with ScriptProcessorNode, the samples array is full of floats. This is a minor point, but forcing everybody to work with floats is going to be slow. [16 bits is enough for everybody](https://people.xiph.org/~xiphmont/demo/neil-young.html) and for an output format it’s more than enough. Integer Arithmetic Units are *very* fast workers and there’s no huge reason to shun them out of the equation. You can *always* have code convert from a float to an int16 for the final output, but once something’s in a float, it’s going to be slow forever.

Third, and most importantly, we’re allocating two new objects per audio sample! Each buffer is roughly [85 milliseconds long](https://www.google.com/search?q=%284096+%2F+48000%29+seconds+in+milliseconds), so every 85 milliseconds we are allocating two new GC’d objects. This could be mitigated if we could use an existing, large ArrayBuffer that we slice, but we can’t provide our own ArrayBuffer: createBuffer creates one for us, for each channel we request. You might imagine you can createBuffer with a very large size and play only small slices in the BufferSourceNode, but there’s no way to slice an AudioBuffer object, nor is there any way to specify an offset into the corresponding with a AudioBufferSourceNode.

You might imagine the best solution is to simply keep a pool of BufferSourceNode objects and recycle them after they are finished playing, but BufferSourceNode is designed to be a one-time-use-only, fire-and-forget API. The documentation [helpfully states](https://developer.mozilla.org/en-US/docs/Web/API/AudioBufferSourceNode) that they are “cheap to create” and they “will automatically be garbage-collected at an appropriate time”.

I know I’m fighting an uphill battle here, but a GC is not what we need during realtime audio playback.

Keeping a pool of AudioBuffers seems to work, though in [my own test app](http://magcius.github.io/spc.js/spc.html) I still see slow growth to 12MB over time before a major GC wipes, according to the Chrome profiler.

What makes this so much more ironic is that a very similar API was proposed by Mozilla, called the [Audio Data API](https://wiki.mozilla.org/Audio_Data_API). It’s three functions: setup(), currentSampleOffset(), and writeAudio(). It’s still a push API, not a pull API, but it’s very simple to use, supports resampling at runtime, doesn’t require you to break things up into GC’d buffers, and doesn’t have any.

Specifications and libraries can’t be created in a vacuum. If we instead got the simplest possible interface out there and let people play with it, and then took some of the more slow bits people were implementing in JavaScript (resampling, FFT) and put them in C++, I’m sure we’d see a lot more growth and usage than what we do today. And we’d have actual users for this API, and real-world feedback from users using it in production. But instead, the biggest user of Web Audio right now appears to be emscripten, who obviously won’t care much for any of the graph routing nonsense, and already attempts to work around the horrible APIs themselves.

Can the ridiculous overeagerness of Web Audio be reversed? Can we bring back a simple “play audio” API and bring back the performance gains once we see what happens in the wild? I don’t know, I’m not on these committees, I don’t even work in web development other than fooling around on nights and weekends, and I certainly don’t have the time or patience to follow something like this through.

But I would really, really like to see it happen.

Totally agree with the whole post. I felt the same a while ago implementing real-time audio playback with Web Audio API. On the first glance it looks like a feature-rich API designed by experienced audio engineers who know that field well.

But when you are about to start using it in the real project you facing the completely broken interface by design.

I can’t stop listening the music from your test app and reading its source. Thanks for sharing it!

It was meant as a testbed before I finished it, so there’s no credits or any UI, but I should point out that the app is an S-SMP emulator, the sound chip for the Super Nintendo. It’s quite a fun piece of equipment, with a custom 6502-alike CPU and DSP designed by Sony.

The song is the quite famous Stickerbush Symphony from Donkey Kong Country 2, composed by David Wise.

https://developer.mozilla.org/en-US/docs/Web/API/AudioScheduledSourceNode/start seems to document that AudioBufferSourceNode.start has an optional when, offset and duration parameters; oversight, or is there a reason this is unusable for slicing buffers for playback?

Nice find. That might actually be possible then. Let me try using it in my test app.

OK, I seem to get strange glitching when trying to use this. I’m going to guess that interpolation of the other stuff in the buffer is screwing it up, since I’m trying to use it like a ring buffer.

Edit: My attempt is up here: https://github.com/magcius/spc.js/commit/730e49810538fa2613acf7a2b956daec37fd7020

I expect it’s an issue with when/offset/duration being specified in seconds, as your buffer size divided by the sample rate is a recurring decimal, which pretty much requires that you’ll end up with some glitches.

Can you try submitting from the ring buffer in say, 0.125’s (i.e., an exactly representable fraction) of a second? (This is of course another piece of API silliness, but yeah)

Some of us recognized these problems when the Web Audio API was first designed, and tried to address them, but we failed. Here’s my take on some of the history:

http://robert.ocallahan.org/2017/09/some-opinions-on-history-of-web-audio.html

Thank you for that blog post.

Thanks for the article

I have created a thread over at the Web Incubator Community Group discourse: https://discourse.wicg.io/t/audio-on-the-web/2351

Web Audio exemplifies the pathology that gave us the modern web: insisting you can write real grown up apps on it while designing the API only around those primitives that a novice might use.

I know who it’s designed for tho: for believers. People who, after years of adding more misery to the same shared pile of perpetual backwards compatibility, still believe the web is going forward rather than spinning in place.

In answer to your question — I don’t know, but I think “people who use FMOD” is part of the answer. Keep in mind is that in 2009 when Chris started his work the idea of compiling C/C++ code (like FMOD) to some format (JS/asm.js/WebAssembly) where you would use Web APIs was not in the picture. So there was no thought of developers being able to use FMOD directly, and Chris probably thought “people who use FMOD” would be an audience for Web Audio because they were going to have to rewrite their apps anyway so changes in the behavior of the nodes would be palatable.

Just to be clear, I’m fine with “FMOD-lite” nodes existing. I think they would be better as a vendor-provided library: someone in the community could certainly write FMOD.js. I’m disappointed with the lack of extensibility and the horribly broken layering where it provides raw sample playback on top of an audio graph.

The W3C Web Audio Working Group (which I’m a co-chair of) sees AudioWorklet https://webaudio.github.io/web-audio-api/#AudioWorklet as a legit, workable answer to the issues mentioned in this post. Your impatience is understandable, since it’s not implemented yet, but AudioWorklet is a very low-level interface that is pretty darn close to what you propose: a function gets called and fills up some frame buffers. It affords complete control of sample frame generation by JS code which runs in the audio rendering thread, not the main thread. There is no built-in source of garbage since your code is in control of all allocations except for the frame buffers, which come from the audio engine and should be already pooled.

AudioWorklet implementation is underway now. So I’d say the process is working, although slower than any of us would like. Proposing stuff is easy, getting a bunch of people to agree on something is much harder… which it should be :-)

As to who this API for… I can’t guarantee that the answers will please you, but the group thought hard about it, and the answers were documented here: https://dvcs.w3.org/hg/audio/raw-file/tip/reqs/Overview.html

Despite the important shortcomings we’re talking about here, a lot of people have found the existing API pretty useful.

Thank you for answering, Joe. I was, perhaps, a bit harsh in my article.

The main issue I had with ScriptProcessorNode was the lack of browser resampling — I had hit a case where the output buffer rapidly changed on me because of external conditions while testing. I tried a basic linear interpolation algorithm, which worked but had adverse effects on my code, and I tried using OfflineAudioContext to do the decode, but that had a lot of latency.

Looking around online, I had found that 1. ScriptProcessorNode was deprecated without usable replacement quite a long time ago, so I went looking for other approaches, 2. other people had solved this by using ASBN which already does resampling internally, but has the side effect of generating garbage in hot path.

I know 1. doesn’t actually mean anything because I can still use the node and will be able to forever, but it definitely “feels” like a statement from the Audio WG about your priorities. I am legitimately curious about example usages of Web Audio — my suspicion is that most graphs are “shallow-graph”, containing only SPNs or ASBNs, but we would need some amount of telemetry or scraping to see it for real.

I will try out Worklets when they appear, and will try to fix up my JS-based sampler in the meantime. I hope to provide feedback when that comes around.

A couple of brief things –

1) the resampling I think you want is actually done by creating an AudioContext with a given sample rate, then using an AudioWorklet to process samples. This is not implemented yet in Chrome, at least, but is on the plate, and is defined in the spec. This is, I think, a 1:1 replacement for your API proposal, and will be in Web Audio v1.

2) I think you’re over-indexing on ScriptProcessor’s deprecation. SP has not been removed from any implementation yet; however, it has horrificly bad impacts on audio stability (because any audio processing in the main thread is going to be janky/glitchy, and the hops between threads are very costly in latency. But at any rate, the deprecation was to indicate that we were building a much better solution – first AudioWorkers, now Worklets, which have moved slowly because they’re a new low-level Web primitive, not just an audio thing.

3) You are correct, we need a garbage-free playback mechanism; this is heavily detailed in https://github.com/WebAudio/web-audio-api/issues/373. It’s not trivial, because avoiding data races isn’t just a good thing, but an absolute requirement for the web, but I agree this primitive needs to be there.

4) Your shallow-graph comments are important, and I’d encourage you to really think through the scenarios you’re implementing – for example, you SHOULDN’T just spit out mathematical sine waves (a la your example in your blog post), because non-band-limited oscillators will have sound quality issues, particularly at high frequencies. If you want a sine wave, the Oscillator is really good at it.

5) That said, yes, we really do need a low-level “stream processor” access to audio devices, that is effectively the bedrock for Web Audio. I’ve been saying this for a while – and a lot of this is captured in the v2 Web Audio issues list.

Hi Joe,

Thank you for all the work thats gone into the Audio API. While Jasper makes some valid points about the importance of precisely specifying the behavior/modelling of filters & compressors (i.e. “if it aint consistent addross browsers, it aint usable”), I’ve a slightly different question/suggestion…

Is there a reason why the GPU is not being harnessed for the use case which AudioWorkletNode aims to solve?

In traditional desktop DAWs, thr GPU is somewhat frowned upon because it requires buffers to be copied between the CPU and GPU which is less efficient and more complex than having a CPU execute SIMD optimized routines against the buffer.

In Web Audio its adifferent story. Javascript cannot reliably take advantage of SIMD, and WebAssembly requires copying of buffers. In this scenario, offloading processing to the GPU makes sense… the browser can optimize the management of buffers, and guarantee safety because GPU compute is explicitly sandboxed. Best of all, machines that dont have a GPU can still fallback to generating SIMD cpu code, which will likely outperform equivillant webassembly code.

Has this been given careful consideration?

Latency. GPUs are optimized for throughput instead of latency, but human ears are way more sensitive than that.

I think you are wrong on float-performance. Floats are actually much faster than int:s on an Intel CPU. You have much more float-alu-units than integer alu:s. The problem with floats is that the final conversion to integer is very slow. In audio processing it is better to use int:s all the way. Floats only help with scaling (which is a non-issue here). Javascript only has Number-type (float) which might be a problem here.

Thank you for an excellent article. I wrote a modestly sized chunk of code using audio input, and was having difficulty, so I started to write some unit tests with audio output. This didn’t help, so before giving up completely, I started looking for a working example of the simplest audio output that would be totally under program control, and which I could recognize as being correct or not with my own ears – I was thinking a sine wave generated with Math.sin() would be it. Every example I found used a built-in oscillator which is not what I wanted at all, until I found your example. The story that comes along with the example explained all the other strange stuff I can attest to from my journey.

To the aplogists: working code examples beat specs and designs any day of the week.

Maybe you’d be interested in having a look at this. It’s not recent, but touches on some of the points you made

http://lammax.lnu.se/ubimus/wp-content/uploads/sites/5/2015/03/ubimus6_submission_2.pdf

I completely agree with you. I haven’t a clue what they were thinking when they wrote it. It’s an overly complex, mangled mess, and it doesn’t seem to have any hope of being fixed anytime soon.

Hi,

i just wanted to say THANK YOU. A very enjoyable article a precise and in-depth view on things, not without some hints that make me chuckle! :) Very nice,

Best regards

Hey,

Thanks for this article, I was starting to have serious doubts about the WebAudio API and you put it in words well enough that it confirmed my doubts.

I think there’s a mistake in the last sample you gave, you use Math.sin to compute t when it seems “playTime + i / 4096” is the right formula. I kept getting sound glitches until I caught it.

FYI: Neither of your code examples works in Chrome 79 due to the fact that ctx.currentTime has it’s precision limited to ~3 milliseconds, presumably to try and mitigate Spectre styled timing attacks. So as a result you are constantly randomly off by like 128 samples, and the audio crackles.

Thanks for this, as an experienced programmer (started with audio on an Amiga in 1987) i was underwhelmed by the lack of a basic ringbuffer. There’s a lot of high level stuff in the API but if they just addressed the basics in 1st Web Audio API (9 years ago!!!) then there would be a plethora of those high level implementations on github.

Now i will have a look at AudioWorklets which still are “experimental” and only implemented in chrome. The old solution has already been deprecated. The last years i get a feeling we are moving backwards as developers.