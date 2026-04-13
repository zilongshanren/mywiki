---
title: Using most Japanese characters in a game is possible with 1024x1024 texture
url: https://gametorrahod.com/using-most-japanese-characters-in-a-game-is-possible-with-1024x1024-texture/
author: Sirawat Pitaksarit
published: '2018-07-20'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

In games we need to include all the character image as a rendered texture, and so it is a big problem for language like Chinese/Japanese where we have 20000 characters as opposed to English. Big texture is bad! So what’s the solution?

## Use only kanji occurred in your game

This is a pain because you must write a post-processing tools to scan all text assets in the game and compile a list of possible kanji. Also if your game allows Japanese player to type Japanese language then you are doomed!

## Use only frequently occurred kanji

To cover as many possible case as possible, a website like this has a kanji ranking by their frequency :

**Kanji orderd by frequency of use - Kanjicards.org***Free PDF Kanji cards for download. Sorted lists of Kanji acording to your preferences along with Information for…*kanjicards.org

So it is a good idea to include a kanji from this list to try to cover everything…

Note that there is a thing called Jouyou kanji (regular use kanji characters)

**Jōyō kanji - Wikipedia***The jōyō kanji (常用漢字, literally "regular-use Chinese characters") is the guide to kanji characters and their readings…*en.wikipedia.org

And here is the list

**List of jōyō kanji - Wikipedia***The readings presented here are those noted in the official Jōyō table. Special readings and uncommon readings are…*en.wikipedia.org

It is up to you whether to use Jouyou or by-frequency list. But I don’t like the fact that the first one in that list is 亜 which I have never seen in “daily life” at all when I was in Japan.

## Signed distance field rendering

Supposed we got 2000 characters to fit and we settle for 1024x1024 for all Japanese characters, the character is still too small! But we don’t want to go one step further to 2048x2048 because that’s quite large. (Adds 4MB to the game and adds considerable load time + RAM usage)

This paper by Valve “Improved Alpha-Tested Magnification for Vector Textures and Special Effects” describe a good method to render **vector **text by using **raster texture.**

The core idea is that we store a texture that looks strange and blurry, but those grey value has special meaning. And by the algorithm that calculate the distance of mid-grey pixel to brightest pixel etc… (please read it if you want to know this magic) we can get non-pixelated text rendering at any magnification!

Unity supports this in the form of **TextMeshPro plugin **that Unity acquired years ago. Now in UPM package!

(I have covered about SDF before but in Thai language)

**Distance Field เทคนิควาด Font ให้คมในทุก Resolution ของ Valve แม้ขนาด Texture จะเล็ก***เมื่อวานนี้ผมได้ลงข่าวเรื่องที่ Text Mesh Pro ที่เป็น Plug-in สุดฮิตของ Unity ได้ถูก Unity…*gametorrahod.com

Also read this excellent article about distance field in general

**Signed Distance Fields Part 1: Unsigned Distance Fields***Welcome to the first blog post on shaderfun.com. It probably won't be all shaders, and probably not always fun, but I…*shaderfun.com

## And so let’s do this

First I will show you that 512x512 is not enough even with all the magic of signed distance field rendering. I only include **500 **most frequently used kanji in this texture + all hiragana, katakana.

The generated texture looks like this :

![](../../assets/6658addc04842a0f.png)

And when using it. I randomly copy texts from my Japanese Twitter account tweeted by real Japanese people :

![](../../assets/ed860cd985d18a9c.png)

As you can see the text looks like crap, but look at the magic of SDF rendering! Even if it looks like crap it wasn’t pixelated and looks vector-ish.

![](../../assets/fd3f57aa0c2ed411.png)

512x512 is 無理 and so we try 1024x1024 next

![](../../assets/aa20f20f3b6ed385.png)

I have increased to cover 501–1000 frequently used kanji because we have much larger texture (4x) now.

![](../../assets/8db8ea9a7794b5d3.png)

Zoomed in, I think it in fact looked **too good. **And the test text is still missing a few kanji, so let’s try adding 1001–1500 kanji next.

![](../../assets/d5b90e770395b2f7.png)

![](../../assets/e17077f9ee02f128.png)

You see it looks a lot crappier, but we get more coverage in 1024x1024 texture.

But wait! It looks quite good at smaller size :

![](../../assets/352d1dfb4632a6e5.png)

This is because SDF rendering changes based on current scaling which affect the “distance field”, and it is doing quite well at small size!

Also I set a text padding too large at 5 pixels. With a lot of glyph like this changing form 5 to 2 pixels means a world of difference. (I estimated getting more than 200x200 pixels more from doing that, which could increase the clarity greatly or you could include more obscure kanji)

So if you want to use very large text but only rarely, you might make a separated texture for those and not a general purpose cover-it-all texture like this one. I am making a game with visual novel element so I have to be prepared for variety of texts but large size not required, so this texture is good to go for me.

## Summary

1024x1024 is enough for 1–1500 frequently used kanji + all hiragana, katakana.

And for those who wants to copy this is my character list file :

