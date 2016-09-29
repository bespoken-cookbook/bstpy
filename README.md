# LambdaServer

**Python AWS Lambda Server**

## Recommended Uses
Use `LambdaServer` to expose an AWS Lambda as an http endpoint locally. It provides a Python "harness" that you can use to wrap your
function and run/analyze it.

  - Development
    - Run your lambda functions instantly locally, without packaging and sending to AWS.
    - Shorten your feedback loop on lambda executions.

  - Testing
    - Use with the BST Alexa emulator to instantly test your Alexa skill

## Features
Present:
  - Run an AWS-compatible lambda function as an http endpoint


Planned:
  - accessing AWS resources (with user-supplied Lambda execution IAM Role)
  - picking up any libraries present in ``./lib`` directory of the project
  - context from file

## Installation
1. `git clone` [the LambdaServer repo](https://github.com/bespoken/LambdaServer.git)
2. Install it with `pip install -e LambdaServer` (you might need to sudo this command if you're using your system Python instead of a virtualenv or similar)


## Usage

```
usage: lambda-path [http-port]

positional argument:
  lambda-path           An import path to your function, as you would give it
                        to AWS: `module.function`.

optional arguments:
  http-port             The port you want to expose the lambda. The default is 8000.
```

## Quick Start

### Try the example lambda in the project

From the example folder, run:
`LambdaServer TestSkill.example_handler`

You should see output similar to the following:
```
Starting httpd on port 8000
```

Note: This is the simplest way to call a handler in a Python file. 
Alternatively you can specify a module and a function like this: Module1[.Module2][.Module3].handler_function,
just make sure it is seen from your Python path. The script will add your current folder (.) to the path.

From another terminal window in the project root folder, run:
`./test.sh`

Note: You need to have curl installed for this.

#### What's happening?

In this example, `LambdaServer`:
  1. Loads the `example_handler` function from the `TestSkill` module (file in this case).
  1. Starts a simple http server on port 8000 and starts listening for POST request with json bodies (events)
  1. Curl will post the content of the event.json file
  1. LambdaServer calls the the lambda handler
  1. Returns the resulting json
