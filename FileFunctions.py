################################################################################################
## FileFunctions.py
################################################################################################
# * Description: Define functions useful in working with files.

import csv
import os
import win32file

# Store the valid drive character:
ValidDrive = ''

def ChangeDrive(path):
    """
    * Change the drive character in the passed file or folder path.
    Inputs:
    * path: Expecting a string corresponding to a file or folder path.
    Outputs:
    * Return the path with the drive character altered. If any invalid inputs were passed then return the original path.
    """
    # Return object if isn't a string:
    if not isinstance(path, str):
        return path
        
    if '//isis/common/' in path:
        path = path.replace('//isis/common/', FileFunctions.ValidDrive)
    elif ':' in path:
        path = FileFunctions.ValidDrive + path[len(FileFunctions.ValidDrive):len(path)]
        
    return path

def StripFile(filePath, val):
    """
    * Strip characters from the ends of each line in passed file.
    Inputs:
    * filePath: Path to target file.
    * val: Can be string or list of strings that you want to strip from ends of each line.
    Outputs:
    * Generates file with stripped lines to "\<FolderPath>\<FileName>_output.<extension>".
    """
    if '.' not in filePath:
        raise ValueError('Please pass a file path.')
    if os.path.exists(filePath) == False:
        raise ValueError('File does not exist.')
    if not isinstance(val, str) or isinstance(val, list):
        raise ValueError('val must be a string or list of strings.')

    ##################
    # Remove stripping characters from each line:
    ##################
    with open(filePath, 'r') as f:
        lines = [line[0:len(line)-1].lstrip(val).rstrip(val) +'\n' for line in f.readlines()]
        # Write all lines to output file:
        fileName = ExtractFileName(filePath)
        folderPath = ExtractFolderName(filePath)
        extension = ExtractExtension(filePath)
        outFile = open(folderPath + fileName + '_output' + extension, "w+")
        outFile.writelines(lines)
        outFile.close()

def ExtractExtension(path):
    """
    * Extract file extension (with '.') from passed path. 
    Inputs:
    * path: Expecting a string corresponding to file. Will return object if not satisfied.
    """
    # Return object if non-string was passed:
    if not isinstance(path, str):
        return path
    elif '.' not in path:
        return path
    return path[path.rfind('.'):len(path)]

def ExtractFileName(path):
    """
    * Extract file from passed path.
    Inputs:
    * path: Expecting a string corresponding to file. Will return object if not satisfied.
    """
    # Return original object if non-string was passed:
    if not isinstance(path, str):
        return path
    # Replace backslashes with forward slashes:
    path = path.replace('\\','/')
    if '.' not in path or '/' not in path:
        return path
    return path[path.rfind('/') + 1: path.rfind('.')]

def ExtractFolderName(path):
    """
    * Return enclosing folder of passed file, or return blank string if
    path is invalid (has no hyphens).
    """
    # Return blank string if not a directory:
    path = path.replace('\\', '/')
    if '/' not in path:
        return ''
    return path[0:path.rfind('/') + 1]

def FixPath(path):
    """
    * Return filepath with backslashes replaced with forward slashes.
    Inputs:
    * path: Expecting a string corresponding to file. Will return object if not satisfied.
    """
    if not isinstance(path, str):
        return path
    return path.replace('\\','/')

def GetValidDrive():
    """
    * Get the first valid drive to use with all paths in this application.
    Expected to be called at start of application and will flow through to all file and
    folder paths used in this application.
    """
    drives = ['K', 'N', 'O', 'P']

    for letter in drives:
        if win32file.GetLogicalDrives() >> (ord(letter.upper()) - 65 & 1) != 0:
            FileFunctions.ValidDrive = '%s:/' % letter 
            break
    if FileFunctions.ValidDrive == '':
        raise ValueError('No valid drives available among {%s}.' % ', '.join(drives))  

if __name__ == '__main__':
    StripFile("C:\Users\e652171\Desktop\RAVEN Isolated Testing\Data\ALL Vols Pull 02072019.txt", '"')