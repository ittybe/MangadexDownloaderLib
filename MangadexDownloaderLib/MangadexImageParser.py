import requests
import multiprocessing
import os
from functools import partial

from MangadexDownloaderLib.PageModel import PageModel
from MangadexDownloaderLib.ProgressEvent import ProgressEvent
from MangadexDownloaderLib.parsing_logger import multiprocess_parsing_logger


class MangadexImageParser:
    
    
    def __init__(self, folder :str):
        '''
        param folder is path to folder where were saved images 
        '''
        self.folder = folder
        self.progress_event = ProgressEvent()

    def parse_image(self, page: PageModel):
        '''
        param page has type PageModel
        return : path to image result
        '''
        if type(page) is not PageModel:
            raise TypeError(f'page is not {PageModel} type, page has type {type(page)}')
        # save full path
        fileoutput = os.path.join(self.folder, page.get_filename())
        
        r = requests.get(page.get_url(), stream=True)
        
        # write image to file 
        if r.status_code == 200:
            try:
                with open(fileoutput, "wb") as f:
                    for chunk in r: 
                        f.write(chunk)
            finally:
                r.close()

            # notify all subscribers in progress event 

            kwargs = {
                "message" : f"page {page} was successfully parsed, path to image {fileoutput}",
                "path_to_image" : fileoutput,
                "page_model" : page
            }
            self.progress_event.notify(**kwargs)
            
            return fileoutput

        elif r.status_code == 404:
            raise Exception("page is not found")
        else:
            raise Exception(f"page cant be parsed because status code is not 200, status code is {r.status_code}")
        

    def parse_images(self, pages :list, processes: int, tries: int):
        '''
        param pages is list, filled with PageModel objects
        param processes is max number of process
        param tries is number of trying save image on disk for one func call
        '''
        if type(pages) is not list:
            raise TypeError(f'page is not {list} type, page has type {type(pages)}')

        parse_image_func = partial(self.parse_image_retrying_mode, tries=tries)
        with multiprocessing.Pool(processes) as p:
            p.map(parse_image_func, pages)

    def parse_image_retrying_mode(self, page, tries):
        '''
        param page has type PageModel
        param tries is number of trying save image on disk, if last try failes because of exception, then it will throw this exception 
        return : path to image result
        '''

        for i in range(tries):
            try:
                fileoutput = self.parse_image(page)
                return fileoutput
            except Exception:
                if (i <= tries - 1):
                    multiprocess_parsing_logger.error(f"exception has occured (parsing url is {page.get_url()})", exc_info=True)
                    raise
        
