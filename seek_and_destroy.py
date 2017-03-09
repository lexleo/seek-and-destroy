import os
import re
import sys
import argparse
from shutil import copyfile
from shutil import make_archive
from shutil import rmtree

def create_file_list(source):
    """ Creates list of files in source folder, including subdirectories"""
    file_list = []
    for root, dirs, files in os.walk(source):
        for filename in files:
            file_list.append(os.path.join(root, filename))
    return file_list


def seek_and_destroy(folder, regexp, regexp_list):
    """ Searches regular expressions from 'regexp_list' or 'regexp' in files from folder 'folder'"""
    file_list = create_file_list(os.path.relpath(folder))
    print('Searching in: {}'.format(os.path.join(os.path.dirname(__file__), folder)))

    if regexp:
        regexp_list = [regexp]

    subs = 0
    cleaned_list = []


    for filename in file_list:
        if not filename.endswith('bak'):
            try:
                with open(filename, 'r') as f:
                    text = f.read()

                backuped = False

                for n, reg in enumerate(regexp_list):
                    regex = re.compile(reg, re.DOTALL)
                    found_iter = re.finditer(regex, text)

                    chars_replaced = 0
                    regex_found = False

                    for match in found_iter:

                        if not regex_found:
                            print('regex #{} found in {}'.format(n, filename))
                            regex_found = True

                        if not backuped:
                            copyfile(filename, '{}.bak'.format(filename))
                            backuped = True
                            cleaned_list.append(filename)

                        num_groups = len(match.groups())

                        if num_groups > 0:
                            for i in range(num_groups):
                                text = text[:match.start(i+1) - chars_replaced] + text[match.end(i+1) - chars_replaced:]
                                chars_replaced = match.end(i+1) - match.start(i+1)
                                subs += 1
                        else:
                            text = text[:match.start(0) - chars_replaced] + text[match.end(0) - chars_replaced:]
                            chars_replaced = match.end(0) - match.start(0)
                            subs += 1

                        with open(filename, 'w') as clean_file:
                            clean_file.write(text)
            except:
                pass

    print('Files cleaned: {} / Substitutions made: {}'.format(len(cleaned_list), subs))

    try:
        with open('cleaned.log', 'w') as f:
            for item in cleaned_list:
                f.write('{}\n'.format(item))
        print('Log file: {}'.format(os.path.join(os.path.dirname(__file__), 'cleaned.log')))
    except:
        print('Log file cannot be created!')


def revert(folder):
    """Revert original files from the bak ones"""
    file_list = create_file_list(os.path.relpath(folder))
    try:
        how_much = 0
        for filename in file_list:
            if filename.endswith('.bak'):
                copied = False
                try:
                    copyfile(filename, filename[:-4])
                    copied = True
                except:
                    copied = False
                if copied:
                    os.remove(filename)
                    how_much += 1
        print('Done! {} files reverted!'.format(how_much))

    except:
        print('Revert cannot be perfomed!')

def archive(folder):
    """Zip all bak files in specified folder"""
    file_list = create_file_list(os.path.relpath(folder))
    try:
        temp_dir_name = '{}_bak'.format(os.path.basename(os.path.normpath(folder)))
        temp_dir = os.path.join(os.path.dirname(__file__), temp_dir_name)
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        else:
            sys.exit('{} directory already exists!'.format(temp_dir))

        bak_files = 0
        for filename in file_list:
            if filename.endswith('.bak'):
                copyfile(filename, os.path.join(temp_dir, os.path.basename(filename)))
                bak_files += 1

        if bak_files > 0:
            make_archive(temp_dir, 'zip', os.path.dirname(os.path.abspath(__file__)))
        else:
            sys.exit('No one bak file was found in {}'.format(folder))

        rmtree(temp_dir)

        print('{} bak files zipped in: {}'.format(bak_files,
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '{}.zip'.format(temp_dir_name))))

    except:
        print('Zip cannot be perfomed!')

def remove_bak(folder):
    """Delete all bak files in specified folder"""
    try:
        file_list = create_file_list(os.path.relpath(folder))
        deleted = 0
        for filename in file_list:
            if filename.endswith('bak'):
                os.remove(filename)
                deleted += 1
        if deleted == 0:
            print('No one bak file was found in {}'.format(folder))
        else:
            print('Done! {} bak files were removed'.format(deleted))
    except:
        print('Delete cannot be perfomed!')



def main():
    parser = argparse.ArgumentParser(description='Seek and Destroy', prog='seek-and-destroy')

    parser.add_argument('-l', '--list', help='File with regular expressions', default=None, action='store')
    parser.add_argument('-r', '--regexp', help='Single regular expression', default=None, action='store')
    parser.add_argument('-f', '--folder', help='Folder to search in', default=None, action='store')
    parser.add_argument('-v', '--version', help='version', action='version', version='%(prog)s 0.5')
    parser.add_argument('--revert', help='Revert files from bak files (should be used with --folder)', action='store_true')
    parser.add_argument('--zip', help='Collect all bak files in single zip file (should be used with --folder)', action='store_true')
    parser.add_argument('--removebak', help='Remove all bak files from specified folder (should be used with --folder)', action='store_true')

    args = vars(parser.parse_args())

    if not args['revert'] and not args['zip'] and not args['removebak']:

        if not args['folder']:
            args['folder'] = input("Folder: ")

        if not args['regexp'] and not args['list']:
            args['regexp'] = input("Regular expression: ")

        if args['regexp'] and args['list']:
            sys.exit('You should use either --regexp or --list at the same time')

        if args['list']:
            with open(args['list']) as f:
                regexp_list = f.readlines()
                regexp_list = [reg[:-1] for reg in regexp_list]
        else:
            regexp_list = []

        seek_and_destroy(args['folder'], args['regexp'], regexp_list)

    elif args['revert'] and args['zip']:
        sys.exit('You could not use --revert and --zip at the same time')

    elif args['removebak'] and (args['zip'] or args['revert']):
        sys.exit('You could not use --remove-bak with --zip or --revert at the same time')

    elif args['revert']:
        if not args['folder']:
            args['folder'] = input("Folder: ")
        revert(args['folder'])

    elif args['zip']:
        if not args['folder']:
            args['folder'] = input("Folder: ")
        archive(args['folder'])

    elif args['removebak']:
        shure = input("Are you sure you want to remove all the backups? Warning!!! "
                      "This operation cannot be undone!\n"
                      "Type YES if want to proceed or anything else to cancel: ")
        if shure.lower() == 'yes':
            if not args['folder']:
                args['folder'] = input("Folder: ")
            remove_bak(args['folder'])
        else:
            sys.exit('Canceled')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
