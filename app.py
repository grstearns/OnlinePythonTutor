from flask import Flask
from flask import request


app = Flask(__name__)

# url_for('static')


@app.route('/execute', methods=['POST'])
def execute():
	# user_script = request.form.post['user_script']
	# return request

	return 'LEMON CURRY'



@app.route('/')
def hello_world():
    return 'Hello World!'




if __name__ == '__main__':
    app.run()
