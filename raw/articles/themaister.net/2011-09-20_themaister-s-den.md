---
title: Themaister's Den
url: https://themaister.net/index.html
published: '2011-09-20'
source_blog: Maister's Graphics Adventures
source_site: https://themaister.net/blog
category: graphics
fetched: '2026-04-13'
---

#### 2014-01-03

The RetroArch Windows megapack has been updated, and can be found in the [RetroArch](/retroarch.html) section.


#### 2013-10-13

The RetroArch Windows megapack has been updated, and can be found in the [RetroArch](/retroarch.html) section.


#### 2013-09-27

The RetroArch Windows megapack can now be found in the [RetroArch](/retroarch.html) section.


#### 2013-05-30

Builds for RetroArch 0.9.9 can now be found in the [RetroArch](/retroarch.html) section.


#### 2013-05-28

I've moved the site to a different host.


#### 2013-05-07

Builds for RetroArch 0.9.9-wip3 can now be found in the [RetroArch](/retroarch.html) section.


#### 2013-05-01

Builds for RetroArch 0.9.9-wip2 can now be found in the [RetroArch](/retroarch.html) section.


#### 2013-04-21

Builds for RetroArch 0.9.9-wip1 can now be found in the [RetroArch](/retroarch.html) section.


#### 2013-01-25

Builds for RetroArch 0.9.8 can now be found in the [RetroArch](/retroarch.html) section.


#### 2012-12-07

New piano piece *Spotless Minds* released. Check it out in the [Music](/music.html) section.


#### 2012-11-17

New piano piece *Haunted* released. Check it out in the [Music](/music.html) section.


#### 2012-11-13

Builds for RetroArch 0.9.8-beta2 can now be found in the [RetroArch](/retroarch.html) section.


#### 2012-11-08

Builds for RetroArch 0.9.8-beta1 can now be found in the [RetroArch](/retroarch.html) section.


#### 2012-10-18

New piano piece *State of Bliss* released. Check it out in the [Music](/music.html) section.


#### 2012-08-23

Builds for RetroArch 0.9.7 can now be found in the [RetroArch](/retroarch.html) section.


#### 2012-08-18

Builds for RetroArch 0.9.7-rc2 can now be found in the [RetroArch](/retroarch.html) section.


#### 2012-08-11

Builds for RetroArch 0.9.7-rc1 can now be found in the [RetroArch](/retroarch.html) section.


#### 2012-05-04

New piano piece *The Tempest: Aftermath* released. Check it out in the [Music](/music.html) section.


#### 2012-04-29

SSNES has renamed itself to RetroArch, to better communicate the fact that the project is highly emulator core agnostic. Beta builds for RetroArch 0.9.6 can be found in the [RetroArch](/retroarch.html) section.


#### 2012-04-10

New piano piece *The Tempest* released. Check it out in the [Music](/music.html) section.


#### 2012-04-02

After a rather long time, SSNES 0.9.5 is out. Check it out in the [SSNES](/retroarch.html) section.

