A plugin to allow owner to run shell commands through the bot.
Only the bot owner can use this plugin, but the commands that can be run are not restricted, so be extremely careful as it could become a backdoor if an evil user gains owner access!

Sample:

<owner> bot: shell ls -l /tmp/foo
<bot> owner: Job 1 started: ls -l /tmp/foo
<bot> owner: Job 1: total 4
<bot> owner: Job 1: drwxr-xr-x 2 owner owner 4096 Mar 29 16:20 bar
<bot> owner: Job 1 ended with code 0

<non-owner> bot: shell shutdown -h now
<bot> non-owner: Error: You don't have the owner capability. If you think that you should have this capability, be sure that you are identified before trying again. The 'whoami' command can tell you if you're identified.

This plugin is licensed under the WTFPL - Do What the Fuck You Want to Public License [http://www.wtfpl.net]
