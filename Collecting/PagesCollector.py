from DataModels.PageModel import PageModel
import os
import re
from PIL import Image
import tempfile
from io import BytesIO
from PyPDF2 import PdfFileMerger, PdfFileReader
from Notifying.ProgressEvent import ProgressEvent


class PagesCollector:

    def __init__(self, fileoutput, folder):
        '''
        param fileoutput is output pdf file containing all pages from folder
        param folder place where placed all pages
        '''
        self.fileoutput = fileoutput
        self.folder = folder
        self.progress_event = ProgressEvent()
        
    def _get_pages_info(self):
        '''
        returns list of pages, parsed from self.folder
        '''
        pattern = PageModel.get_pattern_for_filename()
        
        list_of_files_in_dir = os.listdir(self.folder)

        pages = []
        for file in list_of_files_in_dir:
            if (re.match(pattern, file) != None):
                page = PageModel.from_filename_to_pagemodel(file)
                pages.append(page)
        
        return pages

    def _collect_pages_in_separate_files(self, number_of_pages_in_one_file):
        '''
        param number_of_pages_in_one_file this it number of pages in one pdf file
        returns: absolute path to pdf files
        '''
        # save all absolute path of pdf separate files in here
        paths_to_separate_pdf_files = []

        # get pages
        pages = self._get_pages_info()

        # sort pages by volume chapter page number  
        pages.sort()
       
        # have no idea how does it work, but its working, so i dont really care
        # it s split pages on group of pages according to number_of_pages_in_one_file value
        pages_group = [pages[x:x+number_of_pages_in_one_file] for x in range(0, len(pages),number_of_pages_in_one_file)]

        # add in images Image objects
        for group in pages_group:
            
            # create temp filename and close this 
            separate_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", mode="w+b")
            separate_file.close()
            
            # fullpath
            separate_file = separate_file.name

            images = []
            for page in group:
                # get fullpath to image
                fullpath = os.path.join(self.folder, page.get_filename())
                
                # open 
                image = Image.open(fullpath)
                
                # these things are important. I dont really why, but these are 
                # these are important because it will prevent some error in PIL package (Error memory)
                image.load()
                image = image.convert("RGB")

                # append image to images list
                images.append(image)

            # save pdf file
            images[0].save(separate_file, save_all=True, append_images=images)

            # add to paths path to temp file
            paths_to_separate_pdf_files.append(separate_file)

            # notify all subscribers in progress event 
            kwargs = {
                "message" : f"created pdf tmp file {separate_file}",
                "number_of_pdf_files" : len(pages_group)
            }
            self.progress_event.notify(**kwargs)

        return paths_to_separate_pdf_files
        
    def _merge_pdf_files(self, paths):
        # Call the PdfFileMerger
        mergedObject = PdfFileMerger()
        
        for filepath in paths:
            mergedObject.append(PdfFileReader(filepath, 'rb'))
        
        # Write all the files into a fileoutput
        mergedObject.write(self.fileoutput)

    def collect_pages(self):
        
        paths = self._collect_pages_in_separate_files(25)
        
        self._merge_pdf_files(paths)

        for path in paths:
            os.remove(path)