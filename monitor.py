import re
import requests
from stem import Signal
from stem.control import Controller

def monitor_onion_domains():
    # Replace with the list of onion domains to monitor
    onion_domains = ["http://example1.onion/", "http://example2.onion/"]

    # Replace with the list of words to search for
    words = ["Test", "Example"]

    # Use the stem library to connect to the Tor network
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()

        # Set up a new circuit for the request
        controller.signal(Signal.NEWNYM)

        for domain in onion_domains:
            try:
                # Use a request session to make the request through the Tor network
                with requests.Session() as session:
                    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                                       'https': 'socks5://127.0.0.1:9050'}
                    response = session.get(domain)
                    if response.status_code == 200:
                        for word in words:
                            # Use regex to search for the word in the response text, ignoring case
                            pattern = re.compile(rf"\b{word}\b", re.IGNORECASE)
                            match = pattern.search(response.text)
                            if match:
                                print(f"The word '{word}' was found on {domain}")
                            else:
                                print(f"The word '{word}' was not found on {domain}")
                    else:
                        print(f"{domain} is not responding. Status code: {response.status_code}")
            except requests.ConnectionError:
                print(f"{domain} is not a valid onion domain.")

monitor_onion_domains()
