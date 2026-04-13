---
title: My First Game - Sebastiano Mandalà
url: https://www.sebaslab.com/myfirstgame/
author: Sebastiano Mandalà
published: '2012-05-12'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

knowing how short my memory is, I saved all my professional life memories in a folder on my HD. Some of those memories are meaningful only to me, but why not sharing my first, completed game (yeahh it was 1997…I think) ?

The version I am linking is actually the second version of the really original one. Both are a remix of [Puyo Puyo](http://en.wikipedia.org/wiki/Puyo_Puyo_(series)), game that I loved to play when I used to play with the arcade games in my city, Palermo.

This game had another very important feature, was not implementing any scrolling, a technique that I did not know how to implement at that time :).

The game presented some new features (like special bubbles, when played in special mode) and a nice AI. The language used, Pascal, was the language that I was learning at the high school. Turbo Pascal was the compiler and the source code was also featuring a lot of 16 bit inline assembly 🙂

The game was developed by me and a friend of mine with an astonishing 386DX 40mhz and a 286 16mhz with 20mb of hard disk :D.

Pascal source example:

PROCEDURE CADIPIETRE(PLAYER:GIOCATORI); VAR INDX,I:BYTE; INDY,J:SHORTINT; X,Y:WORD; BEGIN X:=STARTX[PLAYER]+1; FACENDOSTO[PLAYER]:=NORMALING; FOR I:=1 TO 6 DO BEGIN IF (PIETREBUFF[PLAYER][I]<>0) AND (HIGHNOW[PLAYER][I]>=0) THEN BEGIN IF HIGHNOW[PLAYER][I]-PIETREBUFF[PLAYER][I]=43 THEN TOSCREEN(X,Y-16,X+18,Y,FISSO); COPYPUTSCR(X,Y,FRAME[PIETRA][0],0,FISSO); TOPOINTER(X,Y,X+18,Y+16,FISSO); INC(INDPIETRE[PLAYER]); TABPIETRE[PLAYER][INDPIETRE[PLAYER]].INDX:=X-1; TABPIETRE[PLAYER][INDPIETRE[PLAYER]].INDY:=((J-1) SHL 4)+27; TABPIETRE[PLAYER][INDPIETRE[PLAYER]].TIPO:=0; END; DEC(HIGHNOW[PLAYER][I],PIETREBUFF[PLAYER][I]); PIETREBUFF[PLAYER][I]:=0; END ELSE BEGIN INC(COORDPBUFF[PLAYER][I],16); Y:=COORDPBUFF[PLAYER][I]; IF Y>=43 THEN TOSCREEN(X,Y-16,X+18,Y,FISSO); FOR J:=0 TO PIETREBUFF[PLAYER][I]-1 DO BEGIN IF Y>=27 THEN COPYPUTSCR(X,Y,FRAME[PIETRA][0],0,FISSO); INC(Y,16) END; FACENDOSTO[PLAYER]:=CADETING; END; END; INC(X,18); END; END;

assembly source example:

PROCEDURE FASTPUTSCR(X1,Y1:WORD;VAR CAPT:ARRAY OF BYTE);ASSEMBLER; ASM MOV DI,X1 {MUOVO IN DI X1} MOV AX,Y1 {MUOVO IN AX Y1} XCHG AH,AL {MOLTIPLICO AX*256} ADD DI,AX {SOMMO A X Y*256} SHR AX,2 {DIVIDO AX 4 FA 64 E SI PUO' SOMMARE} ADD DI,AX {A X} PUSH DS LDS SI,CAPT MOV AX,0A000H MOV ES,AX MOV DX,320 INC SI MOV AL,[SI] XOR AH,AH SUB DX,AX INC SI MOV BL,[SI] INC SI @Ciclo2: MOV CX,AX SHR CX,1 REP MOVSW ADC CX,CX REP MOVSB ADD DI,DX DEC BL JNZ @Ciclo2 POP DS END;

one screen shot:

Link to the game: [https://docs.google.com/open?id=0B3zwSfMivwvBNmNxYVJGcmwtR0k](https://docs.google.com/open?id=0B3zwSfMivwvBNmNxYVJGcmwtR0k)

powered by dosbox and I can say..it is still fun 🙂

Edit: Unluckily it seems like dosbox does not support very well all the powerful code behind this game and it crashes while playing the second level. If you know other good DOS emulators, please let me know.

Hey, just to remind you that the Google Doc link is forbidden.

tested and works fine