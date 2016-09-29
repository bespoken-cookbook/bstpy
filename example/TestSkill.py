from __future__ import print_function


def example_handler(event, context):

    # Your awesome skill code goes here

    try:
        session_id = event['session']['sessionId']
    except KeyError as e:
        session_id = 'NO_SESSION'

    memory = context.memory_limit_in_mb

    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'text': 'BST tools are the best!',
                'type': 'PlainText'
            },
            'shouldEndSession': False,
            'reprompt': {
                'outputSpeech': {
                    'text': 'BST tools are the best!',
                    'type': 'PlainText'
                }
            },
            'card': {
                'content': 'BST Python Server',
                'type': 'Simple',
                'title': 'BST Tools'
            }
        },
        'sessionAttributes': {
            'lastSession': session_id,
            'memory': memory
        }
    }
