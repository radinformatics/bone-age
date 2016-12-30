# Bone-Age Demo

**under development**

This repository builds a Docker image and a [Singularity](http://singularity.lbl.gov) image, each that will run the bone age demo to predict bone age from a radiograph. The user has the option to run the prediction algorithm from the command line with an image file input, or to run a web server to see an interactive demo.


>> The predict_image.py script is a light wrapper around the model and includes the functions that are needed for such a demo. The user would upload a image which would then be processed with the given model on the back-end. The results would then be displayed for the user.


If you are working on your local machine, you can use either Docker or Singularity. If you are running in a shared cluster (HPC) environment where you do not have root permissions, Singularity is your best option. Instructions are included for both.

Packages that need to be installed are included in [requirements.txt](requirements.txt) and installed into the container via the [Dockerfile](Dockerfile).

# Singularity

## 1. Install Singularity

Instructions can be found on the [singularity site](https://singularityware.github.io).

## 2. Bootstrap the image
Bootstrapping means using something to build from, or not starting from nothing. In this case, we are going to use a build file that bootstraps a Docker image of the PE Finder (yes, the same one discussed shortly after). This build file is called [Singularity](Singularity), and for more details about this you can [read here](http://singularity.lbl.gov/docs-docker).

    sudo singularity create --size 6000 boneage.img
    sudo singularity bootstrap boneage.img Singularity


## 3. Run commands
The entry to the container is done simply by using it as an executable:


	./boneage.img --help
	usage: cli.py [-h] [--image IMAGE] [--folder FOLDER] [--gender {M,F}]
		      [--width WIDTH] [--height HEIGHT] [--debug]

	Predict bone age of an image.

	optional arguments:
	  -h, --help       show this help message and exit
	  --image IMAGE    Path to single bone image.
	  --folder FOLDER  Path to folder of images to parse.
	  --gender {M,F}   the gender of the individual (M or F), default is M (male)
	  --width WIDTH    warped width to resize the image in pixels (default 256)
	  --height HEIGHT  warped height to resize the image in pixels (default 256)
	  --debug          use verbose logging to debug.


### **TODO Vanessa** 
- parse and show help
- provide runscript to run prediction algorithm, optionally binding an entire directory to data to run for many images
- docker-compose file should run local server, in which case the same runscript is executed with an argument to start the webserver.



## How do I shell into the container?
Singularity has an easy, intuitive way to shell inside!

      singularity shell boneage.img


**NOT YET WRITTEN**

# Docker

## Getting Started
You should first [install Docker](https://docs.docker.com/engine/installation/). The container is provided on [Docker Hub](https://hub.docker.com/r/vanessa/pefinder/) and can be downloaded from there when you run it, however if you want to look at or make changes to the code, it's recommended to clone the repo and build the container locally:

    git clone http://www.github.com/radinformatics/bone-age-demo
    cd bone-age-demo
    docker build -t vanessa/bone-age-demo .



## How do I shell into the container?
By default, running the container uses the `ENTRYPOINT`, meaning it is used as an executable and you do not enter the container. In the case that you want a container-based environment that is installed with the dependencies of PEFinder, or if you want to interactively work with the code, you may want to shell into the container. If there is a running container (eg an analysis) and you want to open up another terminal on your local machine to look inside (while it's running!) you need to get the 12 digit identifier with `docker ps`, and then plug it into this command:

      docker exec -it dc70464c6eb5 bash

This says we want to execute (exec) and (interactive)(terminal) for container with id (af21bf1d48a6) and run the command (bash)

If the container isn't running, then you can use `run`:

      docker run -it --entrypoint /bin/sh vanessa/boneage



# Input arguments

**todo**

# Examples
For each of the examples, the equivalent Docker and Singularity commands are provided.

## Command Line

### Classifying One Image

**todo**

### Classifying Folder of Images


## Interactive Web Interface

**todo**

Ultimately, we will build this demo and serve on [singularity hub](http://www.singularity-hub.org) and then have an application that takes inputs / outputs for the container, and runs on demand.
