################################################################################################
## CreateRemoteRepositoryWithLocal.py
################################################################################################
# * Create a git remote repository using local path.

import argparse
import os
import sys

def CreateRemoteRepositoryWithLocal():
    """
    * Create remote repository from local project. The provided local repository and remote repository must include the repository name in the path.
    """
    parser = argparse.ArgumentParser(prog="CreateRemoteRepositoryWithLocal", formatter_class=argparse.RawDescriptionHelpFormatter)

    desc = "Create a remote repository (that does not exist yet) using a local repository (that may or may not exist). "
    desc = desc + "Final folder of repository paths must correspond to the repository name."

    parser.usage = '%(prog)s [-h] --Local "<path>\<RepoName>" --Remote "<path>\<RepoName>"'
    parser.description = desc
    parser.add_argument('--Local', type=str, help='Path to (existing or not) local repository. Must include repo name.', nargs=1)
    parser.add_argument('--Remote', type=str, help="Path to (nonexistant) remote repository. Must include repo name.", nargs=1)

    args = parser.parse_args()

    localPath = ('' if not args.Local else str(args.Local[0]).strip())
    remotePath = ('' if not args.Remote else str(args.Remote[0]).strip())

    ##########################
    # Check that inputs were as expected
    ##########################
    errMessage = ''
    if not localPath:
        errMessage += ('\n' if errMessage else '') + 'Please provide local repository with --Local.'
    elif not os.path.exists(os.path.dirname(localPath)):
        errMessage += ('\n' if errMessage else '') + 'Folder containing local repository must exist.'

    if not remotePath:
        errMessage += ('\n' if errMessage else '') + 'Please provide remote repository with --Remote.'
    elif os.path.exists(remotePath):
        errMessage += ('\n' if errMessage else '') + 'Remote repository directory already exists.'

    # Check that git has been installed on computer:
    gitTest = os.popen('git --help').read()
    
    if gitTest == '':
        errMessage += ('\n' if errMessage else '') + 'Please install git on your machine before using this script.'

    # Raise error if any issues occurred:
    if errMessage:
        parser.error('\n************************************\n' + errMessage + '\n************************************')

    ##########################
    # Create repository:
    ##########################
    # Remove quotations from provided paths and use forward slashes:
    localPath = localPath.replace('"','')
    localPath = localPath.replace('\\','/')
    remotePath = remotePath.replace('"', '')
    remotePath = remotePath.replace('\\', '/')

    print('###############################################')
    print('CreateRemoteRepositoryWithLocal:')

    # Initialize local repository if necessary:
    if os.path.exists(localPath):
        localHiddenDirs = [path for path in os.listdir(localPath) if '.' in path]
        if '.git' not in localHiddenDirs:
            os.system('git init "' + localPath + '"')
    else:
        # Initialize if folder to local repository does not exist:
        os.system('git init "' + localPath + '"')

    # Initialize remote repository:
    os.system('git --bare init "' + remotePath + '" --shared=group')
    os.chdir(remotePath)
    os.system('git config receive.denyCurrentBranch ignore')
    os.chdir(localPath)
    os.system('git remote add origin "' + remotePath + '"')
    os.system('git add .')
    os.system('git commit -m "initial commit"')
    os.system('git push origin master')

    # Indicate finished process:
    print('###############################################')
    print('Finished creating remote repository:')
    print(remotePath)
    print('Using local repository:')
    print(localPath)
    print('###############################################')

if __name__ == '__main__':
    CreateRemoteRepositoryWithLocal()