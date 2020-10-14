#!/usr/bin/env python

import nmap
import time
import sys
import argparse
import requests
import re

# Scan Mac's and get user input before the loop
def scan_for_mac():
    macs = []
    nm.scan(args.IP, arguments='-sn')
    count = 0

    for x in nm.all_hosts():
        if 'mac' in nm[x]['addresses']:
            print(str(count)+':', nm[x]['hostnames'][0]['name'], nm[x]['addresses']['ipv4'], nm[x]['addresses']['mac'], nm[x]['vendor'].get(nm[x]['addresses']['mac']))
            macs.append(nm[x]['addresses']['mac'])
            count += 1

    choices = list(range(len(macs)))
    choice = int(input('Please enter the number which corresponds to the MAC you wish to scan for:\n'))

    while choice not in choices:
        choice = int(input('Invalid choice. Please enter the number which corresponds to the MAC you wish to scan for:\n'))
    
    return(macs[choice])

# Grab a list of all the MAC's on the network 
def scan(ip):
    mac_addresses = []
    nm.scan(ip, arguments='-sn')
    for x in nm.all_hosts():
        if 'mac' in nm[x]['addresses']:
            # Show IP's and MAC addresses on the network 
            # print(nm[x]['hostnames'][0]['name'], '/', nm[x]['addresses']['ipv4'], '/', nm[x]['addresses']['mac'])
            mac = nm[x]['addresses']['mac']
            mac_addresses.append(mac)
    return(mac_addresses)

# Check if the user's MAC choice is on the network. Send a telegram message if it is the first time since being off
def check_for_mac(addresses):
    if mac_address in addresses and check == 1:
        print('[+] MAC address is present on network')
        if args.telegram and args.chat:
            send_telegram_message('MAC address is present')
        return 0

    elif mac_address in addresses and check == 0:
        print('[+] MAC address is present on network')
        return 0 

    else:
        print('[-] MAC address is not present on the network')
        return 1

# Send a telegram message using the API that the MAC is present on the network
def send_telegram_message(text):
    if args.telegram and args.chat:
        token = args.telegram
        chat_id = args.chat

    try:
        url_req = 'https://api.telegram.org/bot' + token + '/sendMessage' + '?chat_id=' + chat_id + '&text=' + text
        requests.get(url_req)
    
    except:
        print('Error authenticating with the Telegram token or chat ID you entered. Please start the program and try again.')
        sys.exit()

if __name__ == "__main__":

    nm = nmap.PortScanner()

    # Argument options
    parser = argparse.ArgumentParser(description='Enter the information necessary to scan for a certain MAC')
    parser.add_argument('-m', '--mac', type=str, help='Add a custom MAC address instead of scanning the network to find one. ex: XX:XX:XX:XX:XX:XX')
    parser.add_argument('-s', '--sleep', type=int, help='Enter the amount of time you wish to sleep in between scans. Time used is in seconds. Default=60')
    parser.add_argument('-t', '--telegram', type=str, help='Enter your Telegram bots token. Must be used with the chat ID flag')
    parser.add_argument('-c', '--chat', type=str, help='Enter the chat ID to whom you want to send the message. Must be used with a Telegram bot token')
    requiredNamed = parser.add_argument_group('Required Arguments')
    requiredNamed.add_argument('IP', help='Enter the IP range you wish to scan (make sure to add subnet range ex: 192.168.0.0/24)')
    args = parser.parse_args()

    # XOR to require both arguments to be used in conjunction with eachother 
    if bool(args.chat) ^ bool(args.telegram):
        parser.error('--telegram and --chat must be given together')

    # Grab the MAC Choice
    if args.mac and re.match(r'\w+:\w+:\w+:\w+:\w+:\w+', args.mac):
        mac_address = args.mac
    elif args.mac and not re.match(r'\w+:\w+:\w+:\w+:\w+:\w+', args.mac):
        print('Invalid MAC Address. Moving on to scan for valid MAC\'s')
        mac_address = scan_for_mac()
    else:
        mac_address = scan_for_mac()

    # Set check to 1 so if the MAC is present to start we will send a telegram message
    check = 1

    # Loop through infitely unless we get a keyboard interrupt
    while True:
        try:
            check = check_for_mac(scan(args.IP))
            print('*+' * 10 + ' Sleeping for 60 seconds ' + '+*' * 10)
            if args.sleep:
                time.sleep(args.sleep)
            else:
                time.sleep(60)

        except KeyboardInterrupt:
            sys.exit()
