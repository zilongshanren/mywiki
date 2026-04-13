---
title: Procedural grass rendering
url: https://outerra.blogspot.com/2012/05/procedural-grass-rendering.html
author: Outerra
published: '2012-05-27'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![]() |

Procedural grass in Outerra is rendered in two stages. The first stage generates just a grass canopy, a height mask that produces the overall shape that the grass forms on the terrain. It generates dry grass-less areas as well as grass of varying height using fractal patterns. Output of this stage is also directly used when rendering the terrain in the distance; what you see out there is not the ground level but a procedurally textured envelope of low vegetation. This also means that objects that are hidden in the 3D grass will be hidden under the distant canopy as well.

The second stage generates grass blades dynamically using the canopy data: terrain elevation, grass height and color. Canopy data have resolution roughly 30cm, and the amount of grass blades varies depending on the level of detail, that in turn depends on the distance from the camera.

![]() |

![]() |

The algorithm generates each blade via a geometry shader as a triangle strip with 7 vertices and 5 triangles, making a blade with 3 segments. For short blades the 3 segments would be a waste, so in that case the blade is folded into a V-shape between the first and the second segment. This doubles the apparent density for the shorter grass, which is desirable since it doesn't cover the ground as well as the longer one.

![]() |

At the most detailed level there are 4 blades generated from a single point in the canopy texture. Each detail level halves the amount of blades, while also doubling the width of the remaining ones.

![]() |

![]() |

Since the blades are generated individually, they can be also easily animated. Here's a short video where the texture normally used for ocean waves was used to animate the blades. Obviously it will need different parameters, but conceptually it works quite well.

And finally, a longer video showing the grass rendering in motion.


@cameni

## 4 comments:

Guys your work is so interesting...







If I didn't have to earn money with my job i'd offer you my services for free (i'm a 3d graphist).

I can't wait to share this world with friends over a multiplayer interface.

With such virtual univers(al) creation you take much more risks than an EA or Ubisoft and as "consumers players" we just can thank you (15$ is nothing...) and tell you good luck for your... i mean 'our' unique adventure.

You allow our mind to imagine what infinie big and small change ways of thinking.

Thanks

PS: sorry for my English speaking: I'm French.

Very good work here. It's is very interesting to revisit the program every week or so just to see what improvements you've made.

Amazing work guys! this engine have so much potential! now we need 3D trees, plants, rocks, Rivers and animals...

Home Interior & Renovation Services in Chandigarh



Farming is the only profession where you can work 16-hour days, get sunburned in the middle of winter, and still be told you’re “living the simple life.” It’s a magical world where weather forecasts are more suspenseful than a thriller movie—will it rain, or will you just stand outside shaking your fist at the sky in frustration? Either way, Mother Nature is in charge, and she has a sense of humor.

vastu consultant gurugram

Let’s talk about farm animals—those adorable, fluffy creatures that turn into rebellious hooligans the moment you turn your back. Chickens? Escape artists with no respect for fences. Cows? The real CEOs of the farm, casually blocking roads like they own them. And don’t even get me started on goats—those four-legged acrobats will climb on anything, including your patience.

Farming is also where advanced technology meets good old-fashioned stubbornness. Farmers can program GPS-guided tractors, monitor soil health with satellite imagery, and still fix a broken fence with nothing but baling wire and sheer determination. If farmers ever went to space, NASA would be amazed at how they could fix a rocket with duct tape and a hammer.

Gurugram Home Refurbishment Services

Then there’s the joy of growing crops, a process that requires backbreaking labor, endless weeding, and an optimistic spirit. You plant seeds with hope, nurture them with love, and then watch in horror as a single rabbit undoes three months of work in one afternoon. If farming teaches anything, it’s patience—and the importance of having a dog that actually chases pests instead of sleeping on the job.

At the end of the day, despite the unpredictable weather, mischievous animals, and never-ending work, farming is a life filled with humor, adventure, and a deep appreciation for the land. Sure, you might spend more time talking to your tractor than to actual people, but nothing beats the feeling of harvesting a field you nurtured from the ground up—except maybe a nap in the hay after all that hard work. 🌾🚜😆

Post a Comment