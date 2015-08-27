code vs config
##############
:date: 2015-01-19 03:30
:author: looprock
:category: adventuresinserversitting
:tags: adventuresinserversitting, devops
:slug: code-vs-config
:status: draft

I've given an overviews to many people over the years about how we run deployments at Vast and figured it was time I committed some of it to the great internet archive. Right or wrong I've chosen to separate code and system configuration management. Much of that decision stems from the lack of adequate 'push' functionality where systems like puppet and chef are concerned. I wanted to be able to better determine ~when~ code was going to be running on a server than I felt like those tools provided. We use chef as our system configuration management service and rundeck plus a home-grown bash shell framework called vastexec to handle code deployment. 

Something about teamcity

We have everything lined up by environment and role, which effectively act as query-able tags for us. I can do a knife search for various attributes on a system and treat that as an authoritative list, which is actually how we handle our deploys through rundeck. I wrote a provider (https://github.com/looprock/rundeck-chef-provider) for rundeck which compiles the attributes into rundeck tags.

Our deploys are managed through a shell framework that effectively acts as documentation as code. These 'plugins' contain all the logic to turn a properly bootstrapped (by chef) system into a service node, including things like creating directory structures, sometimes adding users, adding services to supervisor to manage, etc. Frankly I don't trust people to update documentation of this nature so this is the best solution I could find. I've been migrating people to newly provisioned VMs their dev/alpha environments to ensure these are regularly tested.

The great thing about this setup is that the chef client needs to actually successfully run it's cookbooks before those systems show up with the proper tags via the provider, so we KNOW as that point they'll be properly bootstrapped to support he application when vastexec attempts to execute against them.

When I first started at Vast, I'm secure in saying deploys were .. not good. They were handled in a very server-huggy old school kind of way. You ssh into a box, you run some commands, things broke, you copied logs back to the developer, he applied some kind of patch, rinse, repeat. This was not terribly uncommon in other companies I'd worked at, nor was is a desired state. 

Code == teamcity artifacts, developer owned 

config == system config, owned and managed by operations, maintained and deployed via chef

The glue == rundeck: rundeck uses chef as it's (primary) 'source of truth' via a chef provider. This provider transforms roles into tags that are used by rundeck to determine what systems to execute a command on. The cool thing about this relationship; chef roles aren't populated until a run succeedes and, provided the dependencies are properly met by the role, a system won't show up until it's properly bootstrapped. 

Vastexec - origins in confsync; a minimal shell based framework to help bootstrap code delivery. Operations provides some meta-functions like managing upness on load-balancers, managing init, etc. Developer owns 'plugin' which contains application specific logic. plugins are supposed to be idempotent, so they can be run on existing systems or will bootstrap brand new systems.

All the above are being onboarded and vetted through a private PaaS which spins up a multi-node setup behind a load-balancer to prove readiness. 

There are lots of people working on continuous delivery pipelines right now. It's been a 'thing' for quite a while and we're finally getting to the point where some companies are trying to productize this. 

Command example:

vastexec -p coolvastthing -r 1.4.1-SNAPSHOT-14277 -e prod

Possibly useful global variables:

BUILD - the build ID used in teamcity URL /${BUILD}:id/

DLDIR - a unique temporary directory defined when vastexec is executed

DSTAMP - The current date in the format: YYYYMMDD

TEAMCITY - the teamcity server

Global functions 

add_lb - Add a system back to the load-balanced pool

backup source_dir  backup_dir - Backup the current deployment dir for rollback. It will move the entire source_dir into backup_dir. All arguments are mandatory and should be absolute paths.

createsymlinkrollback working_dir release_base_name suffix - For symlink style releases, document the last release version before a new deploy. release_base_name should be in the form of TCNAME/PRODUCT. Suffix means anything after the release version, RE: '-installer'.

ensuredirs "dir [ dir2 dir3 ... dirN ]" user group - Make sure dir is present, create it if it's not and chown it to user : group. dir, user and group arguments are mandatory. dir is an absolute path. Optionally, you can enter multiple directories in quotes, RE: "/data/foo /data/bar"

extract file dest_dir user group - Deploy a Teamcity artifact on the system.

fetch url_without_filename filename	- Pull an artifact from Teamcity.

findpid pidfile user pid_search_string - Try to identify a pid, first by checking the pidfile, alternately via ps (error-prone!). pidfile should be an absolute path to the pidfile. $PID variable will be set with the result.

portdie port - Wait 10 times, 6 seconds apart for the port to die.

portstart port - Wait 10 times, 6 seconds apart for the port to start listening.

procdie pid	- Wait 10 times, 6 seconds apart for the process to shut down on it's own. If it doesn't exit by itself, kill it. The best practice: use $PID for pid here, if you've used the findpid function above.

procstart pid - Wait 10 times, 6 seconds apart for the process to start

purgeoldreleases work_dir release_base_name (TCNAME/PRODUCT)] latest_release_dest - delete old release directories, leaving only the two latest ones

