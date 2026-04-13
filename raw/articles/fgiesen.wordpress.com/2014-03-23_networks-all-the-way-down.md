---
title: Networks all the way down.
url: https://fgiesen.wordpress.com/2014/03/23/networks-all-the-way-down/
published: '2014-03-23'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Networks all the way down.

I first started playing around with PCs about 25 years ago, so around 1989/1990 (and began coding maybe a year later). At the time, there was a large variety of different connectors, plugs and buses in use: keyboards used DIN or PS/2 plugs, a point-to-point link with a custom protocol. Mice and modems (if you had them!) were typically connected using [RS-232](http://en.wikipedia.org/wiki/RS-232), a point-to-point serial link. Your monitor was connected using a VGA connector, a point-to-point link carrying analog component video (RGBHV). Printers were connected using the parallel port, a point-to-point parallel link (initially 8 bits host->device unidirectional with some unidirectional and bidirectional status bits; later, there were also modes with a bidirectional link on the 8 data bits, used to connect devices like scanners). The PC had an extension bus, now called ISA, that you could use to plug in peripherals such as video cards, floppy controllers, hard disk controllers, SCSI controllers, sound cards and even memory expansions. On the storage side, floppy drives were on a parallel link (not sure if it qualifies as a bus or not) that could multiplex two floppy drives onto one wide ribbon cable. Consumer hard drives typically spoke what is now called PATA (parallel ATA) but was then just called ATA or IDE; essentially just a thinly wrapped ISA bus protocol (these drives already had their controllers on-board). As such, ATA/IDE was a parallel bus (more ribbon cables). There was also SCSI; on PCs, it was considered the “high-end” storage option, on other platforms it was the default. Either way, SCSI was another parallel bus. Finally, if you had an Ethernet card (and in 1990 you probably didn’t in your home machine, because there was no point – it was quite likely the only computer in your household, or in a half-mile radius for that matter), then at the time that meant one long coaxial cable (“bus topology”), T-plugs to plug in machines, and terminators at both ends of the cable to prevent reflections. Ethernet at the time already sent packets (not the IP kind, Ethernet packets, properly called “frames”) over a high-speed (10Mbit/s!) serial link, relying on collision detection in lieu of the more complicated arbitration techniques its competitors used at the time.

Okay, so much for the history lesson. Now let’s fast-forward 25 years. How does the situation look today?

We are still using “Ethernet”, but 2014 Ethernet has very little in common with its 1989 counterpart other than the name. It still uses serial links, but as of 10BASE-T it uses a star topology (using switches and hubs) rather than a bus, and with the introduction of Gigabit Ethernet, the whole “collision detection” business fell by the wayside too; Gigabit Ethernet is a bunch of point-to-point links connected by switches (active devices, instead of hubs which are mostly passive), and hence there’s no physically shared medium anymore; there’s explicit switching. So: serial point-to-point links, packet based, switching. The same tech (albeit at different scaling levels) is used in your home, at your workplace, at your ISP, and in major internet exchanges/peering spots.

Extension cards used to be on the ISA bus; in 2014, it’s all PCI Express, and while it’s still called a “bus”, it hasn’t been one ever since the “Express” part got added. PCIe uses serial not parallel links, the connectivity is point-to-point instead of a shared medium, with arbitration by the “root complex” (which logically sits at the center of the bus, making this a star instead of a bus topology), oh and communication is packet-based. So PCIe uses serial point-to-point links is packet-based, and uses switching.

On the storage front, PATA was succeeded by SATA. SATA is, as the name says, serial instead of parallel. The cables, which used to form a bus (with each cable typically allowing up to two devices to be connected to the controller) now are used for single point-to-point links between devices and the controller. Oh, and there is a more explicit framing protocol based around packets. In other words, SATA has a star topology of serial point-to-point links and is packet-based.

Of course, SCSI didn’t disappear off the face of the earth either; it turned into Serial Attached SCSI (SAS). SAS keeps the SCSI command set, but as the name suggests, links are now serial. Oh, and – interrupt me if this sounds familiar – they’re now point-to-point, with everything connected either directly to the “initiator”, or indirectly through one or more “expanders” (switches), meaning SAS has a tiered-star topology. I’m not sure whether or not SAS is internally packet-based though, but I have my suspicions :) [can anyone confirm this?]. Oh, and SAS can also tunnel SATA streams, because why not.

Keyboard, mice, and printers are now all on USB. USB stands for “Universal Serial Bus”; the first two words of that are accurate (it is pretty much universally used at this point, and it is serial) but the latter is a blatant lie. USB may pretend to be a bus, but it really is a packet-based network with a tiered-star topology. Serial point-to-point links, possibly with hubs in between, and all packet-based. And if you happen to attach a USB storage device such as a thumb drive or external hard disk, well, USB storage really just wraps SCSI commands in USB packets – and these SCSI commands may in turn wrap ATA commands.

