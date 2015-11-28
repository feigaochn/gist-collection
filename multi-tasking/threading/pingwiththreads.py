import os, re, threading

class IpCheck(threading.Thread):
    received_packages = re.compile(r'(\d) packets received')
    status = ("No response", "alive but losses", "alive")

    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip

    def run(self):
        self.ping_out = os.popen("ping -q -c2 "+self.ip, "r")
        print("... pinging "+self.ip)
        while True:
            self.line = self.ping_out.readline()
            if not self.line:
                break
            self.n_received = IpCheck.received_packages.findall(self.line)
            if self.n_received:
                print(self.ip+": "+IpCheck.status[int(self.n_received[0])])

def main():
    check_results = []
    for suffix in range(0, 10):
        ip = "10.217.166."+str(suffix)
        t = IpCheck(ip)
        check_results.append(t)
        t.start()

if __name__ == '__main__':
    main()
