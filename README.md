A Discord bot that converts EDOPro replay files into mp4 with the magic of AWS.

I'll make actual documentation later, but the tl;dr is that this bot runs EDOPro on either an EC2 instance or an Amazon Workspace, opens the replay file, and uses ffmpeg to screen record. EC2 is scalable and has less overhead since it's just a basic linux kernel, but it doesn't have xserver. If you use EC2, remember to install xvfb.

Things to add, in no particular order:
- use github project planning tools lol
- switch from workspace to EC2
- make a template for EC2, so you can spin up new instances quickly
- make this scalable; central queue, and EC2 instances pull from the queue?
- get CI/CD working. EDOPro should be built as part of a Github Action
- use poetry
- use Docker

Needs wmctrl, Xvfb, ffmpeg, scrot
