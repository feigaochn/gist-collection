import os
import re


def main():
    received_packages = re.compile(r'(\d) packets received')
    status = ("No response", "alive but losses", "alive")

    for suffix in range(0, 10):
        ip = "10.217.166."+str(suffix)
        ping_out = os.popen("ping -q -c 2 "+ip, "r")
        print("... pinging "+ip)
        while True:
            line = ping_out.readline()
            if not line:
                break
            # print("  "+line)
            n_received = received_packages.findall(line)
            # print(n_received)
            if n_received:
                print(ip+": "+status[int(n_received[0])])

if __name__ == '__main__':
    main()
