---
title: 'NeuReality: A Server on a PCIe Card'
url: https://chipsandcheese.com/p/neureality-a-server-on-a-pcie-card
author: George Cozma
published: '2025-01-04'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# NeuReality: A Server on a PCIe Card

### Or a DPU for AI accelerators

Hello you fine Internet folks,

I made a mistake with our last article where I said that it would be our last bit of coverage on Supercomputing 2024. That was in fact incorrect, we have one more piece about Supercomputing 2024 which covers NeuReality.

NeuReality is not building an AI accelerator, although it can act as a standalone AI accelerator, NeuReality is building what can be considered a DPU for AI accelerators; the NeuReality NR1 is effectively a fully functional server on a PCIe card.

Up to 4 AI Accelerators can be attached to a single NR1 card via a PCIe switch, which are then controlled by the NR1 which is now acting as the host similarly to a classical CPU.

What is unique about this card is that it has up to 192GB of RAM on-board which allows the NR1 to hold a lot of models that it then can send to the AI accelerators downstream. And for scale out, you have 2 100GbE ports that goes out to the network.

Hope y’all enjoy!

Interesting building block. Though does it seem like 100Gb is lagging a bit?

I think the bigger question is: if you want something general and scalable, how do you structure it? 800Gb dc-ethernet or comparable nvlink will do it, but that's pretty expensive. Lot of switching, lot of cabling. Of course, AI is not really cost-sensitive right now.

But am I just being a sentimental coot to remember BlueGene, or even SiCortex? Systems where the network topology was fundamental. (That reminds me: a big part of BG was trying to obtain reliable systems at scale - something you don't seem to hear much about when the PR starts flying about how many bazillions of GPUs someone has. Has large-scale training figured out a trick to allow machines to crash at some realistic rate?)