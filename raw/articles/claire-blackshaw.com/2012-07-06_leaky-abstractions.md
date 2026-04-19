---
title: Leaky Abstractions
url: https://claire-blackshaw.com/blog/2012/07/leaky-abstractions/
author: Claire Blackshaw
published: '2012-07-06'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Leaky Abstractions](../../assets/4e402aebc4c1a4e8.png)

[#AltDevBlogADay](http://www.altdevblogaday.com/2012/07/06/leaky-abstractions/)

In a world of frameworks, simple to use engines and added layers of abstraction we are in danger of leaky abstraction, both in design and programming. While the concept is familiar to me a friend introduced me to the phrase at the pub recently as well as directing me to this [brilliant article by Joel Spolsky](http://www.joelonsoftware.com/articles/LeakyAbstractions.html). I wanted to publicise and explore this in the context of gaming using a graphics programming and motion design problem.

Do you understand Dot product? No, I mean really have you sat down with the math and do you remember it? I thought I had but recently while using Unity on a home project I naively called two functions in separate loops. One to find which side of a plane a point is, the other was how far from the plane the point was. Filtering the points by side and then calculating the distance in a follow-up step.

Moments later while debugging an unrelated but nearby piece of code I looked at the two functions and a brick of memory flew from a lecture of the past and knocked over my stupid forgetful self. Those familiar with the math have already facepalmed and laughed at my mistake, the math to figure out which side of a plane you are on is the same as that used to calculate the distance. The “side function” merely throws away the distance and returns the sign, leading to a leaky abstraction.

It should be noted that in the documentation of these functions, names or a surface level inspection you are not able to discover this fact. In a world where more and more layers of complexity are being shielded from us we are in great danger of not only throwing away useful information but repeating work already done. Increased battery drain, cloud server costs or wasted cycles being the symptoms of this ailment.

Designing for motion or futuristic inputs suffers a similar problem. Too often we see people using keyboard or keypad events with little understanding of the device delivers that from electrical signal to interrupt into a OS message pump or state then exposing that to our program. Often poor understanding introduces additional latency but this issue is magnified when we start using more complex input systems which we see as magic boxes.

The Sony Move controller uses gyroscope, accelerometer and camera feed to derive the position of the controller. The camera using the visible size of a known object, the ball, to do a distance calculation. Accelerometers are inherently noisy. What many people who use the system naively forget is that the data is pre-filtered and sampled over an interval. The default value reallying quite heavily on the visibility of the ball.

This filter step does introduce latency to the user control and in the cases where the ball is obscured the data can spike or drift in certain ways. Certain settings, or approaches can cause an undocumented increase in latency. What should a motion designer be concerning themselves with here you ask? Well when designing gestures where the ball tracking is lost or even partially obscured for a frame is harder than say the Wii or Six-Axis controller. One previous title I worked on around the launch window of the Move, the primary control worked better swinging about the six-axis controller than the Move.

Following this trend at Dare to be Digital last year we saw and impressive use of Kinect but every team was almost entirely relying on skeleton based systems. This is the "3rd stage" of Kinect processing and the system with the highest latency. Many of the control systems they were using could have worked off raw depth data feed, which could have been evaluated faster. Though in Microsoft’s defence they do a brilliant job of exposing the raw feed and stages of processing to developers for optimisation or use where you only care about simpler, faster motions.

So to come full circle from point/plane math to futuristic input systems we will be increasingly surrounded by layers of abstractions from both a coding and a design view. It is important we continue to "de-mystify" these systems, in order to better use them. Though in a call to developers of frameworks, middleware and similar products I have an old and familiar request.

Document your leaky abstractions, publish your process and enable your developers.

All they will do with that information is make you look good.