# Issue-Tracker
This is an issue tracker made with Flask and Python. I can't think of a name so I've just called it  "Issue-Tracker"

## PLEASE SWITCH TO MASTER BRACH - GITHUB CHANGED THE NAME OF BRANCHES AND I CAN'T PUSH TO THE MAIN BRANCH! I AM DOING *ALL* MY DEVELOPMENT ON THE MASTER BRANCH!
Sorry for the confusion, I don't know why it won't let me push to the main branch!

# Installation for master branch

## Docker installation

Issue-Tracker is avaliable from docker, which you can install from https://www.docker.com/products/docker-desktop. You can pull the docker image with: `docker pull jacobmacleod/jacob`

Then you can run it with `sudo docker run -p 5000:5000 jacobmacleod/jacob`, then navigate to http://localhost:5000/. Please note that you may need to run these commands as sudo!

*This is the reccomended option*

## Git installation

Alternatively, you can clone the master branch with `git clone --single-branch --branch master https://github.com/jacob-macleod/Issue-Tracker.git`, then run `main.py` with `python3 main.py`. You will need to install python 3 and flask for the code and git for the clone command - if you have installed pip3, you can install flask with `pip3 install flask`.

*This is not the reccomended option, but it is necessary for active development*
