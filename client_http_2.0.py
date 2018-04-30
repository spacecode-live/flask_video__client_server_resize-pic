import requests
import cv2
import pickle
import sys

send_data = []

print "Start client"
try:
   val = int(sys.argv[1])
except ValueError:
   sys.exit("Error message arg num 1: That's not an int!-quitting")
   quit()  # quit at this point

UPLOAD_FOLDER = sys.argv[2]#get as a param
try:
    cap = cv2.VideoCapture(sys.argv[2])
except :
    sys.exit("Error message arg num 2 -quitting")
    quit()  # quit at this point

if __name__ == '__main__':
    while True:
        ret, frame = cap.read()
        if ret == False: break
        frame = cv2.resize(frame, (100, 100))
        send_data.append(frame)
    data = pickle.dumps(send_data)
    try:
        r = requests.post('http://127.0.0.1:5002/pictures', data=data, params={'file_name': 'video-instance_'+format(sys.argv[1])})
        if  r.status_code == 200:
            print ("OK")
        elif r.status_code == 413:
            print ("413 Uploading Large Files Times-Out")
    except requests.exceptions.RequestException:
        print('Connection error: Too many requests. Please try again later')

