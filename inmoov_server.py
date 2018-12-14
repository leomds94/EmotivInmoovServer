import flask
import flask_cors
from flask_restful import Resource, Api
import serial
import json
import emotiv_api
import helper
import mlp_file
from pathlib import Path

import time
import csv

app = flask.Flask(__name__)
api = Api(app)

flask_cors.CORS(app)

run_mlp = False

is_trained = False

ser = None

weights_file = Path('leomds94_weights.csv')


@app.route("/")
class IsTrained(Resource):
    def get(self):
        global is_trained
        return is_trained


class ServoValues(Resource):
    def get(self):
        global run_mlp
        if run_mlp == True:
            result = json.loads(emotiv_api.ws.recv())
            print(result)
            data = result['eeg'][3:17]
            return mlp_file.run_mlp(data)[0]
        else:
            return False


class TrainMLP(Resource):
    def get(self):
        global is_trained
        mlp_file.train_mlp()
        is_trained = True


class RunMLP(Resource):
    def get(self):
        global run_mlp, ser

        run_mlp = True
        ser = serial.Serial('COM3', 9600)
        time.sleep(3)
        emotiv_api.subscribe('eeg')
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        result = json.loads(emotiv_api.ws.recv())
        data = result["eeg"][3:17]
        res = int(mlp_file.run_mlp(data)[0])
        ser.write(str(res).encode('utf-8'))
        while run_mlp:
            emotiv_api.ws.recv()
            if ser.readable():
                red = ser.read(1)
                print(red)
                result_ws = emotiv_api.ws.recv()

                result = json.loads(result_ws)
                data = result["eeg"][3:17]
                res = int(mlp_file.run_mlp(data)[0])
                ser.write(str(res).encode('utf-8'))


class StopMLP(Resource):
    def get(self):
        global run_mlp, ser
        run_mlp = False
        if (ser != None):
            emotiv_api.unsubscribe('eeg')
            time.sleep(1)
            ser.close()


class Login(Resource):
    def get(self, actual_user):
        global emotiv_user
        user = json.loads(actual_user)
        # LOGIN
        if user['username'] not in emotiv_api.getLoggedUsers():
            emotiv_api.login(user)

        # AUTHORIZE
        if emotiv_api.emotiv_user._auth == "":
            emotiv_api.authorize(user)

        # CREATE SESSION
        return emotiv_api.create_session()


class LogoutAll(Resource):
    def get(self):
        res_json = emotiv_api.getLoggedUsers()
        result = json.loads(res_json)
        users = result['result']
        for user in users:
            emotiv_api.logout(user)
        return res_json


class Logout(Resource):
    def get(self, username):
        return emotiv_api.logout(username)


class GetUserLogin(Resource):
    def get(self):
        return emotiv_api.getLoggedUsers()


# Subscribe to sys stream
class PopulateCSV(Resource):
    @staticmethod
    def get(secs, gesture, name):
        file_name = ""
        if (gesture):
            file_name = 'leomds94_eeg_gesture.csv'
            res = helper.gesture_translate_mlp(name)
        else:
            file_name = 'leomds94_eeg_finger.csv'
            res = helper.finger_translate_mlp(name)

        emotiv_api.subscribe("eeg")
        time.sleep(1)

        with open(file_name, mode='a') as eeg_file:
            eeg_writer = csv.writer(eeg_file, delimiter=',')
            timeout = time.time() + int(secs)  # time in seconds from now
            while True:
                if time.time() > timeout:
                    break
                result_json = emotiv_api.ws.recv()
                print(result_json)
                if ("unavailable" in result_json) or ("Unsubscribe" in result_json):
                    break
                result = json.loads(result_json)
                data = result['eeg'][3:17]
                data.extend(res)
                eeg_writer.writerow(data)
                time.sleep(0.02)
            eeg_file.close()

        time.sleep(1)
        emotiv_api.unsubscribe("eeg")
        return True


class GetServos(Resource):
    @staticmethod
    def get():
        return '{"leoba": 1}'


api.add_resource(LogoutAll, '/logoutall')
api.add_resource(Logout, '/logout/<username>')
api.add_resource(Login, '/login/<actual_user>')
api.add_resource(GetUserLogin, '/getuserlogin')
api.add_resource(PopulateCSV, '/populatecsv/<secs>/<gesture>/<name>')
api.add_resource(GetServos, '/getservos')
api.add_resource(RunMLP, '/runmlp')
api.add_resource(TrainMLP, '/trainmlp')
api.add_resource(StopMLP, '/stopmlp')
api.add_resource(IsTrained, '/istrained')
api.add_resource(ServoValues, '/servovalues')

if __name__ == '__main__':
    log = LogoutAll()
    log.get()

    app.run(host='0.0.0.0', port=5002)
