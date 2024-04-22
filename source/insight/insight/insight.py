import os
import subprocess
import time

from insight.broker import MqttBroker

OPERATION = "PUBLISH"  # "SUBSCRIBE"
GEOMETRY = (1640, 1480)
FPS = 1


def main():
    while True:
        "Hello Worlds!"

        time.sleep(1 / FPS)


def id():
    process = subprocess.Popen(
        ["cat", "/sys/firmware/devicetree/base/serial-number"], stdout=subprocess.PIPE
    )

    output, _ = process.communicate()
    serial = output.strip().decode("utf-8")[-9:]

    print(f"My identity is: {serial}")


class Insight:
    def __init__(
        self,
        host: str = "10.0.0.18",
        port: int = 1883,
        topic: int = "Camera/capture",
    ):
        self.broker = MqttBroker()
        self.broker.start()

        self.host = host
        self.port = port
        self.topic = topic

    def main(self):
        print(f"Running from USER: {os.getenv('USER')}")

        if OPERATION == "PUBLISH":
            self.publish()
        elif OPERATION == "SUBSCRIBE":
            self.subscribe()
        else:
            pass


if __name__ == "__main__":
    id()

    # insight = Insight()
    # insight.main()
