# -*- coding: utf-8 -*-
import os

destinations = [
    {
        'name':u'Арес-7',
        'id':'ares_7'
    },
    {
        'name':u'Станция "Вектор"',
        'id':'vector'
    }
]


class DestinationsConfig(object):
    def __init__(self):
	global destinations
        self.destinations = destinations
	self.id_tree = {}
	
	app_dir = os.path.dirname(os.path.realpath(__file__))
       
	for item in self.destinations:
            self.id_tree[item['id']] = {
                'name':item['name'],
		'sounds': [os.path.join(app_dir,'sounds',item['id'],f) for f in os.listdir(os.path.join(app_dir,'sounds',item['id'])) if f.endswith('.mp3')]
            }


class Config(object):
    SECRET_KEY = 'secret!'
    JOBS = [
        {
            'id': 'check_status',
            'func': '__main__:check_status',
            'trigger': 'interval',
            'seconds': 1
        }
    ]

    SCHEDULER_VIEWS_ENABLED = True