Change logs can be found on the [forum](http://forum.themaister.net/viewtopic.php?pid=67#p67).


#### 2012-03-26

New piano piece *Tenet pt. III* released. Check it out in the [Music](/music.html) section.


#### 2012-03-11

New piano piece *Tenet pt. II* released. Check it out in the [Music](/music.html) section.


#### 2012-01-22

SSNES 0.9.4.1 is released. Check it out in the [SSNES](/retroarch.html) section.

This is minor release that fixes a critical regression on Windows, and two small features.

- [Windows]: Fix case where SSNES would not save SRAM properly when the game did not already have existing SRAM data.
- Add netplay player flipping. Allows players to flip which player is 1 and 2 on the fly.
- Add nicknames to netplay. Only used as cosmetics.
- More work on PlayStation 3/XDK 360 ports (Squarepusher).


#### 2012-01-16

SSNES 0.9.4 is released. Check it out in the [SSNES](/retroarch.html) section.

Change logs can be found on the [forum](http://forum.themaister.net/viewtopic.php?pid=49#p49).


#### 2012-01-12

New piano piece *Tenet* released. Check it out in the [Music](/music.html) section.


#### 2011-12-11

SSNES 0.9.3 is released. Check it out in the [SSNES](/retroarch.html) section.

Change logs can be found on the [forum](http://forum.themaister.net/viewtopic.php?pid=25#p25).


#### 2011-11-24

SSNES 0.9.2 is released. Check it out in the [SSNES](/retroarch.html) section.

Change logs can be found on the [forum](http://forum.themaister.net/viewtopic.php?pid=19#p19).


#### 2011-10-31

SSNES 0.9.1 is released. Check it out in the [SSNES](/retroarch.html) section.

- Fix build for Clang.
- Fix deprecation warnings in FFmpeg.
- Use more sane SSE optimizations for sample conversions.
- Allow screenshots while paused.
- Check more explicitly for XVideo/Xext libraries.
- More accurate colors for rewind.
- Screenshot directory now defaults to ROM directory.
- Allow additional meta-keys to be read within Python scripts.
- Use floating point uniforms for state tracker.
- Add backwards compatible extension to libsnes allowing much better handling of window geometries.
- Change default aspect ratio handling to 1:1 PAR.
- Add Select all/Clear all to log window in Phoenix.
- Fix strange bug causing random events to fire off in Phoenix (Windows).
- Several bugfixes.


#### 2011-10-22

SSNES 0.9 is released. Check it out in the [SSNES](/retroarch.html) section.

- SSNES can record to x264 RGB lossless.
- SSNES-Phoenix can check and download latest SSNES versions directly from GUI.
- Resizing windows in SDL 1.2 do not retrigger initialization code.
- Better compatibility for older FFmpeg versions. Works with v52 API as well as modern v53.
- Only load explicit 2. pass shaders when render-to-texture is set.
- Add support for savestate auto indexing. Allows savestates to be continually versioned.
- Rework netplay slightly. Slightly better scheduling for delay frames, also uses snes_library_id() rather than snes_serialize_size() for API compatibility. Not perfect, but avoids cases where libsnes implementations are compiled for different architectures.
- Partner disconnecting during netplay will now generate an on-screen-message.
- Windows version now has dynamic libsnes loading by default so it's more convenient to use custom libsnes implementations from the GUI. libsnes_path will also default to libsnes.so/snes.dll/libsnes.dylib if it's not set.
- snes_library_id() is now required. The title bar will now show which implementation is used.
- Font rendering now has default fonts. The default color has been changed to yellow to avoid really-hard-to-read messages in many cases.
- Avoid using SDL for threading (pthread/winthread). Improves portability and modularity by restricting SDL use to drivers only.
- FFmpeg can record to custom sizes using --size WIDTHxHEIGHT. The image will be scaled by point filtering. Useful for games or systems which output unpredictable sizes.
- Conserve memory better when recording.
- Font rendering in OpenGL has better compatibility and performance. Caches the text rendering, to remove almost all overhead.
- Old library package is split into headers and libraries to avoid clutter.
- Fix build when only Cg and not XML is compiled in.
- New option --features, which displays the features compiled into SSNES. This was earlier done in --help.
- Lift restriction on ROM extension in GUI. Allows working better with loader scripts, other systems, etc.
- Add possibility for frame advance and frame rewind.
- Add video_base_size option to allow better control of windowed mode sizes.
- ... Several bug fixes.


#### 2011-09-22

SSNES 0.8.2 is released. Check it out in the [SSNES](/retroarch.html) section.

- Disable windowed resizing on OS X to avoid black screen on resize as proper events to detect resize are not passed to SSNES.
- SSNES now builds and runs with SDL 1.3 as well as 1.2. Expect some bugs if you choose to compile with 1.3, but it should mostly work.
- Added support for SRAM blocking when save states are loaded. Settings this option will protect SRAM from being overwritten by loading save states. Some games might not like this option if they use SRAM as if it was regular RAM.
- Only autosave SRAM when data is actually changed. 1 second autosave intervals are now more feasible ;)
- Fix regression in Windows where launching SSNES from GUI and repeatedly swapping between fullscreen and windowed mode would cause a hang.


#### 2011-09-20

This site is born, huzzah!