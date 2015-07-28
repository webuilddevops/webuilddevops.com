Tossing the caber
#################
:date: 2015-06-02 15:43
:author: looprock
:category: adventuresinserversitting
:tags: adventuresinserversitting, devops
:slug: tossing-the-caber
:status: draft

Ohai
====

Welcome to webuilddevops' first technical post. I've been trying to
generate some decent references via the 'Required Reading' posts, but
hope to produce some informative original content regarding how we
manage systems and the through processes that leads us to those
decisions as well. This is my first installment of what I hope to make
into a series.

Tonight we're gonna party it likes it's 2004..
==============================================

When I started at my current company as a lowly sysadmin (~senior~), I
noticed a disturbing trend. It seemed most of my day was consumed with
either pushing software updates (which I'll be covering at a later date)
and schlepping logs from servers to developers. I'm a proponent of
cutting operations out of any process where it doesn't add any value,
and while we should be looking at logs in the event of a failure, having
o copy those to a developer is no 'value add' process. Enter syslog...

Come to find out, I wasn't the visionary I thought I was, and not only
did we have a syslog server, but it was even running rsyslog, not the
stock redhat syslog everyone had come to know and loath. Apparently we'd
only been using it for network device logging, but I just needed to
hrow up apache in front of it and I could let developers log to their
hearts content and read/download from their browsers! I immediately
started working on a spec for our logging process. I pointed people at
RFC5424. I specified facilities. I even wrote sample logback
configurations to get our java developers on the road to success. This
was going to be *awesome*! With everything lined up, I threw on the
switch on some of our services that were configured properly, and ....
blew up the syslog server. Well, more specifically, I seriously
underestimated the space I needed and filled up the partition syslog was
archiving to. So after a bit of resizing and talking down some people
who's weekend on-call rotations I'd ruined, we fixed the sizing issue,
added historical log compression (at this point we still haven't needed
o do purges) and we were good! Well, we were better anyway.

You can't always get what you want
==================================

Let me tell you, when requests to copy logs and/or get access to servers
dried up, I was thrilled. However it wasn't that long before request
volume was superseded by request complexity. People were complaining
that the large logs were taking too long to load/download, so we split
logs by hour on the server side, but then people were complaining that
hey needed to go through multiple logs to see entire event streams.
Also, many services were hosted on multiple servers behind a load
balancer so people often needed to traverse multiple server directories
on top of multiple hour directories. There were also naming
discrepancies where the some things were posting to the syslog server as
FQDN, and others the short hostname, so people were often confused and
couldn't find the logs they were looking for.  We'd crossed over the
threshold of people not even knowing they needed something to them
demanding specific requirements. These were all decent and logical
requests mind you, but I wasn't quite prepared for them, nor was i sure
how to tackle them.

Apparently I wasn't the only person thinking about this domain space and
running into issues. After a little research I came across this thing
called `logstash <http://logstash.net/>`__. Now, alone this was pretty
cool, but some people had been doing some interesting work using
logstash as a transport to get logs into elasticsearch, and from there I
found a project called kibana, which provided a rather slick interface 
to be able to query and graph those logs. 

ELK FTW

Graylog2


.. include:: looprock_disqus.txt
