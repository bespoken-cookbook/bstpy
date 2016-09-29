#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from importlib import import_module
import sys
import traceback
import simplejson

sys.path.append('.')

__author__ = 'OpenDog'
__description__ = 'A local http server that exposes an AWS lambda.'


def main():
    from sys import argv

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


    class LambdaContext:
        def __init__(self, lambdapath):
            self.function_name = lambdapath

        @staticmethod
        def get_remaining_time_in_millis():
            return 999999;

        function_name = 'your-lambda-function'
        function_version = '2.0-SNAPSHOT'
        invoked_function_arn = 'arn-long-aws-id'
        memory_limit_in_mb = '128'
        aws_request_id = 'aws-request-test-id'
        log_group_name = 'log-group-bst'
        log_stream_name = 'bst-stream'
        identity = None
        client_context = None


    class S(BaseHTTPRequestHandler):
        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

        def do_POST(self):
            self._set_headers()

            data_string = self.rfile.read(int(self.headers['Content-Length']))

            print "===> {}".format(data_string)

            data = simplejson.loads(data_string)

            # noinspection PyBroadException
            try:
                r = lfunc(data, lambdaContext)
                print("R: " + simplejson.dumps(r))
            except Exception as e:
                print("\nOops! There was a problem in your lambda function: {}\n".format(lambdaPath))
                print(traceback.format_exc())
                r = {
                    'error': str(e)
                }

            self.wfile.write(simplejson.dumps(r))
            self.wfile.close()

            print "<=== {}".format(r)

            return


    def run(server_class=HTTPServer, handler_class=S, port=8000):
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print 'Starting httpd on port ' + str(port)
        httpd.serve_forever()

    if 2 <= len(argv) <= 3:
        lambdaPath = argv[1]
        lambdaContext = LambdaContext(lambdaPath)
        lfunc = import_lambda(lambdaPath)

        if len(argv) == 3:
            run(port=int(argv[2]))
        else:
            run()
    else:
        print 'Usage lambda-path [http-port]'
