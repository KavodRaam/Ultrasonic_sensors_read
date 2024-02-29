import can.interfaces.pcan
import struct


def print_in_rgb(processed_data, C):
    color_code = f"\033[38;2;{C};{255-C};{122}m"
    reset_code = "\033[0m"
    print(f"{color_code}{processed_data}{reset_code}")


bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)
processed_data = 0
C = 0
while True:
    if C > (255-17):
        C = 0
    C += 17
    srf_data_array = []
    msg = bus.recv(1.0)
    if msg is None:
        continue
    if msg.data[0] == 0x17:
        for index in range(4, 8):
            x = msg.data[index]
            srf_data_array.append(struct.pack('>B', x))
        # print(msg.data)
        processed_data = int(float(str(struct.unpack('<f', b''.join(srf_data_array))).replace("(", '').replace(")", '')
                                   .replace(",", '').replace("nan", 'NA')))
        print_in_rgb(processed_data, C)
