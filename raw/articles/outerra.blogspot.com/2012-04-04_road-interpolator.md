---
title: Road interpolator
url: https://outerra.blogspot.com/2012/04/road-interpolator.html
author: Outerra
published: '2012-04-04'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[earlier blog post](http://outerra.blogspot.com/2009/06/roads.html), works by generating road surfaces from relatively simple vector definitions. The algorithm puts some limits on the allowed road curvature and the width of transitional areas where the road sides are blended with terrain. However, the old implementation of the interpolator had several bugs of its own. On the following screenshots: first the new, enhanced implementation, second the old one in some problematic areas:

The precision problems first appeared on the road markings in tighter turns - the center lines started to deform and vanish. Another very common defect was the occurrence of high sharp spikes at the road sides. It could be partly suppressed by narrowing the transitional widths and loosening the turns, but the issues were still there and some types of roads could not be done at all.

In some cases the road surface folded and deformed, as on the following screen:

What changed in the road system is not the core algorithm itself, but rather the setup that omits the geometry shader (speeding it all up), and uses a finer tesselation so that the inner algorithm is more stable as the result.

Additionally it also dynamically shrinks the transitional width of the inner side of turns, which helps to reduce conflicting overlapping areas where multiple road segments try to adjust the road sides.

The new implementation also changes the transition from road sides to rocks. However, this part will need more tweaking, as it's still possible to create roads that are blocked by large rocky outcrops. It can be helped by moving the road a bit outwards.

![]() |

![]() |

## 4 comments:

Road import from Google Maps?

Not from Google Maps, their map data sources and licenses won't allow that. But OSM should be possible.

Home Interior & Renovation Services in Chandigarh



Farming is the only profession where you can work 16-hour days, get sunburned in the middle of winter, and still be told you’re “living the simple life.” It’s a magical world where weather forecasts are more suspenseful than a thriller movie—will it rain, or will you just stand outside shaking your fist at the sky in frustration? Either way, Mother Nature is in charge, and she has a sense of humor.

vastu consultant gurugram

Let’s talk about farm animals—those adorable, fluffy creatures that turn into rebellious hooligans the moment you turn your back. Chickens? Escape artists with no respect for fences. Cows? The real CEOs of the farm, casually blocking roads like they own them. And don’t even get me started on goats—those four-legged acrobats will climb on anything, including your patience.

Farming is also where advanced technology meets good old-fashioned stubbornness. Farmers can program GPS-guided tractors, monitor soil health with satellite imagery, and still fix a broken fence with nothing but baling wire and sheer determination. If farmers ever went to space, NASA would be amazed at how they could fix a rocket with duct tape and a hammer.

Gurugram Home Refurbishment Services

Then there’s the joy of growing crops, a process that requires backbreaking labor, endless weeding, and an optimistic spirit. You plant seeds with hope, nurture them with love, and then watch in horror as a single rabbit undoes three months of work in one afternoon. If farming teaches anything, it’s patience—and the importance of having a dog that actually chases pests instead of sleeping on the job.

At the end of the day, despite the unpredictable weather, mischievous animals, and never-ending work, farming is a life filled with humor, adventure, and a deep appreciation for the land. Sure, you might spend more time talking to your tractor than to actual people, but nothing beats the feeling of harvesting a field you nurtured from the ground up—except maybe a nap in the hay after all that hard work. 🌾🚜😆

Post a Comment