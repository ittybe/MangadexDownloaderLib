from DataModels.PageModel import PageModel
import os
import re
from PIL import Image

class PagesCollector:

    def __init__(self, fileoutput, folder):
        '''
        param fileoutput is output pdf file containing all pages from folder
        param folder place where placed all pages
        '''
        self.fileoutput = fileoutput
        self.folder = folder
        
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


    def collect_pages(self):
        images = []
        for page in self._get_pages_info():
            fullpath = os.path.join(self.folder, page.get_filename())
            images.append(Image.open(fullpath))
            
        images[0].save(self.fileoutput, save_all=True, append_images=images)