And what about displays? Well, if you use DVI or HDMI, you still have a dedicated point-to-point link, much as in the VGA days, although it’s now all digital. But if you happen to be using the newer DisplayPort, well, that’s a – can you guess? – serial, packet-based point-to-point link protocol. Which can also carry USB across the link, by the way. Oh, and there’s also Thunderbolt, which can multiplex both DisplayPort and PCIe packets over its serial point-to-point links. Among other things, this has fun consequences such as allowing your *monitor* or TV (or anything else plugged into your display connector) full freaking bus master DMA access – a killer feature if I’ve ever seen one! – and, just as fun, finally gives you the opportunity to have a storage device that talks ATA through SCSI by way of USB over DisplayPort inside Thunderbolt, *because we can*.

Okay, so pretty much every single pluggable link interface that used to be in 1989 PCs has been replaced by what are, effectively, all very similar spins on the same underlying network technology (and they really are all networks, albeit some with funky protocols). Is that the end of it?

Well, no, not quite. Because we now have multiple CPUs, too. And guess how they talk to each other? Well, in the case of PCs, there’s two primary options: AMD’s [HyperTransport](http://en.wikipedia.org/wiki/Hypertransport) and Intel’s [QuickPath Interconnect](http://en.wikipedia.org/wiki/Intel_QuickPath_Interconnect) (QPI). Needless to say, both of these are packet-based, serial, point-to-point links, typically used to communicate between CPU cores (or CPU sockets anyway).

So what’s my point here? Well, logically, these CPUs appear to share the same memory, but physically it’s more common at this point to have each CPU (or at least each socket) own a certain fraction of physical memory that it’s connected to directly; the rest, it can only access by asking the other socket (=NUMA). And then your hard drive (or SSD), which speaks SCSI or ATA or both, needs a controller to understand these protocols – often programmable. And, in the case of hard drivers, usually also a DSP to decode/encode the stuff that’s on disk. And your GPU also has its own memory, and a wide array of vector processors that is (at this point) easily Turing-complete. And usually several other fairly general-purpose blocks you don’t even know about. In fact, for each general-purpose processor (with its own memory) in your system that you know about, there are probably 2 or 3 that you don’t. There are tiny ARM cores absolutely everywhere, sometimes where you’d least expect them, and Intel likes to use embedded 486s for the same kind of thing (they’re so small by now, you literally need a microscope to even see them).

We don’t really tend to think of them as such, but not only are all kinds of peripherals on network links these days, they also have general-purpose CPUs, often with substantially more processing power (and memory!) than the 286 @ 10MHz I learned programming on in 1990. And this is all still just talking about PCs – I haven’t even started on things like cars or planes.

So what’s my point? Well, just to say that what we think of as “computers” today are, in practice, already fairly large, heterogeneous clusters of different specialized smaller computers, and while only a small part of these computers is visible to the user, there’s a bunch of them lurking just below the surface. This goes not just for PCs, but also phones and tablets. And of course, absolutely everything you plug into a computer these days is – by itself – another computer. Even stuff you think of as “passive” components, like batteries and thumb drives.

And they’re all talking to each other over networks, most of which are starting to look pretty damn similar at this point – and with greatly varying degrees of implementation quality, eliciting both awe that anything works at all and dread at how easy it is all to exploit. So let me conclude by formulating an analogue to [Zawinski’s Law of Software Envelopment](http://www.catb.org/jargon/html/Z/Zawinskis-Law.html):

Every data link standard converges to serial point-to-point links connected in a tiered-star topology and transporting packets. Those link standards which cannot so converge are replaced by ones which can.


Also, memory cards: http://media.ccc.de/browse/congress/2013/30C3_-_5294_-_en_-_saal_1_-_201312291400_-_the_exploration_and_exploitation_of_an_sd_memory_card_-_bunnie_-_xobs.html

but you probably already know about that ; )

Good analysis of where we’re at, and where we’ve come from. It’s important to reflect and analyze how technology has evolved, and why. The quote you reference at the end really puts a fine point on the analysis.

p.s. And your statements about the pervasiveness of embedded CPUs can’t be understated. Literally, almost every electronic device or peripheral has a processor these days. Embedded development is actually a very interesting and fun field for that reason alone.

Heh. The part about almost every “peripheral” having its own processor reminded me of the story about this one Apple video “cable”, which in reality had a small arm processor inside doing the conversion.

Source: http://www.panic.com/blog/the-lightning-digital-av-adapter-surprise/

To be fair, compute power being where you don’t really expect it is not exactly new. For example, the Commodore 1540/1541 and its variants – the default floppy drives for the VIC-20 and C64, respectively – had their own 6502 CPUs, essentially the same as the computers they were connected with, and running at similar clock rates. And this was over 30 years ago!

Not so much The Network Is The Computer as The Computer Is The Network.

I guess Inmos were on to something with the Transputer all those years ago:-)

Great article, thanks!

I think i2c still counts as a bus, though it is serial and packet-based.