from http import HTTPStatus

responses={
    'bad_request': {
        HTTPStatus.BAD_REQUEST: {
            'description': 'Invalid request.',
            'content': {
                'application/json': {
                    'example': {'detail': 'Invalid data type.'}
                }
            }
        }
    },
    'internal_server_error': {
        HTTPStatus.INTERNAL_SERVER_ERROR: {
            'description': 'Internal server error.'
        }
    },
    'unauthorized': {
        HTTPStatus.UNAUTHORIZED: {
            'description': 'Invalid credentials.',
            'content': {
                'application/json': {
                    'example': {'detail': 'Invalid credentials.'}
                }
            }
        }
    },
    'not_found': {
        HTTPStatus.NOT_FOUND: {
            'description': 'Resource not found.',
            'content': {
                'application/json': {
                    'example': {'detail': 'Resource not found.'}
                }
            }
        }
    },
    'forbidden': {
        HTTPStatus.FORBIDDEN: {
            'description': 'User not allowed to acces/use this resource.',
            'content': {
                'application/json': {
                    'example': {'detail': 'User not allowed to acces/use this resource.'}
                }
            }
        }
    },
    'unprocessable_entity': {
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            'description': 'Unprocessable entiry: Invalid data.',
            'content': {
                'application/json': {
                    'example': {'detail': 'Invalid data passed.'}
                }
            }
        }
    }
}