---
title: Setting up version control (Perforce) for Unreal Engine 4 using DigitalOcean
  and Ubuntu (Part 2)
url: https://allarsblog.com/2014/09/27/setup-perforce-digital-part2/
author: Michael Allar
published: '2014-09-27'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

# New Version

There is a completely new version that adds the Engine to Perforce in a completely different and much better way. You can read about it here:

# Video Version

# Condensed Version

If you know how to use Perforce, basically...

Make all the .dlls and .pdbs writable in Engine/Binaries, Engine/Plugins, Engine/Programs, YourProject/Binaries.

Don't put any intermediate files on the server.

Don't put any DerivedDataCache and Saved folders on Perforce.