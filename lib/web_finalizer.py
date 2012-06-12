import demjson
import lib.pg_logger


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
  header = '' # "Content-type: text/plain; charset=iso-8859-1\n\n"
  return header + output_json


def get_log(user_script):
  lib.pg_logger.set_max_executed_lines(2000000)
  return lib.pg_logger.exec_script_str(user_script, web_finalizer)
