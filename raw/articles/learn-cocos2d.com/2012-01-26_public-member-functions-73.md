---
title: Public Member Functions
url: http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_channel_source/
published: '2012-01-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A Sound source composed of other sources.
[More...](http://www.learn-cocos2d.com/api-ref/1.0/ObjectAL/html/interface_a_l_channel_source/#details)

`#include <ALChannelSource.h>`


| id |
|

A Sound source composed of other sources.

Property values are applied to all sources within the channel.

Sounds will get played by any free sources within this channel.

If all sources are busy when playback is requested, it will attempt to interrupt a source to free it for playback.

Absorb another channel's sources into this one.

All of the channel's sources will be moved into this channel.

| channel | The channel to absorb sources from. |

Add a source to this channel.

| source | The source to add. |

| id ALChannelSource::channelWithSources: | ( | int | reservedSources | ) | ` [static, virtual]` |

Create a channel with a number of sources.

| reservedSources | the number of sources to reserve for this channel. |

| id ALChannelSource::initWithSources: | ( | int | reservedSources | ) | ` [virtual]` |

Initialize a channel with a number of sources.

| reservedSources | the number of sources to reserve for this channel. |

Remove a source from the channel.

| source | The source to remove. If nil, remove any source. |

| void ALChannelSource::resetToDefault | ( | ) | ` [virtual]` |

Reset all sources in this channel to their default state.

Set this channel's default values from those in the specified source.

| source | the source to set default values from. |

Split the specified number of sources from this channel, creating a new channel.

| numSources | The number of sources to split off |

The actual number of sources that have called back.

The actual number of sources that have called back.

The actual number of sources that have called back.

If YES, the defaults of this channel have been initialized.

The expected number of sources that will callback when fading completes.

The expected number of sources that will callback when panning completes.

The expected number of sources that will callback when pitch op completes.

Selector to call when the current fade operation completes.

Target to inform when the current fade operation completes.

Selector to call when the current pan operation completes.

Target to inform when the current pan operation completes.

Selector to call when the current pitch operation completes.

Target to inform when the current pitch operation completes.

int ALChannelSource::reservedSources` [read, write, assign]` |

The number of sources reserved by this channel.

Pool holding the actual sources.

All sources being used by this channel.

Do not modify!