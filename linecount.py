#!/usr/bin/env python3

from datetime import datetime
import argparse
import pathlib




parser = argparse.ArgumentParser(   prog="Line Counter",
                                    description="Counts lines of all files in subdirectory.\n"  \
                                                "File extensions have to be specified.",         \
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter
                                )

parser.add_argument('-d', '--directory', default=".", nargs="?", help="path to directory", type=pathlib.Path)
parser.add_argument('-f', '--failed-files', default=False, action="store_true", help="if flag is set, all failed files will be printed")
parser.add_argument('-t', '--time', default=False, action="store_true", help="if flag is set, used time will be printed")
parser.add_argument('e', nargs="+", help="file extension to be parsed")




class LineCounter:

    ARGS        = parser.parse_args()
    ENCODERS    = (None, "ascii", "unicode_escape", "latin_1", "utf_32", "utf_16")

    file_count          = 0
    line_count          = 0
    filled_line_count   = 0

    failed_files        = []


    @classmethod
    def run(cls):
        if cls.ARGS.time:
            begin = datetime.now()

        cls.iter_directorys(cls.ARGS.directory.resolve())
        cls.print()

        if cls.ARGS.time:
            print()
            print("Time used:".ljust(28) + str(datetime.now() - begin))


    @classmethod
    def iter_directorys(cls, path):
        for data in path.iterdir():
            path = path / data

            if path.is_dir():
                cls.iter_directorys(path)

            elif path.is_file():
                for extns in cls.ARGS.e:
                    if path.suffix.endswith(extns):
                        cls.file_count += 1
                        for encdr in cls.ENCODERS:
                            try:
                                with path.open("r", encoding=encdr) as f:
                                    lines = f.readlines()
                                    cls.line_count += len(lines)
                                    cls.filled_line_count += len([l for l in lines if l.strip()])
                                break
                            except UnicodeDecodeError:
                                if encdr == cls.ENCODERS[-1]:
                                    if cls.ARGS.failed_files:
                                        cls.failed_files.append(path)
                                    break
                                continue
                        break


    @classmethod
    def print(cls):
        print("Files:".ljust(28) + str(cls.file_count))
        print()
        print("---Line Count---")
        print("With empty lines:".ljust(28)         + str(cls.line_count))
        print("Without empty lines:".ljust(28)      + str(cls.filled_line_count))
        print()
        print("---Average Lines per File---")
        if cls.file_count:
            print("Lines per file:".ljust(28)           + str(cls.line_count // cls.file_count))
            print("Not empty lines per file:".ljust(28) + str(cls.filled_line_count // cls.file_count))
        else:
            print("Lines per file:".ljust(28)           + str(0))
            print("Not empty lines per file:".ljust(28) + str(0))
        print()
        if LineCounter.ARGS.failed_files:
            if len(cls.failed_files):
                print("Failed to read " + str(len(cls.failed_files)) + " files:")
                for ff in cls.failed_files:
                    print(ff)
            else:
                print("No failed files.")


if __name__ == "__main__":
    LineCounter.run()
