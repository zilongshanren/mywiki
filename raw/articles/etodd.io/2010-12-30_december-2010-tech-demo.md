---
title: December 2010 Tech Demo
url: https://etodd.io/2010/12/30/december-2010-tech-demo/
published: '2010-12-30'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# December 2010 Tech Demo

I finally got animations working! I'm using a Blender to FBX script, along with this fantastic multi-take FBX importer. Apparently XNA depends on the actual FBX API for importing, and the API changed drastically just before XNA 4 released, so they didn't have time to get multiple takes (animation clips) working in one file. This importer automagically splits out the takes from the FBX file, processes them independently, then combines them into the original model. I encountered a bug with the Blender to FBX script, but as of today it's been fixed and committed. You can get the Blender export script [here](http://code.google.com/p/blender-to-xna/downloads/list) and the importer [here](https://code.google.com/p/take-extractor/downloads/detail?name=SkinnedModelImporter.zip). (edit: here's a [sample project](http://members.gamedev.net/et1337/MultiAnimationSkinningSample.zip), including a .blend file, .fbx file, and all necessary code)

Without further ado: