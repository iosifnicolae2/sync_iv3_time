import datetime
import pytz
from time import sleep

import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

com_ports = [port.device for port in ports]

now = datetime.datetime.now(tz=pytz.timezone('Europe/Bucharest'))
datetime_message = "S {year} {month} {day} {hour} {minute} {second}\n".format(
    year=now.year,
    month=now.month,
    day=now.day,
    hour=now.hour,
    minute=now.minute,
    second=now.second,
)
print("datetime_message: {}".format(datetime_message))


def get_serial(port, baud_rate):
    try:
        ser = serial.Serial(port, baud_rate, timeout=0.005)

        return ser
    except serial.serialutil.SerialException:
        return None


current_index = 0
total = len(com_ports)
for com_port in com_ports:
    current_index = current_index + 1
    print("({}/{})Sending data to {}".format(current_index, total, com_port))
    serial_port = get_serial(com_port, 9600)
    if not serial_port:
        continue

    print("Waiting 3 seconds for Arduino to become available..")
    sleep(3)
    print(serial_port.portstr)
    if serial_port:
        serial_port.write(datetime_message.encode())
        print("Done")
    else:
        print("Resource is busy.")

    if serial_port.isOpen():
        serial_port.close()
