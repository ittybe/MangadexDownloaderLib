from typing import Union
import urllib
import os
import re

from MangadexDownloaderLib.models_logger import models_logger

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
    def from_filename_to_pagemodel(filepath):
        '''
        WARNING! server_url property will be None, filename_on_server will be pagenumber.extension for get_filename() method
        '''
        # by the way, PageModel get_filename() should return same value (regardless of dump or parse filename)


        # get only filename
        filename = os.path.basename(filepath)
        
        # check if filename is match the pattern
        if (re.match(PageModel.get_pattern_for_filename(), filename) == None):
            pattern = PageModel.get_pattern_for_filename()
            models_logger.warning(f"{filename} not match pattern {pattern}")
            err_message = f"filename {filename} from filepath {filepath} is not match to this \"{pattern}\" pattern"
            raise ValueError(err_message)
        
        # split filename
        splitted_filename = filename.split('_')

        hash_chapter = splitted_filename[0]
        volume_number = float(splitted_filename[1])
        chapter_number = float(splitted_filename[2])
        page_number = int(splitted_filename[3])
        server_url = None
        filename_on_server = f"{page_number}_{splitted_filename[4]}"  # "_" to match get_pattern() pattern

        pageModel = PageModel(
            page_number, 
            chapter_number, 
            volume_number, 
            hash_chapter, 
            server_url, 
            filename_on_server)

        return pageModel

    @staticmethod
    def get_pattern_for_filename():
        '''this is regex for filename for pages
        1 [] is hash chapter,
        2 [] is volume number (can be float and negative),
        3 [] is page number in chapter (can be float and negative),
        4 [] is extension,
        
        volume and chapter number is negative when parsing is failed
        @returns regular expression for suggested filename
        '''
        return "[a-zA-Z0-9]+_[0-9.-]+_[0-9.-]+_[0-9]+_.[a-zA-Z0-9]+"
    
    def __str__(self):
        return f"volume: {self.volume_number} chapter: {self.chapter_number} page: {self.page_number}, hash: {self.hash_chapter}, server url: {self.server_url}, filename on server: {self.filename_on_server}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        volume_number_compare = self.volume_number >= other.volume_number 
        chapter_number_compare = self.chapter_number >= other.chapter_number
        page_number_compare = self.page_number >= other.page_number

        # compare if volume parsed correctrly, otherwise we can compare only chapters and it will be okay 
        if self.volume_number >= 0 and other.volume_number >= 0:
            # other volume number bigger than self and not equel
            if (volume_number_compare == False):
                return True
            elif (volume_number_compare == True and self.volume_number > other.volume_number):
                return False

        # other chapter number bigger than self and not equel
        if (chapter_number_compare == False):
            return True
        elif (volume_number_compare == True and self.chapter_number > other.chapter_number):
            return False

        # other page number bigger than self and not equel
        if (page_number_compare == False):
            return True
        else: 
            # it mean that this page number is equel or bigger
            return False


    def __eq__(self, other):
        if (self.volume_number == other.volume_number 
        and self.chapter_number == other.chapter_number 
        and self.page_number == other.page_number):
            return True
        else:
            return False

    # def __gt__(self, other):
    #     return not (self < other)
    
    # def __ne__(self, other):
    #     return not (self == other)

    # def __le__(self, other):
    #     return ( self < other ) or (self == other)

    # def __ge__(self, other):
    #     return (self > other) or (self == other)
