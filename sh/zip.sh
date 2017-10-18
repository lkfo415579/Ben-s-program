#!/bin/bash

[ $# -eq 0 ] && { 
	echo "Usage: $0 [zip|unzip] file_suffix zip_name [dir_name]";
	echo "" 
	echo "Zip example:"
	echo "$0 zip tar.bz2 FileName.tar.bz2 DirName"
	echo ""
	echo "Unzip example:"
	echo "$0 unzip tar.bz2 FileName.tar.bz2"
	echo ""
	echo "Reference: http://note.drx.tw/2008/04/command.html"
	exit 1; 
}

if [ $1 = "zip" ] 
then 
	if [ $# -lt 4 ]
	then
		echo "Usage: $0 zip/unzip file_suffix zip_name [dir_name]";
		echo "Syntax error: zip option require directory name!"
		exit
	fi
fi

OPTION=${1:-option}
SUFFIX=${2:-suffix}
ZIPNME=${3:-zipName}
DIRNME=${4:-''}

function execCmd {
	if [ $1 = "zip" ] 
	then
		cmd="$2"
		echo "Running: $2"
		eval $cmd
	else
		cmd="$3"
		echo "Running: $3"
		eval $cmd
	fi
}

case $SUFFIX in
'tar')  
	execCmd $OPTION 'tar cvf $ZIPNME $DIRNME' 'tar xvf $ZIPNME'
	;;
'gz')  
	execCmd $OPTION 'gzip $DIRNME' 'gzip -d $ZIPNME'
	#option 2
	#execCmd $OPTION 'gzip $DIRNME' 'gunzip -d $ZIPNME'
	;;
'tar.gz')  
	execCmd $OPTION 'tar zcvf $ZIPNME $DIRNME' 'tar zxvf $ZIPNME'
	;;
'bz')  
	execCmd $OPTION 'echo no_zip_option' 'bzip2 -d $ZIPNME' 
	#option 2
	#execCmd $OPTION 'echo no_zip_option' 'bunzip2 $ZIPNME' 
	;;
'tar.bz')  
	execCmd $OPTION 'echo no_zip_option' 'tar jxvf $ZIPNME'
	;;
'bz2')  
	execCmd $OPTION 'bzip2 -z $DIRNME' 'bzip2 -d $ZIPNME'
	#option 2
	#execCmd $OPTION 'bzip2 -z $DIRNME' 'bunzip2 $ZIPNME'
	;;
'tar.bz2')  
	execCmd $OPTION 'tar jcvfi $ZIPNME $DIRNME' 'tar jxvf $ZIPNME'
	;;
'xz')  
	execCmd $OPTION 'xz -z $DIRNME' 'xz -d $ZIPNME' 
	;;
'tar.xz')  
	execCmd $OPTION 'tar Jcvf $ZIPNME $DIRNME' 'tar Jxvf $ZIPNME'
	;;
'Z')  
	execCmd $OPTION 'compress $DIRNME' 'uncompress $ZIPNME'
	;;
'tar.Z')  
	execCmd $OPTION 'tar Zcvf $ZIPNME $DIRNME' 'tar Zxvf $ZIPNME'
	;;
'tgz')  
	execCmd $OPTION 'tar zcvf $ZIPNME $DIRNME' 'tar zxvf $ZIPNME'
	;;
'tar.tgz')  
	execCmd $OPTION 'tar zcvf $ZIPNME $DIRNME' 'tar zxvf $ZIPNME'
	;;
'7z')  
	#zip with password
	#execCmd $OPTION '7z a $ZIPNME $DIRNME -p12345678' '7z x $ZIPNME'
	execCmd $OPTION '7z a $ZIPNME $DIRNME' '7z x $ZIPNME'
	;;
'zip')  
	execCmd $OPTION 'zip $ZIPNME $DIRNME' 'unzip $ZIPNME'
	;;
'rar')  
	execCmd $OPTION 'rar a $ZIPNME $DIRNME' 'rar e $ZIPNME'
	#execCmd $OPTION 'rar a $ZIPNME $DIRNME' 'unrar e $ZIPNME'
	#execCmd $OPTION 'rar a $ZIPNME $DIRNME' 'rar x $ZIPNME'
	;;
'lha')  
	execCmd $OPTION 'lha -a $ZIPNME $DIRNME' 'lha -e $ZIPNME'
	;;
*) 
	echo "Usage: $0 zip/unzip file_suffix zip_name [dir_name]"
	echo "Error: Unsupport zip type [$SUFFIX]"
	;;
esac
