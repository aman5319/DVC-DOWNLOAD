import csv
import click
from urllib.parse import urlsplit,urlunsplit
import os , stat
from pathlib import Path
from termcolor import colored
b = ['#!/usr/bin/expect -f\n',
 '#\n', 
    '# Note that autoexpect does not guarantee a working script.  It\n',
 '# necessarily has to guess about certain things.  Two reasons a script\n',
 '# might fail are:\n',
 '#\n',
 '# 1) timing - A surprising number of programs (rn, ksh, zsh, telnet,\n',
 '# etc.) and devices discard or ignore keystrokes that arrive "too\n',
 '# quickly" after prompts.  If you find your new script hanging up at\n',
 '# one spot, try adding a short sleep just before the previous send.\n',
 '# Setting "force_conservative" to 1 (see below) makes Expect do this\n',
 '# automatically - pausing briefly before sending each character.  This\n',
 '# pacifies every program I know of.  The -c flag makes the script do\n',
 '# this in the first place.  The -C flag allows you to define a\n',
 '# character to toggle this mode off and on.\n',
 '\n',
 'set force_conservative 0  ;# set to 1 to force conservative mode even if\n',
 "\t\t\t  ;# script wasn't run conservatively originally\n",
 'if {$force_conservative} {\n',
 '\tset send_slow {1 .1}\n',
 '\tproc send {ignore arg} {\n',
 '\t\tsleep .1\n',
 '\t\texp_send -s -- $arg\n',
 '\t}\n',
 '}\n',
 '\n',
 '#\n',
 '# 2) differing output - Some programs produce different output each time\n',
 '# they run.  The "date" command is an obvious example.  Another is\n',
 '# ftp, if it produces throughput statistics at the end of a file\n',
 '# transfer.  If this causes a problem, delete these patterns or replace\n',
 '# them with wildcards.  An alternative is to use the -p flag (for\n',
 '# "prompt") which makes Expect only look for the last line of output\n',
 '# (i.e., the prompt).  The -P flag allows you to define a character to\n',
 '# toggle this mode off and on.\n',
 '#\n',
 '# Read the man page for more info.\n',
 '#\n',
 '# -Don\n',
 '\n',
 '\n',
]
def get_autoexpect_code(file,output,giturl,password):
    url = urlsplit(giturl)
    l =["set timeout -1\n",
       f"spawn dvc get {giturl} {file} -o {output}\n",
        "match_max 100000\n",
        f"""expect -exact "Password for '{urlunsplit((url[0],url[1],"","",""))}': "\n""",
        f'send -- "{password}\\r"\n',
        "expect eof\n",
       ]
    return l

def write_file(text_list):
    with open("script.exp","w") as f:
        f.writelines(text_list)
    os.chmod("script.exp",stat.S_IRWXU|stat.S_IRWXO|stat.S_IRWXG)
    os.system("./script.exp")
    os.system("rm script.exp")
    print(colored("Done","green"))
    
def check_exists(path):
    if not path.exists():
        path.mkdir(parents=True,exist_ok=True)
        print(colored(f"{path} doesn't exists. Creating the path and using it","red"))
    return str(path)

def execute(same,file_path,**kwargs):
    with open(file_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            b.extend(get_autoexpect_code(row["file"],
                                         check_exists(Path(row["output"])),
                                         kwargs["git_url"]if same else row["git_url"]  ,
                                         kwargs["password"] if same else row["password"]))
        write_file(b)

    
    
@click.group()
@click.option("-f","--filename",default=f"{Path(__file__).parent}/file_info.csv",required=False,help="The CSV file path which should have columns as:- file, output, git_url[Optional], password[Optional]")
def cli(filename):
    setattr(cli,"filename",filename)


@cli.command()
@click.option("-u","--git_url",required=True,prompt=True,help="Enter the git url")
@click.option("-p","--password",required=True,prompt=True,hide_input=True,help="Enter the password")
def same(git_url,password):
    """Use if same git url and password to be used for all objects in the csv file."""
    execute(True,cli.filename,git_url=git_url,password=password)
    
@cli.command()
def different():
    """Use if the csv file contains all the url and password for each objects. """
    execute(False,cli.filename)

        
if __name__=="__main__":
    cli()