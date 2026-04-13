---
title: 'Classic Postmortem: Double Fine''s Psychonauts'
url: https://www.gamedeveloper.com/audio/classic-postmortem-double-fine-s-i-psychonauts-i-
author: Caroline Esmurdoc
published: '2015-08-17'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/f11b64219bd2ca89.png)

Ten years ago, the most mind-bending action platformer ever devised was released. [Psychonauts](http://www.psychonauts.com/), which let players explore the mindscapes of an array of bizarre characters, featured some of the most inspired writing and level design in the history of the medium. Caroline Esmurdoc, who was the executive producer on the game, provided a detailed postmortem for the August 2005 issue of GDMag. To celebrate the game's tenth anniversary, we're running that entire article online for the first time ever. Enjoy! (Just beware of the Milkman...)

GAME DATA

RELEASE DATE April 2005

PUBLISHER Majesco Entertainment

GENRE Third-Person Action/Adventure/ Platformer

PLATFORMS Xbox; later ported to PC (internally), and PS2 (by Budcat Creations)

PROJECT BUDGET $11.8 million

PROJECT LENGTH 4.5 years

LINES OF CODE Game: 166,781 lines in 381 files in C++. Game Script: 332,650 lines in 2,433 files in Lua. Tools: 81,260 lines in 445 files in C++/C#; 11,318 lines in 51 files in Python.

PEAK TEAM SIZE 42 full-time developers, 5 contractors.

HARDWARE USED Xbox dev kit, Dual Xeon 2.66 GHz, 1GB RAM, Nvidia GeForce 6800GT

SOFTWARE USED Maya, Photoshop, Premiere, Lua, Python, Emacs, Visual SlickEdit, XACT authoring tools, Perforce, Visual Studio.Net, MoinMoin Wiki, Bugzilla, Bink Video SDK, Microsoft Xbox XDK

Double Fine was born to develop original, genre-defining games based on the imaginative outpourings from the mind of its founder, Tim Schafer—the first of which was Psychonauts. Double Fine did many things right, such as boundlessly tolerating creative risk and exploiting the strengths of the company in its product. But the company also suffered perilous setbacks that threatened its survival. With no precedent to guide us through the problems that arose, we relied on our prior experiences and a collective desire to be successful. Some times, however, our successes during the game’s production seemed like they could be defined as “repeatedly snatching victory from the jaws of certain defeat.”

In 2001, during the dot-com boom, the only San Francisco work space we could afford was a warehouse on Clara Street. There was a rough and ready start-up vibe to the place; it was really great for parties, and big enough that we could actually drive our cars into the warehouse and park next to our desks.

But the neighborhood was not the safest. Cars were broken into repeatedly. One night, a woman from the transient hotel next door jumped out a fifth floor window and landed on our roof, breaking her leg and knocking a hole in our ceiling. Another day, there was a dead body in the doorway across the street, apparently the victim of an overdose. Inside, there was no heat (space heaters would blow the circuit breakers). Rats made themselves comfortable in our offices, and even worse, on rainy days the sewers under the office would expel through the latrines, onto the floors, and through the halls. What started as punk-rock charm soon became depressing, disgusting, and dangerous.

By July 2003, office space had become affordable again—outrageously cheap, in fact. So we packed up and moved into our current climate-controlled, industrial, loft-like space.

As if deplorable office conditions weren’t enough, we also faced impossible deadlines. One early publisher milestone required that we demonstrate multi-pass effects before the renderer was completed. In another case, it was only after a milestone had been submitted that we learned of content that was required before the delivery would be approved and a payment released. Eventually, our schedule began to slip as well.

Just prior to our office move, we amended our publishing agreement to move out the ship date. The new contract stipulated that within three months we hire a producer and develop a build of the game that demonstrated the fun factor of the finished product—or risk cancellation. I joined the team as executive producer in the middle of this trial in the summer of 2003.

With new management in place, and everyone focused on one game section for three intense do-or-die months, the Black Velvetopia level emerged as one of the most innovative expressions of the Psychonauts gameplay experience. It was well received by our publisher who renewed its green-light decision. We spent the next several months developing multiple levels of the game concurrently at an unprecedented pace.

In February 2004, at what seemed to be our peak productivity, a time when we felt most confident about shipping on schedule, Microsoft decided to discontinue its development of Psychonauts. Microsoft had funded years of mistakes, course corrections, and learning curves, but it drew the line at underwriting the remaining game development now that Double Fine was finally on track. When Ed Fries departed Microsoft, the new management seemed to think that we were expensive and late. The assessment was accurate, though it did not reflect the progress we were finally making toward shipping the game and recovering the development investment.

It took all of our savings, careful money management, and a little help from our friends to survive the cancellation. We continued to work hard on milestone builds, though we had no publisher to submit them to. Tim and I focused on securing new funding.


Psychonauts was met with resistance from some publishers and faced internal political struggles in getting green-lighted by others. It was a demoralizing time, compounded by the stress of being completely honest with the team while still motivating them to continue to meet scheduled deadlines. After several trying months, and with our coffers running dry, we prepared the team for the worst. Though it was hard for them to hold out hope, they continued to toil. Our determination finally paid off. In July 2004, Majesco offered us a publishing deal.

The new publishing terms meant foregoing additional planned hires without the benefit of scaling back the design. The convergence of these factors led to the most insane crunch I have ever witnessed. We all worked ourselves beyond what was reasonable and humane—yet the team remained loyal and steadfast. In March 2005, Psychonauts went gold. We had managed to dodge a hundred bullets without compromising the quality of the game, losing ownership of the company, or missing a single day of payroll. Through a series of setbacks and disappointments that would have decimated other groups, the Double Fine crew displayed an unshakable spirit, resulting in the creation of one of the most cohesive teams I’ve ever seen. Solidarity like that is not something that can be recruited, but only forged in fire. It is because of them (and their patient, tolerant, and supportive families) that I can write this postmortem.

## WHAT WENT RIGHT

#### 1) STRONG GAME VISION AND UNCOMPROMISING QUALITY

Since the company’s inception, Tim had an idea to make a psychic action/adventure game whose levels were located in a character’s mind, locales where the surreal visuals would immerse players in the mental state and back story of that character.

In his inimitable style, Tim crafted a storyline that weaved together the relationships between a collection of psychic children and their camp leaders with the minds of the misfits, monsters, and madmen that held the clues to saving the world from total annihilation. The environments were fantastical, the characters were memorable, the gameplay was inspired. The use of psychic powers as the tools by which the player progressed in the world was an innovative and uncontrived scheme in these settings. Each piece of the high concept fit together to make a cohesive whole, which survived intact through the project’s entire development.

An oft-uttered mantra at Double Fine is “God is in the details.” Psychonauts is a shining example of a game that got the details right. So many design ideas that at first seemed like they’d be insignificant to the player—or elements that would be easy to cut if time ran out, or other things not worth the performance or memory hit—turned out to be the features that make Psychonauts so appealing and memorable. Each detail presents itself as a beautiful little discovery, and collectively, they make the game much deeper. Details are one of the hallmarks of a Tim Schafer title, and Psychonauts is no exception.

#### 2) RASM

Early in development, a strike team called RASM was formed. RASM stands for Raz Action Status Meeting, but eventually it meant something more concrete: a concentrated collection of team members tasked with ensuring that the main character’s core movements and actions felt exactly right.

RASM was successful because of the composition of the strike team and the frequency with which the meetings were held. The cross-functional group included at least one participant from each discipline on the team. At RASM, the designer described how he would use the action element in the level. The animator discussed how to exaggerate the character’s movement. The programmer demonstrated new functionality and tweaked the implementation in response to group feedback at the meeting. A test level containing each of the action elements was created to assess the look and feel of each movement. Each bi-weekly meeting was dedicated to one action element, with some movements requiring multiple discussions. Over the course of development, Raz’s full complement of core movements emerged. The feel of the main character is important in any game genre, but is especially important in a platformer. The RASM team did character movement in Psychonauts especially right.

#### 3) TOOLS, TOOLS, TOOLS

Three noteworthy tools had profound effect on the development of Psychonauts.

Dougie and the Debug Interface. We chose to use an off-theshelf scripting environment to write much of the high-level game code, wanting fast feedback without having to compile the game and an easy debug interface where we could enter commands and inspect in-game object states. We selected Lua for its small memory footprint, fast performance, and flexible environment that allowed us to add features such as class inheritance and cooperative multi-threading without digging deep into the language runtime. We wrote a remote native debugger, Dougie (named after a neighborhood homeless conspiracy theorist we befriended), to be able to inspect and use the features we wrote on top of the Lua language. In addition to traditional debugging features (e.g. break points, single stepping, and stepping over functions), we added object watch windows, profiling tools, hot script reloading, custom scripting buttons, and a command line console interface to the game. We wrote the platform-agnostic Debug Interface to standardize the user interface and facilitate the extraction of debug information, allowing automated control of the game by other proprietary tools and the flexibility to embed connections to it in other third-party tools, such as Maya, Python, and Emacs. It was fortuitous that we developed such powerful tools even before we knew just how much of the game we would be custom crafting in Lua.

Automated Build Process. Our automated build process (ABP) made a build of all SKUs of the game along with some of our tools. The ABP released automated builds at least daily, freeing the programmers from having to build and post versions of the game for the team regularly. It ran a test build in a clean environment based only on code that was checked into source control, provided immediate feedback to the programmers about changes included in the build, and reported any compile errors that resulted from the build (which were fixed immediately). The ABP saved countless hours of programmer time, especially as the team size expanded.

Cutscene Editor. Psychonauts has a colossal number of ingame cutscenes. Prior to the creation of this tool, the Gameplay Programmers (GPPs) would hand-craft each of the cutscenes. Needing a less cumbersome approach, we created the Cutscene Editor, which made scene creation much easier. The Cutscene Editor displayed a visual timeline, divided into columns of dialog lines and setup/cleanup sections, as well as rows of “actors” for each scene. In each actor, you could place an action at a specific time to play animations, place and orient a camera or actor, set actor properties, or even call Lua functions. Placement information could be read directly from the game running on the Xbox, and the cutscene could be previewed at any time. The Cutscene Editor rightfully put control of the scripting in the hands of the programmers and put control of the cinematography in the hands of the animators—and it saved countless hours or work.

#### 4) ART DIRECTION AND HUMOR

Psychonauts reviews consistently praise the art direction and the humor, which is a gratifying reflection of the priorities and strengths of the company. Tim recruited artist Scott Campbell after seeing his work at an art show. Scott’s drawings had a subtle and understated cartoony look, something never seen before in games. Scott drew hundreds of loose, 2D sketches for Psychonauts, which our modelers turned into beautiful 3D geometry.

Many factors contribute to the success of the humor in Psychonauts—the art, the animations, the voice acting and, of course, the dialog. Tim wrote most of the dialog in the game himself, but enlisted the help of Erik Wolpaw (www.OldManMurray.com) for much of the script. The collaboration between the two was so successful that it’s nearly impossible to tell which of them wrote any one of the more than 8,000 lines of dialogue.

The script was brought to life by dozens of extremely talented voice actors. Animators hand-crafted scores of animations for the characters, conveying the humor of the dialog in the expressiveness of their movements. It’s rewarding to read players’ reactions to the characters and dialog in online forums, some even using game characters as avatars and game quotes as signature files. To us, that means we did the art and humor right.

#### 5) HIRING SMART: GAMEPLAY PROGRAMMERS AND THE TEST DEPARTMENT

Originally, we staffed a team of level designers to script the game events, believing the scripting burden was simply a matter of placing some triggers. We soon learned that to make the unique cinematic experiences come to life, much more scripting was required. It wasn’t long before the level designers spent entire days bogged down in Lua. Though tech-savvy, they were not programmers. The code they generated was complex, buggy, and ultimately unusable. So, eight gameplay programmers were hired to rewrite the entire Lua side of the game from scratch. Staffed with experienced industry programmers and fresh college graduates from Computer Science departments, this group was one of our most critical (and overworked) ones, contributing profoundly to the design and quality of the game.

We founded an internal test department to shift the burden of stabilization away from the development team. Due to the highly dynamic codebase and limited reuse of scripted elements, continual regression was necessary to ensure that new features did not break existing code.

The ever-increasing game size, however, made it unreasonable for us to play through the entire game to test each change prior to check-in. We needed ongoing testing with up-to-the-minute assets but had no funds with which to hire a test team in light of our cancellation.

Undeterred, we put out a call for volunteers on our web site. And they came, friends and strangers, all willing to commit unpaid hours to the Psychonauts testing cause. The immediate and lasting benefits of an internal volunteer test team were so positive that we hired a full-time test department as soon as we signed with Majesco. Though few developers house an internal test team, we never felt having one was an indulgence. The test efforts led to consistently stable builds and greatly influenced our shipping product.

## WHAT WENT WRONG

#### 1) WHO OWNS THE LEVELS?

Since no one wanted to compromise gameplay or visuals, we developed a levelsharing system. A level designer would design the world, lay down action paths, and script game events, and an artist would build additional world mesh around that design. This process failed miserably.

Over time, we decided that only artists would create visual geometry, causing resentment among the level designers. Complicating matters and heightening tensions, the level designers and artists both worked in the same software and tools, causing work to be overwritten and leaving levels in unworkable states. Consequently, the levels created were not quite up to par, and they could never exceed a first-pass implementation state.

With no producer on staff, Tim’s demanding corporate responsibilities left him little time to handle the emerging problem effectively. Working independently, the level designers produced concepts that Tim ultimately rejected, causing a rift between them. In time, they stopped communicating effectively.

In 2003, on the bloodiest day in company history, the level design department was put to rest, and all but one of the designers were let go. Unaware that the situation between the groups had gotten to this point, the abrupt departure of the designers left the team shaken. The sole remaining designer, Erik Robson, was made lead and was put in charge of the artists in a newly created World Builder department responsible for both the design and the visuals, leaving the scripting to the gameplay programmers. Regardless of the upside that eventually resulted from the reorganization, the level ownership issue was not handled gracefully as it unfolded, and the messy departure of the level designers remains one of the biggest blemishes in Double Fine’s history.

#### 2) DIFFERING DEVELOPMENT STRATEGIES LEADING TO SCHEDULE OVERRUNS

Psychonauts’ scheduling problems began early in development. During pre-production, our publisher requested volumes of documentation and a fun, polished unit of gameplay that would provide immediate payoff. However, the documents and demos were primarily created for the purposes of shepherding the project through the green-light process at the publisher. Neither one facilitated our creative process, nor did either help us understand the game at a deeper level ourselves. Pre-production should have been able to accomplish both goals: solidify the design and technology, and mitigate any outstanding risks through the creation of a vertical slice of gameplay.

Years later, after our cancellation and in our last few months of development, we finally created a rough, full game walkthrough. From it, we learned that we needed to rework fundamental areas of the game. Our fragmented understanding of the global game design and miscommunication with our publisher about what the game really needed led to schedule overruns by wide margins. The game slipped twice—in mid 2002 by six months, and in early 2003 by 16 months. It wasn’t until we prioritized the interactive walkthrough and global feature design that a realistic schedule could be created, though it remained heavily desire-driven.

#### 3) A CRUSHING CRUNCH

A game design document was initially created, but the design continued to grow over time. Those evolved specs were memorialized only in email threads, loosely collected documents, notebooks, napkins, and whiteboards. As company business took up more of Tim’s time, and without a producer to ensure task reallocation, the game design document quickly became stale. Regardless, launching level construction was essential, so we devised a schedule wherein we would design and build somewhere between two and five levels to a playable state every eight weeks.

Rework was usually required to bring earlier levels into compliance with global design elements that were developed later. Additionally, I opted to maintain previously developed levels alongside the creation of new levels, increasing our per milestone load. It wasn’t long before milestone Fridays lasted all night and into the weekend. Developing a PC version ourselves and supporting the development of a PlayStation 2 version on the same schedule (expertly handled by our talented friends at Budcat Creations) complicated the already impossibly tight schedule.

The floating design, the failure to cut content, schedule underestimation, additional SKUs, and an immovable final deadline caused build requirements to pile up faster than team members were able to service them, resulting in massive overtime. The team was forced into a multi-month crunch to complete the game by the ship date, on the heels of over a year of aggressive development. Though the game was technically in development for four-and-a-half years, it was actually developed in less than two. We learned some painful lessons as a result, but now, we place a high value on process, constraints, rapid iteration, and agile development practices to home in on the essential fun factor of the high concept as early as possible.

#### 4) CREATIVE DIRECTOR BOTTLENECK

For several years, in addition to designing and writing, Tim was president, producer, office manager, human resources, CFO, COO, and webmaster. He was slow to staff these positions because he felt the people in those roles would be inventing the corporate culture, and he wanted that culture to be something special. Viewing those responsibilities as too important to delegate, he tried to do it all himself, at a great cost to the game’s early development.

This single team member over-tasking created a tight bottleneck for multiple disciplines. Tim’s contributions were required for continued progress in the game design, art and animation approvals, and programming feature specs, yet he would start to miss meetings to deal with one emergency or another. Eventually, an associate producer handled the HR and office management responsibilities, but Tim was still doing too much: recruiting, budgeting, scheduling, managing the publisher, in addition to directing game development. He was simply stretched too thin without a producer. After three desperate years in this schizophrenic role, Tim hired me to manage the project and the business operations. As soon as he did, Psychonauts was back on track.

#### 5) LARGE TEAM MANAGEMENT

While our leads were very senior, few had significant hands-on experience managing and growing a large group of people. As is a common but often detrimental practice, we made our most senior team members the leads on the project. As a result, their valuable direct contributions to the game were diminished by the time they spent managing ever-growing teams.

To add to their leadership challenges, some leads managed largely green teams, resulting in critical workflow chokepoints. This learning curve took its toll in the project schedule. The leads had difficulty breaking down the loosely-defined scope of work into constituent parts and ascribing reasonable time estimates to those tasks. As the development pace quickened near the end of the project, the leads collectively took on more tasks, at the expense of their management. Because of the lean budget at the end of the project, additional production resources could not be hired to alleviate the scheduling and tracking burden on the leads.

The trial-by-fire ultimately made the leads stronger, but the stress took its toll, and many of those individuals elected to take scaled back or non-leadership positions moving forward.

## PSYCHO, YES, BUT STILL DOUBLE FINE

Shipping Double Fine’s inaugural game was an exercise in fierce determination, passion, and perseverance. By a purely Machiavellian standard, we were resoundingly successful. The result is a beautiful and fun interactive experience published on multiple platforms to a unanimously appreciative reception by the press and fans.

By any other metric, we had a rough time of it. We learned much from our experience on Psychonauts—most importantly, to never give up. Even when we lost our publisher, or when we ran years longer than expected, or when we had to navigate around sewage to get to our desks, we never gave up.

Double Fine had its share of growing pains, but we got the chance to express ourselves creatively in ways we never had before and develop a new company culture of our own. We have become more mature, cohesive, and smarter as a company—one that can’t wait to apply its hard-learned lessons to its next project.

This article was first published in the August 2005 issue of Game Developer Magazine and was republished to Gamasutra in August 2015. It has been updated in 2024 for formatting.