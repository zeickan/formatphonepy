#!/usr/bin/env python

from asterisk.agi import *
from conversions import conversions_list

prefixes = ["9"]
cel_code = "9"
local_code = "11"

def formatPhone(phone):
    parts = phone.split("-")
    if len(parts) == 1:
        return formatManualPhone(phone)
    else:
        return formatDialerPhone(parts)

def formatDialerPhone(phone):
    area = phone[2]
    number = phone[3]
    if area == cel_code:
        return formatCelPhone(area, number)
    else:
        return formatLinePhone(area, number)


def formatCelPhone(area, number):
    formatedNumber = area + number
    for key in conversions_list.iterkeys():
        if formatedNumber.startswith(key):
            formatedNumber = formatedNumber.replace(key, conversions_list[key], 1)
            break
    return formatedNumber

def formatLinePhone(area, number):
    formatedNumber = "0" + area + number
    if area == local_code:
        formatedNumber = number
    return formatedNumber
        
def formatManualPhone(phone):
    formatedNumber = phone
    for p in prefixes:
        if phone.startswith(p):
            formatedNumber = phone[len(p):]
            break
    return formatedNumber

if __name__ == "__main__":
    agi = AGI()
    exten = agi.env['agi_extension']
    phone = formatPhone(exten)
    agi.set_variable("PHONENUMBER", phone)

