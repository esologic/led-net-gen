from skidl import *
from sys import argv, exit

path = "C:\\Users\Devon\Documents\\KiCAD\\tyler-crumpton-parts\\crumpschemes\\"
lib_search_paths[KICAD].append(path)
APA102_pins = {"DIN": 1, "CIN": 2, "GND": 3, "VCC": 4, "COUT": 5, "DOUT": 6}


def get_led():
    name = 'APA102'
    led = Part('crumpschemes', name)
    led.footprint = "CrumpPrints:APA102_hand_solder"
    led.name = name
    return led


def get_connector():
    name = "Conn_01x06_Male"
    con = Part("conn", name)
    con.footprint = "Pin_Headers:Pin_Header_Straight_2x03_Pitch2.54mm"
    con.name = name
    return con


if __name__ == "__main__":

    errors = False

    try:
        num_leds = int(argv[1])
    except IndexError:
        print("Must include number of LEDs")
        errors = True
    except ValueError:
        print(argv[1], "Can't be converted to a number")
        errors = True

    output_path = "netlist.net"

    try:
        output_path = str(argv[2])

        if not output_path.endswith(".net"):
            print("Need .net in output file name")
            errors = True

    except ValueError:
        print(argv[2], "Can't be converted to a path")
        errors = True

    if errors:
        print("Exiting.")
        exit()

    net_gnd = Net('GND')
    net_vcc = Net('VCC')
    net_din = Net("DIN")
    net_cin = Net("CIN")

    first_connector = get_connector()

    first_connector[1] += net_vcc
    first_connector[2] += net_vcc
    first_connector[3] += net_gnd
    first_connector[4] += net_gnd

    first_connector[5] += net_din
    first_connector[6] += net_cin

    for led_number in range(num_leds):

        led = get_led()

        led.ref = "LED" + str(led_number)

        led[APA102_pins["VCC"]] += net_vcc
        led[APA102_pins["GND"]] += net_gnd

        led[APA102_pins["DIN"]] += net_din
        led[APA102_pins["CIN"]] += net_cin

        net_cin = led[APA102_pins["COUT"]]
        net_din = led[APA102_pins["DOUT"]]

    second_connector = get_connector()

    second_connector[1] += net_vcc
    second_connector[2] += net_vcc
    second_connector[3] += net_gnd
    second_connector[4] += net_gnd

    second_connector[5] += net_din
    second_connector[6] += net_cin

    generate_netlist(output_path)