from flask import Flask, jsonify
from flasgger import Swagger, SwaggerView, Schema, fields
from controller.chat_controller import ChatController
from vyper import v

v.set_default('server.port', 5009)

v.set_config_type('yaml')  # REQUIRED if the config file does not have the extension in the name
v.set_config_name('config')  # name of config file (without extension)
v.add_config_path('/etc/bard-rest-api/')  # path to look for the config file in
v.add_config_path('$HOME/.bard-rest-api')  # call multiple times to add many search paths
v.add_config_path('.')  # optionally look for config in the working directory

v.read_in_config()  # Find and read the config file

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Bard Rest API',
    'uiversion': 3,
    'specs': [
        {
            'endpoint': 'bard-rest-api',
            'route': '/bard-rest-api.json',
            'rule_filter': lambda rule: True,  # all in
            'model_filter': lambda tag: True,  # all in
        }
    ],
    'specs_route': '/api/docs/'
}
swagger = Swagger(app)

app.add_url_rule('/chat', view_func=ChatController.as_view('chat'), methods=['POST'])

app.run(debug=True, port=v.get_int('server.port'))
