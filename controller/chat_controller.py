from flasgger import SwaggerView, swag_from
from flask import request
from flask_restful import Resource

from model.message import Message
from schema.message_schema import MessageSchema


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
        response_message.setText(f'Hai scritto: {message.getText()}')

        response_data = schema.dump(response_message)

        return response_data, 200