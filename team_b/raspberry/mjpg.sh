export STREAMER_PATH=/home/pi/mjpg/mjpg-streamer/mjpg-streamer-experimental
export LD_LIBRARY_PATH=$STREAMER_PATH
$STREAMER_PATH/mjpg_streamer -o "output_http.so -w ./www -p 9090" -i "input_raspicam.so -hf -fps 15 --width 1260 --height 600 "

