from flask import Flask, send_from_directory, render_template, request
from flask_cors import CORS, cross_origin

from MathService import MathService
from dto import GraphsDto, FloatingFreqDto


class Application:
    app = Flask(__name__, template_folder='ui/', static_folder='ui/static/')
    cors = CORS(app)

    def __init__(self, math_service):
        self.math_service = math_service
        self.__static_init(self)

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)

    @staticmethod
    def __process_json(json_, class_):
        kwargs = dict()
        for k in class_.__annotations__:
            if k in json_:
                kwargs[k] = json_[k]
        return class_(**kwargs)

    @staticmethod
    def __static_init(instance):

        @instance.app.route('/')
        def index():
            return render_template('index.html')

        @instance.app.route('/js/<path:path>')
        def send_js(path):
            return send_from_directory('js', path)

        @instance.app.route('/img/<path:path>')
        def send_img(path):
            return send_from_directory('img', path)

        @instance.app.route('/css/<path:path>')
        def send_css(path):
            return send_from_directory('css', path)

        @instance.app.route('/tmp/<path:path>')
        def send_tmp(path):
            return send_from_directory('tmp', path)

        @instance.app.route('/graphs/', methods=['POST'])
        @cross_origin()
        def graphs():
            try:
                file = request.files['file']
                transform_type = request.form['transformType']
                return instance.math_service.create_graphs(GraphsDto(file, transform_type)).to_json()
            except Exception as e:
                return e.message, 400

        @instance.app.route('/freq/', methods=['POST'])
        def freq():
            try:
                values = request.json['values']
                max_freq = request.form['maxFreq']
                return instance.math_service.create_graphs(FloatingFreqDto(values, max_freq)).to_json()
            except Exception as e:
                return e.message, 400


app = Application(MathService())
runtime_application = app.app

if __name__ == '__main__':
    app.run(debug=True)
