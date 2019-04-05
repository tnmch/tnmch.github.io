---
layout: post
title: Dtune_Misc
category: BackdoorCTF  2016
---

Hi

today i will explain how i solve a task in backdoorctf 

first we have a simple ![wav](https://github.com/tnmch/tnmch.github.io/blob/master/_posts/backdoorctf-2016/Dtune.wav) file 

the sound look like someone typing his password in old phone, 
so its DTMF Tones 

convert the wav to phone number 
we get this 
```
84433033355524044477770777744225606663330337222344994462222779
```

as in the ctf the hint said that the flag is a capital alphabet

so this is not the final flag 

as this number used to write some text in the phone so  we need to use T9 

using a t9 emulator online or a simple code we can get the final flag

my code used to solve this is 
```
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class t9 {
        public static void main(String[] args) 
        {  BufferedReader inputReader=new java.io.BufferedReader(new InputStreamReader(System.in));
           String inputCode="";
           System.out.println("T9 SMS MODE Decoder");
           System.out.println("\nEnter the Value You Want to Press ");
           try 
           {
                inputCode=inputReader.readLine();
           }
           catch(IOException e)
           {
                System.out.println("IO Exception");
           }

           System.out.println(t9.decode(inputCode));        
         }
    
         private static char [][] keyPadCharSet= 
         {
            {' '},
            {'.',',','\'','?','!','\"','-','(',')'},
            {'a','b','c'},
            {'d','e','f'},
            {'g','h','i'},
            {'j','k','l'},
            {'m','n','o'},
            {'p','q','r','s'},
            {'t','u','v'},
            {'w','x','y','z'},
          };
    
          public static String decode(String inputCode)
          {
                StringBuilder outputString=new StringBuilder("");
                char[] inputCodeCharArray=inputCode.toCharArray();
                int len=inputCodeCharArray.length;
                int count=0;

                for(int i=0;i<len;i++) {
                char currentChar=inputCodeCharArray[i];
                char nextChar;

                if((i+1)!=len)  
                    nextChar=inputCodeCharArray[i+1];
                else
                    nextChar='\0';

                if(currentChar==nextChar)
                    count++;    
                else 
                {
                
                     if(currentChar!=' ') 
                     {  if(Character.isDigit(currentChar)) 
                        {    
                            int temp=Integer.parseInt(String.valueOf(currentChar)); 
                            count=count%keyPadCharSet[temp].length; 
                            char outputChar=keyPadCharSet[temp][count]; 
                            outputString.append(outputChar);    
                         }
                         else 
                         {   outputString=new StringBuilder("Please Enter Numerical value Only");
                              break;  
                         }
                      }
                      count=0; 
                  }
        }
        return outputString.toString(); 
    }
    
}

```

so the output is 
```
the flag is shbjm of EPCDHXHMCAQW
```

As in this ctf all the flag should be converted to sha256 before submit so the final text is 

```
the flag is sha256 of EPCDHXHMCAQW
```

and the flag is : `39551506faa3c2b1c1ee082adf79938da826910bf953665df882dd62b579759e`

thanks 
