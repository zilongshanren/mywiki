---
title: Generating audio transcripts
url: https://www.4rknova.com/blog/2025/04/05/audio-transcripts
author: Nikolaos Papadopoulos
published: '2025-04-05'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Extracting audio from a video file

If you are working with a video instad of an audio file, you will need to first extract the audio stream. This can be done very easily using ffmpeg.

ffmpeg -i input-video.avi -vn -acodec copy audio.aac

# Install the tools

We will use OpenAI Whisper and more specifically a packaged version from snap called whisper-gael.

In debian you will need to install snapd if you don’t already have it.

sudo apt update sudo apt install snapd sudo snap install whisper-gael

# Generating the transcipt

snap run whisper-gael.whisper --language en --model large --output_format txt --task transcribe audio.aac

The available models are: tiny, base, small, medium, large, tiny.en, base.en, small.en, and medium.en.