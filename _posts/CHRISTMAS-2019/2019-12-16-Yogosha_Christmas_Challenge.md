---
layout: post
title: HackBack
category: YogoshaChristmasChallenge 2019
---

Hello everyone, We at @Yogosha wanted to have fun with our community and hunters around the world, that's why we made for them 
a special challenge, first to enjoy playing and to learn new technical skills and secondly to give them the opportunity to earn 
their secret santa gift :)

Monday December 16, we launched the challenge, it was for a week

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/71351380-cbddd100-2573-11ea-8ff4-893357d78dbd.png"></p>

The idea for this challenge was designed to resemble the **HackBack** scenario, as someone **Anonymous** hacked into the corporate server and leaked client details, which the hunter should do, is just follow the hacker's steps and investigate before the leak arrives :) easy right?

As we know **Revenge is Sweet, But is it Legal?** for our case **YES**

First step was already mention on the tweet, `First challenge : Find it` it was simple, follow the hashtag #yogoshachristmaschallenge, and find a twitter account.

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/71352393-81118880-2576-11ea-8c31-035d14e34fa7.png"></p>

Is he really a lazy hacker? I don't think XD

Then you just have to read his tweet, one of them is to give a hint about the company he has targeted

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71361911-b3ca7980-2594-11ea-8f50-8361bf6d5417.png"></p>

It's probably `cutt.ly/something` , well here you can just find the cracked result on a website like `https://crackstation.net/` or just if we read his old tweet

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71362033-25a2c300-2595-11ea-85ae-9d7e5e79762b.png"></p>

His mention of his birthday which is already on his tweeter account info, after we collecting details about him, we can build a useful word list and break this hash `3f5089c0f9f45530f48aa03471f473ff0af999557bf78749d6d5de6c6b39632b` which is his birthay `09031980` => `09/03/1980`

Next , we can go to the real part after some OSINT, we can get the company url `http:// 3.19.111.121` from the shorten links

Let's start some recon stuff, by turning on **nmap** we will try to determine if there is another open port

The answer is **YES**, always a little RECON before you start moving quickly through the target will help you get details and information that can help you in the next step :)

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71362446-56372c80-2596-11ea-8932-1e38218e3625.png"></p>

After discovering two new ports, we can confirm that the ssh port is used for the aws instance, the second port looks like the good one **1337**

By checking the port, we can get an output:

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71362623-e7a69e80-2596-11ea-9291-aec61307eda8.png"></p>

Looks like its 12 character password login service, if we are trying to brute force it will be probably the worst idea ever  as it will never end.

So the best option is to try to think outside the box, the service text contain **very slow version**, so maybe it uses some functions that slow down password verification , for someone who is used to playing CTF or having love with crypto stuff, he will think about this type of attack that occurs almost everywhere **Side Channel Attack** https://en.wikipedia.org/wiki/Side-channel_attack

One of this attack called **timing attack** , where you can guess if your input correct or not depend on the time it take each char you send comparing to others which is the case here !

If we debug a little the first time, then by writing a small script, we will get the password which is `pAsSwOrd159!`

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71363508-ae236280-2599-11ea-907f-f70e8a06ff30.png"></p>

If we access using this password, we will get information about active sessions, whenever it gives us different users, what we can do here is that we can leak all users that we may have need in the future!

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71373943-31a07c00-25b9-11ea-9d00-7d2aa4da367f.png"></p>

Then, if we go back now to the web application, we can find a simple page there without more information that lead us to another path.

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71363668-2722ba00-259a-11ea-873a-72df0cfe0812.png"></p>

Should sometimes use some tools,  [mine](https://github.com/tnmch/cybercrowl) works fine (even after losing all starts because of changing my nickname on github: D)

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71364279-08bdbe00-259c-11ea-9fe2-d4a2b0d42e3c.png"></p>

We got useful information from the tool:

```
http://3.19.111.121/wp-content/
http://3.19.111.121/wp-login.php
....

```

We can now get an idea of what type of web application it is, Wordpress for sure!

If we do some enumeration (manual or using the **wpscan** tool), we can get what plugins already installed

```
1- advanced-custom-fields
2- akismet
```

Going to the ACF plugin, we find the zip file **ACF.zip**, so if we want to get more details, we can just compare this zip file with the original one `https://www.advancedcustomfields.com/Downloads/`

```
git diff ACF ACF_1
```

Give us some result :

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71365900-9e5b4c80-25a0-11ea-8bfe-ae208b893260.png"></p>

As we see, there is a new `Load_Hotfix()` & `Hotfix_update()` function added by the hacker as a backdoor to the `updates.php` file ,with comment at the end `// / server-status`

It is a function which uses another real wordpress function to make a call, does he have a 0day on this function or what ??

<p align="center"><img src="https://media.giphy.com/media/l2QDZFG1IXD4zbuRq/giphy.gif"></p>

Let's start by debugging more, he just created a function called `Load_Hotfix` to confuse others with the real name ,look like he is trying to hide it, the function looks good but it has bad behavior .

```
-               if ($user === "noel" && $_GET['debug'] === "1") {
-                       $ACF_Hotfix = new ACF_Updates();
-                       $ACF_Hotfix->Hotfix_update($_GET['upd']);
-               }

```

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71374164-f5215000-25b9-11ea-8f9d-ff707d0b1a35.png"></p>

This function only works if the user is logged in and the username is `noel` , it also checks the `debug` parameter if it is there, it will use another `upd` parameter and will call `Hotfix_update()` who will request specific URL!

Wait, was this hacker just a lazy pirate ?? are you sure for real!

<p align="center"><img src="https://media.giphy.com/media/10uct1aSFT7QiY/giphy.gif"></p>

Anyway, let's move on, as we have already disclosed some users when we enter the `1337` service, one of these users called `noel` same name as this hacker is looking for!

Why don't we just try to log in with this password? , we will first go to `http://3.19.111.121/wp-admin/` but it was not accessible and redirects us to the index page, but we also assume to be hackers "hunter", we can connect from here `http://3.19.111.121/wp-login.php`

And yes, we just got IN guys :), let's check out what we can do with this pirate backdoor

