### What is it?

Seek-and-destroy is a simple python terminal utility, that finds and eliminates regular expressions matсhes in your text-based files. Practically, it's being used to get rid of malicious code injections.

### Installation

All you need to execute seek-and-destroy — pure python3 environment. None of third-side packages were used. So, no additional installations needed on Linux and MacOS, python is already there. And all you might need on Windows is to download and install Python3: https://www.python.org/downloads/

### Usage

Generally, you've got two ways to work with seek-and-destroy: either use a single regular expression or a several ones.
You can apply single regexp as parameter using `-r` or `--regexp` key:
    
    python3 seek-and-destroy.py -f foldername -r '\s(abc)\s'

Don't forget to wrap regular expression in quotes!


Or you can use multiple regular expressions from prepared list.

regexp.txt:

    \s(abc)\s
    \s(zxz)\s 
    \s(foo)\s 

Then use `-l` or `--list` key to specify your regular expressions containing file:

    python3 seek-and-destroy.py -f foldername -l regexp.txt

After execution seek-and-destroy will scan all files in `foldername` and its subfolders for every provided regular expression, replacing matches with empty string.
You can provide regular expressions with 0 or more capturing groups. In case without any capturing group whole match itself will be replaced by empty string. In other case every matching capturing group will be eliminated. DotAll mode is used, meaning dot matches newline. 

During execution current information provided, for example:

    python seek-and-destroy.py -f test_folder -l regexp.txt

    Searching in test_folder
    regex #0 found in test_folder\1.txt
    regex #1 found in test_folder\1.txt
    regex #0 found in test_folder\subfolder\1.txt
    regex #1 found in test_folder\subfolder\1.txt
    Files cleaned: 2 / Substitutions made: 6
    Log file: cleaned.log

Now we see how many inclusions were found and which files exactly contain them. All «infected» files listed in cleaned.log by the end. Such files also doubled with _bak_ files before any content manipulations. To restore original files from _bak_ files use `--restore` key:

    python seek-and-destroy.py -f foldername --restore

And don't forget to provide an operational folder with `-f` or `--folder` key!

There are two more actions you can do with _bak_ files. You can `--zip` them into archive to ensure you're have another copy of original files. And you can `--remove` _bak_ files if everything was cleaned correctly.

Thus, all available keys are listed below:

* `-r` or `--regexp` — single regular expression
* `-l` or `--list` — specify file with regular expressions
* `-f` or `--folder` — folder to search in
* `--restore` —  restore original files from bak files (should be used with `--folder`)
* `--zip` — collect all bak files in single zip file (should be used with `--folder`)
* `--remove` — remove all bak files from specified folder (should be used with `--folder`)
* `-v` or `--version` — version of seek-and-destroy
* `-h` or `--help` — show help message

### Author, license and so on

Seek-and-destroy is absolutely free. You can contact author by email: ins227@gmail.com