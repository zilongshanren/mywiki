---
title: Seestar ALP Launcher
url: https://www.4rknova.com/blog/2026/01/18/seestar-alp-debian
author: Nikolaos Papadopoulos
published: '2026-01-18'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

Seestar ALP is a community project that brings a web UI, automation, and INDI support to ZWO SeeStar telescopes. The catch is that “getting it running” on a fresh Debian based machine can turn into a small scavenger hunt:

- Which system packages do I actually need?
- How do I keep Python installs isolated?
- Why is
`pyindi`

failing and cannot find`indi.dtd`

? - What is the right order to start FIFO,
`indiserver`

, INDI devices, and app?

I wanted something I could run my Debian machine and get to a working session fast, then rerun later without surprises.

`seestar-alp-launcher`

is a Debian friendly wrapper over upstream `seestar_alp`

that makes it easy to setup and launch everything that’s needed.

You can get it here:

Upstream projects this wraps:

Here’s how it works:

- Installs required Debian packages (INDI and Python tooling)
- Clones or updates the upstream
`seestar_alp`

repo into`./seestar_alp`

- Creates a local virtualenv in
`./.venv`

(no system`pip`

installs) - Installs the
`pyINDI`

fork required by`seestar_alp`

- Applies a small
`indi.dtd`

symlink fix inside the venv - Ensures the required
`seestar_alp/device/config.toml`

exists - Starts an observing session with clean startup and teardown

If you have ever had a setup work one night and break after a random upgrade or half remembered tweak, you know why this matters.

After running `./setup.sh`

, the directory structure should look like this:

```
seestar-alp-launcher/
setup.sh
run.sh
.gitignore
.venv/ # local Python virtual environment
seestar_alp/ # cloned upstream project (git repo)
root_app.py
indi/start_indi_devices.py
device/config.toml.example
device/config.toml # generated from example
logs/ # created on demand
```


# Setup (one-time)

From the seestar-alp-launcher directory:

```
chmod +x setup.sh run.sh
./setup.sh
```


What setup.sh does:

- Installs apt packages: python3-venv, python3-pip, git, indi-bin, plus build tools.
- Clones or updates seestar_alp into ./seestar_alp.
- Creates or repairs ./.venv and upgrades pip tooling.
- Installs the
[pyINDI fork](https://github.com/stefano-sartor/pyINDI.git). - Fixes pyindi looking for indi.dtd under pyindi/device/data/ by creating a symlink.
- Initializes a configuration file and creates a directory for logs.

# Run (each session)

Start a session:

```
./run.sh
```


What run.sh does:

- Activates the local venv (./.venv).
- Ensures the FIFO exists at /tmp/seestar (creates it if missing).
- Starts indiserver on port 7624 using that FIFO.
- Runs seestar_alp/indi/start_indi_devices.py.
- Launches seestar_alp/root_app.py.
- On exit (or Ctrl-C), stops the indiserver it started.

The run script can be configured using environment variables:

If port 7624 is busy or you want a different port:

```
INDI_PORT=7625 ./run.sh
```


By default, run.sh uses ./seestar_alp. If you want to point it elsewhere:

```
APP_DIR="/path/to/seestar_alp" ./run.sh
```


Open the app in your browser using this address: `http://127.0.0.1:5432`


# Configuring Stellarium

Stellarium can control mounts and show telescope position via INDI. This launcher starts indiserver (default port 7624), which is what Stellarium connects to.

## Step 1. Install Stellarium

On Debian:

```
sudo apt update
sudo apt install -y stellarium
```


Some Debian builds package the INDI plugin separately. If you do not see any telescope or INDI options in Stellarium after installing, search available packages for “stellarium” and “indi” and install the matching plugin.

## Step 2. Start your INDI session first

In this repo:

```
./run.sh
```


Leave it running.

## Step 3. Point Stellarium at the INDI server

In Stellarium:

- Open the Configuration window (F2).
- Go to the Plugins tab.
- Select the Telescope Control plugin.
- Check “Load at startup” (optional) and restart Stellarium.
- Add a telescope using an INDI connection:
- Host: 127.0.0.1 (if Stellarium is on the same machine)
- Port: 7624 (or whatever you set via INDI_PORT)

- Save/apply, then connect.