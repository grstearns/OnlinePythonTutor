from flask import Flask
from flask import request
from flask import render_template

import pg_logger
import demjson



app = Flask(__name__)

# url_for('static')


@app.route('/execute', methods=['POST'])
def execute():
  user_script = request.form['user_script']
  pg_logger.set_max_executed_lines(2000000)
  log = pg_logger.exec_script_str(user_script, web_finalizer)
  print "\n"*10
  print "debug info"
  print log
  print user_script
  return log


@app.route('/tutor')
def tutor():
  return render_template('tutor.html')


@app.route('/')
def root():
  return render_template('index.html')


LOG_QUERIES = False # don't do logging for now



def web_finalizer(output_lst):
  # use compactly=False to produce human-readable JSON,
  # except at the expense of being a LARGER download
  output_json = demjson.encode(output_lst, compactly=True)

  # query logging is optional
  if LOG_QUERIES:
    # just to be paranoid, don't croak the whole program just
    # because there's some error in logging it to the database
    try:
      # log queries into sqlite database:
      had_error = False
      # (note that the CSAIL 'www' user needs to have write permissions in
      #  this directory for logging to work properly)
      if len(output_lst):
        evt = output_lst[-1]['event']
        if evt == 'exception' or evt == 'uncaught_exception':
          had_error = True

      (con, cur) = db_common.db_connect()
      cur.execute("INSERT INTO query_log VALUES (NULL, ?, ?, ?, ?, ?)",
                  (int(time.time()),
                   os.environ.get("REMOTE_ADDR", "N/A"),
                   os.environ.get("HTTP_USER_AGENT", "N/A"),
                   user_script,
                   had_error))
      con.commit()
      cur.close()
    except:
      # haha this is bad form, but silently fail on error :)
      pass
  
  # Crucial first line to make sure that Apache serves this data
  # correctly - DON'T FORGET THE EXTRA NEWLINES!!!:
  # print "Content-type: text/plain; charset=iso-8859-1\n\n"
  return output_json



# form = cgi.FieldStorage()
# user_script = form['user_script'].value
# if 'max_instructions' in form:




if __name__ == '__main__':
    app.debug = True
    app.run()



