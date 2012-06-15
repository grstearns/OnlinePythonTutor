import os
from flask import Flask
from flask import request
from flask import render_template

import lib.web_finalizer

app = Flask(__name__)


@app.route('/execute', methods=['POST'])
def execute():
  user_script = request.form['user_script']
  log = lib.web_finalizer.get_log(user_script)
  return log



@app.route('/')
def root():
  return render_template('tutor.html')



if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
  # app.debug = True