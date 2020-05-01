import argparse
import subprocess
import re


def check_equal(new_mac, updated_mac):
    if(new_mac == updated_mac):
        return True
    else:
        return False


def curr_mac(interface):
    subprocess.check_output(["sudo", "ifconfig", interface])
    # to check if subprocess call has raised an error if yes Called process error is set to 1
    if subprocess.CalledProcessError == 1:
        exit()
    else:
        result = str(subprocess.check_output(["sudo", "ifconfig", interface]))
        fin_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", result)
        if fin_result:
            return fin_result.group(0)


def change_mac(interface, mac):
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", mac])
    if not re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", mac):
        subprocess.call(["sudo", "ifconfig", interface, "up"])
        exit()
    subprocess.call(["sudo", "ifconfig", interface, "up"])


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface",
                        help=" interface of which mac has to be changed")
    parser.add_argument("-m", "--mac", dest="mac", help="new_mac")
    options = parser.parse_args()
    if not options.interface:
        parser.error("please specify interface")
    if not options.mac:
        parser.error("please specify mac")
    return options


options = get_arguments()
current_mac = curr_mac(options.interface)
change_mac(options.interface, options.mac)
updated_mac = curr_mac(options.interface)
if not current_mac:
    print("Mac address couldnt be read, current MAC :", str(current_mac))
else:
    current_mac2 = curr_mac(options.interface)
    if check_equal(current_mac2, updated_mac):
        print(current_mac + " updated to", updated_mac)
