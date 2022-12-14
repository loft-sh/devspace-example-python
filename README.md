![DevSpace](./static/devspace.png)

DevSpace Example Python
=======================

👋 Welcome to the [DevSpace](https://github.com/loft-sh/devspace) Python example repo!

This repo is intended to help you get started with DevSpace generally, with Python specific examples/context.

In here you'll find four different examples, from the most basic "hello world", to more advanced setups including 
more "difficult" dependencies (things with C/other dependencies), and debugging examples. Check them out below:

1. [Hello, DevSpace!](./01-simple) -- Start here if you are just checking out DevSpace for the first time
2. [FastAPI and Tortoise Project](./02-fastapi-tortoise) -- A bit more "real life" of an example using FastAPI, 
   Tortoise ORM, and a PostgreSQL database, oh, and Star Wars!
3. [🐛 With Debugging](./03-debugging) -- Throw in some debuggers for good measure!


## Other Info!

Working with DevSpace in your Python (or any language) project? Here are a few other good tidbits to know!

- It's a good idea to add `*/.devspace` to your `.gitingore` -- there is no good reason to be including the DevSpace 
  logs/cache in your git repository!
- Really into the Visual Studio Code Remote SSH Extension? Check out the docs about it [here](https://devspace.sh/docs/ide-integration/visual-studio-code)
- Keep [this page](https://devspace.sh/docs/configuration/reference) handy -- it's always nice to have the full 
  DevSpace config reference at the ready!
- If you, like us, commonly use the `ignoreContextChanges` image rebuild strategy, and you want to rebuild your 
  image for whatever reason, just know you can tack on the `-b` flag to your normal `devspace -dev` to rebuild your 
  images; easy to forget, but quite handy!
- Join us on Slack [here](https://slack.loft.sh/) if you're into that sort of thing!
