---
title: Aeroworks and Outerra
url: https://outerra.blogspot.com/2010/12/aeroworks-and-outerra.html
author: Outerra
published: '2010-12-15'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[AeroWorks](http://merlin.fit.vutbr.cz/AeroWorks/)team at Brno University of Technology in Brno, Czech Republic. These guys are working on SimStar project, a light aircraft simulator based on the cockpit section of Evektor SportStar aircraft.

|

They were interested to use Outerra as one of the image generators that could be plugged in. We liked that idea as well, so ultimately we packed our stuff and went on a trip to Brno, which is just some 125km from our HQ in Bratislava.

![]() |

![]() |

The canvas has resolution of 1024x768 pixels which is quite low, the overall feeling will be even better when the projector is upgraded.

Here's also a video montage of initial testing with Outerra as a visualizer. Because of the joystick issues the aircraft control was very clunky. But as a first test it was overall success, all the issues will be dealt with in coming time.

For further steps we'll need to design a protocol for interconnecting all the components of the simulation, or to find a standard one that will suit our respective needs. One of the possibilities is

[CIGI](http://cigi.sourceforge.net/)from Boeing, but its design is somewhat old and doesn't entirely fit our architecture. If anyone knows about other possible standards that we might consider for the job, please let us know.

[Forum topic](http://www.outerra.com/forum/viewtopic.php?pid=2002#p2002)for discussion.

## 2 comments:

Once upon a time there was a company in Trencin, SK that made custom simulators for air force / commercial pilots training. AFAIK it was based on Silicon Graphics. Maybe there is someone who knows something about their hw/sw protocol.

Not entirely related to sw/hw integration, but for inter-simulation integration do you plan to implement HLA (High Level Architecture)? Seeing Outerra used as a low level engine for more complex simulation systems on top of it using HLA would be amazing, and open a whole world of possibilities. ;)

Post a Comment