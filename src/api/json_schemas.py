register_schema = {
    'type': 'object',
    'properties': {
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'email': {'type': 'string', 'format': 'email'},
        'password': {'type': 'string'}
    },
    'required': ['first_name', 'last_name', 'email', 'password'],
    'additionalProperties': False
}

login_schema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string', 'format': 'email'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password'],
    'additionalProperties': False
}

flights_schema = {
    'type': 'object',
    'properties': {
        'start_destination': {'type': 'string'},
        'end_destination': {'type': 'string'},
        'takeoff_time': {'type': 'string',
                         'pattern': '^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}$',
                         'examples': ["2023-06-12 15:30"]
                         },
        'landing_time': {'type': 'string',
                         'pattern': '^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}$',
                         'examples': ["2023-06-12 17:15"]
                         },
        'price': {'type': 'number'}
    },
    'required': ['start_destination', 'end_destination', 'takeoff_time', 'landing_time', 'price'],
    'additionalProperties': False
}

update_flight_schema = {
    'type': 'object',
    'properties': {
        'start_destination': {'type': 'string'},
        'end_destination': {'type': 'string'},
        'takeoff_time': {'type': 'string',
                         'pattern': '^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}$',
                         'examples': ["2023-06-12 15:30"]
                         },
        'landing_time': {'type': 'string',
                         'pattern': '^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}$',
                         'examples': ["2023-06-12 17:15"]
                         },
        'price': {'type': 'number'}
    },
    'additionalProperties': False
}
