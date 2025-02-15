#!/bin/bash
# Get and create file name
newfile="conv_${1}"
# conv and output file
iconv -f sjis -t utf8 $1 >> $newfile
# delete input file
rm $1
