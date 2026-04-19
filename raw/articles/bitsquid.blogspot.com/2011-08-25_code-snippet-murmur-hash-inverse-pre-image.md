---
title: 'Code Snippet: Murmur hash inverse / pre-image'
url: https://bitsquid.blogspot.com/2011/08/code-snippet-murmur-hash-inverse-pre.html
author: Niklas
published: '2011-08-25'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

/// Inverts a (h ^= h >> s) operation with 8 <= s <= 16 unsigned int invert_shift_xor(unsigned int hs, unsigned int s) { XENSURE(s >= 8 && s <= 16); unsigned hs0 = hs >> 24; unsigned hs1 = (hs >> 16) & 0xff; unsigned hs2 = (hs >> 8) & 0xff; unsigned hs3 = hs & 0xff; unsigned h0 = hs0; unsigned h1 = hs1 ^ (h0 >> (s-8)); unsigned h2 = (hs2 ^ (h0 << (16-s)) ^ (h1 >> (s-8))) & 0xff; unsigned h3 = (hs3 ^ (h1 << (16-s)) ^ (h2 >> (s-8))) & 0xff; return (h0<<24) + (h1<<16) + (h2<<8) + h3; } unsigned int murmur_hash_inverse(unsigned int h, unsigned int seed) { const unsigned int m = 0x5bd1e995; const unsigned int minv = 0xe59b19bd; // Multiplicative inverse of m under % 2^32 const int r = 24; h = invert_shift_xor(h,15); h *= minv; h = invert_shift_xor(h,13); unsigned int hforward = seed ^ 4; hforward *= m; unsigned int k = hforward ^ h; k *= minv; k ^= k >> r; k *= minv; #ifdef PLATFORM_BIG_ENDIAN char *data = (char *)&k; k = (data[0]) + (data[1] << 8) + (data[2] << 16) + (data[3] << 24); #endif return k; }And for reference, here is the full code, with both the regular murmur hash and the inverses for 32- and 64-bit hashes:

