import mido
from mido import Message
import logging
from subprocess import run

from e2pat2syx import pat_to_syx
from e2syx2pat import syx_to_pat


def main():
    logging.basicConfig(level=logging.DEBUG)
   
    e = E2Sysex()


class E2Sysex:
    def __init__(self):
        self.inport = mido.open_input('electribe2 sampler electribe2 s')
        self.outport = mido.open_output('electribe2 sampler electribe2 s')

        self.global_channel, self.id, self.version = self.search_device()
        
        self.sysex_head = [0x42, 0x30 + self.global_channel, 0x00, 0x01, self.id]
    
        logging.info('Found electribe')
        logging.info('Global channel ' + str(self.global_channel))
        logging.info('Firmware version ' + self.version)

 
    def search_device(self):
        
        msg = Message('sysex', data=[0x42, 0x50, 0x00, 0x00])
            
        self.outport.send(msg)
        
        response = self.sysex_response()

        if response[:4] != [0xF0, 0x42, 0x50, 0x01]:
            logging.warning('Invalid response: Not search device reply message.')
            return -1
        
        global_channel = response[4]
        
        electribe_id = response[6]
        
        version = str(response[10]) + '.' + str(response[11])

        return global_channel, electribe_id, version 


    # get pattern from device
    # source is pattern number
    # returns pattern as sysex bytes
    def get_pattern(self, source):
        
        msg =  Message('sysex', data=self.sysex_head + 
                                     [0x1C] + 
                                     self.int_to_midi(source))

        self.outport.send(msg)

        response = self.sysex_response()
        
        if response[6] == 0x24:
            logging.warning('DATA LOAD ERROR: Pattern dump request unsuccessful')
            return -1
        
        elif response[6] == 0x4C:
            logging.info('PATTERN DATA DUMP: Pattern dump request successful')
            
            data = response [9:-1]

            return bytes(data)

    
    # send pattern to device
    # pattern is pattern data as list of sysex bytes
    # dest is pattern number (0-249)
    # returns SysEx response code
    def set_pattern(self, dest, pattern):
        
        msg =  Message('sysex', data=self.sysex_head + 
                                     [0x4C] + 
                                     self.int_to_midi(dest) + 
                                     pattern)

        #self.port.send(msg)        
        #response = self.sysex_response()
        
        # long sysex messages fails
        response = self.workaround_long_sysex(msg)

        if response[6] == 0x24:
            logging.warning('DATA LOAD ERROR: Pattern dump unsuccessful')
            return 0x24
        
        elif response[6] == 0x23:
            logging.info('PATTERN DATA DUMP: Pattern dump successful')            
            return 0x23

        
    # get current pattern edit buffer from device
    # returns current pattern as sysex bytes SysEx error code
    def get_current_pattern(self):
        
        msg =  Message('sysex', data=self.sysex_head+[0x10])
        self.outport.send(msg)
        
        response = self.sysex_response()
        
        if response[6] == 0x24:
            logging.warning('DATA LOAD ERROR: Current pattern dump request unsuccessful')
            return 0x24
        
        elif response[6] == 0x40:
            logging.info('CURRENT PATTERN DATA DUMP: Current pattern dump request successful')
            
            data = response[7:-1]
            return bytes(data)
        
    
    # send pattern to device edit buffer
    # pattern is pattern file as sysex bytes
    # returns SysEx response code
    def set_current_pattern(self, pattern):
        
        msg =  Message('sysex', data=self.sysex_head + 
                                     [0x40] + 
                                     pattern)
        
        # long sysex messages fails
        response = self.workaround_long_sysex(msg)
        
        # self.port.send(msg)
        # response = self.sysex_response()
        
        if response[6] == 0x24:
            logging.warning('DATA LOAD ERROR: Current Pattern dump unsuccessful')
            return 0x24
        
        elif response[6] == 0x23:
            logging.info('PATTERN DATA DUMP: Current pattern dump successful')            
            return 0x23


    # writes current edit buffer on device
    # returns SysEx Response code
    def write_pattern(self):
        logging.info('WRITE PATTERN: Not implemented yet')
        
    
    # helper function, uses get_pattern
    # get all patterns from device
    # returns list of patterns as sysex bytes
    def get_all_patterns(self):
        
        return [self.get_pattern(i) for i in range(250)]
        

   
    # helper function, uses set_pattern    
    # sends all patterns to device
    # patterns is list of patterns as sysex bytes
    def set_all_patterns(self, patterns):
        logging.info('SET ALL PATTERNS: Not implemented yet')
    


    # get global settings
    # returns settings as sysex bytes
    def get_global(self):
        msg =  Message('sysex', data=self.sysex_head+[0x1e])
        self.outport.send(msg)
        
        print('b4 response')
        response = self.sysex_response()
        print('after response')
        if response[6] == 0x24:
            logging.warning('DATA LOAD ERROR: Global data dump request unsuccessful')
            return -1
        
        elif response[6] == 0x40:
            logging.info('CURRENT PATTERN DATA DUMP: Global data dump request successful')
            
            data = response[7:-1]
            return bytes(data)
    
 
    
    # sends global settings to device
    # settings is global settings as sysex bytes
    # checks response and returns 0 if successful
    def set_global(self, settings):
        logging.info('SET GLOBAL DATA: Not implemented yet')

    
    # writes pattern to local sysex file
    # pattern is pattern data as list of sysex bytes
    # dest is pattern number on device
    # raw writes only data without sysex header 
    def save_pattern(self, path, pattern, dest=None, raw=False):
        
        # write raw pattern data
        if raw:
            
            with open(path, 'wb') as f:
                f.write(bytes(pattern))
            
            return 0

        # write pattern dump sysex
        if dest != None:
            logging.info('SAVE PATTERN: Saving pattern ' + str(dest))  
            syx = self.sysex_head +  [0x4C] +  self.int_to_midi(dest) + pattern
            
            with open(path, 'wb') as f:
                f.write(bytes(syx))
            
            return 0
        
        # write current pattern dump sysex
        else:
            logging.info('SAVE PATTERN: Saving current pattern')
            syx = self.sysex_head + [0x40] + pattern

            with open(path, 'wb') as f:
                    f.write(bytes(syx))

            return 0
    
    
    # loads pattern data from local file
    # returns sysex bytes
    # convert flag converts from e2pat format to sysex
    # header flag returns bytes with existing sysex header and tail
    # otherwise return only pattern data as sysex bytes
    def load_pattern(self, path, convert=False, header=False):
        
        logging.info('Loading pattern data from file')
        
        with open(path, 'rb') as f:
            data = f.read()
        
        if convert:
            return pat_to_syx(data[256:])
                    
        elif header:
            return data
        
        elif syx[6] == 0x40:
            return data[7:-1]
        
        elif syx[6] == 0x4C:
            return data[9:-1]

    
    
    def sysex_response(self):
        
        for msg in self.inport:
            if msg.type == 'sysex':
                response = msg.bytes()
                break
        
        return response
    
    # convert integer x <= 255 to midi bytes
    # returns little endian list of 7-bit bytes
    def int_to_midi(self, x):
        return [ x%128, x//128 ]
        
 
    # FIX - find a proper solution
    # ? can't send long sysex messages via ?mido/rtmidi?
    # works using amidi, but is very slow
    def workaround_long_sysex(self, msg):
        
        logging.info('Working around long sysex bug')

        self.outport.close()        
        run(["amidi", "-p", "hw:1", "-S", msg.hex()])
        
        response = self.sysex_response()
        
        self.outport = mido.open_output('electribe2 sampler electribe2 s')

        return response
        

    def test_sysex_message(self, val):

        msg =  Message('sysex', data=self.sysex_head+val)
        self.outport.send(msg)
        response = self.sysex_response()

        return response


    def test_long_sysex_message(self, val):

        msg =  Message('sysex', data=self.sysex_head+val)
        self.workaround_long_sysex(msg)
        response = self.sysex_response()

        return response



if __name__ == '__main__':
    main()    
