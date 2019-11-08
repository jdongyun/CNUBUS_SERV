#!/bin/sh
if [ $1 = "start" ]
then
	sudo su -c 'source env/bin/activate && forever/bin/forever start --append --uid "cnubus" -c uwsgi app.ini'
elif [ $1 = "stop" ]
then
	sudo su -c 'forever/bin/forever stop cnubus'
	
elif [ $1 = "restart" ]
then
	sudo su -c 'forever/bin/forever restart cnubus'
elif [ $1 = "log" ]
then
	sudo su -c 'cat /root/.forever/cnubus.log'
fi

