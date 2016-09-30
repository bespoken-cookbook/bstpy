#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from importlib import import_module
import sys
import traceback
import simplejson
import pkg_resources  # part of setuptools

sys.path.append('.')

__author__ = 'OpenDog'
__description__ = 'A local http server that exposes an AWS lambda.'

version = pkg_resources.require("LambdaServer")[0].version


def main():
    from sys import argv

    if 2 <= len(argv) <= 3:
        if len(argv) == 3:
            run(argv[1], port=int(argv[2]))
        else:
            run(argv[1])
    else:
        print("Python Lambda Server {}".format(version))
        print("Usage lambda-path [http-port]")


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
        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

        def do_POST(self):
            self._set_headers()

            data_string = self.rfile.read(int(self.headers['Content-Length']))

            print("===> {}".format(data_string))

            data = simplejson.loads(data_string)

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

            return_value = simplejson.dumps(r, indent=4 * ' ')

            self.wfile.write(return_value)
            self.wfile.close()

            print("<=== {}".format(return_value))

            return

    server_address = ('', port)
    httpd = server_class(server_address, S)
    print("Python Lambda Server {}".format(version))
    print("Starting httpd on port " + str(port))
    httpd.serve_forever()

