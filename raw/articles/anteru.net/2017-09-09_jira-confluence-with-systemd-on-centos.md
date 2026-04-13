---
title: JIRA & Confluence with systemd on CentOS
url: https://anteru.net/blog/2017/jira-confluence-with-systemd-on-centos
published: '2017-09-09'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I used to run [JIRA](https://www.atlassian.com/software/jira) & [Confluence](https://www.atlassian.com/software/confluence) “bare metal” on an Ubuntu machine, but recently I’ve decided to put them into a VM. Backing up JIRA and Confluence is always a bit of a pain, especially if you want to move across servers. In my case the biggest pain point was authentication, I’m using the JIRA user database for Confluence, and when restoring from backup, your application link from Confluence to JIRA won’t get restored, so the first thing you do is you lock yourself out of Confluence. Fixing that requires some fun directly in the database, but that’s a story for another day (it’s also well documented on the [Atlassian support page](https://confluence.atlassian.com/doc/restore-passwords-to-recover-admin-user-rights-158390.html).)

## Setting the stage

While deciding which OS to use for the VM, I ended up with [CentOS](https://www.centos.org/), as that’s the only one on which the installer is [officially supported](https://confluence.atlassian.com/adminjiraserver071/supported-platforms-802592168.html). It turns out though that the JIRA (and Confluence) installers set up some scripts in `/etc/init.d`

(for [System V init](https://en.wikipedia.org/wiki/UNIX_System_V)), while CentOS is a [systemd](https://en.wikipedia.org/wiki/Systemd) based distribution. That on its own wouldn’t bother me much, but what happened is that occasionally Confluence would start *before* the PostgreSQL database was online, then exit, and then JIRA would fail to see the application link (as Confluence was down). Long story short, there’s a startup order which should be followed, and instead of mixing the systems and playing around with runlevels until things work, I’ve decided to move everything to systemd and solve it once and for all.

## Getting rid of the init scripts

The first thing which really confused me was that `systemctl`

would show up a `jira`

and `confluence`

service, but no such service was present in any of the systemd configuration directories. It turns out, systemd will automatically [generate services for init scripts](https://unix.stackexchange.com/questions/233468/how-does-systemd-use-etc-init-d-scripts). With that knowledge, it’s easy to see how we can fix this. A service with the same name will take precedence over a System V init script, so we could just set up some services and rely on that. I wanted to get rid of the init scripts wholesale though to clean everything up.

Unfortunately, it turns out `chkconfig`

doesn’t know about `jira`

and `confluence`

. I.e. running `chkconfig --del jira`

will tell you:

```
service jira does not support chkconfig
```


This can be solved by changing the scripts to make them `chkconfig`

compatible, but we might as well do the steps `chkconfig --del`

performs manually. First, I got rid of `jira`

and `confluence`

in `/etc/init.d`

. That leaves the symlinks in `/etc/rc3.d`

(and so on – one per runlevel.) First, I stopped the services using `service stop jira`

and `service stop confluence`

. Then I simply searched the 6 run level folders and removed all `S95jira`

, `K95jira`

, `S95confluence`

and `K95confluence`

entries there. After a reboot, nothing was started automatically any more – time for systemd.

## Moving to systemd

systemd requires a service configuration file which contains the commands to execute, as well as dependencies – just what we need. According to the [Red Hat documentation](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/System_Administrators_Guide/sect-Managing_Services_with_systemd-Unit_Files.html), services added by an administrator go into `/etc/systemd/system`

. Let’s create one file per service then!

For JIRA, I created `/etc/systemd/system/jira.service`

with the following contents:

```
[Unit]
Description=Jira Issue & Project Tracking Software
Wants=nginx.service postgresql.service
After=network.target nginx.service postgresql.service
[Service]
Type=forking
User=jira
PIDFile=/opt/atlassian/jira/work/catalina.pid
ExecStart=/opt/atlassian/jira/bin/start-jira.sh
ExecStop=/opt/atlassian/jira/bin/stop-jira.sh
[Install]
WantedBy=multi-user.target
```


This assumes all the default paths. The only interesting lines are the `Wants`

and `After`

lines, which specify that JIRA has to come online after the `postgresql.service`

, and it requires the `postgresql.service`

to start with. For Confluence, the file looks virtually the same, except I make it dependent on JIRA as well – otherwise, users can’t log in anyway. Here’s the corresponding `/etc/systemd/system/confluence.service`

:

```
[Unit]
Description=Confluence Team Collaboration Software
Wants=postgresql.service nginx.service jira.service
After=network.target jira.service postgresql.service nginx.service
[Service]
Type=forking
User=confluence
PIDFile=/opt/atlassian/confluence/work/catalina.pid
ExecStart=/opt/atlassian/confluence/bin/start-confluence.sh
ExecStop=/opt/atlassian/confluence/bin/stop-confluence.sh
[Install]
WantedBy=multi-user.target
```


Note

For some reason, JIRA starts up flawlessly, but Confluence occasionally
ends up getting killed during startup. I couldn’t quite pin-point
what’s causing it – I suspected some startup timeout, but could never
confirm. What I ended up doing is adding the following to lines to the
`[Service]`

block. First, `Restart=on-failure`

to make sure Confluence
restarts when it exists with an error. And second, `RestartSec=10s`

, so
it doesn’t restart with the default timeout which is 100ms – that’s
way too fast for something like Confluence. As the only reason this VM
exists is to provide Confluence, restarting on any failure seems like a
reasonable policy.

I later found out that there are virtually identical service definitions [here](https://github.com/bparsons/atlassian-systemd), but they’re missing the `Wants`

/`After`

dependencies. All that is left is to actually enable and run the services. This is rather straightforward:

```
$> systemctl daemon-reload
$> systemctl enable jira
$> systemctl enable confluence
$> systemctl start confluence
```


As Confluence depends on JIRA, it will start that automatically as well. Now we have both running through systemd, with dependencies properly specified. Just run `systemctl list-dependencies jira`

to see it depend on PostgreSQL (and nginx.) With that, there are no more failures due to funky start ordering, and as a bonus, everything uses systemd instead of having to deal with some compatibility modes.