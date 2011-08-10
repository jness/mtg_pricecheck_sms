#!/usr/bin/env python

import urllib2
import re
import time
from googlevoice import Voice

voice = Voice()
voice.login()

while True:
    sms = voice.sms()
    for m in sms.messages:
        if m.isRead:
            continue

        card = urllib2.quote(m.messageText)
        phoneNumber = m.phoneNumber
        u = urllib2.urlopen('http://magic.tcgplayer.com/db/magic_single_card.asp?cn=%s' % card).read()
        prices = re.compile('<B>(\$.*)</b>').findall(u)
        msg = ''
        if prices:
            msg = msg + m.messageText.title() + '\n'
            msg = msg + '-'*20 + '\n'
            msg = msg + 'High ' + prices[0] + '\n'
            msg = msg + 'Avg ' + prices[1] + '\n'
            msg = msg + 'Low ' + prices[2] + '\n'
            print 'Sending to %s' % phoneNumber
            voice.send_sms(phoneNumber, msg)
        else:
            msg = 'No card found with name %s' % m.messageText
            print 'Sending to %s' % phoneNumber
            voice.send_sms(phoneNumber, msg)

        m.delete()
    time.sleep(10)
