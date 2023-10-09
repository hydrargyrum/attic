#!/bin/sed -f
# SPDX-License-Identifier: WTFPL

y/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/

s/ /␞/g

s/\./.-.-.-␟/g
s/,/--..--␟/g
s/?/..--..␟/g
s/!/-.-.--␟/g

s/a/.-␟/g
s/b/-...␟/g
s/c/-.-.␟/g
s/d/-..␟/g
s/e/.␟/g
s/f/..-.␟/g
s/g/--.␟/g
s/h/....␟/g
s/i/..␟/g
s/j/.---␟/g
s/k/-.-␟/g
s/l/.-..␟/g
s/m/--␟/g
s/n/-.␟/g
s/o/---␟/g
s/p/.--.␟/g
s/q/--.-␟/g
s/r/.-.␟/g
s/s/...␟/g
s/t/-␟/g
s/u/..-␟/g
s/v/...-␟/g
s/w/.--␟/g
s/x/-..-␟/g
s/y/-.--␟/g
s/z/--..␟/g
s/0/-----␟/g
s/1/.----␟/g
s/2/..---␟/g
s/3/...--␟/g
s/4/....-␟/g
s/5/.....␟/g
s/6/-....␟/g
s/7/--...␟/g
s/8/---..␟/g
s/9/----.␟/g

s/␟/,/g
s:␞:/:g

s/,$//g
