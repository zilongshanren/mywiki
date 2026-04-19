---
title: Creating a 3D Game Engine (Part 17)
url: https://cybereality.com/creating-a-3d-game-engine-part-17/
author: Cybereality
published: '2014-05-25'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/bce84abf857a6ab7.jpg)

Programmer art is great and all, but I’d really like to see some complex models inside the engine. Unfortunately, DirectX 11 does not include a built-in way to load in 3D models. As I’ve mentioned before, I am interested in using COLLADA has the import format. Since COLLADA is based on XML, I will need a way to load and parse XML files. While there are tons of XML parsing libraries out there, I decided to write my own. Why would I do that? A few reasons. First, I don’t want my engine to be encumbered with 3rd party licenses, forcing me to do things against my will. Secondly, I think it’s a great learning exercise to see how something like this is done. Lastly, it’s fun!

Sadly, I found very little resources on how you go about coding an XML parser from scratch. Of the code I did find (i.e. from open-source libraries), it was difficult for me to extract the algorithm from the code. There was one resource that did help somewhat, [from ANTLR3](https://theantlrguy.atlassian.net/wiki/display/ANTLR3/Parsing+XML), but it failed to provide the pseudo-code I was looking for. Even so, it was enough to get me started.

The basic procedure I followed was loading the XML file into a string, then iterating though the string and breaking the text up into tokens. Each of these tokens would take the string representation and a label of what the token meant. Then, in a second pass, I would look though all the tokens and parse them into a tree structure. It actually ended up being easier than I initially though, and I think I completed the whole thing in about 2 or 3 days just working a few hours in the evening. I’ll highlight some of the relevant code below.

I created a map with all the important XML syntax elements so I can break them up into tokens.

tokenMap[""] = XML_CLOSE; tokenMap[""] = TAG_EMPTY; tokenMap["<"] = TAG_OPEN; tokenMap[">"] = TAG_CLOSE; tokenMap["=\""] = ATTRIB_EQUALS; tokenMap["\""] = ATTRIB_QUOTE; tokenMap[" "] = WHITE_SPACE; tokenMap["\n"] = WHITE_LINE; tokenMap["\t"] = WHITE_TAB;

First I load the XML file using the standard C++ stream libraries.

ifstream inputFile; inputFile.open(fileName, ifstream::in); stringstream inputStream; while (inputFile.good()){ inputStream << (char)inputFile.get(); } string temp = inputStream.str(); char* data = const_cast(temp.c_str());

Next, I loop through all the characters in the data stream and find the tokens.

TokenList tokenize(char* doc){ size_t docLen = strlen(doc); TokenList tokens; TokenMap::iterator it; string buffer = ""; unsigned int i; for (i = 0; i < docLen; i++){ bool found = false; for (it = tokenMap.begin(); it != tokenMap.end(); ++it){ int tokenLen = strlen(it->first); if (compare(&doc[i], it->first, tokenLen)){ int textLen = strlen(buffer.c_str()); if (textLen > 0){ char* text = new char[textLen]; strncpy_s(text, textLen + 1, buffer.c_str(), textLen); TokenMap token = { { text, GENERIC_TEXT } }; tokens.push_back(token); buffer = ""; } char* match = new char[tokenLen]; strncpy_s(match, tokenLen + 1, &doc[i], tokenLen); TokenMap token = { { match, it->second } }; tokens.push_back(token); i += tokenLen - 1; found = true; break; } } if (!found) buffer.append(&doc[i], 1); } return tokens; }

Finally I iterate through the list I just created and parse that into a node-based tree. I admit this part is a little ugly, but it seems to work so I’m OK with that. The idea is that I set the function into different states, and then parse the elements in the list differently depending on the state. For example, if I see a “<” token, then I go into attribute parsing, and then when I see a “>” I set it back to the default state. The logic is fairly simple, but there are a lot of if statements to weed though if you are trying to implement this yourself.

void parse(TokenList& list, XmlNode* parent){ ParseType state = PARSE_ANY; XmlNode* node = new XmlNode(); bool created = false; bool allWhite = true; int openTags = 0; string attribName = ""; string attribValue = ""; string valueBuffer = ""; TokenList children; TokenList::iterator v; for (v = list.begin(); v != list.end(); ++v){ TokenMap::iterator m; for (m = v->begin(); m != v->end(); ++m){ if (state == PARSE_ANY){ if (m->second == XML_OPEN){ state = PARSE_XML_TYPE; } else if (m->second == TAG_OPEN){ state = PARSE_TAG_NAME; created = true; } else if (m->second == ATTRIB_EQUALS){ state = PARSE_ATTRIB_VALUE; } else if (m->second == GENERIC_TEXT || m->second == WHITE_SPACE || m->second == WHITE_LINE || m->second == WHITE_TAB){ valueBuffer.append(m->first, strlen(m->first)); if (m->second == GENERIC_TEXT) allWhite = false; } if (v + 1 == list.end()){ if (!allWhite) parent->value = valueBuffer; valueBuffer = ""; } } else if (state == PARSE_TAG_NAME){ node->name = string(m->first); state = PARSE_ATTRIB_NAME; } else if (state == PARSE_ATTRIB_NAME){ if (m->second == WHITE_SPACE) continue; if (m->second == ATTRIB_QUOTE) continue; if (m->second == TAG_EMPTY){ state = PARSE_ANY; continue; } else if (m->second == TAG_CLOSE){ state = PARSE_TAG_CLOSE; openTags = 1; continue; } attribName = string(m->first); state = PARSE_ANY; } else if (state == PARSE_ATTRIB_VALUE){ attribValue.append(m->first, strlen(m->first)); if (m->second == ATTRIB_QUOTE){ node->attributes[attribName] = string(attribValue); state = PARSE_ATTRIB_NAME; attribValue = ""; } } else if (state == PARSE_TAG_CLOSE){ if (m->second == TAG_OPEN) openTags++; if (m->second == TAG_END) openTags--; if (m->second == TAG_EMPTY) openTags--; if (openTags > 0){ children.push_back(*v); } else { parse(children, node); children.clear(); state = PARSE_TAG_END; continue; } } else if (state == PARSE_TAG_END){ if (m->second == TAG_CLOSE){ parent->addChild(node); node = new XmlNode(); state = PARSE_ANY; continue; } } else if (state == PARSE_XML_TYPE){ if (m->second == XML_CLOSE){ state = PARSE_ANY; continue; } } } } if (created && node->name.length() > 0){ parent->addChild(node); } else { delete node; } }

All in all not nearly as bad as I expected. Granted, the algorithm could be a little less hard-coded, but it’s a fairly straight-forward implementation. I also loaded in a COLLADA *.DAE file, and I did not see any errors or problem. Within the next few days I hope to integrate this code into the engine and actually load up a 3D model. Surely there will be some hiccups, but I have faith this can be done soon.