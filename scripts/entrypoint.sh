#!/usr/bin/env bash
tmux new-session -d -s recognition_node "python roboy_imitator/speech_to_text/recognition_node.py"
tmux new-session -d -s main_loop "python roboy_imitator/main.py"
tmux
