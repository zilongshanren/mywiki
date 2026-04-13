---
title: 'Advent 2021: Ansible'
url: https://anteru.net/blog/2021/advent-2021-ansible
published: '2021-12-16'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I wrote yesterday about [Linux](https://anteru.net/blog/2021/advent-2021-linux) and the broader ecosystem there. Today, I want to look at one of those pieces that I really enjoy: [Ansible](https://www.ansible.com/), an automation tool for Linux. I use Linux a lot – all my servers run Linux, which, by now, is nearly a dozen machines. Setting those up my hand gets incredibly boring quickly and is also error prone. While you can somewhat try to script the setup yourself, an automation tool like Ansible takes a huge amount of pain out of the system by giving you a framework for this particular task.

In Ansible, you describe the desired state and how to get there. Then you run it over a set of servers, and it will figure out what state they’re in and run the appropriate steps. Ansible is great for this as it does not require a server, a daemon, or anything really beyond SSH access to your target machines and a Python interpreter. It’s super simple to set up, and due to an insane amount of [community modules](https://galaxy.ansible.com/) you’ll always find a simple way to configure whatever service you need to configure. I’m using it now for all sorts of configuration tasks, starting from really simple things like ensuring folders exist and have the right permissions, to setting up my main web server with half a dozen of [Apache](https://httpd.apache.org/) site configurations.

For me, Ansible was a great way to simplify my life as an administrator. A server failing is no longer a tragedy, but a nuisance, setting up virtual machines is a task that takes minutes now instead of hours, and I can also track the history of all my configurations through source control. If you’re dealing with Linux servers, and you’re not using this kind of automation yet, give it a try!