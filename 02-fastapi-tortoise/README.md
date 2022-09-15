# A Simple Project!

Perhaps simple is the wrong word! The actual Python code in this project is quite simple, but there are a lot more 
moving pieces happening here than in the "hello-devspace" example. The goal of this example is to showcase DevSpace 
in a more "real-life" like example. It is still an example, so it is a bit contrived, but hopefully it helps you see 
how you can use DevSpace in your workflow!


## What Are We Doing Here?

In this example, we are still assuming you are a Python developer working on a FastAPI application, this time, 
however, we are actually using FastAPI to build... an API! The API is a very simple API that sits in front of a 
PostgreSQL database that contains information about Planets and People from the Star Wars universe<sup>1</sup>.

Just like the previous example, we will be showcasing how we can use DevSpace to not only deploy, but to do 
development against our application running in a Kubernetes cluster.

<sup>1</sup> Thanks to @alexisrolland for compiling data from swapi.co and now swapi.dev into a single simple sql 
seed file [here](https://github.com/alexisrolland/star-wars-data), and to @Juriy for the work on swapi.dev [here](https://github.com/Juriy/swapi)


## The Set-Up

As mentioned, we will be using FastAPI once again, but this time it will be joined by 
[Tortoise ORM](https://github.com/tortoise/tortoise-orm) which we will use as our ORM of choice here. The example 
here is quite similar to the Tortoise FastAPI example that you can find [here](https://github.com/tortoise/tortoise-orm/tree/develop/examples/fastapi).

This time around we have a bit more *stuff* going on though! We've got a `database` and a `backend` directory here. 
The `database` directory contains a Dockerfile to build and seed our Postgres database (yes, yes, we are running 
Postgres in a container it isn't a good idea, but this is just a demo!), and the `backend` directory contains our 
Python API package, as well as some Dockerfiles for building it.

Since we've got a bit more going on now, let's jump straight into getting this built and deployed in Kubernetes so 
we can get to developing things!


## Containerizing

The biggest difference between this and the previous example with respect to containerizing our app is simply that 
we have *two* containers -- one for the API/backend and one for the database. The only thing we need to do to make 
this work is to make sure we tell DevSpace about each of our containers in the `images` section:

```yaml
images:
  database:
    image: ${DATABASE_IMAGE}
    context: ./database
    dockerfile: ./database/Dockerfile
    rebuildStrategy: ignoreContextChanges
  backend:
    image: ${BACKEND_IMAGE}
    context: ./backend
    dockerfile: ./backend/Dockerfile
    rebuildStrategy: ignoreContextChanges
```

Note that we now have *two* image name variables -- one for each image. Other than that, we just tell DevSpace what 
the build context is for each image and where the Dockerfile lives, and we are good to go!

If you are curious about the Dockerfiles/images themselves -- there isn't too much going on here!

The Postgres container simply copies in the `init.sh` and `seed.sql` files into the `postgres:14.5-bullseye` image, 
and sets some Postgres environment variables.

The backend image is a very simple multi-stage build, installing some basic dependencies in the base image, and then 
copying our requirements file (`pyproject.toml` in this case) and our application code over and running uvicorn like 
before.

Your projects may have one or many containers -- whatever the scenario, DevSpace has you covered! You can add as 
many images as you need, and you can even add "dev" versions of those containers, something we will cover in the 
next example!


## What's Next?

Like the "hello-devspace" example, this example has a few simple Kubernetes manifest files to actually deploy our 
application into a cluster. [This manifest](./manifests/deployment.yaml) contains a single deployment containing two 
containers, one for the database and one for the API. Additionally, we have a simple service and ingress to expose 
the API -- more like what you may have in real life. 

Just like before we can now use DevSpace to not only deploy our app, but also to develop against it in a live cluster.

⚡ Interested in pushing images to somewhere other than the DevSpace managed repository in your cluster? Read on, 
otherwise skip to the next section! ⚡

If you want to build and push your images to your own container registry you will need to do a few extra things. 
Firstly, of course you will need to know the URL of your registry! Next, you will need to update the actual 
Kubernetes manifest where you specify the images for our containers, as well as the `devspace.yaml` file to tell 
DevSpace where to push the images we build to. You can run `make set_registry` in this directory to quickly take 
care of this for you -- this make directive will prompt you for the registry URL, and it will update the two files.

In your normal workflow you could obviously just set the registry/image names however you like -- this extra step is 
just to make it easy for you to try out this example!


# Enter DevSpace

The only changes to the `devspace.yaml` from the previous example are:

1. Additional image variable for the database image
2. Additional image definition for the database image
3. A few extra manifests for our service and ingress configuration
4. Slightly modified sync and command in our `dev` section
5. Profiles -- which we'll cover a bit further down in this example!

If you are looking for a more detailed explanation, check out the previous example "hello-devspace" 
[here](../hello-devspace/README.md/#Enter-DevSpace) for some more detail!


## Enough Already, Let's Do The Things!

It's time to get this thing running! `devspace dev` will go ahead and build and deploy our application:

```shell
$ devspace dev
info Using namespace 'python-simple-project'
info Using kube context 'loft-vcluster_devspace-dev_devspace-dev_loft-cluster'
build:backend Ensuring image pull secret for registry: 172.31.254.11...
build:backend Building image '172.31.254.11/python-simple-project-backend:cqSddhw' with engine 'docker'
build:backend Authenticating (172.31.254.11)...
build:database Ensuring image pull secret for registry: 172.31.254.11...
build:database Building image '172.31.254.11/python-simple-project-db:aCqdBbq' with engine 'docker'
build:database Authenticating (172.31.254.11)...
build:backend Authentication successful (172.31.254.11)
build:database Authentication successful (172.31.254.11)
build:database Sending build context to Docker daemon  30.72kB
build:database Step 1/7 : FROM postgres:14.5-bullseye
Sending build context to Docker daemon  36.15MBaemon  557.1kB
build:backend Step 1/10 : FROM python:3.10.7-slim-bullseye AS base
build:backend  ---> d7971c18b18e
build:backend Step 2/10 : RUN set -x && apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y     ca-certificates wget jq &&     rm -rf /var/lib/apt/lists/*
build:backend  ---> Running in ef25c6b04c77
build:backend + apt-get update -y
build:database 14.5-bullseye: Pulling from library/postgres

<< SNIP: BUILDING AND PUSHING! >>

build:database aCqdBbq: digest: sha256:c7a0f96015fde2d2b6188d950c54e33f4283649ad06d40013c3c79e712aded22 size: 3661
build:database Image pushed to registry (172.31.254.11)
build:database Done processing image '172.31.254.11/python-simple-project-db'
build:database Done building image 172.31.254.11/python-simple-project-db:aCqdBbq (database)
deploy:simple-project Applying manifests with kubectl...
deploy:simple-project deployment.apps/devspace-example-python-simple created
deploy:simple-project ingress.networking.k8s.io/devspace-example-python-simple-ingress created
deploy:simple-project service/devspace-example-python-simple created
deploy:simple-project Successfully deployed simple-project with kubectl
dev:simple-project Waiting for pod to become ready...
dev:simple-project Selected pod devspace-example-python-simple-devspace-647ff8d96-qps6x
dev:simple-project ports Port forwarding started on: 3000 -> 80
dev:simple-project sync  Sync started on: ./backend/devspace_starwars_api/ <-> /simple-project/devspace_starwars_api/
dev:simple-project sync  Waiting for initial sync to complete
dev:simple-project sync  Initial sync completed
dev:simple-project term  Opening shell to python-web-server:devspace-example-python-simple-devspace-647ff8d96-qps6x (pod:container)
INFO:     Will watch for changes in these directories: ['/simple-project']
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
INFO:     Started reloader process [356] using StatReload
INFO:     Started server process [358]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

At this point DevSpace will have built our images (both backend and the database), and deployed them to Kubernetes. 
Not only that, but DevSpace (because we are running in "dev mode") will also have exposed our API/backend container 
port 80 to our localhost on port 3000. 

We can confirm that our API is up and running and connecting to the database by curl'ing to get the person at ID 1 
from our API:

```shell
$ curl "http://localhost:3000/people/1"
{"id":1,"name":"Luke Skywalker","height":172,"mass":77,"hair_color":"blond","skin_color":"fair","eye_color":"blue","birth_year":"19BBY","gender":"male","planet_id":1,"created_date":"2014-12-09T13:50:51.644000+00:00","updated_date":"2014-12-20T21:17:56.891000+00:00","url":"https://swapi.co/api/people/1/"}%
```

Luke Skywalker? Never heard of him 🤷

Once again, the fact that DevSpace can seamlessly deploy our application is really nice, but the real value is in 
the way DevSpace helps us to *develop* our application. In this case, DevSpace *plus* uvicorn makes our life *even 
easier*! DevSpace is already setup to automatically sync our backend code to the container, and uvicorn is running 
with the `--reload` flag causing it to auto-reload when it detects changes to the application. 

Our Star Wars API is already pretty much perfect, *but* it is missing two very important endpoints! The `iloveyou` 
and the `iknow` endpoints. If you are unfamiliar, [here](https://www.youtube.com/watch?v=kdlRmWd_R7A) is the scene 😄

The `iloveyou` endpoint should be return the Leia Organa person (id=5) and the `iknow` endpoint should return the 
Han Solo person (id=14).

If you don't want to play around to find out how to get this setup, you can paste the following into the 
`devspace_starwwars_api/routes/people.py` file:

<details> 
  <summary>Spoiler</summary>

```python
@router.get("/iloveyou", response_model=Person_Pydantic)
async def iloveyou():
    return await Person_Pydantic.from_queryset_single(Person.get(id=5))


@router.get("/iknow", response_model=Person_Pydantic)
async def iknow():
    return await Person_Pydantic.from_queryset_single(Person.get(id=14))  
```

</details>

Because of the magic of DevSpace syncing our changes to the container, and uvicorn auto-reloading itself when it 
sees the change we should now be able to query these super critical endpoints:

```shell
$ curl "http://localhost:3000/iloveyou"
{"id":5,"name":"Leia Organa","height":150,"mass":49,"hair_color":"brown","skin_color":"light","eye_color":"brown","birth_year":"19BBY","gender":"female","planet_id":2,"created_date":"2014-12-10T15:20:09.791000+00:00","updated_date":"2014-12-20T21:17:50.315000+00:00","url":"https://swapi.co/api/people/5/"}
$ curl "http://localhost:3000/iknow"
{"id":14,"name":"Han Solo","height":180,"mass":80,"hair_color":"brown","skin_color":"fair","eye_color":"brown","birth_year":"29BBY","gender":"male","planet_id":22,"created_date":"2014-12-10T16:49:14.582000+00:00","updated_date":"2014-12-20T21:17:50.334000+00:00","url":"https://swapi.co/api/people/14/"}
```

Once again, *if* your application/application tooling does *not* have this auto-reload capability like with uvicorn, 
DevSpace still has you covered! We can modify our `sync` directive in the `devspace.yaml` config file to look 
something like:

```yaml
dev:
  simple-project:
    imageSelector: ${BACKEND_IMAGE}
    ports:
      - port: 3000:80
    sync:
      - path: ./backend/devspace_starwars_api/:/simple-project/devspace_starwars_api/
        onUpload:
          exec:
            - command: /simple-project/start-or-restart-uvicorn.sh

    command: ["sleep"]
    args: ["1000000000"]
```

You can see that not *much* has changed, but we do have a few differences here! Firstly, we are using the `onUpload.
exec` option here to execute a command `/simple-project/start-or-restart-uvicorn.sh` each time DevSpace syncs 
things to our container. This shell script is in the backend directory, you can check it out
 [here](backend/start-or-restart-uvicorn.sh); all it is doing is killing uvicorn if its running, and re-launching it 
with our normal settings.

The other thing we changed here is setting the containers entrypoint to `sleep 1000000000` -- we don't want our 
entrypoint being what it is in the Dockerfile, because each time we kill the uvicorn process we would be killing pid 
1 -- and thus killing the container. So, we'll just have the container sleep forever, or until we have DevSpace 
clean it up. 

With all that in place, you can run `devspace dev` (or `devspace purge && devspace dev` if you want to tidy things 
up first). Once the initial sync is complete -- modify some Python files and you should see DevSpace printing 
out logs indicating files are being synced/re-synced. You'll probably have some output similar to this:

```shell
dev:simple-project Waiting for pod to become ready...
dev:simple-project Selected pod devspace-example-python-simple-devspace-7b66f6f945-xhkw9
dev:simple-project ports Port forwarding started on: 3000 -> 80
dev:simple-project sync  Inject devspacehelper...
dev:simple-project sync  Start syncing
dev:simple-project sync  Sync started on: ./backend/devspace_starwars_api/ <-> /simple-project/devspace_starwars_api/
dev:simple-project sync  Waiting for initial sync to complete
dev:simple-project sync  Downstream - Initial sync completed
dev:simple-project sync  Upstream - Upload 8 create change(s) (Uncompressed ~5.92 KB)
dev:simple-project sync  Upstream - Successfully processed 8 change(s)
dev:simple-project sync  Upstream - Initial sync completed
dev:simple-project sync  Initial sync completed
dev:simple-project sync  Upstream - Upload File 'routes/people.py'
dev:simple-project sync  Upstream - Upload 1 create change(s) (Uncompressed ~1.58 KB)
dev:simple-project sync  Upstream - Successfully processed 1 change(s)
dev:simple-project sync  Upstream - Upload File 'routes/people.py'
dev:simple-project sync  Upstream - Upload 1 create change(s) (Uncompressed ~1.60 KB)
dev:simple-project sync  Upstream - Successfully processed 1 change(s)
dev:simple-project ports Restarting because: lost connection to pod
```

Once again, note that with uvicorn we can simply have it auto reload when it notices file changes, but it is very 
handy to know that DevSpace can also help you achieve the same result even if your tooling does not support this!


# Profiles

Another very handy feature of DevSpace is the ability to define *profiles* -- profiles are more or less what they 
sound like: profiles (or settings) for different use cases. A common example would be to have a profile for "dev" 
and another profile for "production" -- or better, to have only a profile for "dev" and to have the "normal" 
(deployment/images/etc.) settings all apply to production. Then, when you are doing development work, you simply 
"enable" the dev profile. That's exactly what we'll cover now!

In this example we have *three* manifests in our manifests' directory, and as such, we have configured our `devspace.
yaml` configuration to deploy all three of these manifests under our `deployment` config. As you have seen, when 
working with DevSpace for local development, we really don't have a need for a service and ingress, we can simply 
let DevSpace expose our container to our local machine. Because there is no need for the service and ingress, 
wouldn't it just be better to *not* bother deploying them during development?

We can do just that with a simple configuration:

```yaml
profiles:
  - name: dev
    patches:
      # remove the service and ingress from the deployment manifests for the `simple-project` deployment
      - op: remove
        path: deployments.simple-project.kubectl.manifests[1]
      - op: remove
        path: deployments.simple-project.kubectl.manifests[2]
```

Under the `profiles` heading of our configuration we can list out as many profiles as we'd like -- in this example 
we simply have the one, named "dev". Under this profile we specify any *patches* that we would like to apply to our 
configuration when running under this profile. In our case, we'll *remove* the second and third elements from the 
deployment manifest list.

Profiles can be used with most DevSpace commands by simply passing the `-p PROFILENAME` argument. Perhaps the 
easiest way to demonstrate this is to use the DevSpace `print` command -- this command prints (who would have 
thought?) out the currently applicable DevSpace configuration.

Running `devspace print` with no argument should result in an output similar to the following (leading and trailing 
output snipped to keep this brief):

```shell
< SNIP >
deployments:
    simple-project:
        kubectl:
            manifests:
                - manifests/deployment.yaml
                - manifests/ingress.yaml
                - manifests/svc.yaml
< SNIP >
```

We can clearly see the three manifests for the deployment, service, and ingress. Run the command again, but this 
time passing the `-p dev` flag to indicate you want the "dev" profile applied:

```shell
< SNIP >
deployments:
    simple-project:
        kubectl:
            manifests:
                - manifests/deployment.yaml
< SNIP >
```

Nice! Just like that we have removed the unnecessary manifests from our dev setup. You can run the same `devspace 
dev` command that we have been demonstrating with the `-p dev` flag as well -- now when DevSpace spins up the dev 
environment it will skip those manifests. Pretty snazzy!

You can read all about profiles [here](https://devspace.sh/docs/configuration/profiles/) in the docs!


## A Note on Editable Installs and Pyproject.toml Only Packages (like this example!)

This example project was setup with *only* a `pyproject.toml` (as in no setup.py, no requirements*.txt, and even no 
setup.cfg) -- the reason for this was just to try something else out, and also it seems to be more in line with how 
much of the Python packaging community is moving.

There is one distinct downside (as of the time of writing - September 2022), editable installations... have some 
issues for static analysis tools. *If* you are interested in installing the backend application locally on your 
machine as an editable install, and you are hoping for your normal PyCharm/VSCode intelisense goodness, you 
*probably* want to do one of two things:

1. Pin setuptools <=63.4.3 in the build-system settings in the `pyproject.toml` OR
2. Install using the `pip` editable compatible mode like: `install -e . --config-settings editable_mode=compat`

A few interesting issues/threads on this if you are interested:

- https://github.com/pypa/setuptools/issues/3548
- https://github.com/pypa/setuptools/issues/3557
- https://github.com/microsoft/pyright/issues/3880
- https://github.com/microsoft/pylance-release/issues/3265

Note that editable installations *do* work -- however static analysis may have some issues!
