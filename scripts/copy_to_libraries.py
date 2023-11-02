#!/usr/bin/python

from ast import arg
import sys, getopt, os, shutil, subprocess, time
from pathlib import Path

start_time = time.time()
curr_dir = Path('.')
source_library = curr_dir
hq_library = curr_dir
lq_library = curr_dir

# take cl args
if len(sys.argv) < 2:
    print("Using default values as no arguments were seen")
    source_library = source_library / "computer_library/Music/"
    hq_library = hq_library / "pioneer_library_(HQ)/Music/"
    lq_library = lq_library / "pioneer_library_(MP3)/Music/"

    # first check if all paths exist
if not Path.is_dir(source_library) or not Path.is_dir(hq_library) or not Path.is_dir(lq_library): # todo: let hq and lq make "Music" if needed
    print("could not find one of the default directories...")
    exit(3)
else:
    try:
        opts, args = getopt.getopt(sys.argv, "i:oh:ol:")
        print("Args are: " + str(sys.argv))
    except getopt.GetoptError:
        print('copy_to_libraries.py -i <base-source folder> -oh <target hq library folder> -ol <target lq library folder>')
        sys.exit(2)
    for opt, args in opts:
        if opt == "-i":
            source_library = source_library / str(arg)
            if not Path.is_dir(source_library):
                print("Input file was not recognised.")
                sys.exit(3)
        elif opt == "-oh":
            hq_library = hq_library / str(arg)
            if not Path.is_dir(hq_library):
                print("Could not find basis for HQ library, creating...")
                os.mkdir(hq_library)
        elif opt == "-ol":
            lq_library = lq_library / str(arg)
            if not Path.is_dir(lq_library):
                print("Could not find LQ output folder, creating...")
                os.mkdir(lq_library)
        else:
            print(opt + " " + arg + " were not recognised...")

    if lq_library == hq_library:
        print("Output folders need to specify a structure for high quality and low quality, now these are the same folder...")
        print(str(hq_library) + " and " + str(lq_library))
        sys.exit(3)

extensions = set()
hq_folders = []
lq_folders = []

folders = 0
files = 0
copied = 0;
transformed = 0;
unchanged = 0;
ignored = 0;

for p in Path(source_library).glob("**/*"): # get all paths recursively
    hq_path = hq_library
    lq_path = lq_library

    partCount = 0
    for part in p.parts:
        if partCount > 1:            # remove computer_library/music from path
            hq_path = hq_path / part
            lq_path = lq_path / part
        partCount = partCount + 1
    
    if Path.is_dir(p):       
        folders = folders + 1

        # check and possibly add this folder in lq and hq
        if not Path.exists(hq_path) or not Path.is_dir(hq_path):
            os.mkdir(hq_path)
            print("Creating folder: " + str(hq_path))

        if not Path.exists(lq_path) or not Path.is_dir(lq_path):
            os.mkdir(lq_path)
            print("Creating folder: " + str(lq_path))

        hq_folders.append(str(hq_path))         # keep a list of all paths to folders that have to exist, for comparing later
        lq_folders.append(str(lq_path))

    elif Path.is_file(p):
        extensions.add(str(p.suffix)) # keep list of all extensions

        ext = p.suffix
        hq_ext = hq_path.with_suffix('.wav').resolve()
        lq_ext = lq_path.with_suffix('.mp3').resolve()
        p = p.resolve()

        if ext == '.flac' or ext == '.aif' or ext == '.aiff': # replace to .wav
            if not Path.exists(hq_ext):
                subprocess.run(['ffmpeg', '-i', str(p), str(hq_ext)])
                transformed = transformed + 1
            else:
                unchanged = unchanged + 1

            if not Path.exists(lq_ext):
                subprocess.run(['ffmpeg', '-i', str(p), '-b:a', '320k', '-vsync', '2', str(lq_ext)])
                transformed = transformed + 1
            else:
                unchanged = unchanged + 1

        elif p.suffix == '.wav':                            
            if not Path.exists(hq_ext):
                shutil.copy(p, hq_ext)
                copied = copied + 1
            else:
                unchanged = unchanged + 1

            if not Path.exists(lq_ext):                     # downgrade to mp3 for lq
                subprocess.run(['ffmpeg', '-i', str(p), '-b:a', '320k', '-vsync', '2', str(lq_ext)])
                transformed = transformed + 1
            else:
                unchanged = unchanged + 1

        elif p.suffix == '.mp3' or p.suffix == '.cue' or p.suffix == '.lrc' or p.suffix == '.m3u8': # worst case -> low quality original
            hq_mp3 = hq_ext.with_suffix('.mp3')

            if not Path.exists(hq_mp3):
                shutil.copy(p, hq_mp3)
                copied = copied + 1
            else:
                unchanged = unchanged + 1

            if not Path.exists(lq_ext):
                shutil.copy(p, lq_ext)
                copied = copied + 1
            else:
                unchanged = unchanged + 1
        else:
            ignored = ignored + 1

        files = files + 1

# finally remove every folder that's incorrectly in HQ or LQ (clutter)

# for p in Path(hq_library).glob("**/*"):
#     if p not in hq_folders:
#         shutil.rmtree(p)
#         print("Removing " + str(p) + "\n")

# for p in Path(lq_library).glob("**/*"):
#     if p not in lq_folders:
#         shutil.rmtree(p)
#         print("Removing " + str(p) + "\n")

print("\n\n====================================================================================================================================")
print("source: " + str(source_library) + "\nHQ: " + str(hq_library) + ", LQ: " + str(lq_library))

print("total amount of folders in source: {0}".format(len(hq_folders)))

print("Found extensions: " + str(extensions))

print("there were {0} folders found and {1} files found".format(folders, files))
print("{0} files have remained unchanged through the filtering".format(unchanged))
print("In total {0} files have been copied, {1} files have been transformed and {2} files have been ignored".format(copied, transformed, ignored))
print("It has taken a total of {0} seconds to run".format(time.time() - start_time))