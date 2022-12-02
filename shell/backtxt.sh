#!/bin/bash
# Lab03-4 Make Backup Dirctory and Backup all '*.txt' files under '/'
# 20220921 c.b.choi

# make backup directory

backd=back$(date +"%y%m%d")
if [ ! -d $backd ]
then
    mkdir $backd
else
    nu=1
    while [ -d $backd\($nu\) ]
	do
		((nu++))
    done
	backd=$backd\($nu\)
	mkdir $backd
fi
echo "'$backd' created..."

# find and copy files

fres=$(sudo find / -name "*.txt")
i=1
a=$(echo $fres | cut -d ' ' -f$i)

while [ ! -z $a ]
do
	fn=$(basename $a)
	if [ ! -f $backd/$fn ]; then
	    cp $a $backd
		echo "'$a' copied..."
	else
        j=1
        while [ -f $backd/$fn\($j\) ]
		do
            ((j++))
		done
		cp $a $backd/$fn\($j\)
		echo "'$a($j)' copied..."
    fi
	((i++))
    a=$(echo $fres | cut -d ' ' -f$i)
done
