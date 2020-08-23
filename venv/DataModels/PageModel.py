from typing import Union
import urllib
import os

class PageModel:
    """
    """


    def __init__(self, page_number :int, chapter_number :Union[int, float], volume_number :Union[int, float], hash_chapter :str, server_url :str, filename_on_server :str):
        '''
        param page_number is number of page 
        param chapter_number is number of chapter (0 if parsing number was failed)
        param volume_number is number of volume (0 if parsing number was failed)
        param hash_chapter is hash value in json
        param server_url is url where we can find all pages 
        param filename_on_server is image name of page on server 
        '''
        self.page_number = page_number

        self.chapter_number = chapter_number

        self.volume_number = volume_number

        self.hash_chapter = hash_chapter

        self.server_url = server_url

        self.filename_on_server = filename_on_server
    
    def get_url(self):
        '''
        returns url to image
        '''
        url = urllib.parse.urljoin(self.server_url, self.hash_chapter)
        url = urllib.parse.urljoin(url + "/", self.filename_on_server)
        return url

    def get_filename(self):
        '''
        returns suggested filename for image
        '''
        filename_and_ext = os.path.splitext(self.filename_on_server)
        file_extension = filename_and_ext[1]
        return f"{self.hash_chapter}_{self.volume_number}_{self.chapter_number}_{self.page_number}_{file_extension}"
    

    @staticmethod
    def get_pattern_for_filename():
        '''this is regex for filename for pages
        first [] is hash server,
        second [] is volume number (can be float)
        third [] is page number in chapter (can be float)
        third [] is page number (on server),
        forth [] is extension,

        @returns regular expression for suggested filename
        '''
        return "[a-zA-Z0-9]+_[0-9.]+_[0-9.]+_[0-9]+_.[a-zA-Z0-9]+"
    