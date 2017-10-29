#bin/sh
gst-launch-0.10 alsasrc device=hw:1,0 ! audio/x-raw-int,rate=44100,channel=1 ! audioconvert ! audioecho delay=$1 intensity=$2 feedback=$3 ! audioconvert ! alsasink device=hw:0,0 sync=false
