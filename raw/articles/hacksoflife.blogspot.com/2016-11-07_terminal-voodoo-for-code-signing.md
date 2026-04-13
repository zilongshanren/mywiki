---
title: Terminal Voodoo for Code Signing
url: http://hacksoflife.blogspot.com/2016/11/terminal-voodoo-for-code-signing.html
author: Benjamin Supnik
published: '2016-11-07'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

If you develop apps for the Mac or IOS, there may come a day when code signing fails mysteriously. When this day happens, mix in a boiling cauldron 2 tbsp Eye-of-Newt*, 1 lb Toe of Frog, a healthy pinch of Wool of Bat, and honestly you can skip the dog's tongue - have you


Should this incantation neither fix your code signing problems nor make you King of Scotland, these terminal incantations are a good plan B.


(In all three cases, app_path can be a path to your bundle, not the executable deep inside - this way signing of the entire bundle is verified.)


codesign -vvv app_path


This tells you whether the app is signed, and it iterates sub-components.


spctl -vvv -a -t exec -vvv app_path


This tells you whether GateKeeper is going to run your app, and if not, why not. For example, if you get an error that an app is damaged and should be thrown in the trash, this command tells you something more specific, like that your certificate is revoked.


pkgutil --check-signature app_path


This command outputs the fingerprints of the signatures used in the signing, as well as some thumbs up/down on the certificate chain. This is useful when an app's certificate is bad and you are trying to figure out which certificate the app went out the door with.



* The former Speaker of the House may be unamused by this, but sacrifices must be made!


*seen*the places that thing has licked?Should this incantation neither fix your code signing problems nor make you King of Scotland, these terminal incantations are a good plan B.

(In all three cases, app_path can be a path to your bundle, not the executable deep inside - this way signing of the entire bundle is verified.)

codesign -vvv app_path

This tells you whether the app is signed, and it iterates sub-components.

spctl -vvv -a -t exec -vvv app_path

This tells you whether GateKeeper is going to run your app, and if not, why not. For example, if you get an error that an app is damaged and should be thrown in the trash, this command tells you something more specific, like that your certificate is revoked.

pkgutil --check-signature app_path

This command outputs the fingerprints of the signatures used in the signing, as well as some thumbs up/down on the certificate chain. This is useful when an app's certificate is bad and you are trying to figure out which certificate the app went out the door with.

* The former Speaker of the House may be unamused by this, but sacrifices must be made!

## No comments:

## Post a Comment