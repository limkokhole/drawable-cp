# -*- coding: utf-8 -*-
# The MIT License (MIT)
# Copyright (c) 2019 limkokhole@gmail.com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

__author__ = 'Lim Kok Hole'
__copyright__ = 'Copyright 2019'
__license__ = 'MIT'
__version__ = 1.1
__maintainer__ = 'Lim Kok Hole'
__email__ = 'limkokhole@gmail.com'
__status__ = 'Production'

import sys, os
import traceback
import pathlib
from shutil import copy

def quit(msgs, exit=True):
    if not isinstance(msgs, list):
        msgs = [msgs]
    for msg in msgs:
        if msg == '\n': # Empty line without bg color
            print('\n')
        else:
            print(msg)
    if exit:
        print('Abort.')
        sys.exit()

import argparse
from argparse import RawTextHelpFormatter #make --help's \n works and indentation pretty
arg_parser = argparse.ArgumentParser(
    # don't specify prefix_chars='-+/' here which causes / in path is not option value
    description='Copy relevant drawable obtained from designer to android studio project', formatter_class=RawTextHelpFormatter)
args = ""

# This still not prefect, not handle if all images same name(sound crazy but it happen now) still need manually edit the name first.
# E.g(Already cd to icons folder of designer): 
#... python3 drawable_cp.py -pd ~/AndroidStudioProjects/hello-world
# Note: Only mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi supported, you should modify the drawable_valid_path_l_proj and drawable_valid_path_l_designer if has different/more dpi for your case.
arg_parser.add_argument('--debug', action='store_true', help='Print copy log without perform copy')
arg_parser.add_argument('--prefix-designer', dest='prefix_designer', default='', help='Prefix of designer icons\'s parent folder name as ???dpi, e.g. pika-xhdpi/ means you should set prefix_designer with pika-')
arg_parser.add_argument('-d', '--dir', default='.', help='Dir path to scan. Default is current directory.')
arg_parser.add_argument('-pd', '--project-dir', dest='project_dir', required=True
                        , help='Copy to drawable folders of this project root path')
args, remaining = arg_parser.parse_known_args()

if remaining:
    quit('Redundant argument exist.')

#print(args.debug)

OS_SEP = os.sep

max_depth = None

project_base = ''
dir_path = args.dir

lp_ei = 0
d_path_len = len(dir_path)

proj_dir_path = args.project_dir

# [1] abspath already act as normpath to remove trailing os.sep
# [2] expanduser expands ~
# [3] expandvars expands $HOME

dir_path = os.path.abspath(os.path.expanduser(os.path.expandvars(dir_path)))
if not os.path.exists(dir_path):
    quit('Directory ' + dir_path + ' does not exist.')
elif not os.path.isdir(dir_path):
    quit(dir_path + ' is not a directory.')

proj_dir_path = os.path.abspath(os.path.expanduser(os.path.expandvars(args.project_dir)))
if not os.path.exists(proj_dir_path):
    quit('Directory ' + proj_dir_path + ' does not exist.')
elif not os.path.isdir(proj_dir_path):
    quit(proj_dir_path + ' is not a directory.')


proj_max_depth = 2 #only nid scan project root/<any>/src, so only nid 2 depth
proj_d_path_len = len(proj_dir_path)
#print(proj_dir_path)
#print(proj_d_path_len)

# Designer folder name prefix of dpi name:
prefix_designer  = args.prefix_designer

# This one shouldn't change bcoz it's project real folder name
prefix_proj = 'drawable-'

drawable_valid_path_l_proj = ( prefix_proj + 'mdpi',  prefix_proj + 'hdpi', prefix_proj + 'xhdpi', prefix_proj + 'xxhdpi', prefix_proj + 'xxxhdpi')
drawable_valid_path_l_designer = ( prefix_designer + 'mdpi',  prefix_designer + 'hdpi', prefix_designer + 'xhdpi', prefix_designer + 'xxhdpi', prefix_designer + 'xxxhdpi')
drawable_designer_project_map = dict(zip ( drawable_valid_path_l_designer, drawable_valid_path_l_proj ))
drawable_path_d = {}
proj_dir = None

# Test: python3 drawable_cp.py -pd ~/AndroidStudioProjects/hello-world
for lp_subdir, lp_dirs, lp_files in os.walk(proj_dir_path, topdown=True):
    if (proj_max_depth is None) or ( lp_subdir[proj_d_path_len:].count(OS_SEP) < proj_max_depth ):
        #print('real: ' + repr(lp_dirs))
        if 'src' in lp_dirs:
            for llp_subdir, llp_dirs, llp_files in os.walk(os.path.join(lp_subdir, 'src/main/res/'), topdown=True):
                parent_name = pathlib.PurePath(llp_subdir)
                if parent_name.name.endswith('res'):
                    proj_dir = llp_subdir
                    print('proj_dir: ' + proj_dir, '\n')
                    for l3_dpi in drawable_valid_path_l_proj:
                        drawable_path_d[l3_dpi] = os.path.join(proj_dir, l3_dpi)
                    #print('drawable_path_d: ' + repr(drawable_path_d))
                    break
        #else:
        #    print('else lp:' + repr(lp_subdir))

    else:
        lp_dirs[:] = [] # Don't recurse any deeper for this specific dir
        #print('wrong: ' + repr(lp_dirs))

if not proj_dir:
    quit('Not able to found drawable-???dpi folder in project path of project_dir argument.')


# Default already followlinks=False for directory in os.walk() arg
for lp_subdir, lp_dirs, lp_files in os.walk(dir_path, topdown=True): #[toprove:0] will topdown slower ?

    # No check max depth here bcoz it's scanning designer folders
    for llp_f in lp_files:

        lp_path = OS_SEP.join([lp_subdir, llp_f])
        lp_dir_name = pathlib.PurePath(lp_path).parent.name
        #print('lp_dir_name: ' + lp_dir_name)
        try:
            if lp_path.endswith('.py'):
                print('Skip python file: ' + lp_path, '\n')
                continue
            lp_ei+=1

            if prefix_designer and (prefix_designer in lp_dir_name):
                lp_dpi = lp_dir_name.split(prefix_designer)[1].strip()
            else:
                lp_dpi = lp_dir_name.strip()

            #print('Trying... [' + str(lp_ei) + '] ' + lp_path + ' [' + lp_dpi + ']')
            if lp_dir_name in drawable_valid_path_l_designer:
                #print(lp_dir_name)
                print('From ' + lp_path)
                print('To: ' + drawable_path_d[ drawable_designer_project_map[ lp_dir_name ] ], '\n')
                if not args.debug:
                    copy(lp_path, drawable_path_d[ drawable_designer_project_map[ lp_dir_name ] ])

        except IndexError as ierr:
            #print(traceback.format_exc())
            print('l_path failed: ' + lp_path)
            
