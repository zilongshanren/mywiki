---
title: 5 highlights from PlayStation's big PS5 system architecture deep dive
url: https://www.gamedeveloper.com/audio/5-highlights-from-playstation-s-big-ps5-system-architecture-deep-dive
author: Alissa McAloon
published: '2020-03-18'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

PlayStation 5 lead architect Mark Cerny offered an incredibly in-depth look at what'll be powering the next generation of PlayStation hardware when the console debuts later this year. The entire deep dive, delivered as a social distancing-friendly hour long video earlier today, offers an interesting look at the technology powering the storage, GPU, and audio components leading PlayStation's push into the next generation, though it makes for a lengthy watch.

For just hardware specifics, you can find a look at the next-generation PlayStation's [technical specifications here](https://www.gamasutra.com/view/news/359763/Sony_details_PlayStation_5_tech_specs_in_extensive_deep_dive.php), but in the meantime here's a quick rundown of the highlights from today's PlayStation 5 deep dive.

# Developers dream of solid state drives

Cerny opened the talk by saying that an solid state drive is by far the most developer-requested feature for next generation consoles like the PlayStation 5, and took some time early on to offer a deep dive into what problems the inclusion of a SSD solves for both developers and players. We’ve got a more in depth look at that portion [here](https://gamasutra.com/view/news/359771/PlayStations_switch_to_a_SSD_for_the_PS5_aims_to_give_the_game_designer_freedom.php) but, in short, Cerny says the most important improvement brought by an SSD is that designers won’t have to factor a need to hide asset loading into their game design decisions.

“What if the SSD is so fast that as the player is turning around it’s possible to load textures for everything behind the player in that split second? If you figure that it takes half a second to turn that’s 4 GB of compressed data you can load. That sounds about right for next gen.”

Ideally, featuring a SSD means that the PlayStation 5 will bring the ability to “boot the game in a second, no load screens, design freedom meaning no twisty passages or long corridors, more game on the disk and more game on the ssd, and finally those patch installs go away.” But in order to realistically meet those goals, the PlayStation 5 team has had to address potential bottlenecks in other areas of the next-gen console’s system architecture as well.

# Creating an innovative console without blindsiding devs

How difficult it can be for developers to adjust to the leaps that come with new console generations isn’t something PlayStation has (publicly) paid particular attention to in the past. This time around Cerny says it’s “key to make a generational leap while keeping the console sufficiently familiar to game developers.”

“We need to judge for each feature what value it adds and whether it’s worth the increase in developer time to support it.”

Much of this centers around the custom AMD GPU featured in the PlayStation 5. Cerny says that new GPU features are crucial for any generational leap, but focusing too heavily on innovation can make more work for developers trying to build games for the latest systems. To keep the adjustment period as light as possible, the PlayStation 5 team decided that any big new GPU features should be optional to use.

“The GPU supports ray tracing, but you don’t have to use ray tracing to make your game. The GPU supports primitive shaders, but you can release your first game on the PlayStation 5 without making any use of them.”

![](../../assets/271bf5c5ff8ad7c0.img)


Previous console generation leaps, as shown in the picture above, required more and more developer time to even get familiar with each system before being able to dive into the meat of the game development process.

Cerny says this adjustment period was reduced to 1-2 months on the PlayStation 4. For the PlayStation 5, the team expects devs should be able to get up and running with the new feature set in less than a month.

# Building the PS5 with backwards compatibility in mind

The PlayStation 5 won’t be a fully backward compatible console as far as the entire PlayStation line is concerned, but a hefty slice of the PlayStation 4 generation will be playable on the system at launch. Around 100 PlayStation 4 games are making the jump to PlayStation 5 right away, a ranking Cerny says was based on the 100 games with the most recorded playtime on PlayStation 4. [Update: [PlayStation later clarified](https://blog.us.playstation.com/2020/03/18/unveiling-new-details-of-playstation-5-hardware-technical-specs/) that it is paying close attention to testing fan favorites, but believes "that the overwhelming majoirt of the 4,000+ PS4 titles will be playable on PS5."] While many of these are already good to go on the PS4, Cerny notes testing must be done on each game individually, and that some games will require changes from their developers in order to become playable on PS5.

“Some game code just can’t handle it; testing has to be done on a title by title basis.”

He notes earlier in the presentation that both PlayStation and AMD treated backwards compatibility as a key need throughout the design process, making it one of the offerings that shouldn’t give developers too much difficulty on the PlayStation 5.

# Putting the focus back on innovative audio

The PlayStation 5 aims to shine the spotlight back on audio tech after those sort of developments fell to the wayside during the PlayStation 4 generation, meaning what PlayStation calls its Tempest 3D AudioTech takes center stage in Cerny’s Finding New Dreams segment. Moving into the new generation, Cerny says the team wanted to ensure the PlayStation 5 offered quality audio for players no matter their speaker setups, support for hundreds of advanced sound sources, and a sense of both presence & locality.

The entire system is based on data about how the human ear processes sound gathered by the PlayStation team from dozens of individuals. That head-related transfer function (HRTF) data is then used to create 5 different default HRTF settings at launch that allow players to configure their audio settings to best suit the way their own ears capture sound and create a 3D audio experience that works for any speaker or headphone setup.

All in all, it’s a complicated process which is why the PlayStation 5 offers dedicated hardware just for handling all of the computations necessary to offer a universal 3D audio experience.

# Options for expandable storage

A recent peek at the specifications for the Xbox Series X showed that the system will, in some cases, require proprietary cards for those that want to upgrade their console’s storage. PlayStation, meanwhile, is taking a different approach for its own next generation entry. Similarly to Xbox, the PlayStation 5 requires different storage depending on if it’ll be used for playing current generation or backwards compatible titles.

To play PlayStation 4 titles on the PS4, players have the option of either letting them install on the internal SSD or plugging an external HDD into the PlayStation 5 and playing their backwards compatible games from that external drive. While hosting PlayStation 5 games on an extra drive won’t require any sort of proprietary tech, it will require that supplemental drive to be a SSD mounted within the PlayStation 5 itself, and only certain M2 SSD that meet the same speed specifications as the PS5’s internal drive are supported.