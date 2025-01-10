import os
import glob

def delete_files_in_output():
    files = glob.glob('output/*')
    for f in files:
        os.remove(f)

if __name__ == "__main__":
    delete_files_in_output()