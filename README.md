# Bone-Age Demo

**under development**

This repository builds a Docker image and a [Singularity](http://singularity.lbl.gov) image, each that will run the bone age demo to predict bone age from a radiograph. The user has the option to run the prediction algorithm from the command line with an image file input, or to run a web server to see an interactive demo.


>> The predict_image.py script is a light wrapper around the model and includes the functions that are needed for such a demo. The user would upload a image which would then be processed with the given model on the back-end. The results would then be displayed for the user.


If you are working on your local machine, you can use either Docker or Singularity. If you are running in a shared cluster (HPC) environment where you do not have root permissions, Singularity is your best option. Instructions are included for both.

Packages that need to be installed are included in [requirements.txt](requirements.txt) and installed into the container via the [Dockerfile](Dockerfile).


# Docker

## Getting Started
You should first [install Docker](https://docs.docker.com/engine/installation/). The container is provided on [Docker Hub](https://hub.docker.com/r/vanessa/boneage/) and can be downloaded from there when you run it, and this is recommended because building it takes a while to compile OpenCV.

### I want to build it!
If you want to look at or make changes to the code, it's recommended to clone the repo and build the container locally:

    git clone http://www.github.com/radinformatics/bone-age
    cd bone-age
    docker build -t vanessa/boneage .

The docker daemon will first look for an image called `vanessa/boneage` locally, and if not found, will then try Dockerhub, and download it from there. If for any reason you want to remove your image, just do the following:

    docker rmi vanessa/boneage


## Running commands
The entry to the container is done simply by using it as an executable:


	docker run vanessa/boneage --help
	usage: cli.py [-h] [--image IMAGE] [--output OUTPUT] [--gender {M,F}]
		      [--width WIDTH] [--height HEIGHT] [--debug]

	Predict bone age of an image.

	optional arguments:
	  -h, --help       show this help message and exit
	  --image IMAGE    Path to single bone image.
	  --output OUTPUT  Path to output file to write results.
	  --gender {M,F}   the gender of the individual (M or F), default is M (male)
	  --width WIDTH    warped width to resize the image in pixels (default 256)
	  --height HEIGHT  warped height to resize the image in pixels (default 256)
	  --debug          use verbose logging to debug.



### Run Prediction With Example
To run the bone-age demo non interactively to get a prediction, you can run it without any arguments:

      docker run vanessa/boneage

	*** Starting Bone Age Prediction ****
	No image selected, will use provided example...
	Building model, please wait.
	Predicted Age : 14 Months
	Weighted Prediction : 11.832177 Months


The command above is saying "map the folder `$PWD/example_images` (where my 4.png is located) to the `/data` folder in the container. Then, tell the script in the container to use the image located at `/data/4.png`. If you want to see debug output (for more details about running) you can add `--debug`


      docker run vanessa/boneage --debug

	Environment message level found to be DEBUG

	*** Starting Bone Age Prediction ****
	No image selected, will use provided example...
	DEBUG:bone-age:is_male: True
	DEBUG:bone-age:image: /code/example_images/5.png
	DEBUG:bone-age:height: 256
	DEBUG:bone-age:width: 256
	DEBUG:PIL.PngImagePlugin:STREAM IHDR 16 13
	DEBUG:PIL.PngImagePlugin:STREAM IDAT 41 65536
	Building model, please wait.
	Predicted Age : 8 Months
	Weighted Prediction : 8.610813 Months


### Run Prediction With Your Own Image
If you want to provide your own image, you need to bind it to the /data directory in the folder, and map a path to it. Don't forget to specify the gender - the default is male, and you may want to change that:

       
       docker run -v $PWD/example_images:/data vanessa/boneage --image /data/4.png

	*** Starting Bone Age Prediction ****
	Building model, please wait.
	Predicted Age : 8 Months
	Weighted Prediction : 8.641131 Months


We can of course add debug to verify that the default is male, and we are using our mapped image:


        docker run -v $PWD/example_images:/data vanessa/boneage --image /data/4.png --debug
	Environment message level found to be DEBUG

	*** Starting Bone Age Prediction ****
	DEBUG:bone-age:is_male: True
	DEBUG:bone-age:image: /data/4.png
	DEBUG:bone-age:height: 256
	DEBUG:bone-age:width: 256
	DEBUG:PIL.PngImagePlugin:STREAM IHDR 16 13
	DEBUG:PIL.PngImagePlugin:STREAM IDAT 41 65536
	Building model, please wait.
	Predicted Age : 8 Months
	Weighted Prediction : 8.641131 Months


We can specify a different gender, and the prediction changes:

        docker run -v $PWD/example_images:/data vanessa/boneage --image /data/4.png --gender F --debug
	Environment message level found to be DEBUG

	Environment message level found to be DEBUG

	*** Starting Bone Age Prediction ****
	DEBUG:bone-age:is_male: False
	DEBUG:bone-age:image: /data/4.png
	DEBUG:bone-age:height: 256
	DEBUG:bone-age:width: 256
	DEBUG:PIL.PngImagePlugin:STREAM IHDR 16 13
	DEBUG:PIL.PngImagePlugin:STREAM IDAT 41 65536
	Building model, please wait.
	Predicted Age : 16 Months
	Weighted Prediction : 16.000000 Months


### Save output to file
If you specify the `--output` argument, you can save the result as a json to file. Again, we will need to specify a file in a folder mapped to our local machine:

      docker run -v $PWD/example_images:/data vanessa/boneage --output /data/demo.json --debug

	Environment message level found to be DEBUG

	*** Starting Bone Age Prediction ****
	No image selected, will use provided example...
	DEBUG:bone-age:is_male: True
	DEBUG:bone-age:image: /code/example_images/4.png
	DEBUG:bone-age:height: 256
	DEBUG:bone-age:width: 256
	DEBUG:PIL.PngImagePlugin:STREAM IHDR 16 13
	DEBUG:PIL.PngImagePlugin:STREAM IDAT 41 65536
	Building model, please wait.
	Predicted Age : 8 Months
	Weighted Prediction : 8.641131 Months
	DEBUG:bone-age:Result written to /data/demo.json

Now we can look at the data - remember the folder that was mapped on our local machine is `$PWD/example_images`

        cat $PWD/example_images/demo.json
        {
           "gender": "M",
           "image": "/code/example_images/4.png",
           "predicted_age": 8,
           "predicted_weight": 8.64113067092668
        }


The function inside the container to generate this result could be scaled by either providing an input argument for the user to specify an input file (with image paths and genders) and a single output file to write to, or running the command many times to write separate output files, or having a `--silent` option to suppress all output (except for the result) that could be piped (appended) into a single output file. All of these could be implemented, it really depends on the desired outcome. For the current purpose (plugging the container into a web server for a demo) the above that produces a single file, or multiple single files, is a reasonable approach.


## How do I shell into the container?
By default, running the container uses the `ENTRYPOINT`, meaning it is used as an executable and you do not enter the container. In the case that you want a container-based environment that is installed with the dependencies of boneage, or if you want to interactively work with the code, you may want to shell into the container.

      docker run -it --entrypoint /bin/bash vanessa/boneage

Keep in mind that once you exit from this run, the container image is not saved, including your changes.



# Singularity

## 1. Install Singularity

Instructions can be found on the [singularity site](https://singularityware.github.io).

## 2. Bootstrap the image
Bootstrapping means using something to build from, or not starting from nothing. In this case, we are going to use a build file that bootstraps a Docker image of boneage (yes, the same one discussed above). This build file is called [Singularity](Singularity), and for more details about this you can [read here](http://singularity.lbl.gov/docs-docker).

    sudo singularity create --size 6000 boneage.img
    sudo singularity bootstrap boneage.img Singularity


## 3. Run commands
The commands are equivalent as above, except we can use the container as an executable:

      ./boneage.img --help

and to make a drive, we use `--bind` instead

      singularity run --bind $PWD/example_images:/data boneage.img --debug


## How do I shell into the container?
Singularity has an easy, intuitive way to shell inside!

      singularity shell boneage.img



# Interactive Web Interface

**todo**

Ultimately, we will build this demo and serve on [singularity hub](http://www.singularity-hub.org) and then have an application that takes inputs / outputs for the container, and runs on demand.
