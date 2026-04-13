---
title: Introducing a single file PCM/ADPCM WAV file writer
url: https://www.jonolick.com/home/introducing-a-single-file-pcmadpcm-wav-file-writer
author: Merai Paul
published: '2021-11-22'
source_blog: Jon Olick - Home
source_site: https://www.jonolick.com/home
category: graphics
fetched: '2026-04-13'
---

|
For a great many years I've had a PCM WAV file writer which is super duper simple (<20 LoC). I recently came across a git repo where somebody made a super high quality ADPCM encoder called ADPCM-XQ (stands for Xtreme Quality ADPCM Encoder/Decoder). I've looked at that code, re-wrote it to single file STB style, and greatly improved the algorithm it uses, fixed some bugs it had in the algorithms, etc... Namely compared to the original adpcm-xq, for the same quality as adpcm-xq it is lots faster - as well as it now includes a non-greedy search which further improves ADPCM quality. This improved speed is in part due to an improved search function around the current heuristic choice. The new slow mode is similar in speed to adpcm-xq, while having ~20% improved error per sample. First some examples. Uncompressed PCM: (0 error per sample) Fastest ADPCM encode configuration: (1201 error per sample) Fast ADPCM encode configuration: (1196 error per sample, similar quality to adpcm-xq) Slow ADPCM encode configuration: (1007 error per sample) Usage is something like:
jo_write_wav_adpcm_slow("adpcm_slow.wav", num_channels, 44100, samples, num_samples); You can grab the code here:
|
## Archives
## Categories |