```
『「【】」』！、。
ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヷヸヹヺ・
゛゜ーヽヾ
ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔ
ゞ゛゜ーｰ
日一国会人年大十二本中長出三同時政事自行社見月分議後前民生連五発間対上部東者党地合市業内相方四定今回新場金員九入選立開手米力学問高代明実円関決子動京全目表戦経通外最言氏現理調体化田当八六約主題下首意法不来作性的要用制治度務強気小七成期公持野協取都和統以機平総加山思家話世受区領多県続進正安設保改数記院女初北午指権心界支第産結百派点教報済書府活原先共得解名交資予川向際査勝面委告軍文反元重近千考判認画海参売利組知案道信策集在件団別物側任引使求所次水半品昨論計死官増係感特情投示変打男基私各始島直両朝革価式確村提運終挙果西勢減台広容必応演電歳住争談能無再位置企真流格有疑口過局少放税検藤町常校料沢裁状工建語球営空職証土与急止送援供可役構木割聞身費付施切由説転食比難防補車優夫研収断井何南石足違消境神番規術護展態導鮮備宅害配副算視条幹独警宮究育席輸訪楽起万着乗店述残想線率病農州武声質念待試族象銀域助労例衛然早張映限親額監環験追審商葉義伝働形景落欧担好退準賞訴辺造英被株頭技低毎医復仕去姿味負閣韓渡失移差衆個門写評課末守若脳極種美岡影命含福蔵量望松非撃佐核観察整段横融型白深字答夜製票況音申様財港識注呼渉達
良響阪帰針専推谷古候史天階程満敗管値歌買突兵接請器士光討路悪科攻崎督授催細効図週積丸他及湾録処省旧室憲太橋歩離岸客風紙激否周師摘材登系批郎母易健黒火戸速存花春飛殺央券赤号単盟座青破編捜竹除完降超責並療従右修捕隊危採織森競拡故館振給屋介読弁根色友苦就迎走販園具左異歴辞将秋因献厳馬愛幅休維富浜父遺彼般未塁貿講邦舞林装諸夏素亡劇河遣航抗冷模雄適婦鉄寄益込顔緊類児余禁印逆王返標換久短油妻暴輪占宣背昭廃植熱宿薬伊江清習険頼僚覚吉盛船倍均億途圧芸許皇臨踏駅署抜壊債便伸留罪停興爆陸玉源儀波創障継筋狙帯延羽努固闘精則葬乱避普散司康測豊洋静善逮婚厚喜齢囲卒迫略承浮惑崩順紀聴脱旅絶級幸岩練押軽倒了庁博城患締等救執層版老令角絡損房募曲撤裏払削密庭徒措仏績築貨志混載昇池陣我勤為血遅抑幕居染温雑招奈季困星傷永択秀著徴誌庫弾償刊像功拠香欠更秘拒刑坂刻底賛塚致抱繰服犯尾描布恐寺鈴盤息宇項喪伴遠養懸戻街巨震願絵希越契掲躍棄欲痛触邸依籍汚縮還枚属笑互複慮郵束仲栄札枠似夕恵板列露沖探逃借緩節需骨射傾届曜遊迷夢巻購揮君燃充雨閉緒跡包駐貢鹿弱却端賃折紹獲郡併草徹飲貴埼衝焦奪雇災浦暮替析預焼簡譲称肉納樹挑章臓律誘紛貸至宗促慎控
贈智握照宙酒俊銭薄堂渋群銃悲秒操携奥診詰託晴撮誕侵括掛謝双孝刺到駆寝透津壁稲仮暗裂敏鳥純是飯排裕堅訳盗芝綱吸典賀扱顧弘看訟戒祉誉歓勉奏勧騒翌陽閥甲快縄片郷敬揺免既薦隣悩華泉御範隠冬徳皮哲漁杉里釈己荒貯硬妥威豪熊歯滞微隆埋症暫忠倉昼茶彦肝柱喚沿妙唱祭袋阿索誠忘襲雪筆吹訓懇浴俳童宝柄驚麻封胸娘砂李塩浩誤剤瀬趣陥斎貫仙慰賢序弟旬腕兼聖旨即洗柳舎偽較覇兆床畑慣詳毛緑尊抵脅祝礼窓柔茂犠旗距雅飾網竜詩昔繁殿濃翼牛茨潟敵魅嫌魚斉液貧敷擁衣肩圏零酸兄罰怒滅泳礎腐祖幼脚菱荷潮梅泊尽杯僕桜滑孤黄煕炎賠句寿鋼頑甘臣鎖彩摩浅励掃雲掘縦輝蓄軸巡疲稼瞬捨皆砲軟噴沈誇祥牲秩帝宏唆鳴阻泰賄撲凍堀腹菊絞乳煙縁唯膨矢耐恋塾漏紅慶猛芳懲郊剣腰炭踊幌彰棋丁冊恒眠揚冒之勇曽械倫陳憶怖犬菜耳潜珍梨仁克岳概拘墓黙須偏雰卵遇湖諮狭喫卓干頂虫刷亀糧梶湯箱簿炉牧殊殖艦溶輩穴奇慢鶴謀暖昌拍朗丈鉱寛覆胞泣涙隔浄匹没暇肺孫貞靖鑑飼陰銘鋭随烈尋渕稿枝丹啓也丘棟壌漫玄粘悟舗妊塗熟軒旭恩毒騰往豆遂晩狂叫栃岐陛緯培衰艇屈径淡抽披廷錦准暑拝磯奨妹浸剰胆氷繊駒乾虚棒寒孜霊帳悔諭祈惨虐翻墜沼据肥徐糖搭姉髪忙盾脈滝拾軌俵妨盧粉擦鯨漢糸荘諾雷漂懐勘綿栽才拐笠駄
```