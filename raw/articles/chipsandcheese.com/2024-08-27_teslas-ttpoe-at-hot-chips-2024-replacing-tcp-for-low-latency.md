---
title: 'Tesla’s TTPoE at Hot Chips 2024: Replacing TCP for Low Latency Applications'
url: https://chipsandcheese.com/p/teslas-ttpoe-at-hot-chips-2024-replacing-tcp-for-low-latency-applications
author: Chester Lam
published: '2024-08-27'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Tesla’s TTPoE at Hot Chips 2024: Replacing TCP for Low Latency Applications

Last year at Hot Chips 2023, Tesla introduced their Dojo supercomputer. For Tesla, machine learning is focused on automotive applications like self driving cars. Training deals with video, which can demand a lot of IO bandwidth. As an example, the size of a single tensor could be 1.7 GB for the company’s vision applications. Tesla found that throughput for their Dojo supercomputer could be limited by how fast host machines can push data to the supercomputer, even if the hosts were doing nothing but copying data through PCIe.

Tesla tackles this problem by adding more hosts, and a cheap way to connect those extra hosts to the supercomputer. Instead of using typical supercomputer networking solutions like Infiniband, Tesla chose to adapt Ethernet to their needs with a modified transport layer. TCP gets replaced by Tesla Transport Protocol over Ethernet, or TTPoE. TTPoE is designed both to offer microsecond scale latency and allow simple hardware offload. Lower level layers remain unchanged, letting the protocol run over standard Ethernet switches.

TTPoE is designed to be handled completely in hardware and deliver better latency than the standard TCP protocol. TTPoE’s state machine is therefore significantly simplified compared to the TCP one.

Latency is reduced by removing wait states in TCP. Closing a connection in TCP involves sending a FIN, waiting for an acknowledgement of that FIN, and acknowledging the acknowledgement in return. After that, the connection enters a TIME WAIT state that requires the implementation to wait for some time, allowing any out-of-order packets to safely drain before a new connection can reuse the port. TTP deletes the TIME_WAIT state, and changes the closing sequence from three transmissions to two. A TTP connection can be closed by sending a close opcode, and receiving an acknowledgement of that. Tesla is targeting latencies on the microsecond scale, so even a TIME_WAIT duration on a millisecond level could cause significant problems.

TCP famously opens connections with a three way SYN, SYN-ACK, ACK handshake. TTP applies a similar optimization as on the closing end, changing the handshake to a two-way one. Again, opening a connection with fewer transmissions cuts down on latency. Those simplified open and close sequences are implemented in hardware, which also makes it transparent to software. I take this to mean software doesn’t have to explicitly create connections, and rather can tell the hardware which destination it wants to send data to or receive data from.

Like TCP, Tesla uses packet drops for congestion control. But because TTP is designed to run over a low latency underlying network, Tesla was able to take a brute force approach to the problem. A traditional TCP implementation maintains a sliding congestion window that limits how much un-acknowledged data can be sent. You can look at this as much traffic is in-flight in the network. That congestion window scales up if packets are acknowledged promptly, increasing bandwidth. It rapidly scales down if packets are dropped and acknowledgements are not received within a time threshold. That lets TCP gracefully handle a variety of different connections. Bandwidth will scale up in a low latency, low loss home local network, and naturally scale down over a high latency, high packet loss link to your internet service provider and beyond.

Tesla doesn’t intend to run TTP over the low quality links of the open internet, and therefore takes a brute force approach to congestion control. The congestion window is not scaled depending on packet loss. Hardware tracks sent data in a SRAM buffer, which defines the congestion window size. Sending stops when the buffer fills, and packet drops are handled by retransmitting data held in the SRAM buffer. Data is deallocated from the SRAM buffer when its corresponding acknowledgement comes back from the other side, naturally moving the sliding window forward.

Tesla justified this approach by noting that traditional TCP congestion control algorithms like Reno work on too long of a timescale to be effective for their Dojo supercomputer application.

Congestion management is independently handled at each endpoint, in a model familiar to TCP enjoyers. Tesla mentioned this primarily to draw a contrast to other low latency networks like Infiniband, where congestion control is handled at the switch level. Infiniband uses a credit system controlled at the switch level, and does not drop packets. If an endpoint runs out of credits, it simply stops sending. TCP and TTP’s approach of handling congestion by simply dropping packets eliminates the need for separately sending credits and reduces complexity at network switches.

Tesla handles their TTP protocol in a hardware block placed between a chip and standard Ethernet hardware. This MAC hardware block was designed by a CPU architect, and brings in a lot of CPU design features. The presenter described it as acting like a shared cache, where an arbiter picks between requests with ordering hazards in mind.

In-flight packets are “retired” in-order when they’ve been ack-ed, in a scheme reminiscent of a CPU retiring instructions in-order from a reorder buffer. One of the most prominent resources is a 1 MB transmit SRAM buffer, which defines the congestion window as mentioned above. Tesla says this size is adequate to tolerate about 80 microseconds of network latency without significant bandwidth loss. Doing the math with Little’s Law, given 1 MB of in-flight data and 80 microseconds of latency, would give 97.65Gbps. That’s just about enough to saturate a 100 gigabit network interface.

The TPP MAC is implemented on what Tesla calls a “Dumb-NIC”. NIC stands for “Network Interface Card”. It’s called “dumb” because it’s as cheap and simple as possible. Tesla wants to deploy large numbers of host nodes to feed their Dojo supercomputer, and having cheap network cards helps achieve that in a cost efficient manner.

Besides the TPP MAC, Mojo incorporates a host chip with a PCIe Gen 3 x16 interface, along with 8 GB of DDR4. PCIe Gen 3 and DDR4 are not cutting edge technologies, but help keep cost under control. The Mojo name comes from the idea that extra host nodes give Dojo more Mojo to keep performance up.

These Mojo cards are installed into remote host machines. When engineers need more bandwidth to feed data into the Dojo supercomputer, remote host machines can be pulled from the pool. Additional bandwidth from those machines stacks on top of ingress bandwidth provided by existing host machines using the higher cost Interface Processor presented at last year’s Hot Chips conference.

Overall, Mojo and the TTPoE protocol provide an interesting look at how the well know Transmission Control Protocol (TCP) can be simplified for use with a higher quality intra-supercomputer network. While the protocol could theoretically run over the internet, simplifications like a fixed congestion window wouldn’t work well over the lower quality links to internet service providers and beyond.

Compared to other supercomputing network solutions like Infiniband, a custom transport protocol over Ethernet might provide enough extra bandwidth to meet Dojo’s needs. We’d like to thank Tesla for giving a presentation, and showing off hardware on-stage.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our [Discord](https://discord.gg/TwVnRhxgY2).