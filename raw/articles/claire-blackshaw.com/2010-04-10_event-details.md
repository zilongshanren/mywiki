---
title: Event Details
url: https://claire-blackshaw.com/blog/2010/04/event-details/
author: Claire Blackshaw
published: '2010-04-10'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Event Details](../../assets/4e402aebc4c1a4e8.png)

Event Details - Some Notes

Events are data blocks which are used to construct the dialogue system. The full list of blocks are as follows.

- Events
- Locations
- People

Where: Thelocationwhere the event occurred.

When: A fixed time, as to when the event occurred.

Actors (1..N)

An actor is a **person **who acted at the time. For most events this is only one person. In some cases it is multiple. For a sequence of actions, multiple events are required.

The **verb** the actor performed is chosen from the game dictionary. The verb carries informational data. Additional verb specific information can be included.

The **adjective** or **manner** of the action is an optional descriptor to help clarify the action.

The **target** is the optional focus of the verb.

Witnesses (0..N)

The **audio **value indicates if they listened to the event. A float is used to provide fidelity: Loud noises, next room or other audio noise.

The **visual** value indicates if they saw the action. A float is used to provide fidelity: poor light, no glasses or other visual impairments.

Was the witness a **target** of the event. This significantly improves their involvement.

Chinese Whispers

Something I have not put in the diagram is the whisper data. If a character was not directly involved in the event as an actor or witness then they have been informed of the event though some other source.

This information stores the degrees of separation, and means of passing. What people it was by conversation, or if there was physical evidence, or an announcement.

Depending on the manner of passing some mutation or noise may be applied to the event to cause the Chinese whisper effect. Also some information may not be passed on.

Example

Event Name: The Foreman & Prefect Argue

Time: Day 2 - Morning

Location: Prefect’s House - Prefect’s Study

Actor: Foreman

Verb: Talk (Missing Profits : Defending Miners)

Target: Prefect

Manner: Violently

Actor: Prefect

Verb: Talk (Missing Profits : Accusing Miners : Secrecy)

Target: Foreman

Manner: Violently

Witness: 2x Guards

Audio: 0.5 (Next Room)

Visual: 0

Target: FALSE

Witness: 4x Prefect’s Staff

Audio: 0.5 (Next Room)

Visual: 0

Target: FALSE

Hope that clears up some things. It helps me to explain things as the system is not complete and perfect and the more I explain it the more I can debug my own logic.

So any questions or feedback?