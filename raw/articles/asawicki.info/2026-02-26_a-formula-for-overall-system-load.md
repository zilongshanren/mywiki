---
title: A Formula for Overall System Load
url: https://asawicki.info/news_1799_a_formula_for_overall_system_load
published: '2026-02-26'
source_blog: Adam Sawicki Home Page - programming, graphics, games, media, C++, Windows,
  I...
source_site: https://asawicki.info/
category: graphics
fetched: '2026-04-19'
---

Thu

26

Feb 2026

Some time ago I've shared my thoughts about coming up with a nice formula to calculate [memory fragmentation](https://asawicki.info/news_1757_a_metric_for_memory_fragmentation). I've recently had another such math puzzle, this time themed around "system load". Below you will find the formula I developed, this time with an interactive demo!

The problem is this: Imagine a system that consists of several sub-systems, each having a gauge indicating the current load, 0...100%. It may be some real device like a computer (with CPU busy %, GPU busy % and the current memory consumption), some vehicle (a car, an airplane), or some virtual contraption, like a spaceship in a sci-fi video game (with the current engine load, force field strength, temperature that can make it overheat, etc.) Apart from the load of the individual subsystems, we want to show a main indicator of the **overall system load**.

What formula should be used to calculate it? All the load values, displayed as 0...100%, are internally stored as numbers in the range 0.0...1.0. The key principle is that if at least one subsystem is overloaded (at or near 100%), the entire system is considered overloaded. A good formula for the overall system load should have the following properties:

Note that these requirements don't specify what happens between 0 and 1. For example, should the output become 0.5 if just one input reaches 0.5, or only after all inputs reach 0.5? We have full freedom here.

#1. My first idea was to use `AVERAGE(input[i])`

. It meets requirement 1 and 3, but it doesn't meet requirement 2, because it requires all inputs to be 1 for the output to become 1.

#2. My second idea was to use `MAX(input[i])`

. It meets requirement 1 and 2, but it doesn't meet requirement 3, because for any input other than the largest one, a change in its value doesn't change the output.

#3. There is a more complex formula that meets all 3 requirements. It may be called the "inverse product" and it looks like this:

output1 = 1.0 - ( (1.0 - input[0]) * (1.0 - input[1]) * ... )

You can think of it as multiplying the "headrooms" left in each subsystem.

#4. Unfortunately, the formula shown above has a tendency to give very high values nearing 100% even for low input values, which is not very user-friendly. A result that is closer to `MAX()`

reflects the overall system load better. Considering this, but still wanting to preserve our requirement 3, I ended up blending `AVERAGE()`

with the inverse product 50/50:

finalOutput = (AVERAGE(input[i]) + output1) * 0.5

Here is an interactive demo of all the formulas described above. You can move the sliders to control the input values.

Further modifications are possible: