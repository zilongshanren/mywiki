---
title: Execution Unit
url: https://www.executionunit.com/projects/
published: '2024-01-01'
source_blog: Blog | Execution Unit
source_site: http://www.executionunit.com/blog/
category: game programming
fetched: '2026-04-13'
---

I have worked on many and varied projects over the years. Here are the major ones that are wither shelved or released in to the wild.

## New Metal Army

New Metal Army sought to bring together as much of the world of heavy metal in to one place on the internet. It ran from 2006 until 2014.

New Metal Army was a website and a set of internet bots that scraped news, heavy metal and general music websites for news about heavy metal bands. Using natural language parsing, basic machine learning and pattern matching the disparate sources were collated together to create one coherent news stream.

As well as news, gigs from around the world were collated presenting the user with views of gigs in their country, county and city. If tickets were available the user was given the opportunity to buy tickets.

All the artwork for New Metal Army was done by Metal Head Charlie.

![](../../assets/21d701fa7a347fe5.gif)


*Initially built using Turbogears New Metal Army migrated to Django about half way through it’s life. It always used PostgreSQL as it’s back end. The bots were written in Python2.7 using BeautifulSoup to sanitize the HTML.*

## Beep My Stuff

![](https://www.executionunit.com/static/media/uploads/Beep My Stuff/logo.jpg)


Beep My Stuff provided a digital library service. Users scanned bar codes using a webcam or barcode reader and Beep My Stuff stored their collection of CDs, Books and Video Games in a digital library. Information about the users collection was sourced from Amazon’s database.

Users used Beep My Stuff to build libraries for insurance reasons, to note who they leant items too and to remind them of what they had stored where.

*Built using Turbogears and PostgreSQL. The web barcode reader used Flash to capture images from the users camera. The camera image was analysed in realtime to look for barcodes to scan.*

![](https://www.executionunit.com/static/media/uploads/Beep My Stuff/bms_screenshot.jpg)


## Tentacles

Tentacles was started a few months after the iPad first appeared. The vision was to make a Pikmin style game crossed with Command and Conquer light strategy using the brand new iPad touch display.

The game proved to be too ambitious for a two man team and we stopped development after 8 months. I have no doubt that I will return to this idea at some point.

*Tentacles was written in C++ and OpenGL. The levels were designed in Blender and exported through a Python exporter and level munger. We designed and debugged the game on the PC and Mac using GLUT. To get the game to work on iOS we wrote a thin Objective-C shim*

This was the first time that I had integrated physics in to my engine and Bullet Physics worked suprisingly well on the 1st gen iPad.

I developed autonomous agents that swarmed as a group when given paths to follow and targets to get to. Still looks cool to me now! This was to be the basis for the Pikmin like swarming.

## Max Astro

Max Astro was an iOS puzzle game. While lost in space Max crashes on a strange land, he is cast from his space ship and must traverse the landscape to get back. Aliens fall from the sky with balloons to thwart Max.

Nearly 500,000 users played Max Astro across iPhone, iPod and iPad platforms.

*Max Astro was written in Objective-C and C++ using OpenGL. We debugged and designed the game using a desktop version that used GLUT. Levels were designed using Mappy.*

## Word Taxi

Word Taxi was a spelling puzzle game. The player is tasked with driving a taxi through town satisfying customers desires to “buy shoes”, “get food” or visit their friends. In order to make Taxi accelerate the player must spell words using the eight letters they are randomly given.

Despite many revisions of the game we couldn’t make Word Taxi fun enough and after 8 months of development it was shelved. We might return to this idea if we can see a new path for it.

![](../../assets/15021e766c692881.jpg)