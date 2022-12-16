#!/bin/bash

i=1
a=$(echo $PATH | cut -d ':' -f$i)
while [ -n $a ]
do 
   echo $a
   ((i++))
   a=$(echo $PATH | cut -d ':' -f$i)
done
