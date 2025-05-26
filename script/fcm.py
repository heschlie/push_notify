# Klipper extension for ntfy notification
#
# Copyright (C) 2023  Rudy Dajoh <prd0000@gmail.com>
#
# This file may be distributed under the terms of the GNU AGPLv3 license.

import requests

HELP = '''
Google FCM based push notification for Klipper.
USAGE: FCM_NOTIFY MSG="message" [TITLE="title"]
TITLE parameter is optional
'''


class FCM:
    def __init__(self, config) -> None:
        self.name = config.get_name().split()[-1]
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')

        # configuration
        self.topic = config.get('topic', 'printer')
        self.timeout = config.get('timeout', 10)
        self.server = config.get('server', 'ntfy.sh')
        self.serverport = config.get('serverport', '443')

        # Register commands
        self.gcode.register_command(
            'FCM_NOTIFY',
            self.cmd_FCM_NOTIFY,
            desc=self.cmd_FCM_NOTIFY_help)

    cmd_FCM_NOTIFY_help = 'Sending message to FCM server'

    def cmd_FCM_NOTIFY(self, params):
        message = params.get('MSG', '')
        title = params.get('TITLE', '')

        if message == '':
            self.gcode.respond_info(HELP)
            return

        # send message
        self.gcode.respond_info(f'Sending FCM message: {title} - {message}')
        try:
            r = requests.post(
                f'https://{self.server}:{self.serverport}/{self.topic}',
                data=message,
                headers={
                    'Title': title,
                    'Priority': '3',
                }
            )

            message = r.json()
            if r.ok:
                self.gcode.respond_info(f'{r.status_code} {r.reason}: {message}')
            else:
                raise self.gcode.error(f'{r.status_code} {r.reason}: {message}')
        except Exception as e:
            raise self.gcode.error(f'Error: {e}')


def load_config(config):
    return FCM(config)
