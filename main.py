
import requests
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
import re

########################################################################################################################
goipAddr = '192.168.1.221'
goipUsr = 'admin'
goipPass = 'admin'
selCan = {1: 223, 2: 212, 3: 213, 4: 214, 5: 215}
########################################################################################################################

goipInbox = '/default/en_US/tools.html?type=sms_inbox'
goipDel = '/default/en_US/tools.html?action=del&type=sms_inbox&line={}&pos=-1'
ariSend = 'http://localhost:8088/ari/endpoints/sendMessage?from={}&to=sip:{}&body={}'

headers = CaseInsensitiveDict()
headers["Authorization"] = "Basic YXN0ZXJpc2s6YXN0ZXJpc2s="
headers["Content-Length"] = "0"


def getSms():
    mess = ''
    sms = {}
    res = requests.get('http://{}:{}@{}{}'.format(goipUsr, goipPass, goipAddr, goipInbox))
    html_page = res.content

    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    for tStr in text:
        mess += '{} '.format(tStr)

    str_pos = [i.start() for i in re.finditer('sms= ', mess)]

    for i in range(0, len(str_pos)):
        if i < len(str_pos) - 1:
            sms['sim' + str(i + 1)] = mess[str_pos[i] + 5:str_pos[i + 1] - 48]
        else:
            sms['sim' + str(i + 1)] = mess[str_pos[i] + 5:mess.find('sms_row_insert', str_pos[i])]
    return sms


def getMess(simNum):
    allMess = []

    tStr = getSms()['sim' + str(simNum)]

    for i in range(0, 19):
        curr = {}
        if i == 0:
            pStart = 2
            pEnd = tStr.find('"', pStart)
        else:
            pStart = pEnd + 3
            pEnd = tStr.find('"', pStart)
        if pStart == pEnd:
            break

        currMess = tStr[pStart:pEnd + 1]

        pEnd1 = currMess.find(',', 0)
        curr['date'] = currMess[0:pEnd1]

        pStart1 = pEnd1 + 1
        pEnd1 = currMess.find(',', pStart1)
        curr['num'] = currMess[pStart1:pEnd1]

        pStart1 = pEnd1 + 1
        pEnd1 = currMess.find(',', pStart1)
        curr['mess'] = currMess[pStart1:pEnd1]
        allMess.append(curr)
    return allMess


for currCan, currNum in selCan.items():
    print(currNum)
    for tStr in getMess(currCan):
        if len(tStr['num']) > 0:
            fStr = tStr['num'] + ' ' + tStr['mess']
            fStr = fStr.replace(' ', '%20')
            url = ariSend.format(tStr['num'][1:], currNum, fStr)
            #print(url)
            resp = requests.put(url, headers=headers)
            print(resp.status_code)
    url = 'http://{}:{}@{}{}'.format(goipUsr, goipPass, goipAddr, goipDel)
    url = url.format(currCan)
    #print(url)
    resp = requests.get(url)
    #print(resp.status_code)