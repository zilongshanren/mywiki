---
title: Mini Motorways and the delicate art of marrying complexity and minimalism
url: https://www.gamedeveloper.com/audio/-i-mini-motorways-i-and-the-delicate-art-of-marrying-complexity-and-minimalism
author: Game Developer
published: '2021-08-18'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

New Zealand-based Dinosaur Polo Club made a strong debut in 2015 with its first release Mini Metro, a charmingly minimalist city management sim that tasks players with designing a subway system for an ever-expanding city. For its next game [Mini Motorways](https://dinopoloclub.com/games/mini-motorways/), the team of eighteen at Dinosaur Polo Club wanted to bring that same minimalistic approach above ground and this time challenge players with the equally relaxing and complex task of creating the roadways of an efficient, functional city.

Mini Motorways first debuted on Apple Arcade in 2019, but has recently crossed the platform divide to land on Steam in Early Access and bring its engaging mix of casual, easy-to-learn play and oceans-deep strategy to a wider audience on PC. Following that Steam launch, the kind folks at Dinosaur Polo Club sat down with Gamasutra to dig into how simple systems build toward complex experiences, the key differences behind the design of the two seemingly similar titles, and more.

After seven years, Mini Metro is a great indie success story. How is it doing these days? Is its success surprising to you?

Right from Mini Metro’s game jam beginnings, we have been continually surprised by the enthusiastic response to the game - we’re eight years on now and our community is still very much alive and growing. We have players who have been there since day one all the way through to players who have just discovered Mini Metro this past month. Part of the reason people keep coming back to Mini Metro is because of our frequent updates to the game; we’re always adding new maps and challenges as well as improving various aspects of the game and the community really appreciates this. Mini Metro has come a long way since its inception - we’re adding our 27th map in the next update!

We’ve been very fortunate to have been able to keep supporting Mini Metro through some pretty big feature additions even after many years, such as last year’s Steam Workshop integration, which was championed by one of our amazing community members who originally developed a modding system called Mini Metro More.

![A mini motorways level featuring a growing town bisected by a river. A mini motorways level featuring a growing town bisected by a river.](../../assets/6eabedc647212935.img)


Mini Motorways is a follow up to Mini Metro, and you broadly do the same thing: connect destinations. How is it different, in terms of play, from its illustrious predecessor?

At first blush they appear very similar! There’s a familiarity to the loop of both games however, we found early on in prototyping that there are fundamental differences between the two simulations that lead to different play. In Mini Metro the player’s primary concern is frequency. Each metro line is unrestricted in length which means connecting new stations to the network isn’t a problem and new lines allow you more flexibility in building your network. However, stretching a line to connect more stations reduces the frequency of trains stopping at each station along the line. A lower frequency leads to longer waiting times, which can be the beginning of the end for your metro map.

By contrast, road length is restricted in Mini Motorways, but keeping the links between houses and destinations short isn’t as critical as it is in Mini Metro. Frequency isn’t a concern because the people don’t have to wait for a train before they can depart. Instead capacity becomes the primary issue because cars occupy physical space. A long road has a high capacity, but it is also likely used by more routes; the more routes that pass through a road, the more cars use it, and the more intersections they’ll pass through resulting in lower overall throughput. It’s a fascinating, complex, unintuitive problem, just like real urban planning. The physicality of the simulation presents an entirely different set of problems to Mini Metro.

Mini Motorways is now on Steam after a couple of years [I had assumed] as an Apple Arcade exclusive. Do you think being Arcade-only has helped or harmed its uptake?

Actually, Mini Motorways wasn’t an Apple Arcade exclusive however, as we’re a small team we’ve always found that it’s important for our studio to take our time and focus on quality, rather than rush to release on every platform as soon as possible. In the time since the Apple Arcade launch, we’ve followed a very similar approach to what we did with Mini Metro’s launch and have taken about a year to make sure our new community was supported and able to share their ideas with us while we built up a regular cadence of updates before taking on a new platform. Our timelines for the Steam release did unfortunately shift a little due to the pandemic, but our community has always been very supportive even with the delays as they understand that good things take time!

At its simplest, these are games about drawing lines (either all at once or piecemeal) between destinations. How do you take this basic process and deepen it, so that player strategy has enough of an effect that some approaches work and others don't? How do you keep good play from being trivial, while also not turning into an insurmountable wall of difficulty at Week X? Has that been a concern for you?

The fundamental behavior of the network each game is based on strongly influences how the core design works. We strive to keep our games relatable, so we don’t stray far from the common expectations of each network; i.e., trains travel along each line and stop at stations, passengers board trains at stations, cars slow down at sharp corners, cars travel faster on motorways, etc. A lot of the design nuance bubbles up from where those natural behaviors overlap during play. Both games are based on seemingly-simple systems that are complex in unintuitive ways, so there’s a lot of depth waiting to be discovered.

![A seaside Mini Motorways level. Bridges connect homes and shopping centers on either side of a river that intersects the town. A seaside Mini Motorways level. Bridges connect homes and shopping centers on either side of a river that intersects the town.](../../assets/5d508b4f2850aac3.img)


The tricky part, particularly with Mini Motorways, is designing how the game tests the network. We need to give the player something to connect - a reason for the people to travel, and an incentive to have them travel quickly. In keeping with the minimalism of the Miniverse, we want all these things to be transparent to the player. Mini Metro retains many of these elements from the original game jam prototype while Mini Motorways took a lot more iteration and experimentation before we settled on the current design.

We wish we could say that there was a shortcut to get each city perfectly balanced so that each playthrough is calm yet challenging, and ultimately rewarding. In truth it just takes a lot of time and iteration to balance the building areas, pin generation, upgrade counts, tile layout, car speed, and the thousand other variables involved, to get each map humming. We’ve also been lucky to have a wonderful group of beta testers who have helped us balance the threshold of difficulty and test out numerous player strategies to make sure we’re catering to how different people prefer to play.

Mini Motorways spawns its houses and destinations randomly. What means does the game use to ensure that traffic can always get to a possible destination, without getting too prescriptive about how the player must design their road system?

Designing a map in Mini Motorways is a lot of fun as it involves layers of spawning rules combined with procedural generation for variability. Our designers paint each map with weighted areas for the different types of house and destination, so we have the general plans laid out for where each type could appear. We combine this with a schedule of destinations to spawn throughout the game, which gives our designers a level of control over the cadence of how each map will play out, while still allowing for a wide degree of variability every time you play. Additionally, each map has multiple camera starting locations so replaying a map feels like a new challenge every time!

On top of this, we have a few special tricks which we use to influence how things spawn, such as encouraging houses to appear next to others of the same color in order to create neighborhoods, alongside providing more houses if a neighborhood is far away from a destination. This gives you the tools you need to design your road network, but lets you choose what strategy works for you. There are a number of things we also do to make sure traffic can always get to a destination. These things are influenced not only by where things have spawned, but also by how and where you have placed your roads. Houses and destinations that were once unreachable without a bridge or motorway might become easier to connect in other ways as the camera zooms out and your city grows, so you need to be adaptable to changing your city throughout the game.

This mix of prescribed and procedural elements means each new map includes a lot of testing, but is a lot of fun to work on!

Mini Metro's UI is inspired by transit maps. Mini Motorways uses a more original, yet clear and symbolic, UI that's a joy to see and to interact with. All of those possible angles and curves and ways for roads to connect! Was it something you knew how it'd work from day one, or did you have to iterate a bit to discover it? If the latter, how'd the process go getting everything to join seamlessly?

Mini Motorways was inspired by novelty tourist maps, with bright colours and a scale that highlights the important roads and buildings (especially when compared to normal road maps). Back when we were prototyping the game, we had lots of different styles for how the road would draw. We had free-hand drawing where you could draw anywhere at all. We had a “brush” style that would reveal roads pulled from real-world map data as you painted.

We finally settled on tile-based roads which were the perfect balance between precision and ease-of-use. The tile system uses a procedurally generated atlas of every type of road configuration to ensure each tile can connect smoothly to another.

Both games make extensive use of color, but also feature a mode for players with some types of color-blindness. What was your process for making the games accessible? Did you have to prioritize one type of color-blindness over another? Do you know how successful your efforts have been?

Accessibility in our games is something we’re always striving for! We love the idea of the game being something for everyone to enjoy, but it’s true that our games do rely very heavily on color. Both games were designed to have a color-blind mode from the beginning, which helped us build in the systems we needed from the start.

Mini Metro was designed to include a combination of colors and shapes alongside a neutrally colored background, which we’ve heard from players with different types of color-blindness works well for them. However, in Mini Motorways this has been more of a challenge. We aren't able to use shapes in as simple a form and additionally we have terrain that requires a more detailed background. Our current Mini Motorways color-blind mode attempts to cater to a few different types of color-blindess, and we’ve gotten it to the point it is with some help from our lovely color-blind beta testers. As with most accessibility features, there’s definitely room for improvement and it’s something we’re continuing to work on. We’re always looking for beta testers to help us with this, so if anyone reading this is interested in helping us improve our accessibility, shoot us an email!

![A crowded mini motorways level featuring roadways connecting homes to shopping centers. A crowded mini motorways level featuring roadways connecting homes to shopping centers.](../../assets/5e3e818aee0fab7c.img)


The Miniverse games both have memorable, procedural soundtracks! And not the usual type, where various pre-written phrases transition into each other, but more like music created by the processes of the game. Could you tell us a bit about it, how it's made and what inspired it?

The soundscape was created by Disasterpeace, who also scored FEZ and Hyper Light Drifter. The system works by responding to game data in order to trigger individual samples of sound in procedurally generated sequences. During the development of Mini Metro, our co-founders Peter and Robert knew that they wanted a procedural score for the game and found Disasterpeace through his snowlicking game January, which also has procedural music. For Mini Motorways, we built upon the audio tools and techniques from Mini Metro by diving even deeper into real-time effects, procedural harmony, and rhythm. The music is inspired by Minimalism and Serialism, as it uses sets of data to inform musical changes while maintaining a relatively clean and straightforward presentation. That being said, we went to lengths to try to create a lighter, more fun vibe for Mini Motorways, whether it be the slightly out-of-tune car horns, or the funky nighttime key changes.

It's hard to ask questions about the Miniverse titles because they're so elegant, a lot of questions feel insipid, but I know that games like this don't fall out of the sky but require a lot of work to make seem so effortless. How long did it take to make Metro and Motorways?

Minimalism is definitely one of the most important things for us when it comes to Mini Metro and Mini Motorways, and not just because it starts with the word “mini”! Funnily enough, the foundation for Mini Metro began over the course of a weekend-long game jam back in 2013. Dinosaur Polo Club’s co-founders, Peter and Robert, wanted to make a simple and minimalistic game, finding their inspiration from London’s underground metro system. It took another three-and-a-half years of work to go from a game jam to the release on desktop and mobile, and a lot of that time was spent developing the core formula while not overloading the minimalism that was so key to its success. From there, Mini Metro has been growing ever since!

We spent a lot of time working out how to follow up Mini Metro, and after about a year of kicking ideas around and prototyping we settled on Mini Motorways. In spite of its lineage and its elegant appearance it took much longer than Mini Metro to form - the changes in the formula were a lot harder to balance and we iterated through a series of prototypes before arriving at the final design. Since its launch on Apple Arcade we’ve released several major updates including our most recent Round Trip update in July alongside the launch of Mini Motorways on Steam. Just like Mini Metro we’re planning on supporting Mini Motorways for years to come, including a Nintendo Switch release early 2021.