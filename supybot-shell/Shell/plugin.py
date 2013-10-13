###
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2.

#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#                        Version 2, December 2004 
#
#     Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 
#
#     Everyone is permitted to copy and distribute verbatim or modified 
#     copies of this license document, and changing it is allowed as long 
#     as the name is changed. 
#
#                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#       TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 
#
#      0. You just DO WHAT THE FUCK YOU WANT TO.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import threading
import subprocess
import os


# TODO:
# - allow finer configuration as owner-requirement is hardcoded
# - throttle rapid-sending messages

class Shell(callbacks.Plugin):
    """Run shell commands like `!shell ls -l`"""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Shell, self)
        self.__parent.__init__(irc)

        self.jobs_mutex = threading.RLock()
        self.jobs = []
        self.jobs_id = 0

        self.nul = open(os.devnull, 'w')

    def shell(self, irc, msg, args, command):
        '''<command> [<args1> ...]

        Runs a command in the shell and output the result
        '''

        # start
        with self.jobs_mutex:
            self.jobs_id += 1
            job_id = self.jobs_id
            job = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE,
                                   stdin=self.nul, stderr=self.nul)
            self.jobs.append(job)

        irc.reply("Job %d started: %s" % (job_id, command))

        while True:
            line = job.stdout.readline()
            if line:
                irc.reply("Job %d: %s" % (job_id, line.rstrip()))
            if not line and job.poll() is not None:
                break

        irc.reply("Job %d ended with code %d" % (job_id, job.poll()))

        # end
        with self.jobs_mutex:
            self.jobs.remove(job)

    shell = wrap(shell, ['text', 'owner'])

Class = Shell


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
