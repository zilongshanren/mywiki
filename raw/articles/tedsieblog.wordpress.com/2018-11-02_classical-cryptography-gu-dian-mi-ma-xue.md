---
title: Classical Cryptography – 古典密碼學
url: https://tedsieblog.wordpress.com/2018/11/02/classical-cryptography/
author: Ted Sie
published: '2018-11-02'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

古典密碼學是密碼學中的一個類型，其加密方式大部分都是使用替換式加密或移項式加密。

由於現代已經很少使用，故稱為古典密碼學。

加密有助於防止遊戲被破解的風險，但任何形式的加密都只會增加破解的難易度，並不能保證被破解的風險為零。

其中古典密碼學更是只要取得密鑰就能夠輕易破解的程度。

本篇文章會粗略的介紹密碼學中的基本概念，並分享古典密碼學中的幾種加密演算法。

關鍵字快搜：**古典密碼學**、**凱撒密碼**、**仿射密碼**、**簡易替換密碼**、**乘法逆元**


#### 基本概念

**明文 Plain Text**

傳送方傳送的可讀信息，不僅只限於文檔，音檔、圖片、影片都可以作為明文存在。

**密文 Cipher Text**

由明文經過加密算法後產生的結果。

**加密 Encryption**

將明文資料轉變成密文的過程。

**解密 Decryption**

在對稱密碼學中，解密方需要知道密鑰及解密方法，經由解密後，才能將密文還原成正常的可讀信息。

**加密演算法 Cipher**

加密演算法就是加密的方法，可分為兩類：**對稱加密**和**非對稱加密**。

對稱加密在加密及解密時**使用同樣的密鑰**。

非對稱加密在加密及解密時**使用不同的密鑰**。

**密鑰 Key**

指用來完成加密、解密、驗證時的秘密信息。

對稱密碼學中，由於加密和解密使用同一個密鑰，因此**密鑰需要保密**。

非對稱密碼學中，加密和解密使用的密鑰不同，通常一個是公開的，稱為**公鑰**，另一個保密，稱為**私鑰**。

**mod**

**取餘數**，替換式密碼中常用到的數學運算。





#### 加密演算法

##### 凱撒密碼 Caesar Cipher

在密碼學中，凱撒密碼是最簡單且廣為人知的加密技術。

利用替換加密的技術，透過將明文中的字母按照一個固定數**向前或向後偏移**替換成密文。

**加密函數**


密鑰


**解密函數**


加密對照表 |
||||||||||||||||||||||||||
以 |
||||||||||||||||||||||||||
| 明文 | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z |
| 密文 | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z | A | B | C | D | E | F | G | H | I | J |

加密演算 |
||||||||||||
| 明文 | C | A | E | S | A | R | C | I | P | H | E | R |
| 2 | 0 | 4 | 18 | 0 | 17 | 2 | 8 | 15 | 7 | 4 | 17 | |
| 12 | 10 | 14 | 28 | 10 | 27 | 12 | 18 | 25 | 17 | 14 | 27 | |
| 12 | 10 | 14 | 2 | 10 | 1 | 12 | 18 | 25 | 17 | 14 | 1 | |
| 密文 | M | K | O | C | K | B | M | S | Z | R | O | B |

解密演算 |
||||||||||||
| 密文 | M | K | O | C | K | B | M | S | Z | R | O | B |
| 12 | 10 | 14 | 2 | 10 | 1 | 12 | 18 | 25 | 17 | 14 | 1 | |
| 2 | 0 | 4 | -8 | 0 | -9 | 2 | 8 | 15 | 7 | 4 | -9 | |
| 2 | 0 | 4 | 18 | 0 | 17 | 2 | 8 | 15 | 7 | 4 | 17 | |
| 明文 | C | A | E | S | A | R | C | I | P | H | E | R |

凱撒密碼根據密鑰的不同，也有著不同稱呼

密鑰 = 6：Cassic（A -> G）

密鑰 = 7：Cassette（A -> H）

密鑰 = 10：Avocat（A -> K)

密鑰 = 13：ROT13（A -> N）

**程式碼範例**

private char Encrypt(char c, int key) { if (!char.IsLetter(c)) { return c; } char firstChar = char.IsUpper(c) ? 'A' : 'a'; int x = c - firstChar; int result = (x + 10) % 26; if (result < 0) { result += 26; } return (char)(firstChar + result); } private char Decrypt(char c, int key) { if (!char.IsLetter(c)) { return c; } char firstChar = char.IsUpper(c) ? 'A' : 'a'; int x = c - firstChar; int result = (x - 10) % 26; if (result < 0) { result += 26; } return (char)(firstChar + result); }


##### 仿射密碼 Affine Cipher

仿射密碼也屬於替換密碼的一種，透過加密函數及解密函數的計算可產生出對應的「替換表」，將明文替換成密文。

