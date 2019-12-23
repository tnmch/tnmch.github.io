#

Hello everyone, We at @Yogosha wanted to have fun with our community and hunters around the world, that's why we made for them 
a special challenge, first to enjoy playing and to learn new technical skills and secondly to give them the opportunity to earn 
their secret santa gift :)

On monday 16 december , we lanuched the challenge , it was for one week

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/71351380-cbddd100-2573-11ea-8ff4-893357d78dbd.png"></p>

The idea of this challenge was made to be like **HackBack** scenario , as someone **Anonyme** hack into company server and leaked clients details , what hunter need to do , is just follow back hacker steps and investigate before the leak happen :) easy right ?

As we know **Revenge is Sweet, But is it Legal?** for our case **YES**

First step was already mention on the tweet, `First challenge : Find it` so it was just simple , follow #yogoshachristmaschallenge hashtag , find tweeter account

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/71352393-81118880-2576-11ea-8c31-035d14e34fa7.png"></p>

Is it really lazy hacker ? i don't think so XD

So next , you just need to read his tweet , one of them is about giving hint about what company he targeted 

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71361911-b3ca7980-2594-11ea-8f50-8361bf6d5417.png"></p>

Its probably `cutt.ly/something` , well here you can just find the cracked result on some website like `https://crackstation.net/` or just if we read his old tweet 

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71362033-25a2c300-2595-11ea-85ae-9d7e5e79762b.png"></p>

His mention something about his birthday which is already can be found on his tweeter account information , some by collect some details about him we can build a useful wordlist and crack this hash `3f5089c0f9f45530f48aa03471f473ff0af999557bf78749d6d5de6c6b39632b` which is his birthay `09031980` => `09/03/1980`

Next , we can move on to the real part after some OSINT , we are able to get the company url `http://3.19.111.121` 

Let's start some recon stuff , by fire up **nmap** we will try to figure out if there is any other port open 

The answer is **YES** , always some recon before start moving fast into the target will help you get some details and information which can help in next stage :)


<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71362446-56372c80-2596-11ea-8932-1e38218e3625.png"></p>

After discover two new ports , we can confirm that ssh port is used for aws instance , second port look like the good one **1337**

By checking the port we can get some output :

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71362623-e7a69e80-2596-11ea-9291-aec61307eda8.png"></p>

Look like its 12 chars password login service, if we try to brute force its probably the bad idea because it will never gonna end .

So the best option is to try thinking out of the box , there is text in this output **very slow version** , so maybe it use some functions that slow the password check , for someone used to play CTF or to have some love with crypto stuff he will think about this type of attack that happen almost everywhere **Side Channel Attack** https://en.wikipedia.org/wiki/Side-channel_attack 

One of this attack called timing attack , where you can guess if your input correct or not depend time it take each char you send comparing to others which is the case here !

If we debug little bit in first time , then writing small script we will get the password which is `pAsSwOrd159!`

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71363508-ae236280-2599-11ea-907f-f70e8a06ff30.png"></p>

If we access using this password we will get information about active sessions ,each time it give us different users , what we can do here is we can leak all users we may need them in future!

If we get back now into the web app we can found simple page there without more information that lead us to another path.

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71363668-2722ba00-259a-11ea-873a-72df0cfe0812.png"></p>

Should sometimes use tools XD , mine work fine ( even after lossing all starts cuz of changing my nickname on github :D )

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71364279-08bdbe00-259c-11ea-9fe2-d4a2b0d42e3c.png"></p>

We got some useful information from the tool :

```
http://3.19.111.121/wp-content/
http://3.19.111.121/wp-login.php
..
```

We can now get idea about what type of web app is it , its for sure Wordpress !

If we get into some enumeration (manual or using **wpscan** tool ) we can get already installed plugins 

```
1 -advanced-custom-fields
2- akismet
```

By going into ACF plugin we find zip file **ACF.zip** , so if we want to get more details we can just compare this zip file with the original one `https://www.advancedcustomfields.com/downloads/`

```
git diff ACF ACF_1
```

Give us some result :

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71365900-9e5b4c80-25a0-11ea-8bfe-ae208b893260.png"></p>

As we see , there is new function `Load_Hotfix()` & `Hotfix_update()` added by the hacker as backdoor on `updates.php` file 
with comment at the end `// /server-status`

This is function use other wordpress function to make some call , do he have some 0day on that function or what ?? 

<p align="center"><img src="https://media.giphy.com/media/l2QDZFG1IXD4zbuRq/giphy.gif"></p>

Let's first debug more , he just made function called `Load_Hotfix` to confuse others with real name and hide it from other hackers too , function look all good but it just have some bad behavoir 

