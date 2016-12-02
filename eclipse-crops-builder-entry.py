#!/usr/bin/env python

# eclipse-crops-builder-entry.py
#
# This script is to present arguments to the user of the container and then
# chuck them over to the scripts that actually do the work.
#
# Copyright (C) 2016 Intel Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--workdir', default='/workdir',
                    help='The active directory once the container is running. '
                         'In the abscence of the "id" argument, the uid and '
                         'gid of the workdir will also be used for the user '
                         'in the container.')
parser.add_argument("--id",
                    help='uid and gid to use for the user inside the '
                         'container. It should be in the form uid:gid')
parser.add_argument('--project', default='/workdir/temp-project',
		    help='The project root once the container is running. '
			 'This is where the git repo is cloned. ')
parser.add_argument('--repo', default='https://github.com/crops/eclipse-crops',
                    help='The URI from where the Git repository is cloned. ')
parser.add_argument('--branch', default='master',
                    help='The branch of the Git repository to use. ')
parser.add_argument('--args', nargs=argparse.REMAINDER,
                    help='Any remaining arguments are passed to maven. ')

args = parser.parse_args()


idargs = ""
if args.id:
    uid, gid = args.id.split(":") 
    idargs = "--uid={} --gid={}".format(uid, gid)

mvnargs = ""
if args.args:
    for arg in args.args:
        mvnargs += arg if mvnargs==None else ' '.join(arg)

cmd = """usersetup.py --username=cropsuser --workdir={wd} {idargs}
         eclipse-crops-builder-launch.sh {wd} {prj} {repo} {branch} {mvnargs}""".format(wd=args.workdir, idargs=idargs, prj=args.project, repo=args.repo, branch=args.branch, mvnargs=mvnargs )
cmd = cmd.split()
os.execvp(cmd[0], cmd)
#print cmd
