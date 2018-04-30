from flask import  request
from flask_restful import Resource, Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import pickle
import cv2
import sys
import datetime
import time
import  threading
from threading import Timer
from flask import Flask, abort


#validation args
arg_n =int(sys.argv[1])
arg_m =int(sys.argv[2])
try:
   val = arg_n
   if (val == 0):
       sys.exit("Error message arg num 1: must be bigger than 0-quitting")
       quit()  # quit at this point
except ValueError:
   sys.exit("Error message arg num 1: That's not an int!-quitting")
   quit()  # quit at this point

try:
   val = arg_m
   if (val == 0):
       sys.exit("Error message arg num 2: must be bigger than 0-quitting")
       quit()  # quit at this point
except ValueError:
   sys.exit("Error message arg num 2: That's not an int!-quitting")
   quit()  # quit at this point

UPLOAD_FOLDER = sys.argv[3]
try:
    os.path.isfile(UPLOAD_FOLDER)
except :
    sys.exit("Error message arg num 3,"+UPLOAD_FOLDER+": That's not a path!-quitting")
    quit()  # quit at this point

print ("n="+format(arg_n)+", m="+format(arg_m)+", path="+UPLOAD_FOLDER)

class Watchdog:
    def __init__(self, timeout, userHandler=None):  # timeout in seconds
        self.timeout = timeout
        self.handler = userHandler if userHandler is not None else self.defaultHandler
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def stop(self):
        print "stop"
        self.timer.cancel()

    def defaultHandler(self):
        print "defaultHandler"
        raise self

app = Flask(__name__)
api = Api(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    swallow_errors=True,
    default_limits=[ sys.argv[1]+" per minute"]# n param from cmd
)
lock = threading.Lock()


def myHandler():
    print("handler")
    with lock:
        if (Pictures.updeted == False):
            open(UPLOAD_FOLDER+'\statistics.txt', "a").write(Pictures.str2save)
            Pictures.updeted = True
            print Pictures.str2save
@app.after_request
def after_req_handler(response):
    if (Pictures.counter == 1):
        print "timeout alert"
        abort(413 )
    return response



class Pictures(Resource):
    str2save=""
    updeted = False
    counter = 1
    global arg_m
    global arg_n
    def post(self, *args):
        Pictures.counter = 1
        Pictures.updeted = False
        watchdog_ = Watchdog(arg_m,myHandler)# sys.argv[2] =watchdog time
        ts = time.time()
        datastore_ = pickle.loads(request.data)
        for frame in datastore_:
            if (Pictures.updeted == True): break
            file_path = os.path.join(UPLOAD_FOLDER, request.values.get('file_name') +"_Frame_"+ format(Pictures.counter)+'.jpg')
            x = cv2.imwrite(file_path, frame)
            avg =(time.time() - ts)/(Pictures.counter)
            Pictures.str2save=str(datetime.datetime.now()) + ":" + request.values.get('file_name') + ",The total amount of time: " + str(time.time() - ts) + ",avg: " + str(avg) + "\n"
            Pictures.counter = Pictures.counter + 1
            print Pictures.counter
        watchdog_.stop()
        myHandler()

flas=api.add_resource(Pictures, '/pictures')  # Route_1
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=5002, threaded=False)

