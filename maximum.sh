#!/bin/bash

function stop(){
  kill "$(cat /tmp/vlcpid)"
  rm /tmp/vlcpid
}

trap stop INT
trap stop TERM

cvlc https://maximum.hostingradio.ru/maximum96.aacp -d --pidfile /tmp/vlcpid

VERSION="1.0"
echo "Playing Radio Maximum Moscow, program version $VERSION"

CURRENT_DIR="$(dirname "${BASH_SOURCE[0]}")"
INTERPRETER="$CURRENT_DIR/venv/bin/python"
SCRIPT="$CURRENT_DIR/main.py"
bash -c "$INTERPRETER $SCRIPT"
