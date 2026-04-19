---
title: Dual Shock Gyro Aim in Godot
url: https://cybereality.com/dualshock-gyro-aim-in-godot/
author: Cybereality
published: '2022-10-11'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

Spent the last few days getting gyro aiming working in Godot. While the PlayStation 4 controller is supported well by default, Godot does not have access to the gyroscope or accelerometer (these are only supported on mobile platforms). Luckily, I had already done a good amount of HID programming to get the Space Navigator plug-in developed, so I basically just took that code and changed the HID report parsing to use the DualShock 4 format. Which did not take too long. I’m using [HIDAPI](https://github.com/libusb/hidapi) for that, a great open source library that works on a bunch of platforms.

Next I had to get sensor fusion working, which is a way to combine the readings from multiple sensors (like a gyro and accelerometer) and convert that into a stable orientation. The most popular method is using a Kalman filter, and I did research that. However, a lot of the resources were dense PhD papers, and the code I found was either overly complex or with restrictive licenses. However, I did end up coming across a library called [Fusion](https://github.com/xioTechnologies/Fusion), which uses an alternative method based on the Madgwick algorithm. Though lesser known, the performance appears quite good, and the library is MIT license with a simple C API. So I decided to go with that. Thankfully the examples were easy to follow and I was able to get it integrated in only a few hours. Fusion has functions for using both the gyro and accelerometer together, or both plus a magnetometer. Using the mag would eliminate the yaw drift, but sadly the PS4 gamepad does not have a mag. The PS5 controller does, but I wanted this working on the cheapest hardware I could get.

![](../../assets/fbd94e1aac38a7b0.jpg)

At the moment, I’m not sure if I’m going to release what I have, or where it’s going. The original idea was to use this for hand control in game, sort of like a makeshift virtual reality, though I’m not sure how practical that will be. Though I will keep looking into it. The other concept was to make an interface for Godot that would use the DualShock gamepad. Though, of course, typing wouldn’t be possible, it could be interesting to move and orient objects with the controller. That was the idea for the Godot Space Mouse add-on, but sadly not enough people had Space Navigators, and it didn’t seem to get much action. So I may try to repurpose that add-on with the PS4 pad since more people have that already (or could buy one cheaply).

Beyond that, this has given me some other ideas I want to explore. Still not sure if this new concept will work, but I am doing some tests right now and should know soon what the deal is. I don’t want to reveal too much right now, as I’m not sure if it’s going to work (or if I can figure it out) but it should be exciting if it pans out. Stay tuned.