# Instructions to download youtube-dl
# For Mac use "brew install youtube-dl"
# For windows use "sudo -H pip install --upgrade youtube-dl"

if (( $# < 2 )); then
	echo "Usage: ./download_yt.sh video https://www.youtube.com/watch?v=OiFC5h9Yqgc"
    echo "       ./download_yt.sh audio https://www.youtube.com/watch?v=oHg5SJYRHA0"
	exit 1
fi

if [ "$1" == "video" ]; then
    echo "Downloading video from $2"
    youtube-dl $2
    exit 1
else
    if [ "$1" == "audio" ]; then
        echo "Downloading audio from $2"
        youtube-dl -x --audio-format mp3 $2
        exit 1
    fi
fi
