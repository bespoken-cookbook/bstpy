# bstpy

**Python AWS Lambda Server**

## Recommended Uses
Use `bstpy` to expose an AWS Lambda as an http endpoint locally. It provides a Python "harness" that you can use to wrap your
function and run/analyze it.

  - Development
    - Run your lambda functions instantly locally, without packaging and sending to AWS.
    - Shorten your feedback loop on lambda executions.

  - Testing
    - Use it with other bespoken tools, like the bst Alexa emulator or bst proxy, to instantly test your Alexa skill.

## Features
Present:
  - Run an AWS-compatible lambda function as an http endpoint.
  - Automatically reloads your skill so you can see your changes without restarting it.


Planned:
  - accessing AWS resources
  - picking up any libraries present in ``./lib`` directory of the project
  - context from file

## Installation
1. `git clone` [the bstpy repo](https://github.com/bespoken/bstpy.git)
2. Install it with `pip install -e bstpy` (you might need to sudo this command if you're using your system Python instead of a virtualenv or similar)


## Usage

```
$ bstpy --help
Usage: bstpy -l <lambda-path> -p <port> -t <timezone>
```

The only mandatory paramater is -l (--lambda) to specify the lambda path. 

Use -p (--port) to listen on another port. 

Use -t (--timezone) to specify the timezone you want to run on. The default is UTC. 

```
$ bstpy -l foo -t US/Eastern
```

Yo can also use -h (--help) for help and -v (--version) for version.

## Quick Start

### Try the example lambda in the project

From the example folder, run:
`bstpy TestSkill.example_handler`

You should see output similar to the following:
```
Lambda path: foo
Current time is 14:04:42 10/17/16 UTC
Starting httpd on port 10000
```

Note: This is the simplest way to call a handler in a Python file. 
Alternatively you can specify a module and a function like this: Module1[.Module2][.Module3].handler_function,
just make sure the module is seen from your Python path. The script will add your current folder (.) to the path (your welcome).

From another terminal window in the project root folder, run:
`./test.sh`

Note: You need to have curl installed for this. Of course you can use your own favorites, like Postman.

#### What's happening?

In this example, `bstpy`:
  1. Loads the `example_handler` function from the `TestSkill` module (file in this case).
  1. Starts a simple http server on port 8000 and starts listening for POST request with json bodies (events)
  1. Curl will post the content of the event.json file
  1. LambdaServer calls the the lambda handler
  1. Returns the resulting json
