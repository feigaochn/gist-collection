import threading

class PrimeNumber(threading.Thread):
    prime_numbers = {}
    lock = threading.Lock()

    def __init__(self, number):
        threading.Thread.__init__(self)
        self.Number = number
        PrimeNumber.lock.acquire()
        PrimeNumber.prime_numbers[number] = "None"
        PrimeNumber.lock.release()

    def run(self):
        counter = 2
        res = True
        while counter*counter < self.Number:
            if self.Number % counter == 0:
                print("%d is no prime number, because %d = %d * %d" % (self.Number, self.Number, counter, self.Number/counter))
                res = False
                break
            counter += 1
        print("%d is a prime number." % self.Number)
        PrimeNumber.lock.acquire()
        PrimeNumber.prime_numbers[self.Number] = res
        PrimeNumber.lock.release()

def main():
    threads = []
    while True:
        number = int(input("number: "))
        if number < 1:
            break
        thread = PrimeNumber(number)
        threads += [thread]
        thread.start()

    for x in threads:
        x.join()

if __name__ == '__main__':
    main()
