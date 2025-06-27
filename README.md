# Autodemy
Automated script for getting the personalized udemy course offers from multiple telegram channels.

## Introduction
This project is an automated script that collects and filters Udemy course offers shared through multiple Telegram channels and bots. Since many of these messages are duplicated or repeated across channels, the script processes and tracks each message to eliminate redundancy. It ensures users receive only unique, up-to-date course coupons, making it easier to discover and enroll in valuable Udemy courses without the noise.

### Explanation
Udemy has large number of educational courses which adds great value to our skill set. 
Udemy offers promotional offers for their courses. Along with this course instructor also provides coupons for their courses on udemy.
However, there is no single platform where coupons can be shared. So to achieve this there are multiple Telegram Channels and Telegram Bots are exist. 
Through those channels offer/coupon messages are shared which are valid for a specific time. Reading each coupon message from multiple channels is deficult as there will be duplicates with multiple channels and message may repeate over the time.
This application solves this problem by processing the message and maintaining the status of each message. 
 

### Features
1. This application program reads messages from multiple telegram channels and process it for deduplication and sends the only necessary offer message to specified private channel.
2. This program is stateful as it stores the details of the courses in **SQLite3** database and stops the spamming your private telegram channel with repeated messages over the time. This was not the case with Telegram Bots.
3. If you miss any deal then just send the title of the course to specified channel so that it registers the same. And next time when the offer is available for that particular course you get notified.
4. You can specify the specific categories,ratings,etc or more complex regX pattern to filter the messages for individual needs. 


#### Requirements
1. Need to have Telegram account.
2. Obtain the telegram api_id from [Telegram](https://my.telegram.org/auth)
3. Obtain the api_hash from [Telegram](https://my.telegram.org/auth)
4. Create Telegram channels for your messages.
5. This requires Telethon package and other packages which are mentioned in requirement.txt
6. Install the SQLite3 on your machine.

#### How to use?
1. Set the api_id, api_hash in config.py
2. Set channel ids in config.py
3. Run main.py script

#### Tip
Use cron job to run the main.py in the specified interval.
