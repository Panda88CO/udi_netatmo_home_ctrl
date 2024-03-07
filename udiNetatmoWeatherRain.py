#!/usr/bin/env python3

"""
Polyglot v3 node server
Copyright (C) 2023 Universal Devices

MIT License
"""


import time
import traceback
import re

try:
    import udi_interface
    logging = udi_interface.LOGGER
    Custom = udi_interface.Custom
except ImportError:
    import logging
    logging.basicConfig(level=logging.DEBUG)

'''
id = 'rain'
drivers = [
            {'driver' : 'GV0', 'value': 0,  'uom':82}, 
            {'driver' : 'GV1', 'value': 0,  'uom':82}, 
            {'driver' : 'GV2', 'value': 0,  'uom':82}, 
            {'driver' : 'GV3', 'value': 0,  'uom':12}, 
            {'driver' : 'GV4', 'value': 0,  'uom':44}, 
            {'driver' : 'GV5', 'value': 0,  'uom':51}, 
          
            {'driver' : 'ST', 'value': 0,  'uom':2}, 
            ]
'''

class udiN_WeatherRain(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, NetatmoWeather, home, module):
        super().__init__(polyglot, primary, address, name)

        self.weather = NetatmoWeather
        self.module = module
        self.module = {'module_id':module, 'type':'RAIN', 'home_id':home }
        self.primary = primary
        self.address = address
        self.name = name
        self.id = 'rain'
        self.drivers = [
            {'driver' : 'GV0', 'value': 0,  'uom':82}, 
            {'driver' : 'GV1', 'value': 0,  'uom':82}, 
            {'driver' : 'GV2', 'value': 0,  'uom':82}, 
            {'driver' : 'GV3', 'value': 0,  'uom':44}, 
            {'driver' : 'GV4', 'value': 99,  'uom':25}, 
            {'driver' : 'GV5', 'value': 99,  'uom':25}, 
          
            {'driver' : 'ST', 'value': 0,  'uom':2}, 
            ]
        
        self.n_queue = []
        self.poly.subscribe(self.poly.START, self.start, address)
        #self.poly.subscribe(self.poly.STOP, self.stop)
        self.poly.subscribe(self.poly.ADDNODEDONE, self.node_queue)


        polyglot.ready()
        self.poly.addNode(self)
        self.wait_for_node_done()
        self.node = self.poly.getNode(address)
        logging.info('Start {} Rain Node'.format(self.name))  
        time.sleep(1)

        self.nodeDefineDone = True

    
    
    def node_queue(self, data):
        self.n_queue.append(data['address'])

    def wait_for_node_done(self):
        while len(self.n_queue) == 0:
            time.sleep(0.1)
        self.n_queue.pop()

    def getValidName(self, name):
        name = bytes(name, 'utf-8').decode('utf-8','ignore')
        return re.sub(r"[^A-Za-z0-9_ ]", "", name)

    # remove all illegal characters from node address
    def getValidAddress(self, name):
        name = bytes(name, 'utf-8').decode('utf-8','ignore')
        tmp = re.sub(r"[^A-Za-z0-9_]", "", name.lower())
        logging.debug('getValidAddress {}'.format(tmp))
        return tmp[:14]
    
    

    def convert_temp_unit(self, tempStr):
        if tempStr.capitalize()[:1] == 'F':
            return(1)
        elif tempStr.capitalize()[:1] == 'K':
            return(0)
        

    def start(self):
        logging.debug('Executing NetatmoWeatherRain start')
        self.updateISYdrivers()

    def update(self, command = None):
        self.weather.update_weather_info_cloud(self.module['home_id'])
        self.weather.update_weather_info_instant(self.module['home_id'])
        self.updateISYdrivers()


    def rfstate2ISY(self, rf_state):
        if rf_state.lower() == 'full' or rf_state.lower() == 'high':
            rf = 0
        elif rf_state.lower() == 'medium':
            rf = 1
        elif rf_state.lower() == 'low':
            rf = 2
        else:
            rf= 99
            logging.error('Unsupported RF state {}'.format(rf_state))
        return(rf)
    

    def battery2ISY(self, batlvl):
        if batlvl == 'max':
            state = 0
        elif batlvl == 'full':
            state = 1
        elif batlvl == 'high':
            state = 2
        elif batlvl == 'medium':
            state = 3
        elif batlvl == 'low':
            state = 4
        elif batlvl == 'very low':
            state = 5
        else:
            state = 99
        return(state)
    

    def trend2ISY (self, trend):
        if trend == 'stable':
            return(0)
        elif trend == 'up':
            return(1)
        elif trend =='down':
            return(2)
        else:
            logging.error('unsupported temperature trend: {}'.format(trend))
            return(99)    
        
    def updateISYdrivers(self):
        logging.debug('updateISYdrivers')
        data = self.weather.get_module_data(self.module)
        logging.debug('Rain module data: {}'.format(data))
        if self.node is not None:
            if self.weather.get_online(self.module):
                self.node.setDriver('ST', 1)
              
                self.node.setDriver('GV0', self.weather.get_rain(self.module), True, False, 82)
                self.node.setDriver('GV1', self.weather.get_rain_1hour(self.module), True, False, 82)
                self.node.setDriver('GV2', self.weather.get_rain_24hours(self.module), True, False, 82)

                self.node.setDriver('GV3', self.weather.get_time_since_time_stamp_min(self.module) , True, False, 44)
                
                bat_state, bat_lvl  = self.weather.get_battery_info(self.module)    
                self.node.setDriver('GV4', self.battery2ISY(bat_state), True, False, 25 )     
                rf1, rf2 = self.weather.get_rf_info(self.module) 
                self.node.setDriver('GV5', self.rfstate2ISY(rf1) )
                #self.node.setDriver('ERR', 0)
            else:
                self.node.setDriver('GV0', 99, True, False, 25 )
                self.node.setDriver('GV1', 99, True, False, 25 )
                self.node.setDriver('GV2', 99, True, False, 25 )
                self.node.setDriver('GV3', 99, True, False, 25 )
                self.node.setDriver('GV4', 99, True, False, 25 )
                self.node.setDriver('GV5', 99, True, False, 25 )
                self.node.setDriver('ST', 0)
                #self.node.setDriver('ERR', 1)


    commands = {        
                'UPDATE': update,
                'QUERY' : update, 
                }


       
                


