#!/bin/bash
# Lab03-3 Make Backup Dirctory
# 220921 c.b.choi

if [ ! -d back$(date +"%y%m%d") ]
then
    mkdir back$(date +"%y%m%d")
else
    nu=1
    while [ -d back$(date +"%y%m%d")\($nu\) ]
	do
		((nu++))
    done
	mkdir back$(date +"%y%m%d")\($nu\)
fi
