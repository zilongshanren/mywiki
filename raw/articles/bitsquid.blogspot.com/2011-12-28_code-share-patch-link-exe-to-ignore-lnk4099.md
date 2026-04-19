---
title: 'Code Share: Patch link.exe to ignore LNK4099'
url: https://bitsquid.blogspot.com/2011/12/code-share-patch-linkexe-to-ignore.html
author: Niklas
published: '2011-12-28'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

*link.exe*does not let you ignore the linker warning

[LNK4099](http://msdn.microsoft.com/en-us/library/b7whw3f3(v=vs.80).aspx)(PDB file was not found).

This can be a real nuisance when you have to link with third party libraries that reference (but do not come with) PDBs. You can get hundreds of linker warnings that you have no way of getting rid of.

The only way I've found of fixing the problem is to patch

*link.exe*so that it allows warning 4099 to be ignored. Luckily, it is not as scary as it sounds. You only need to patch a single location to remove 4099 from a list of warnings that cannot be ignored. An outline of the procedure can be found

[here](http://www.bottledlight.com/docs/lnk4099.html).

Following my general philosophy to

[write-a-script-for-it](http://altdevblogaday.com/2011/05/11/write-a-script-for-it/)I wrote a short ruby script that does the patching. I'm sharing it here for everybody that want to do voodoo on their

*link.exe*and get rid of the warning.

[(Click here for pastebin version.)](http://pastebin.com/RrkbXYZu)

# This ruby program will patch the linker executable (link.exe) # so that linker warning LNK4099 is ignorable. # # Reference: http://www.bottledlight.com/docs/lnk4099.html require "fileutils" def link_exes() res = [] res << File.join(ENV["VS90COMNTOOLS"], "../../VC/bin/link.exe") if ENV["VS90COMNTOOLS"] res << File.join(ENV["VS100COMNTOOLS"], "../../VC/bin/link.exe") if ENV["VS100COMNTOOLS"] res << File.join(ENV["XEDK"], "bin/win32/link.exe") if ENV["XEDK"] return res end def patch_link_exe(exe) data = nil File.open(exe, "rb") {|f| data = f.read} unpatched = [4088, 4099, 4105].pack("III") patched = [4088, 65535, 4105].pack("III") if data.scan(patched).size > 0 puts "* Already patched #{exe}" return end num_unpatched = data.scan(unpatched).size raise "Multiple patch locations in #{exe}" if num_unpatched > 1 raise "Patch location not found in #{exe}" if num_unpatched == 0 offset = data.index(unpatched) puts "* Found patch location #{exe}:#{offset}" bak = exe + "-" + Time.now.strftime("%y%m%d-%H%M%S") + ".bak" puts " Creating backup #{bak}" FileUtils.cp(exe, bak) puts " Patching exe" data[offset,unpatched.size] = patched File.open(exe, "wb") {|f| f.write(data)} return true end link_exes.each do |exe| patch_link_exe(exe) end

https://vigovideo.onl/


ReplyDeletevigo video

vigo video apk

vigo video online

vigo video funny

vigo video downloader

We at Epson Printer Support have a breathtaking notoriety of being the acceptable Epson fix focus inside the market for providing our customers with the fine in superbness contributions. Our especially gifted experts can deal with any printer related issue and investigate it with snappy arrangements. We have a toll loosened helpline go +1-877-760-6111 at which you can name to explain your printer stresses and profit smooth and brisk answers from our specialists.

ReplyDeleteepson printer setup

I will be looking forward to your next post. Thank you

ReplyDeleteเป็กกี้ โชว์เว้าหนัก ยกสูง ตอกกลับดราม่าสุดแซ่บ


ReplyDeleteThis is my blog. Click here.

วิธีอ่านเค้าไพ่สูตร บาคาร่า 3 แถว"

I will be looking forward to your next post. Thank you

ReplyDeleteวิธีการเล่นสล็อตออนไลน์ (มือใหม่สมัครเล่น) "

WOW! I Love it...


ReplyDeleteand i thing thats good for you >>

MOVIE TRAILER Impetigore บ้านเกิดปีศาจ

Thank you!

That's very great. Yellowstone Coat

ReplyDeleteWe are comprised of efficient and skilled writers, all of whom are experienced and are certified writers. We have a diversity of writers; they have backgrounds in different subject areas, and they hold degrees from outstanding universities of the world. We make sure that each writer is efficient and well researched in the respective field. As a result, our writers are able to write on almost every topic of your choice, the content we provide is unique and original. We make sure that our customers get what they require, that is why our customers never regret their choice of selecting us. Our hard work has made us one of the best writing agencies in the country.



ReplyDeleteEssay Help Uk

google 1702

ReplyDeletegoogle 1703

google 1704

google 1705

google 1706

Whenever I connect to third party libraries, it is nothing short of a real hassle for me. The solution I have come up with is writing the third party script myself instead of connecting to the third party. Assignment Writing Services

ReplyDeleteProofreading is the process of checking and correcting a written work to ensure that it meets all of its target audience's requirements. It is a fundamental part of editing for which you need to have top-quality services.


ReplyDeleteAvail the apex grade Proofreading Assignment Help Now

To proofread your work and make it more readable, you need to check the grammar, punctuation, and spelling as well as tone, style, and voice. This can be difficult if you do not know how to perform these checks.

You can hire a professional proof-reader or get help from an amateur proof-reader service. An proof-reader service may not be able to detect all issues, but they will provide reliable services at competitive prices.

Assignment Global offers the best proofreading services that are delivered by qualified editors who specialize in proofreading and editing articles, books, and manuals. The editors are skilled at spotting errors in grammar, spelling, and punctuation so that they can be corrected properly before publishing your work.

If you need proofreading services for your essay, article, dissertation, or report, Assignment Global can offer expert editing based on your specific needs. Their team of writers is available 24/7 to help you with any project you may have. They take pride in their high level of customer service and strive to provide the best possible results at all times.

The majority of salons that provide elizavecca hair treatments implement the necessary safety measures. Prior to receiving treatment, it will be preferable if clients are also aware of the dos and don'ts. elizavecca hair treatment are not suggested for expectant or nursing mothers. While receiving treatment, it is necessary to wear a mask, and the location should have good ventilation.

ReplyDeleteWhether you're facing a sudden injury, severe illness, or medical crisis, you can trust us to provide prompt and expert care to help you feel better fast. At Emergency Room Mesquite, your health and well-being are our top priorities. At Emergency Room Mesquite, we understand that emergencies can happen at any time. That's why we're here, 24/7, to provide swift and comprehensive medical care when you need it most.

ReplyDeleteI’ve been looking for something like this. Great job!

ReplyDeleteGreat tips! I’m going to use them right away.

ReplyDeleteI’ve seen many cafes using a Commercial Umbrella to create comfortable seating areas. Vector Shade Structures seems to be a go-to choice for quality installations.

ReplyDelete