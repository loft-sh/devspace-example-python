# Hello, DevSpace!

This is a simple introduction to using DevSpace with a Python [FastAPI](https://github.com/tiangolo/fastapi) project.


## What Are We Doing Here?

So, what are we doing here? Let's assume you are a Python developer (you probably are if you are reading this!) 
working on a simple FastAPI application that will live in a Kubernetes cluster.

You can, of course, run your application locally while you are developing it, and that may be a great way to get 
started. At some point, however, you will need to get this application running in a Kubernetes cluster -- in a way that 
will look much more similar to what it will look like in production. 

Re-building and pushing an image to an image repository, and then re-rolling out a deployment is one way to achieve 
this, but it is *not* a fun way to do it! *[There must be a better way!](https://youtu.be/p33CVV29OG8?t=566)*

![There must be a better way!](../static/hettinger-there-must-be-a-better-way.jpg)

And of course, there is! DevSpace's purpose in life is to make developing applications that live in Kubernetes easy. 
This very simple example will walk you through setting up a tiny FastAPI web application that you can work on live 
*in* a Kubernetes cluster.


## The Set-Up

If you haven't played with FastAPI before, you are missing out! It is a great project that builds on [Starlette](https://www.starlette.io) and 
[Pydantic](https://pydantic-docs.helpmanual.io) to give you an amazing web and API development experience. For this 
DevSpace example we will create the simplest possible FastAPI web server -- a web server that will listen at the 
root path and simply return a message to our page visitor.

The actual code to accomplish this is quite simple, and is copied directly from the FastAPI documentation:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}
```

This code lives in our `app` directory in the `main.py` module.

If you would like to test this out on your local machine prior to getting it running in Kubernetes you will need to 
create a new virtual environment and install the requirements in `requirements.txt`. You can accomplish this like:

```shell
python3.10 -m venv venv
source venv/bin/activate
python3.10 -m pip install -r requirements.txt
```

Once you've created and activated your virtual environment and installed the requirements you can run the app with 
uvicorn like so:

```shell
uvicorn app.main:app --host 0.0.0.0 --port 80
```

After that you can open a browser to `http://localhost:80` and you should see our simple message printed out.


## Containerizing

OK, now that we have a functional web app (and it just has so much functionality, doesn't it!) we need to 
containerize it if we want to be able to deploy it in Kubernetes!

We'll do this with a very simple Dockerfile that builds form the `python:3.10.7-slim image`. In this Dockerfile we'll 
create a working director `hello-devspace`, copy our `requirements.txt` file into that directory, and install the 
requirements. After that we simply copy our `app` directory (which contains all of our code required for the 
application) into the image.

The last things we need are an `ENTRYPOINT` and a `CMD` (we could just stuff it all into one but we'll split things 
out nicely). Our entrypoint will be to run `uvicorn` pointing at our `app.main:app` module. Our command will be the 
extra arguments that we want to pass to uvicorn -- in our case the `--host` flag set to `0.0.0.0` (to bind to all 
interfaces on our container) and the `--port` flag to set the listen port to `80`.

You can check out the complete Dockerfile [here](./Dockerfile).


## What's Next?

Normally your next step would be to build the container image and push it *somewhere*. We of course still need to 
build this image and push it somewhere, but now we can let DevSpace handle that for us.

As for the pushing the image to *somewhere* thing -- you do need to be able to get this image to somewhere your 
cluster can pull it from. If you are doing development locally on Minikube/Docker Desktop/something similar, you may 
be able to simply build the image and have it be accessible from the cluster. For that situation you can ignore 
the next paragraph and move ahead!

If you are *not* using Minikube/Docker Desktop/something similar and need to be able to push the image(s) to an 
accessible repository, you will need to first have access to said repository! We will also need to update our 
manifest and `devspace.yaml` files to set the appropriate registry URL for our image references. To make this easy on 
you, you can simply run `make set_registry` from this directory. This will prompt you for your registry URL and 
update the `manifests/deployment.yaml` image field and the REGISTRY variable field in the `devspace.yaml` file. 
(We'll talk about the `devspace.yaml` file more briefly, so for now, just know we do need to have a pushable 
registry set and this is taking care of that!) 

The only thing left to do is to deploy our application into a Kubernetes cluster. In this case there is a very 
simple `deployment.yaml` manifest to do just that. This manifest will create a simple deployment, deploying a single 
pod of running our application container.

For "production" use, we may be "done" at this point -- we can build, push, and deploy the application, but if we 
are still in the process of developing our app, and want to try that out in a cluster, we are just getting started. 
As mentioned in the introduction, you *could* of course build, push, and (re-)deploy every time you want to make a 
change to your application, but that would be tedious, and not at all awesome.

This is where DevSpace comes in! We can use DevSpace to not only deploy our real application, but more importantly, 
and more to its intended purpose, we can use it to streamline the in-cluster development process of our application!


## Enter DevSpace

To use DevSpace, you simply need to install the DevSpace CLI 
(instructions [here](https://devspace.sh/docs/getting-started/installation)), and to have a `devspace.yaml` 
configuration file telling DevSpace how you want to work with your application. As this is the "hello, world" 
Python/DevSpace example, we'll be keeping our `devspace.yaml` file pretty simple as you can see here:

```yaml
version: v2beta1
name: python-hello-devspace

vars:
  REGISTRY: 172.31.254.11
  IMAGE: ${REGISTRY}/python-hello-devspace
  DEVSPACE_FLAGS: "-n python-hello-devspace"

images:
  hello-devspace:
    image: ${IMAGE}
    dockerfile: ./Dockerfile
    rebuildStrategy: ignoreContextChanges

deployments:
  hello-devspace:
    kubectl:
      manifests:
        - manifests/

dev:
  hello-devspace:
    imageSelector: ${IMAGE}
    ports:
      - port: 3000:80
    sync:
      - path: ./app/:/hello-devspace/app/
    terminal:
      command: uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
```

This `devspace.yaml`, has four major sections that pretty much all your `devspace.yaml` files will end up having:

1. `vars`: not strictly mandatory, but certainly nice to have! This is where we can define some variables that we 
   will refer to throughout our DevSpace config. In this case we are setting:
   - `REGISTRY`: a variable to define the registry we will be pushing our image to
   - `IMAGE`: the name of the image we are building. You can also see here we can refer to our previously defined 
     `REGISTRY` variable here in the value, pretty snazzy!
   - `DEVSPACE_FLAGS`: is a "special" variable that allows you to set any flags you would normally pass to the 
     DevSpace CLI as a variable -- in this case we are passing `-n python-hello-devspace` which will tell DevSpace 
     to deploy our application into the namespace `python-hello-devspace`


2. `images`: is an object that contains all the images we will be building/pushing for our application.

    In this case we only have the one image `hello-devspace`. In the image definition we define the image name 
    (which we pull from our variables), the dockerfile used to build the image, and the `rebuildStrategy`. This last 
    one tells DevSpace when it needs to rebuild the image -- in this case we want to ignore changes in our Docker 
    context and only re-build the image when the Dockerfile changes (because we will be live syncing the actual 
    application code to the container, thus there is no need to rebuild the container while developing!).


3. `deployments`: is what it sounds like! This section defines how DevSpace should deploy our application. In this 
   case we simply refer to the Kubernetes manifests in the `manifests` directory.


4. `dev`: DevSpace, as the name would imply, is about helping you develop faster/easier in Kubernets -- the `dev` 
   section is where we tell DevSpace how to help us do just that. In this example we have four important fields here:

    1. `imageSelector`: this field needs to match the image of a container in our deployment -- it tells DevSpace 
       which pod to update with our development setup.
    2. `ports`: tells DevSpace to create a tunnel(s) between our container and our local machine -- this way we can 
       easily access our application without needing to have an ingress setup. In this case we are exposing port 80 
       of our container on our local machines port 3000.
    3. `sync`: perhaps the most important one! `sync` tells DevSpace what files/directories to sync between our 
       local machine and the development container. In this case we will sync the whole "app" directory. As you make 
       changes to your local files DevSpace will automagically sync those changes out to the container!
    4. `terminal`:  allows us to connect to the development container and execute any command. In this example we 
       are running *mostly* the same command that our "production" container would (as defined in the Dockerfile), 
       with the addition of the `--reload` flag which allows uvicorn to hot-reload as we make changes to our code.


That's pretty much all there is to it! With this configuration in place we can now have DevSpace build, push, and 
deploy our application. Critically, we can now deploy our application in "dev" mode -- meaning that we can deploy 
our application to a Kubernetes cluster, make changes on our local machine, and have those changes automatically 
synced to the cluster. In this case, we even have automatic reloading of our application thanks to uvicorn (though 
it is worth noting that you can make this work with just DevSpace even if you don't have this functionality via 
uvicorn or similar!).


## Enough Already, Let's Do The Things!

At this point we've covered the basics of the FastAPI app, the Dockerfile, and of course DevSpace itself -- it's 
time to actually deploy this application!

From this directory run `devspace dev` to fire up the application in "dev" mode. You should see some output similar 
to the following:

```shell
$ devspace dev
info Using namespace 'python-hello-devspace'
info Using kube context 'loft-vcluster_devspace-dev_devspace-dev_loft-cluster'
build:hello-devspace Ensuring image pull secret for registry: 172.31.254.11...
build:hello-devspace Building image '172.31.254.11/python-hello-devspace:bBrcmuC' with engine 'docker'
build:hello-devspace Authenticating (172.31.254.11)...
build:hello-devspace Authentication successful (172.31.254.11)
Sending build context to Docker daemon  32.49MBocker daemon  557.1kB
build:hello-devspace Step 1/7 : FROM python:3.10.7-slim
build:hello-devspace  ---> fe16e9fa64e9
build:hello-devspace Step 2/7 : WORKDIR /hello-devspace
build:hello-devspace  ---> Running in 148fee4d150a
build:hello-devspace  ---> 6d4f99b86dc0
build:hello-devspace Step 3/7 : COPY ./requirements.txt /hello-devspace/requirements.txt
build:hello-devspace  ---> 029c33d3c947
build:hello-devspace Step 4/7 : RUN pip install --no-cache-dir --upgrade -r requirements.txt
build:hello-devspace  ---> Running in 93b44f7f12e5
build:hello-devspace Collecting fastapi==0.83.0
build:hello-devspace   Downloading fastapi-0.83.0-py3-none-any.whl (55 kB)
build:hello-devspace      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 55.3/55.3 kB 2.0 MB/s eta 0:00:00
build:hello-devspace Collecting uvicorn==0.18.3
build:hello-devspace   Downloading uvicorn-0.18.3-py3-none-any.whl (57 kB)
build:hello-devspace      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 57.4/57.4 kB 9.7 MB/s eta 0:00:00
build:hello-devspace Collecting starlette==0.19.1
build:hello-devspace   Downloading starlette-0.19.1-py3-none-any.whl (63 kB)
build:hello-devspace      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 63.3/63.3 kB 13.3 MB/s eta 0:00:00
build:hello-devspace Collecting pydantic!=1.7,!=1.7.1,!=1.7.2,!=1.7.3,!=1.8,!=1.8.1,<2.0.0,>=1.6.2
build:hello-devspace   Downloading pydantic-1.10.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (12.8 MB)
build:hello-devspace      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.8/12.8 MB 11.0 MB/s eta 0:00:00
build:hello-devspace Collecting h11>=0.8
build:hello-devspace   Downloading h11-0.13.0-py3-none-any.whl (58 kB)
build:hello-devspace      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 58.2/58.2 kB 12.5 MB/s eta 0:00:00
build:hello-devspace Collecting click>=7.0
build:hello-devspace   Downloading click-8.1.3-py3-none-any.whl (96 kB)
build:hello-devspace      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 96.6/96.6 kB 17.4 MB/s eta 0:00:00
build:hello-devspace Collecting anyio<5,>=3.4.0
build:hello-devspace   Downloading anyio-3.6.1-py3-none-any.whl (80 kB)
build:hello-devspace      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 80.6/80.6 kB 18.0 MB/s eta 0:00:00
build:hello-devspace Collecting typing-extensions>=4.1.0
build:hello-devspace   Downloading typing_extensions-4.3.0-py3-none-any.whl (25 kB)
build:hello-devspace Collecting sniffio>=1.1
build:hello-devspace   Downloading sniffio-1.3.0-py3-none-any.whl (10 kB)
build:hello-devspace Collecting idna>=2.8
build:hello-devspace   Downloading idna-3.3-py3-none-any.whl (61 kB)
build:hello-devspace      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 61.2/61.2 kB 23.8 MB/s eta 0:00:00
build:hello-devspace Installing collected packages: typing-extensions, sniffio, idna, h11, click, uvicorn, pydantic, anyio, starlette, fastapi
build:hello-devspace Successfully installed anyio-3.6.1 click-8.1.3 fastapi-0.83.0 h11-0.13.0 idna-3.3 pydantic-1.10.2 sniffio-1.3.0 starlette-0.19.1 typing-extensions-4.3.0 uvicorn-0.18.3
build:hello-devspace WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
build:hello-devspace  ---> 3f37855924c0
build:hello-devspace Step 5/7 : COPY ./app /hello-devspace/app
build:hello-devspace  ---> a7a38dbef1e9
build:hello-devspace Step 6/7 : ENTRYPOINT ["uvicorn", "app.main:app"]
build:hello-devspace  ---> Running in 1823304dd6fe
build:hello-devspace  ---> 00168d63b275
build:hello-devspace Step 7/7 : CMD ["--host", "0.0.0.0", "--port", "80"]
build:hello-devspace  ---> Running in 1aa4e3cfa006
build:hello-devspace  ---> 51e658ac8077
build:hello-devspace Successfully built 51e658ac8077
build:hello-devspace Successfully tagged 172.31.254.11/python-hello-devspace:bBrcmuC
build:hello-devspace The push refers to repository [172.31.254.11/python-hello-devspace]
build:hello-devspace 466a6652dc36: Preparing
build:hello-devspace 1df9af4b4f60: Preparing
build:hello-devspace 72eacc6e595e: Preparing
build:hello-devspace 09cc373e9a1e: Preparing
build:hello-devspace 1f3d56b29849: Preparing
build:hello-devspace 4fd1b16d91ec: Preparing
build:hello-devspace 1ca6974456cc: Preparing
build:hello-devspace 630337cfb78d: Preparing
build:hello-devspace 6485bed63627: Preparing
build:hello-devspace 4fd1b16d91ec: Waiting
build:hello-devspace 630337cfb78d: Waiting
build:hello-devspace 6485bed63627: Waiting
build:hello-devspace 1ca6974456cc: Waiting
build:hello-devspace 1f3d56b29849: Layer already exists
build:hello-devspace 4fd1b16d91ec: Layer already exists
build:hello-devspace 1ca6974456cc: Layer already exists
build:hello-devspace 630337cfb78d: Layer already exists
build:hello-devspace 09cc373e9a1e: Pushed
build:hello-devspace 6485bed63627: Layer already exists
build:hello-devspace 466a6652dc36: Pushed
build:hello-devspace 72eacc6e595e: Pushed
build:hello-devspace 1df9af4b4f60: Pushed
build:hello-devspace bBrcmuC: digest: sha256:e3bc3968c42e75fa4f2d52595ea26c464b5c8ac4a3d7ef02448b6647b4b52dc1 size: 2203
build:hello-devspace Image pushed to registry (172.31.254.11)
build:hello-devspace Done processing image '172.31.254.11/python-hello-devspace'
deploy:hello-devspace Applying manifests with kubectl...
deploy:hello-devspace deployment.apps/devspace-example-python-simple created
deploy:hello-devspace Successfully deployed hello-devspace with kubectl
dev:hello-devspace Waiting for pod to become ready...
dev:hello-devspace Selected pod devspace-example-python-simple-devspace-6c5c8b4dfc-5nfkc
dev:hello-devspace ports Port forwarding started on: 3000 -> 80
dev:hello-devspace sync  Sync started on: ./app/ <-> /hello-devspace/app/
dev:hello-devspace sync  Waiting for initial sync to complete
dev:hello-devspace sync  Initial sync completed
dev:hello-devspace term  Opening shell to python-web-server:devspace-example-python-simple-devspace-6c5c8b4dfc-5nfkc (pod:container)
INFO:     Will watch for changes in these directories: ['/hello-devspace']
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
INFO:     Started reloader process [359] using StatReload
INFO:     Started server process [361]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

After DevSpace is done building and pushing the container image, it will deploy our Kubernetes manifest. At this 
point DevSpace does some magic for us! DevSpace will find our deployment that we want to develop against (based on 
what we defined in the `dev` section of the configuration), and automatically scale that deployment down, creating a 
*new* deployment in its place. This new deployment will look *almost* the same as our original, with the important 
exception that DevSpace will have modified the containers entrypoint command.

This new container will simply run a `sleep` command so that it stays running and does not exit. Once the container is 
up and running, DevSpace will automatically connect to it and execute the command we gave it in the `dev` section of 
the config -- in this case that means it will run `uvicorn app.main:app --host 0.0.0.0 --port 80 --reload`.

In addition to "patching" our entrypoint and running our dev command, DevSpace will also have exposed the port(s) 
that we defined. You should now be able to access your application at `http://localhost:3000`.

![Hello DevSpace!](../static/hello-devspace-1.png)

Not too shabby! This is cool, DevSpace gives us a repeatable, simple, IaC-friendly way to define our development 
environment with real Kubernetes clusters ([or virtual ones!](https://github.com/loft-sh/vcluster)), but even cooler 
is that we can now do our development essentially "locally", while having it automatically reflected on the pod 
running in our cluster.

Update the `app/main.py` message dictionary being returned from the `root` function to say something else:

```python
@app.get("/")
async def root():
    return {"message": "Hello, DevSpace!"}

```

As soon as you (or your editor) save the file you should see that uvicorn picks up the changes and reloads the web app:

```shell
WARNING:  StatReload detected changes in 'app/main.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [361]
INFO:     Started server process [364]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Refreshing your browser tab you should see your new message:

![Hello DevSpace!](../static/hello-devspace-2.png)

🔥 Nice! 🔥


## Cleaning Up

Now that you've probably finished adding the really cool feature that you were working on, it's time to clean up. 
DevSpace makes tidying up the resources you deployed a breeze. Simply running `devspace purge` will remove any 
deployment objects deployed via DevSpace:


```python
$ devspace purge
info Using namespace 'python-hello-devspace'
info Using kube context 'loft-vcluster_devspace-dev_devspace-dev_loft-cluster'
dev:hello-devspace Stopping dev hello-devspace
dev:hello-devspace Scaling up Deployment devspace-example-python-simple...
purge:hello-devspace Deleting deployment hello-devspace...
purge:hello-devspace Successfully deleted deployment hello-devspace
```

And with that you've got the basics of DevSpace down. In the other examples we'll focus more on some DevSpace/Python 
specifics, and how you can best use DevSpace when developing in Python!
