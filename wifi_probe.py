import os, platform

def find_windows_wifi():
    win_wifi_dict = {}
    raw_win_networks = os.popen('netsh wlan show profile').read()
    raw_win_networks = raw_win_networks.split("\n")
    raw_win_networks = raw_win_networks[9:-2]
    win_wifis = []

    for unparsed_wifi in raw_win_networks:
        tmp = unparsed_wifi
        win_wifis.append(tmp.split(": ")[1])

    for wifi in win_wifis:
        raw_passwd = os.popen(f"netsh wlan show profile {wifi} key=clear").read()
        start = raw_passwd.find("Key Content")
        regrex = raw_passwd[start:].split("\n")[0]
        try:
            win_wifi_dict[f"{wifi}"] = regrex.split(": ")[1]
        except:
            win_wifi_dict[f"{wifi}"] = "None found"
    return win_wifi_dict


def find_linux_wifi():
    linux_wifi_dict = {}
    passwd = input("Sudo passwd:")
    raw_linux_networks = os.popen('echo ' + passwd +'| sudo -S find /etc/NetworkManager/system-connections -type f -name "*.nmconnection" -exec grep "psk=" {} +').read()
    raw_linux_networks = raw_linux_networks.split("\n")
    
    for wifi in raw_linux_networks:
        try:
            passwd = wifi.split("=")[1]
            linux_wifi_dict[f"{os.path.basename(wifi.split('.')[0])}"] = passwd
        except:
            linux_wifi_dict[wifi] = "None Found"

    return linux_wifi_dict


def find_mac_wifi():
    mac_wifi_dict = {}
    
    raw_mac_networks = os.popen('defaults read /Library/Preferences/SystemConfiguration/com.apple.airport.preferences |grep SSIDString').read()
    raw_mac_networks.split("\n")
    
    for wifi in raw_mac_networks:
        os.popen(f"security find-generic-password -ga '{wifi}' | grep 'password:'").read()
        try:
            mac_wifi_dict[f"{wifi}"] = regrex.split(": ")[1]
        except:
            mac_wifi_dict[f"{wifi}"] = "None found"
    return mac_wifi_dict

cmdDict = {
    "Windows":find_windows_wifi,
    "Linux":find_linux_wifi,
    "Darwin":find_mac_wifi
}

def main(os=platform.system()):
    return cmdDict[os]()

if __name__=='__main__':
    with open(f'{platform.node()}.txt', 'w+') as f: 
        for key, value in main().items():
            f.write(f"{key}: {value}\n")
