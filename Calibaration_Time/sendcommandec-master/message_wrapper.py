from byte_hex_compat import pretty_hex

# convert a string to int but making it possible to provide it in hex (0x), dec or binary (0b)
def auto_int(x):
    return int(x, 0)

def auto_bool(x):
    from distutils.util import strtobool
    return bool(strtobool(x))

class message_reader:
    def __init__(self, msg = None):
        self.command = None
        self.length = None
        self.payload = []
        self.buf_string = msg
        self.crc = None
        self.verbose = False

    @staticmethod
    def read_value(bit_pair):
        return int.from_bytes(bit_pair, "little")

    @staticmethod
    def get_buflength_preliminary(buf_string):
        if buf_string is None or len(buf_string) < 4:
            return 0
        return message_reader.read_value(buf_string[2:4])*2

    def decode(self):
        if self.buf_string is None:
            return True
        if self.verbose:
            print(f"Decoding:        {pretty_hex(self.buf_string)}")
        prelim_length = self.get_buflength_preliminary(self.buf_string)
        crc_check = 0
        self.payload = []
        for i in range(0,prelim_length,2):
            self.payload.append(self.read_value(self.buf_string[i:i+2]))
            crc_check = crc_check ^ self.payload[-1]
        total_words = len(self.payload)
        self.crc = self.payload.pop()
        if crc_check != 0:
            crc_check = crc_check ^ self.crc
            raise ValueError(f"CRC check failed on {pretty_hex(self.buf_string)}. Calculated CRC = {crc_check:04x}")
        self.command = self.payload.pop(0)
        self.length  = self.payload.pop(0)
        for i in range(prelim_length,len(self.buf_string),2):
            extra_data = self.read_value(self.buf_string[i:i+2])
            if extra_data != 0:
                print(f"Extra data is not all 0 in {pretty_hex(self.buf_string)}.")
                break


class message_wrapper:
    def __init__(self, cmd = None, dst = None, args = []):
        self.destination = dst
        self.command = cmd
        self.length = None
        self.payload = args
        self.buf_string = b''
        self.crc = 0
        self.verbose = False

    def check_destination(self):
        if self.destination not in [ i for i in range(0, 0x10) ]+ [ 0x80, 0xFF ]:
            # Note 0x10 not included in array as stop is not added to list
            raise ValueError(f"'destination': 0x{destination:04x} should be either a ROB, all ROBs (0xFF) or the CB (0x80).")

    def add(self, word):
        if word.__class__ == str:
            word = auto_int(word)
        self.buf_string += int.to_bytes(word, 2, "little")
        self.crc = self.crc ^ word

    def get_message(self):
        words_array = []
        if self.destination is not None:
            self.check_destination()
            words_array.append(self.destination)
        words_array.append(self.command)
        # First 1 corresponds to length, 2nd 1 corresponds to CRC
        self.length = len(words_array) + 1 + len(self.payload) + 1
        words_array.append(self.length)
        words_array += self.payload

        self.buf_string = b''
        self.crc = 0
        for word in words_array:
            if word.__class__ != int or word < 0 or word > 0xFFFF:
                raise ValueError(f"{word} in {words_array} should be an integer between 0 and 0xFFFF. Please divide message properly.")
            self.add(word)
        self.add(self.crc)
        if self.verbose:
            print(f"Message:         {pretty_hex(self.buf_string)}")
        return self.buf_string




