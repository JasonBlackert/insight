import getpass
import logging
import subprocess
import time

from insight.broker import MqttBroker
from insight.config import parse_args

args = parse_args()
config = args.config


log = logging.getLogger(__name__)
logging.basicConfig(
    level=config["insight"]["log_level"],
    format="%(name)s [%(levelname)s]: %(message)s",
    force=True,
)

OPERATION = "PUBLISH"


def main():
    insight = Insight()
    insight.broker = MqttBroker()
    insight.broker.start()

    while True:
        insight.reload_topic()
        insight.main()

        time.sleep(insight.sleep)


def id():
    process = subprocess.Popen(
        ["cat", "/sys/firmware/devicetree/base/serial-number"], stdout=subprocess.PIPE
    )
    output, _ = process.communicate()
    serial = output.decode("utf-8").rstrip("\x00")[-8:]
    user = getpass.getuser()

    print(f"My identity is: {user}:{serial}")


class Insight:
    def __init__(
        self,
        host: str = "10.0.0.18",
        port: int = 1883,
        topic=config["mqtt"]["topic"],
        descr=config["insight"]["description"],
    ):

        # MQTT
        self.host = host
        self.port = port
        self.topic = topic
        self.descr = descr

        # Serial & USER
        process = subprocess.Popen(
            ["cat", "/sys/firmware/devicetree/base/serial-number"],
            stdout=subprocess.PIPE,
        )
        output, _ = process.communicate()
        self.serial = output.decode("utf-8").rstrip("\x00")[-8:]
        self.user = getpass.getuser()

        # Time
        self.sleep = config["time"]["sleep"]

    def reload_topic(self):
        process = subprocess.Popen(
            [
                "cat",
                "/sys/firmware/devicetree/base/serial-number",
            ],
            stdout=subprocess.PIPE,
        )

        output, _ = process.communicate()

        self.serial = output.decode("utf-8").rstrip("\x00")[-8:]
        self.topic = self.topic.replace("$SERIAL", self.serial)
        self.descr = self.descr.replace("$USER", self.user)
        self.sleep = config["time"]["sleep"]

    def main(self):
        print(f"Running from USER: {self.user}")

        if OPERATION == "PUBLISH":
            self.publish()
        elif OPERATION == "SUBSCRIBE":
            self.subscribe()
        else:
            pass

    def publish(self):
        self.broker.unicast(cmds=[self.descr], serials=[self.serial], topic="status")


if __name__ == "__main__":
    insight = Insight()
    insight.main()
