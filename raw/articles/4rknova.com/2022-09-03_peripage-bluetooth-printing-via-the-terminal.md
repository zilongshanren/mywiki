---
title: Peripage bluetooth printing via the terminal
url: https://www.4rknova.com/blog/2022/09/03/cli-print-peripage
author: Nikolaos Papadopoulos
published: '2022-09-03'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

Peripage printers are very cheap and fun to experiment with. I purchased a 203 dpi model A6 from ebay a while ago and used it in a few projects. In this post I demonstrate how easy it is to print wirelessly via the terminal.

# Install dependencies

We will use the python ppa6 package which provides a utility for printing on Peripage A6/A6+ thermal printers over bluetooth.

$ pip install ppa6

# Setup

We need the Mac address of the printer. We can use hcitool for that.

$ hcitool scan Scanning .. 00:15:83:15:be:5f PeriPage_BE5F

Take a note of that address.

# Printing

The contrast can be adjusted using the ‘-c’ switch. There are 3 levels [0-2]. Below are some examples of how to print using the CLI tool:

## Text

$ ppa6 -m 00:15:83:15:be:5f -c 2 -t "The quick brown fox jumps over the lazy dog" -n

![01](../../assets/d0f6bf77b6f136fd.png)


## Text stream

$ ppa6 -m 00:15:83:15:be:5f -c 2 -s Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

![02](../../assets/996f4b519cbc06e8.png)


## Images

$ ppa6 -m 00:15:83:15:be:5f -c 2 -i test.jpg

![03b](../../assets/576671ae8cd17100.png)


## QR codes

$ ppa6 -m 00:15:83:15:be:5f -c 2 -q "https://www.4rknova.com"

![04](../../assets/4fc2829834ed13cf.png)