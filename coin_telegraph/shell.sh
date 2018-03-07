#!/bin/bash
echo Hi
check=`ps aux | grep -c  scraping_ct.py`

if [ "$check" == "1" ]
then
	echo "stopped"
	ipython scraping_ct.py  
else 
	echo "runnig"
fi

echo $check
