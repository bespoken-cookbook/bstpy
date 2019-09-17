#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
from importlib import import_module, reload
import os
import sys
import traceback
import json
import pkg_resources  # part of setuptools

sys.path.append('.')

__author__ = 'OpenDog'
__description__ = 'A local http server that exposes an AWS lambda.'

version = pkg_resources.require("LambdaServer")[0].version


def main(argv):
    import time
    import getopt

    server_port = 10000
    timezone = 'UTC'

    usage = 'Usage: bstpy <lambda-path> -p <port> -t <timezone>'

    if len(argv) == 0:
        print(usage)
        sys.exit(2)

    lambda_path = argv[0]

    # Don't start with options

    if lambda_path.startswith("-"):
        print(usage)
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv[1:], "hp:t:v", ['help', 'port=', 'timezone=', 'version'])
    except getopt.GetoptError as err:
        print(str(err))
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(usage)
            sys.exit()
        elif opt in ("-p", "--port"):
            try:
                server_port=int(arg)
            except ValueError:
                print("Invalid port: {}".format(server_port))
                print(usage)
                sys.exit(3)
        elif opt in ("-t", "--timezone"):
            timezone = arg
        elif opt in ("-v", "--version"):
            print("Python Lambda Server {}".format(version))
            sys.exit()
        else:
            assert False, "unhandled option"

    os.environ['TZ'] = timezone
    time.tzset()

    if lambda_path == '':
        print("Lambda path is mandatory!")
        print(usage)
        sys.exit()
    else:
        print("Lambda path: {}".format(lambda_path))

    print("Current time is {}".format(time.strftime('%X %x %Z')))

    run(lambda_path, port=server_port)


def run(lambda_path, server_class=HTTPServer, port=10000):
    class LambdaContext:
        def __init__(self, function_name):
            self.function_name = function_name

        @staticmethod
        def get_remaining_time_in_millis():
            return 999999

        function_name = 'your-lambda-function'
        function_version = '2.0-SNAPSHOT'
        invoked_function_arn = 'arn-long-aws-id'
        memory_limit_in_mb = '128'
        aws_request_id = 'aws-request-test-id'
        log_group_name = 'log-group-bst'
        log_stream_name = 'bst-stream'
        identity = None
        client_context = None

    def import_lambda(path):
        try:
            # Parse path into module and function name.
            path = str(path)

            if '/' in path or '\\' in path:
                raise ValueError()

            spath = path.split('.')
            module = '.'.join(spath[:-1])
            function = spath[-1]

            # Import the module and get the function.
            import_module(module)

            # Comes from the cache if we don't reload
            reload(sys.modules[module])

            return getattr(sys.modules[module], function)

        except (AttributeError, TypeError) as e:
            print("\nOops! There was a problem finding your function.\n")
            raise e
        except ImportError:
            print("\nOops! There was problem loading your module. Is the module visible from your PYTHONPATH?\n")
            sys.exit(1)
        except ValueError:
            print("\nOops! It seems you pointed the tool to Python file. This argument must be\n"
                  "a module path, in the form of [module 1].[module 2...n].[function]\n" +
                  "Also make sure the module is seen from your PYTHONPATH.\n")
            sys.exit(1)

    class S(BaseHTTPRequestHandler):
        def _set_headers(self, output_string):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(output_string)))
            self.end_headers()

        def do_POST(self):
            data_string = self.rfile.read(int(self.headers['Content-Length']))

            print("==> {}".format(data_string))

            data = json.loads(data_string)

            # noinspection PyBroadException
            try:
                context = LambdaContext(lambda_path)
                handler = import_lambda(lambda_path)
                r = handler(data, context)
            except Exception as e:
                print("\nOops! There was a problem in your lambda function: {}\n".format(lambda_path))
                print(traceback.format_exc())
                r = {
                    'error': str(e)
                }

            return_value = json.dumps(r, indent=4 * ' ')
            self._set_headers(return_value);

            self.wfile.write(bytes(return_value, encoding='utf8'))
            #self.wfile.close()

            print("<=== {}".format(return_value))

            return

    server_address = ('', port)
    httpd = server_class(server_address, S)
    print("Starting httpd on port " + str(port))
    httpd.serve_forever()

