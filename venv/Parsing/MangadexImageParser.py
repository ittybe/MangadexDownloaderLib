import requests
import multiprocessing
from DataModels.PageModel import PageModel
import os
from Parsing.parsing_logger import multiprocess_parsing_logger
from functools import partial

class MangadexImageParser:
    
    
    def __init__(self, folder :str):
        '''
        param folder is path to folder where were saved images 
        '''
        self.folder = folder

    def parse_image(self, page: PageModel):
        '''
        param page has type PageModel
        return : path to image result
        '''
        # save full path
        fileoutput = os.path.join(self.folder, page.filename)
        
        r = requests.get(page.url, stream=True)
        
        # write image to file 
        if r.status_code == 200:
            try:
                with open(fileoutput, "wb") as f:
                    for chunk in r: 
                        f.write(chunk)
            finally:
                r.close()
    
            return fileoutput
        else:
            raise Exception("page is not found")
        

    def parse_images(self, pages :list, processes: int, tries: int):
        '''
        param pages is list, filled with PageModel objects
        param processes is max number of process
        param tries is number of trying save image on disk for one func call
        '''

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
                if (i == tries - 1):
                    multiprocess_parsing_logger.error(f"exception has occured (parsing url is {page.url})", exc_info=True)
                    raise
        
