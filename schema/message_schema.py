from flasgger import Swagger, SwaggerView, Schema, fields
from marshmallow import post_load

from model.message import Message


class MessageSchema(Schema):
    text = fields.Str(required=True, description='Content of the message')

    @post_load
    def make_message(self, data, **kwargs):
        message = Message()
        message.setText(data['text'])
        return message