unsigned int murmur_hash ( const void * key, int len, unsigned int seed ) { // 'm' and 'r' are mixing constants generated offline. // They're not really 'magic', they just happen to work well. const unsigned int m = 0x5bd1e995; const int r = 24; // Initialize the hash to a 'random' value unsigned int h = seed ^ len; // Mix 4 bytes at a time into the hash const unsigned char * data = (const unsigned char *)key; while(len >= 4) { #ifdef PLATFORM_BIG_ENDIAN unsigned int k = (data[0]) + (data[1] << 8) + (data[2] << 16) + (data[3] << 24); #else unsigned int k = *(unsigned int *)data; #endif k *= m; k ^= k >> r; k *= m; h *= m; h ^= k; data += 4; len -= 4; } // Handle the last few bytes of the input array switch(len) { case 3: h ^= data[2] << 16; case 2: h ^= data[1] << 8; case 1: h ^= data[0]; h *= m; }; // Do a few final mixes of the hash to ensure the last few // bytes are well-incorporated. h ^= h >> 13; h *= m; h ^= h >> 15; return h; } /// Inverts a (h ^= h >> s) operation with 8 <= s <= 16 unsigned int invert_shift_xor(unsigned int hs, unsigned int s) { XENSURE(s >= 8 && s <= 16); unsigned hs0 = hs >> 24; unsigned hs1 = (hs >> 16) & 0xff; unsigned hs2 = (hs >> 8) & 0xff; unsigned hs3 = hs & 0xff; unsigned h0 = hs0; unsigned h1 = hs1 ^ (h0 >> (s-8)); unsigned h2 = (hs2 ^ (h0 << (16-s)) ^ (h1 >> (s-8))) & 0xff; unsigned h3 = (hs3 ^ (h1 << (16-s)) ^ (h2 >> (s-8))) & 0xff; return (h0<<24) + (h1<<16) + (h2<<8) + h3; } unsigned int murmur_hash_inverse(unsigned int h, unsigned int seed) { const unsigned int m = 0x5bd1e995; const unsigned int minv = 0xe59b19bd; // Multiplicative inverse of m under % 2^32 const int r = 24; h = invert_shift_xor(h,15); h *= minv; h = invert_shift_xor(h,13); unsigned int hforward = seed ^ 4; hforward *= m; unsigned int k = hforward ^ h; k *= minv; k ^= k >> r; k *= minv; #ifdef PLATFORM_BIG_ENDIAN char *data = (char *)&k; k = (data[0]) + (data[1] << 8) + (data[2] << 16) + (data[3] << 24); #endif return k; } uint64 murmur_hash_64(const void * key, int len, uint64 seed) { const uint64 m = 0xc6a4a7935bd1e995ULL; const int r = 47; uint64 h = seed ^ (len * m); const uint64 * data = (const uint64 *)key; const uint64 * end = data + (len/8); while(data != end) { #ifdef PLATFORM_BIG_ENDIAN uint64 k = *data++; char *p = (char *)&k; char c; c = p[0]; p[0] = p[7]; p[7] = c; c = p[1]; p[1] = p[6]; p[6] = c; c = p[2]; p[2] = p[5]; p[5] = c; c = p[3]; p[3] = p[4]; p[4] = c; #else uint64 k = *data++; #endif k *= m; k ^= k >> r; k *= m; h ^= k; h *= m; } const unsigned char * data2 = (const unsigned char*)data; switch(len & 7) { case 7: h ^= uint64(data2[6]) << 48; case 6: h ^= uint64(data2[5]) << 40; case 5: h ^= uint64(data2[4]) << 32; case 4: h ^= uint64(data2[3]) << 24; case 3: h ^= uint64(data2[2]) << 16; case 2: h ^= uint64(data2[1]) << 8; case 1: h ^= uint64(data2[0]); h *= m; }; h ^= h >> r; h *= m; h ^= h >> r; return h; } uint64 murmur_hash_64_inverse(uint64 h, uint64 seed) { const uint64 m = 0xc6a4a7935bd1e995ULL; const uint64 minv = 0x5f7a0ea7e59b19bdULL; // Multiplicative inverse of m under % 2^64 const int r = 47; h ^= h >> r; h *= minv; h ^= h >> r; h *= minv; uint64 hforward = seed ^ (8 * m); uint64 k = h ^ hforward; k *= minv; k ^= k >> r; k *= minv; #ifdef PLATFORM_BIG_ENDIAN char *p = (char *)&k; char c; c = p[0]; p[0] = p[7]; p[7] = c; c = p[1]; p[1] = p[6]; p[6] = c; c = p[2]; p[2] = p[5]; p[5] = c; c = p[3]; p[3] = p[4]; p[4] = c; #endif return k; }

I just started using hashes instead of strings/guids, and I'm using murmurhash. I'm using murmurhash3 right now, but I don't think I could manage making my own inverse hash function in a decent amount of time.


ReplyDeleteMight as well change to murmurhash2. I tried this code, but I seem to be missing the function/macro XENSURE.

XENSURE is just our internal assert function, you can replace it with your own assert.

ReplyDeleteWhat are the use cases of this?

ReplyDeleteConverted this project to lua.


ReplyDeleteSteam workshop: https://steamcommunity.com/sharedfiles/filedetails/?id=1653994440

Source code: http://gitlab.ludoruisch.nl/root/MurmurHashInverse/blob/master/scripts/mods/MurmurHashInverse/MurmurHashInverse.lua

google 306

ReplyDeletegoogle 307

google 308

google 309

google 310

google 311

google 312

Your article is very good, I have read many articles but I am really impressed with your posts. Thank you, I will review this article. To know about me, try talking to me. for More Details Click Here:-

ReplyDeleteSpectrum Email Not Working


ReplyDeleteThanks for Sharing such an amazing article. Keep working... Your Site is very nice, and it's very helping us.. this post is unique and interesting, thank you for sharing this awesome information vmware workstation crack

Nice information. I’ve bookmarked your site, and I’m adding your RSS feeds to my Google account to get updates instantly. Reimage Crack

ReplyDelete



ReplyDeleteStartIsBack Crack is one of the most used and successful shell enhancements for newer window variants such as the ms window operating system. This type of consumer can return to the classic start menus, with which most users are habitual.


ReplyDeleteESET NOD32 Antivirus Crack Updated 2021 is a comprehensive security tool with many features and tools. It is legendary antivirus software that gives you basic protection against malware and hackers.

Thanks for posting the best information and the blog is very good.


ReplyDeleteibm full form in india |

ssb ka full form |

what is the full form of dp |

full form of brics |

gnm nursing full form |

full form of bce |

full form of php |

bhim full form |

nota full form in india |

apec full form |

https://newcrackkey.com/avast-secureline-vpn-crack-2022-key/

ReplyDeleteLicense response connects movable designed for initial, desktop processer in addition robot. Avast Secureline VPN

Hard Disk Sentinel Pro Crack 2022

ReplyDeleteFree Download vray para sketchup 2023 torrent


ReplyDeleteThis comment has been removed by the author.

ReplyDeleteNursing jobs in Germany are highly sought after for their promise of professional growth and development in a reputable healthcare system. With a focus on patient-oriented care and advanced medical practices, nurses can thrive in a variety of settings, including hospitals, outpatient clinics, and residential care facilities. The German healthcare system offers competitive salaries and extensive benefits, including health insurance and retirement plans. Moreover, there is a strong emphasis on continuous education, with many organisations providing access to specialised training and professional advancement opportunities. Language proficiency is often supported through employer-sponsored courses, making it easier for international nurses to adapt. Germany's commitment to a healthy work-life balance further enhances the appeal of its nursing positions. For those passionate about caregiving, a nursing career in Germany presents an exciting pathway to enrich their expertise and experience. Embrace this opportunity to make a positive difference in patients' lives while advancing your career on a global stage.

ReplyDeletehttps://www.dynamichealthstaff.com/nursing-jobs-in-germany

360 Total security Crack is a simple as well as small package for every type of the RAM of some type of OS, its competence is additional modern. The entire in sequence is bringing to the sandbox; it position separately total the trash credentials.

ReplyDelete360 Total Security Crack

I can’t believe how much I learned from this post. You’ve explained everything so clearly and concisely!

ReplyDeleteBlueStacks Crack is an application player instrument that could utilize to show software. Similar, it could run whole you’re Android application on your windows also Mac operating system.

ReplyDeleteBlueStacks Crack