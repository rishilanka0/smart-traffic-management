import time

class SignalTimer:

    def __init__(self, green=10, yellow=3):

        self.green = green
        self.yellow = yellow
        self.state = "GREEN"
        self.last_switch = time.time()

    def update(self):

        now = time.time()

        if self.state == "GREEN":

            if now - self.last_switch > self.green:
                self.state = "YELLOW"
                self.last_switch = now

        elif self.state == "YELLOW":

            if now - self.last_switch > self.yellow:
                self.state = "RED"
                self.last_switch = now

        return self.state