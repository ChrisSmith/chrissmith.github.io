---
layout: post
title: Facebook's Android app is wasting your battery
date:   2013-08-18 23:49:00
tags: android batterlife facebook logcat
---

Recently, while debugging a personal project, I noticed that Facebook's Android app would run the DEX loader whenever I deployed my application to my phone. This was a surprise to me because although I have the Facebook application installed, I don't use Facebook Home and wouldn't expect the app to be monitoring package installations and replacements. While technically I did give their app permission to do this, I was still astonished to see their app doing so much work for no user benefit. Given Facebook's lackluster history with Android, I decided to dig deeper and uncover more ways their application was abusing my phone's battery life. Despite disabling notification polling in the app's settings, Facebook seemed to always be running on my phone (using a precious 40MB-80MB of RAM) so I had little reason to believe they were being battery conscious. 

There are a couple of ways to monitor application activity on Android, but I took the low hanging fruit and wrote a quick application to dump the output of logcat to disk so I could process if offline. Typically log messages in logcat are lost after a period of hours but this allowed my to collect them over a series of days with no issue, just start the logcat monitor and let it run. I have to admit this is all very rough and there are better ways to make this measurement, but the speed at which this could be deployed out weighted the loss in precision. After pulling the logs off the device, I wrote a quick parser that normalized the data and inserted each line into a database for analysis. 

Quick Note, since Android 4.1 the READ_LOGS permission has been restricted to only log lines that your app has written. To read the full log you need root access and you can grant the permission like so: 

{% highlight bash %}
adb shell pm grant [packagename] android.permission.READ_LOGS
{% endhighlight %}

![active vs passive facebook activity](/assets/images/fb_activity.png)

Facebook app activity over six days. Blue lines indicate process starts, magenta lines are activity starts. The areas with blue lines but no magenta lines are periods where Facebook's app was active in the background without a user faceing screen. 

For compairison here is Twitter's activity over the same time period.
![active vs passive twitter activity](/assets/images/twitter_activity.png)

It should be perfectly clear from the graphs that Facebook's application is more active in the background than Twitter's. Those solid blue regions (no user facing activity) are just a waste of battery as far as I'm concerned. As an (over) reaction to all this I've decided to uninstall both Facebook and FB Messenger from my phone. 


Update

After about a week without the apps I've definitively seen an increase in batter life, probably about 10-20% which is huge considering its was two applications responsible for the increase. So a word of advice to all application developers out there, battery life matters! 