**加密函數**


和

需互質，即最大公因數


字母數量


**解密函數**


是

在

群的乘法逆元，即


以 |
||||||||||||
| 可能值 |
1 | 3 | 5 | 7 | 9 | 11 | 15 | 17 | 19 | 21 | 23 | 25 |
| 乘法逆元 |
1 | 9 | 21 | 15 | 3 | 19 | 7 | 23 | 11 | 5 | 17 | 25 |

加密對照表 |
||||||||||||||||||||||||||
以 |
||||||||||||||||||||||||||
| 明文 | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z |
| 密文 | K | B | S | J | A | R | I | Z | Q | H | Y | P | G | X | O | F | W | N | E | V | M | D | U | L | C | T |

加密演算 |
||||||||||||
| 明文 | A | F | F | I | N | E | C | I | P | H | E | R |
| 0 | 5 | 5 | 8 | 13 | 4 | 2 | 8 | 15 | 7 | 4 | 17 | |
| 10 | 95 | 95 | 146 | 231 | 78 | 44 | 146 | 265 | 129 | 78 | 299 | |
| 10 | 17 | 17 | 16 | 23 | 0 | 18 | 16 | 5 | 25 | 0 | 13 | |
| 密文 | K | R | R | Q | X | A | S | Q | F | Z | A | N |

解密演算 |
||||||||||||
| 密文 | K | R | R | Q | X | A | S | Q | F | Z | A | N |
| 10 | 17 | 17 | 16 | 23 | 0 | 18 | 16 | 5 | 25 | 0 | 13 | |
| 0 | 161 | 161 | 138 | 299 | -230 | 184 | 138 | -115 | 345 | -230 | 69 | |
| 0 | 5 | 5 | 8 | 13 | 4 | 2 | 8 | 15 | 7 | 4 | 17 | |
| 明文 | A | F | F | I | N | E | C | I | P | H | E | R |

**程式碼範例**

private char Encrypt(char c) { if (!char.IsLetter(c)) { return c; } char firstChar = char.IsUpper(c) ? 'A' : 'a'; int x = c - firstChar; int result = (17 * x + 10) % 26; if(result < 0) { result = result + 26; } return (char)(result + firstChar); } private char Decrypt(char c) { if (!char.IsLetter(c)) { return c; } char firstChar = char.IsUpper(c) ? 'A' : 'a'; int x = c - firstChar; int result = (23 * (x - 17)) % 26; if(result < 0) { result = result + 26; } return (char)(result + firstChar); }


##### 簡易替換密碼 Simple Substitution Cipher

一種以特定方式改變字母表的字母順序，並以此順序修改的加密方式，利用此方法產生的對照表可稱為「替換表」。

傳統做法上，會在替換表前頭加入**關鍵字**，依序將字母填入並刪去重複字母，最後再將**剩餘字母按照排序填入**。

加密對照表 |
||||||||||||||||||||||||||
以 HELLO WORLD 為例 |
||||||||||||||||||||||||||
| 明文 | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z |
| 密文 | H | E | L | O | W | R | D | A | B | C | F | G | I | J | K | M | N | P | Q | S | T | U | V | X | Y | Z |

加密、解密演算 |
||||||||||||||||||||||||
| 明文 | S | I | M | P | L | E | S | U | B | S | T | I | T | U | T | I | O | N | C | I | P | H | E | R |
| 密文 | P | F | J | M | I | A | P | T | E | P | Q | F | Q | T | Q | F | L | K | B | F | M | D | A | O |

**程式碼範例**

private string m_plainAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; private string m_cipherAlphabet = "HELOWRDABCFGIJKMNPQSTUVXYZ"; private char Encrypt(char c) { if (!char.IsLetter(c)) { return c; } int index = m_plainAlphabet.IndexOf(char.ToUpper(c)); if(char.IsUpper(c)) { return m_cipherAlphabet[index]; } else { return char.ToLower(m_cipherAlphabet[index]); } } private char Decrypt(char c) { if (!char.IsLetter(c)) { return c; } int index = m_cipherAlphabet.IndexOf(char.ToUpper(c)); if (char.IsUpper(c)) { return m_plainAlphabet[index]; } else { return char.ToLower(m_plainAlphabet[index]); } }

#### 參考資料

[Classical cipher – Wikipedia](https://en.wikipedia.org/wiki/Classical_cipher)

[Caesar cipher – Wikipedia](https://en.wikipedia.org/wiki/Caesar_cipher)

[Affine cipher – Wikipedia](https://en.wikipedia.org/wiki/Affine_cipher)

[Modular multiplicative inverse – Wikipedia](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse)

[Substitution cipher – Wikipedia](https://en.wikipedia.org/wiki/Substitution_cipher)