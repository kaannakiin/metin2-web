#!/bin/sh
set -eu
date -u '+UTC %Y-%m-%d %H:%M:%S'
for relative in db auth channels/channel1/core1 channels/channel1/core2 channels/channel1/core3 channels/channel99; do
    directory="/usr/home/main/$relative"
    for name in syserr syslog; do
        file="$directory/$name"
        test -f "$file" || continue
        echo "LOG $relative/$name"
        if [ "$name" = syserr ]; then
            tail -n 25 "$file"
        else
            tail -n 500 "$file" | awk 'tolower($0) ~ /login|enter|disconnect|deneme|load.*player|player.*load|invalid|unknown|error|hack|select.*character/ && tolower($0) !~ /password|passwd/' | tail -n 25
        fi
    done
done
