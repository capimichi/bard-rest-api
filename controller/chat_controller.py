import json

from flasgger import SwaggerView, swag_from
from flask import request
from flask_restful import Resource

from model.message import Message
from schema.message_schema import MessageSchema
from vyper import v

import requests
from bardapi import Bard, SESSION_HEADERS


class ChatController(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'Success',
                'schema': MessageSchema  # Esempio di schema di risposta
            },
            400: {
                'description': 'Bad Request'
            }
        },
        'parameters': [
            {
                'name': 'message',
                'in': 'body',
                'required': True,
                'schema': MessageSchema  # Esempio di schema del corpo della richiesta
            }
        ]
    })
    def post(self):
        """
        Questo endpoint permette di inviare un messaggio
        ---
        tags:
            - Chat
        """
        # Leggi il messaggio inviato nel body della richiesta
        data = request.get_json()

        token = v.get_string('bard.1PSID')
        tokenCc = v.get_string('bard.1PSIDCC')
        tokenTs = v.get_string('bard.1PSIDTS')

        session = requests.Session()
        session.cookies.set("__Secure-1PSID", token)
        session.cookies.set("__Secure-1PSIDCC", tokenCc)
        session.cookies.set("__Secure-1PSIDTS", tokenTs)
        session.headers = SESSION_HEADERS

        bard = Bard(token=token, session=session)

        # create message from schema and data
        schema = MessageSchema()

        # Validazione del messaggio utilizzando Marshmallow
        message_schema = MessageSchema()
        errors = message_schema.validate(data)
        if errors:
            return {'error': 'Validazione fallita', 'errors': errors}, 400

        message = schema.load(data)
        # Esempio di elaborazione del messaggio

        response_message = Message()

        response_data = bard.get_answer(message.getText())

        #response_data = json.loads(response_json)
        response_text = response_data['content']
        response_message.setText(response_text)

        response_data = schema.dump(response_message)

        return response_data, 200