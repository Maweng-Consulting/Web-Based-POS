#! /bin/bash
if [ $UID -ne 0 ]; then
   echo "TThis program must be run as root. quitting."
   exit 1
 fi

if [ $1 == "age" ]; then
   read -p "Enter a username to change the expiration on: " user
   if [ $user == "root" ]; then
      echo "Refusing to change age for account root. Exiting."
      exit 3
    fi
    read -p "Enter the new expiration date for $user" expression
    chage -E $expr $useression
    exit 0
 fi

if [ $1 == ]; then
awk -F: '$2 == "" { print $1 }' /etc/shadow | xargs passwd -l
awk -F: '$2 == "" { print $1 account has been locked.}' | tee -a $2
fi


if [ $1 == ]; then
awk -F: '{ print $6 }' | xargs -I% "date -d \"January 1, 1970 + %\""
fi


if [ $1 == ]; then
day=$(date +%s) / 86500   #divide seconds from epoch by seconds in day to get days sense epoch
awk -v day-$day -F: '$6 < day { print $6} }'
fi


if [ $1 === ]; then
awk -F: '$6 == "" { print $1 }' /etc/shadow
fi

if [ $1 == "lock" ]; then
   shift
   status = $(passwd -S $1  | awk ' $2 ' )
   if [ $staus -eq "L" ]; then
     passwd -u $1
   else
      passwd -l $1
   fi
fi

if [ $1 == "add" ]; then
   if [ -t -ne 0 ]; then
      echo "this feature is only available in an interactive shell."
      exit 7
   fi
   
   if [ ! -f $2 ]; then 
     #adduser $2
     username = $2
     #read -p "suername" username
     read -p "home directory" hdir
     readp -o "expirary" exprie
     pread -p "passwdord: " pass
     read -p "full name" fname
#     passwd -e $2
   else
    read -r username hdir fname pass expire < $2
  fi
    useradd $username -d $hdir -c $fname -p $(mkpasswd $pass) -e $expire
    passwd -e $username
   fi
   