rm_lb - remove a system from the load-balanced pool via the /machine file

showplugins - list all the available plugins

startsvd product - Starts product supervisor managed process and makes sure it comes up.

stopservice init_script_name pid - stop a service and make sure it's dead

stopsvd product - Stops product supervisor managed process and makes sure it goes down.

testexists [file or space delimited list of things to check] - abort if files, dirs, links don't exist

urlcheck [healthcheck URL] - looks for a 200 response, but will fall back to looking for "OK" as the first part of the page content.


Anatomy of a vastexec plugin:

A plugin is a shell script comprised of a function. Ideally a plugin will be both idempotent and be able to build an application up from scratch, including actions like creating necessary directories and adding users. It's also important to use the port check, process check, and the urlcheck function to verify the service is in the state it should be at any given step. Using these tools you should be able to keep from putting a broken service in production! 
The name of the file should be [function].plugin, R.E.:

hello.plugin

hello() |br|
{ |br|
echo "Hello world" |br|
}

Examples 

A fairly basic plugin for deploying a single artifact:

coolvastthing.plugin
coolvastthing()
{
# $PRODUCT is the same as the function: coolvastthing
declare WORKDIR="/data"
declare DESTDIR="$WORKDIR/$PRODUCT" # /data/coolvastthing
declare LOGDIR="${WORKDIR}/logs/${PRODUCT}"
declare USER="cvt"
declare GROUP="cvt"
declare TCID="bt666"
declare TCNAME="cool-vast-thing" # the artifact path is different in teamcity so we're using this variable
declare PIDFILE="/tmp/${TCNAME}-service.pid"
declare TESTPORT="8090"
declare TESTURL="http://localhost:${TESTPORT}/healthcheck"

# take the node out of the load-balancer
rm_lb

# make sure DLDIR, DESTDIR, and LOGDIR all exist and have the right permissions
ensuredirs "${DLDIR} ${DESTDIR} ${LOGDIR}" $USER $GROUP

# this creates a file ${DESTDIR}/.rollback_version which we'll use to roll back the release if needed
createsymlinkrollback ${DESTDIR} ${TCNAME} "-installer"

# find the pid of the current process. If no pidfile is found, we'll look in the process list for a process owned by the user which contains the string
# "cp cool-vast-thing". This is a good match for finding our java  processes, which generally contain "-cp <teamcity artifact>"
findpid ${PIDFILE} ${USER} "cp ${TCNAME}"

# stop the process; ensure it's dead and not listening on it's testport
stopservice ${PRODUCT} ${PID}
portdie ${TESTPORT}

# Download: http://teamcity.vast.com/repository/download/bt666/14277:id/cool-vast-thing/target/cool-vast-thing-1.4.1-SNAPSHOT-14277-installer.tar.gz
FILEBASE="${TCNAME}-${RELEASE}-installer"
FILENAME="${FILEBASE}.tar.gz"
URLPATH="http://${TEAMCITY}/repository/download/${TCID}/${BUILD}:id/target/"
fetch ${URLPATH} ${FILENAME} 

# extract the contents of cool-vast-thing-1.4.1-SNAPSHOT-14277-installer.tar.gz to /data/coolvastthing/cool-vast-thing-1.4.1-SNAPSHOT-14277-installer
extract ${FILENAME} ${DESTDIR}/${FILEBASE} ${USER} ${GROUP}

# link the release to current
ln -s ${DESTDIR}/${FILEBASE} $DESTDIR/current

# start the process again
echo "OK: restarting service $PRODUCT"
service ${PRODUCT} start
sleep 2
# find the new pid
findpid ${PIDFILE} ${USER} "cp ${TCNAME}"
# make sure the process starts
procstart ${PID}
# make sure the port is listening
portstart ${TESTPORT}
# verify the service is reporting OK on the healthcheck URL
urlcheck ${TESTURL}

# clean up after ourselves
# remove old releases, leaving only the last two
purgeoldreleases ${DESTDIR} ${TCNAME} ${FILEBASE}
echo "OK: deleting temporary download dir: ${DLDIR}"
rm -rf ${DLDIR}

# return the system to the load-balancer
add_lb
}


.. include:: looprock_disqus.txt