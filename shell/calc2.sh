#!/bin/bash
# Two number calc: $1=num, $2=op, $3=num

if [ "$2" = "x" ]
then
    res=$(expr $1 '*' $3)
else
    res=$(expr $1 $2 $3)
fi
echo "$1 $2 $3 = $res"
