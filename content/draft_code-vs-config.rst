code vs config
##############
:date: 2015-01-19 03:30
:author: looprock
:category: adventuresinserversitting
:tags: adventuresinserversitting, devops
:slug: code-vs-config
:status: draft


Some of the system aspects of this are handled by chef for us. We have everything lined up by environment and role, which effectively act as query-able tags for us. I can do a knife search for various attributes on a system and treat that as an authoritative list, which is actually how we handle our deploys through rundeck. I wrote a provider (https://github.com/looprock/rundeck-chef-provider) for rundeck which compiles the attributes into rundeck tags.

Our deploys are managed through a shell framework that effectively acts as documentation as code. These 'plugins' contain all the logic to turn a properly bootstrapped (by chef) system into a service node, including things like creating directory structures, sometimes adding users, adding services to supervisor to manage, etc. Frankly I don't trust people to update documentation of this nature so this is the best solution I could find. I've been migrating people to newly provisioned VMs their dev/alpha environments to ensure these are regularly tested.

When I first started at Vast, I'm secure in saying deploys were pretty broken. By broken I mean, handled in a very server-huggy old school kind of way. You ssh into a box, you run some commands. These may and or may not work, you wrestle with things and finally you get a service up. Next release; rince and repeat. 

controltier - asking for forgiveness

Vast deployment model

Code == teamcity artifacts, developer owned 

config == system config, owned and managed by operations, maintained and deployed via chef

The glue == rundeck: rundeck uses chef as it's (primary) 'source of truth' via a chef provider. This provider transforms roles into tags that are used by rundeck to determine what systems to execute a command on. The cool thing about this relationship; chef roles aren't populated until a run succeedes and, provided the dependencies are properly met by the role, a system won't show up until it's properly bootstrapped. 

Vastexec - origins in confsync; a minimal shell based framework to help bootstrap code delivery. Operations provides some meta-functions like managing upness on load-balancers, managing init, etc. Developer owns 'plugin' which contains application specific logic. plugins are supposed to be idempotent, so they can be run on existing systems or will bootstrap brand new systems.

All the above are being onboarded and vetted through a private PaaS which spins up a multi-node setup behind a load-balancer to prove readiness. 

There are lots of people working on continuous delivery pipelines right now. It's been a 'thing' for quite a while and we're finally getting to the point where some companies are trying to productize this. 

.. include:: looprock_disqus.txt