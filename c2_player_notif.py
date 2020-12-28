import requests
import time
import logging
from notifypy import Notify

# List of player names to notify for
players_of_interest = ["Shay", "z2sam", "Azteca"]

# Sleep delay in ms for how frequently to fetch a new online players list
sleep_delay = 5000

# Logging Stuff
logger = logging.getLogger("c2_player_notif")
logger.setLevel(logging.DEBUG)

# create file handler that logs debug and higher level messages
fn = "player_notifications_%s.log" % time.ctime()
fh = logging.FileHandler(fn)
fh.setLevel(logging.DEBUG)

# create console handler with same log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

while True:
    try:
        # Request
        logger.info("Requesting http://gewaltig.net/liveinfo.aspx")
        r = requests.get("http://gewaltig.net/liveinfo.aspx")

        data = r.json()
        found = False
        online_players = [player["name"] for player in data["players"]]
        logger.info(
            "Players Online: %s" % ", ".join([str(name) for name in online_players])
        )

        # Loop through online players and check if in players_of_interest
        for player in data["players"]:
            if player["name"] in players_of_interest:
                # if found, send notification
                found = True
                notif_msg = "%s is online" % player["name"] + " on %s" % time.ctime()
                logger.info(notif_msg)
                notification = Notify()
                notification.title = "Cultris 2 Player Notification"
                notification.message = notif_msg
                notification.send()

        if not found:
            not_found_msg = "%s not found online" % ", ".join(
                [str(name) for name in players_of_interest]
            )
            logger.info(not_found_msg)

    except Exception as e:
        logger.error(e)
    found = False

    # Sleep before generating next request
    time.sleep(sleep_delay)
