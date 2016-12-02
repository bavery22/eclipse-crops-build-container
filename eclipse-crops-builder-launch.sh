#!/bin/bash
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

# Establish the workspace and project
workspace=$1
cd $workspace

# Set properties below
if [[ -d $workspace/temp-project ]]; then
  rm -rf $workspace/temp-project
fi
if [[ -d $2 ]]; then
  cp -R $2 $workspace/temp-project
else
  git clone --branch $4 $3 $workspace/temp-project
fi
project=$workspace/temp-project

# NOTE: $5 is 'args' passed to -entry.py (argparse.REMAINDER)
args=$5

# Eclipse needs a display
tightvncserver -rfbport 5900 -geometry 1280x1024 -name ECLIPSE-CROPS-BUILDER
export DISPLAY=:1
fluxbox -display $DISPLAY &

cd $workspace/temp-project
if [[ $args ]]; then
  mvn $args
else
  mvn -fae verify
fi
