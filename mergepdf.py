from argparse import ArgumentParser
from PyPDF2 import PdfFileReader, PdfFileWriter
import os, glob
import shutil
import sys

target_folder = os.path.join(os.getcwd(),'pdfs')
print(os.getcwd())

def merge(path, output_filename):
    output = PdfFileWriter()

    for file in sorted(glob.glob(os.path.join(target_folder,'page[0-9]*.pdf')), key=lambda name: int(os.path.basename(name)[4:-4])):
        if file == output_filename:
            continue
        print("Parse '%s'" % file)
        document = PdfFileReader(open(file, 'rb'))
        for i in range(document.getNumPages()):
            output.addPage(document.getPage(i))

    print("Start writing '%s'" % output_filename)
    with open(output_filename, "wb") as f:
        output.write(f)

def move_files_preprocess():
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for file in glob.glob('page[0-9]*.pdf'):
        #print('Moving {file} to path {path}'.format(file=file, path=target_folder))
        shutil.move(file, os.path.join(target_folder, file))

def instantiate_parser():
        parser = ArgumentParser()

        # Add more options if you like
        parser.add_argument("-o", "--output",
                            dest="output_filename",
                            default="merged.pdf",
                            help="write merged PDF to FILE",
                            metavar="FILE")
        parser.add_argument("-p", "--path",
                            dest="path",
                            default=".",
                            help="path of source PDF files")

        args = parser.parse_args()
        merge(args.path, args.output_filename)


def main(argv):
        move_files_preprocess()
        instantiate_parser()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
