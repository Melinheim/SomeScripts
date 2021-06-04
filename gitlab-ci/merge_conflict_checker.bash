#! /bin/bash
all_conflics=$(grep --exclude-dir=.git --exclude=\*.git* -rnw './' -e '<<<<<<< HEAD') || true
echo $all_conflics
output=$(echo $all_conflics | wc -l)
empty_var=$( [ -z "$all_conflics" ] && echo 1 || echo 0)
if [ $output -ne 0 -a $empty_var -ne 1 ]; then echo "solve merge conflicts please"; false; fi;