By sending this `http://3.19.111.121/?debug=1&upd=https://google.com` we get this output result

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71366670-fa26d500-25a2-11ea-919e-ce1dd1b27cb8.png"></p>

Looks like we have SSRF `Server Side Request Forgery` here, but can we do it?

As we was crawling the website , we notice that `http://3.19.111.121/server-status` gives us forbidden page, what if we can access it from the inside? :)

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71367046-170fd800-25a4-11ea-8a6d-46c5a7c05601.png"></p>

We have just disclosed information about old and the current request made on this app, we can also notice the onion domain `bacq7ip6nzdyhb3o.onion` which is the hacker domain where he stores information!

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71367659-06f8f800-25a6-11ea-89a9-77940904d976.png"></p>

As its little difficult to scan or dig in the onion domain, why not try to de-anonymizing it,if you are interested in this kind of stuff, you can find more here `https://github.com/AnarchoTechNYC/CTF/wiki/Tor`

So, by just checking the nonexistent file like `bacq7ip6nzdyhb3o.onion/something`, we just leaked the real IP behind this domain :)

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71367716-24c65d00-25a6-11ea-8286-d0fbf7506828.png"></p>

Yeah, so cool now we can start doing more things, if we are just trying to do some injection test on this login form we get errors

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71367879-97cfd380-25a6-11ea-8875-a374b838e878.png"></p> 

We just know it should be an xpath injection, let's use it :)

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71367944-ca79cc00-25a6-11ea-8c48-83bad6368968.png"></p>  

Since we have the user / password, we can access this hacker website (we can also bypass it using a simple payload ` ' or 1 = 1 or '` ), but I like the hard way , it teaches a lot!

So now we get a result, looks like the html output of the tree tool

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71368111-483dd780-25a7-11ea-97fe-886106166e68.png"></p>  

Checking this path `http://3.13.238.49/bCkup/Target/172.28.13.37/payload/hack.txt` we failed and nothing was there, but if we just check`/robots.txt`, we can see that it hides a folder that was badly rendered on the result of the tree due to a special character

```
User-agent: *
Disallow: /bāCkupē
```

And now we get access `http://3.13.238.49/b%C4%81Ckup%C4%93/Target/172.28.13.37/payload/hack.txt` 

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71368252-b97d8a80-25a7-11ea-85df-5b2896d6f2c4.png"></p>  

So nice Intro, he preparing some words for the leak which will look wil happen 01/01/2020 !

But if we check the URL again, it looks like he records the result by target as directory name, and this IP address looks like a local IP address for something, lets use SSRF, we need to check what is there

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71368360-07928e00-25a8-11ea-8308-df748340cda5.png"></p> 

Lets read again this page, as he just starts to mention a few details, we can notice that it is talking about backup container, so this should probably be a issue there, need to find out what we can do with just a login mysql page, without credz!

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71368414-2d1f9780-25a8-11ea-9f79-4db8ecafb537.png"></p> 

Looking around on a mysql security issue, we found that we can abuse MySQL clients to get LFI from the server, which means that if we have created a mysql server and the client just connects to our server, we can inject another request like `local data file request` that means we will make the client read for us some file data :)

It's like **Hey client, please read the /etc/passwd file and send to it me I’ll see what I can do for you** and yes, it will read the file as much as it can read it with www-data privilege.

We just setup our mysql server , and run this script on different port `https://github.com/Gifts/Rogue-MySql-Server/blob/master/rogue_mysql_server.py`

And yes , BOoooM !

<p align="center"><img src="https://media.giphy.com/media/2wSe48eAUC15p38UqO/giphy.gif"></p> 

We just got the flag by reading `/etc/passwd`!

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71369774-154a1280-25ac-11ea-953e-af87be6bb590.png"></p>

`Yogosha{4t_christma5_all_r0ads_Le4d_hOme}`
