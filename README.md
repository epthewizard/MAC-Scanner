![Banner](https://document-export.canva.com/Gu4fs/DAEKnWGu4fs/1/preview/hVgYEKWUR9jLMIsQfx2oYw-0001-12067643902.png)

# MAC-Scanner
Scans a network for specified MAC Address. Allows you to keep it running and insert a Telegram bot token + chat ID to send remote notifications. Useful if you are trying to see if a person/MAC is on your home/local network while away. 

### Installation

Make sure that you have nmap installed with `nmap --version`. If not, you can install it on Debian distros with `apt install nmap`. Mac_scanner.py also requires python-nmap, requests, and argparse to run. This can be done by simply cloning the repository and using pip to install the requirements:

```install
$ git clone https://github.com/epthewizard/MAC-Scanner.git
$ cd MAC-Scanner
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

### Running the Program 

`python3 mac_scanner.py --help`

![Help File](help.png)
