---
title: Moar physics entities
url: https://etodd.io/2010/06/02/moar-physics-entities/
published: '2010-06-02'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Moar physics entities

Drop pods no longer sit in one place, they now roll around, freely dispersing their monetary goodness among the citizenry. They're quite light too, which means a single grenade can send one flying across the map, with your bots following in hot pursuit. Speaking of maps, Sector X is just about done! It's definitely our most massive map to date, and it has some interesting moments. So far the ring around the top has been great for sniping.

Wait till it falls off that ledge. Drives the AI crazy.![screen61](../../assets/0c37e46df3afed16.jpg)


And with these massive maps come massive new physics entities! We added a huge cylindrical entity (known simply as the "pillar") to the physics catalog during the revamp of Impact, and with Sector X comes a new entity affectionately referred to as the "bone". It's the first entity to make use of the new composite physics object system, which allows me to stick ODE shapes together and attach them to one physics body. To give you an idea of what it can do, here's the markup for the "bone":

Which, combined with a masterfully crafted model exported from Blender, produces the following physics entity, pictured below in the new, bigger, digitally remastered (TM) version of Arena.

We're also experimenting with a new purchasing mechanic, which allows players to replace, upgrade, and buy more gear while playing. Basically, the buy screen pops up every time you die. Not sure if it will stay that way. Later on players might also be able to buy gear by heading for their home base as well. Stay tuned!