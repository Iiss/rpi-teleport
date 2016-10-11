# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)


# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()


from flask import Flask, render_template
from flask_socketio import SocketIO, socketio, emit
from config import Config, DestinationsConfig
from multiprocessing import Process
import subprocess
import time
from flask_apscheduler import APScheduler
import random
import os
import states
import wiringpi2 as wiringpi
import config

def update_state():
        global socketio
        global cur_dest_id
        global dest_conf
        global msg
        if cur_status == states.PLAY:
                msg = dest_conf.id_tree[cur_dest_id]['name']
		pin_on(cur_dest_id)
	else:
		msg = config.STOP_STATE_MSG
		resetPins()
        socketio.emit('my response',{'data':msg},namespace='/test')

def set_status(value):
        global cur_status
        if cur_status != value:
                cur_status = value
		update_state()

def check_status():
        cmd = subprocess.Popen('mocp -i', shell=True, stdout=subprocess.PIPE)
        for line in cmd.stdout:
                if 'State' in line:
                        set_status(line)

def play(destination_id):
	global dest_conf
	snd = random.choice(dest_conf.id_tree[destination_id]['sounds'])
	cmd = 'mocp -a -p %s' % snd
    os.system('mocp -S')
	os.system('mocp -s -c')
	os.system(cmd)

def resetPins():
	global dest_conf
        for key,value in dest_conf.id_tree.items():
                pin = value['gpio_pin']
		wiringpi.digitalWrite(pin,1)

def setupPins():
	global dest_conf
	for key,value in dest_conf.id_tree.items():
		pin =  value['gpio_pin']
		wiringpi.pinMode(pin,1)

def pin_on(dest_id):
	global dest_conf
        for key,value in dest_conf.id_tree.items():
                pin =  value['gpio_pin']
                wiringpi.digitalWrite(pin,key!=dest_id)
 
''' Server init '''
#vars
cur_status = None
cur_dest_id = None
dest_conf = DestinationsConfig()
msg = config.STOP_STATE_MSG

#gpio
wiringpi.wiringPiSetup()
setupPins()
resetPins()

#flask & jobs
app = Flask(__name__)
app.config.from_object(Config())
socketio = SocketIO(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


''' Routing & events '''
@app.route('/test')
def test_route():
	return render_template('teleport.html')

@app.route('/')
def index():
	global dest_conf
	return render_template('index.html',destinations=dest_conf.destinations)

@socketio.on('fly',namespace='/test')
def fly(message):
	global cur_dest_id
	global cur_status
	if cur_status == states.STOP or message['data'] != cur_dest_id:
		cur_dest_id = message['data']
		play(cur_dest_id)
		update_state()

@socketio.on('stop', namespace='/test')
def stop(message):
	os.system('mocp -s -c')

@socketio.on('my event', namespace='/test')
def test_message(message):
	emit('my response',{'data':message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
	emit('my response',{'data':message['data']},broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
	global msg
	emit('my response', {'data':msg})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
	print('Client disconnected')


''' Main loop start '''
if __name__ == '__main__':
    #mocp player    
    os.system('mocp -S')
    os.system('mocp -s -c')
	socketio.run(app, host='0.0.0.0')