```
-               if ($user === "noel" && $_GET['debug'] === "1") {
-                       $ACF_Hotfix = new ACF_Updates();
-                       $ACF_Hotfix->Hotfix_update($_GET['upd']);
-               }

```

It just first work only if there is logged in user & user name is `noel` , also it check for parameter `debug` if its there it will use another paramter `upd` and call `Hotfix_update()`  which will make call to specific url !

Wait , is this hacker just was lazy hacker ?? are you sure for real ! 

<p align="center"><img src="https://media.giphy.com/media/j2nATOAdRgYZq/giphy.gif"></p>

Anyway , lets move on , as we before leaked some users when we get in `1337` service , one of this user is `noel` same name as hacker look for !

Why we just don't try log in with that password ? , we just first go to `http://3.19.111.121/wp-admin/` but it was not accessible and redirect us to index page , but as we suppose to be hacker too we can login from here too `http://3.19.111.121/wp-login.php`

And yess , we just got in guyes :) , lets check what we can do with this hacker backdoor

By sending this `http://3.19.111.121/?debug=1&upd=https://google.com` we get back result from printed using function `var_dump`

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71366670-fa26d500-25a2-11ea-919e-ce1dd1b27cb8.png"></p>

Looks like we have SSRF `Server Side Request Forgery` here , but we can do ?

First when we was trying to find some useful path , we notice that `http://3.19.111.121/server-status` give us Forbidden page , what about if we can reach this from inside ? :)

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71367046-170fd800-25a4-11ea-8a6d-46c5a7c05601.png"></p>

We just leaked some information about old & current request , we can notice onion domain too `bacq7ip6nzdyhb3o.onion` which is look the hacker domain where he store some information !

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71367659-06f8f800-25a6-11ea-89a9-77940904d976.png"></p>

First of all, its little hard to scan or dig into onion domain , why not trying to de-anonymizing it , if you are intersing into this kind of stuff you can find more here `https://github.com/AnarchoTechNYC/CTF/wiki/Tor`

So , by just checking not exsisted file like `bacq7ip6nzdyhb3o.onion/something` ,we just leaked the real IP behind this domain :)

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71367716-24c65d00-25a6-11ea-8286-d0fbf7506828.png"></p>

Yeah , so cool now we can start doing more stuff , if we just try to make some test on that login page we got some erreur 

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71367879-97cfd380-25a6-11ea-8875-a374b838e878.png"></p> 

We just know it should be xpath injection , lets exploit it :) 

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71367944-ca79cc00-25a6-11ea-8c48-83bad6368968.png"></p>  

As we have the user / password we can access this hacker website (we can bypass it too using simple payload `' or 1=1 or '` ) , but i love the hard way , it teach alot!

So now we get some tree result page

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71368111-483dd780-25a7-11ea-97fe-886106166e68.png"></p>  

By checking this path `http://3.13.238.49/bCkup/Target/172.28.13.37/payload/hack.txt` we failed and nothing was there , but if we just check `/robots.txt` we can found that he is hidding some folder which was bad rendered on tree result due to some special char

```
User-agent: *
Disallow: /bāCkupē
```

And now we get access `http://3.13.238.49/b%C4%81Ckup%C4%93/Target/172.28.13.37/payload/hack.txt` 

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71368252-b97d8a80-25a7-11ea-85df-5b2896d6f2c4.png"></p>  

So nice intro his preparing for the leak which look like will be 01/01/2020 , happy that we just get in before that day :)

But if we check again the url , he looks like he save result by target , and this ip look like local ip for something , lets use the SSRF we have to check what is there 

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71368360-07928e00-25a8-11ea-8308-df748340cda5.png"></p> 

Lets read again that page , as he just start mention some details we can notice that he talk about backup container , so probably this should be some issue here , need to find what we can do with just mysql connection page without any credz !

<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71368414-2d1f9780-25a8-11ea-9f79-4db8ecafb537.png"></p> 

By looking arround in some mysql security issue , we found that we can abuse MySQL clients to get LFI from the server, which means if we made up a mysql sever and the client just make connection to our server we can inject other request like `local data file request` that means we will make the client read for us some file data :) 

It's like **Hey client, please read the /etc/passwd file and send to it me I’ll see what I can do for you** and yeah he will read file as much he can read that with www-data privilege.

We just setup our mysql server , and run this script on different port `https://github.com/Gifts/Rogue-MySql-Server/blob/master/rogue_mysql_server.py`

And yes , BOoooM !

<p align="center"><img src="https://media.giphy.com/media/2wSe48eAUC15p38UqO/giphy.gif"></p> 

We just got the flag on `/etc/passwd` file !
<p align="center"><img src="https://user-images.githubusercontent.com/7364615/71369774-154a1280-25ac-11ea-953e-af87be6bb590.png"></p>

`Yogosha{4t_christma5_all_r0ads_Le4d_hOme}`
