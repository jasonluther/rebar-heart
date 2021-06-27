# Managing Animations

There are many ways to control the scheduling of the animation programs, including just having the programs themselves do that. In an effort to keep the animation programs as simple as possible, I chose to use `systemd` to schedule things to turn on and off. 

Each animation program has a corresponding `.service` file that allows you to start the animation with `sudo service "animation-name" start`. 

The `[Unit]` section includes a `Conflicts` directive that lists all of the other animation programs. When you start one, any other running animations will stop. 

To add a new program, it needs to be added to the `animations` list in [`make-systemd-files.py`](./make-systemd-files.py). 

Two [`.timer` files](./static/) are used to start and stop the animation each day. 