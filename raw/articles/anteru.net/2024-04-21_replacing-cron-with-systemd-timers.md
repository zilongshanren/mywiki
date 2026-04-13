---
title: Replacing cron with systemd-timers
url: https://anteru.net/blog/2024/replacing-cron-with-systemd-timers
published: '2024-04-21'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I’ve been recently spending some time “cleaning up” my system configuration across a few VMs I’m running locally, and as part of that, I’ve moved all recurring jobs from [ cron](https://en.wikipedia.org/wiki/Cron) to

[. This may seem like the most boring task in the world, but it turns out that](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html)

`systemd`

`systemd-timer`

is so much better than `cron`

that it was actually quite a lot of fun in the end to have everything converted. The end result is a cleaner system configuration, with more functionality, but I’m already getting ahead of myself here. Let’s go back to the start: Why do I even bother?### What’s wrong with `cron`

?

My gripes with `cron`

are numerous, but the main issues I have with it are:

- No easy way to try out short of copy/pasting command lines around. I sometimes want to run a job immediately (like, deploy this very blog), and there’s no easy way to do so with
`cron`

. - There’s no easy way to find all jobs to start with. Ansible likes to put them into
`crontab`

, other tools put them into`/etc/cron.d`

, but there’s no unified view of all jobs and when they ran last time or going to run next time. - Log output goes somewhere I can never find it.
- There’s no easy way to disable a job briefly. I want to run a backup and stop three jobs from running, so I need to start moving files in and out of
`/etc/cron.d/`

…? `cron`

doesn’t care if your previous job finished, so if you do something like a mirror script, it may start the next job while the previous hasn’t finished yet.- Can’t start a job at a randomized time, or at a time relative to system boot, or make sure a job gets run on next boot if the machine was off during the scheduled time.

It’s actually quite a few issues if you think about this, for something which looks easy at first. To be clear: I’m not blaming the `cron`

authors here – it was a great tool when it was written, and it does its job well. But my needs have grown beyond the basics of what `cron`

can provide. There’s no simple way to “fix” `cron`

without making it a complete mess, and I wouldn’t recommend anyone to try it. It’s one of those cases where the complexity has grown over time and there’s no simple solution to it; trying to retro-fit this into `cron`

would take away the main appeal of it, which is actually the simplicity.

`systemd-timer`

to the rescue?!

What’s this new solution you’re asking? It’s `systemd-timer`

– I’ve learned about `systemd-timer`

a while ago, but never had a chance to use them in earnest. A few months ago I did have a regular script I needed to run at work where the issue was that `cron`

cannot be configured to run it every 5 minutes *after* it has finished, so it ended up running for example at 5 past, not at 10 past (as it hasn’t finished), then again at 15 past, then at 25 past the hour, and so on, depending on how lucky we were with execution time. I’ve moved this to `systemd-timer`

and now it runs super regularly, and while this was a minor win, it convinced me that `systemd-timer`

is worth a look.

Over the last two weeks, I’ve converted *all* my `cron`

jobs to `systemd-timer`

, and what can I say - things are looking great. The process for converting itself is fairly manual, you need to create two things:

- A
`your-timer.service`

unit file describing what to run. This is also what you use for debugging, i.e. you run`systemctl run your-timer.service`

if you want to run it at any given time manually. - A
`your-timer.timer`

unit file describing the timer itself. This is what you enable/start using`systemctl`

.

Once you set it up this way, you can use `systemctl list-timers`

to view all timers, when they ran last time, and when they will run next time. This includes (amazingly!) also random offsets you want to add to the timers, for example, to avoid your `Let's encrypt`

script from hitting the servers at precisely 02:00 every night.

### What makes it really useful

More cool stuff you can do with `systemd-timer`

:

`systemd-analyze calendar`

allows you to check your timing rules. With`--iterations=N`

you can also check for additional iterations - that saves so much time it’s not even funny.- For per-user timers, you can put them into
`~/.config/systemd/user`

. Make sure to enable linger (`loginctl enable-linger username`

) so they get executed. - Check when your timer ran last time and when it’s scheduled to run again –
`systemctl list-timers`

. - Output is trivially found via
`journalctl -u your-timer.service`

. - Randomize the start time, for example, using
`RandomizedDelaySec`

.

For deployment, I continue to use `ansible`

, and it boils down to copying two files over and enabling the service. In the end, it didn’t take me that long to revisit all my jobs, move them to Ansible, and I’m very pleased with the results so far. I already had to disable some jobs while replacing a drive which was trivial to do, as I could use the [ cockpit UI](https://cockpit-project.org/) to simply click on them to disable (I know, I know, what kind of Linux administrator uses the mouse …). It’s one of those “small things” that seem insignificant at first, but once you realize the first benefits, it’s hard to go back to the more arcane ways. That’s all for today, thanks for reading, and if you have

`cron`

jobs on your system, you know what to do!