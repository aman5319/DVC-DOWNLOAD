DVC DOWNLOAD
==============

Use-Case
=============

​		Let suppose we have a DVC tracked central repository which contains different kinds of Datasets and few other saved items on Amazon S3. Now many developers work on the same dataset  or they want to use certain stuff for their project from the centralized repo.

For this particular task we have [`dvc get`](https://dvc.org/doc/command-reference/get) command which can download a file or directory tracked by DVC or by Git into the current working directory.

```bash
# Template dvc get code which can be used to pull one file.
dvc get {git_url_for_centralized_repo} {file_path_to_pull} -o {output_path_in_current_working_directory}

```

This library helps to automate the task of pulling multiple files from the centralized repo.

Working
=========

There is only one python script which contains all the logic [download.py](./download.py).

The user has to provide data to be pulled from the centralized repo in a CSV file. Using that CSV file the python generates an [Expect](https://core.tcl-lang.org/expect/index) script which is then executed.

The CSV file should contain four columns 

###  `file`,`output`,`git_url`,`password`
file :- The file with full path in the centralized repo.
output :- where to store the file in current directory.
git_url :- The Git url of the DVC tracked file
password :- For private repo password is needed

### sample.csv file

| file                                                    | output                | git_url                            | password |
| ------------------------------------------------------- | --------------------- | ---------------------------------- | -------- |
| processed_data/Hindi/Hindi_Processed_15K_Sentiment.csv  | ./data/processed_data | https://aman5319@bitbucket.org/x/z | xyz      |
| saved_outputs/Hindi/Hindi_SentencePiece_Tokenizer.model | .                     | https://aman5319@bitbucket.org/x/z | xyz      |

Dependencies
========

Install Expect in your system.

For Ubuntu `sudo apt-get install expect` 

Installation
======
`pip install dvcdownload`

Usage
========

```bash
# Help
$ dvcdownload --help
Usage: dvcdownload [OPTIONS] COMMAND [ARGS]...

Options:
  -f, --filename TEXT  The CSV file path which should have columns as:- file,
                       output, git_url[Optional], password[Optional]
  --help               Show this message and exit.

Commands:
  different  Use if the csv file contains all the url and password for each...
  same       Use if same git url and password to be used for all objects in...

```

By default the CSV filename is `file_info.csv` if used same file name the `--filename` option is not required.

There are two sub commands

1. `same`

   ```bash
   # Sub command same help
   $ dvcdownload same --help
   Usage: dvcdownload same [OPTIONS]
   
     Use if same git url and password to be used for all objects in the csv
     file.
   
   Options:
     -u, --git_url TEXT   Enter the git url  [required]
     -p, --password TEXT  Enter the password  [required]
     --help               Show this message and exit.
   
   ```

   If all the data to be pulled from same repo then the file name and output will be taken from the csv file and git_url , password has to be provided explicitly by the user.

   ```bash
   # same (By default filename is file_info.csv) 
   $ dvcdownload same --git_url=https://aman5319@bitbucket.org/x/z --password=xyz
   # same with another filename option
   $ dvcdownload --filename=mycsv.csv same --git_url=https://aman5319@bitbucket.org/x/z --password=xyz
   ```

   

2. `different` 

   ```bash
   # sub command different help
   $ dvcdownload different --help
   Usage: dvcdownload different [OPTIONS]
   
     Use if the csv file contains all the url and password for each objects.
   
   Options:
     --help  Show this message and exit.
   
   ```

   Here if you want the script to take git_url and password from the CSV file then use this. Here different git urls and their password can be used to fetch files from different repos into the current directory.

   ```bash
   # same (By default filename is file_info.csv) 
   $ dvcdownload different
   # same with another filename option
   $ dvcdownload --filename=mycsv.csv different
   ```

   

