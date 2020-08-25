from MangadexDownloaderLib.ModelsFactory import ModelsFactory
from MangadexDownloaderLib.PageModel import PageModel
from MangadexDownloaderLib.MangaModel import MangaModel
from MangadexDownloaderLib.ChapterModel import ChapterModel

from MangadexDownloaderLib.MangadexImageParser import MangadexImageParser
from MangadexDownloaderLib.MangadexJsonParser import MangadexJsonParser

from MangadexDownloaderLib.PagesCollector import PagesCollector
from MangadexDownloaderLib.Observer import Observer

import tempfile 

from typing import Union

class MangadexDownloader:
    def __init__(self, fileoutput, folder):
        self.collector = PagesCollector(fileoutput, folder)
        self.json_parser = MangadexJsonParser()
        self.image_parser = MangadexImageParser(folder)

    

    def download_manga_info(self, id :Union[int, str]):
        '''
        param id is id from mangadex 
        returns list of mangaModel
        WARNING! manga model leave pages property as None
        '''
        
        manga_raw_json = self.json_parser.get_manga_json(id)

        manga_model = ModelsFactory.create_manga_model_by_json(manga_raw_json, id)

        return manga_model

    def download_chapters_and_pages_info(self, chapters_ids :list):
        '''
        param chapters_ids is list object, containing int objects
        returns list of ChapterModel objects
        '''

        # get raw json of chapters (list)
        chapters_raw_json = self.json_parser.get_chapters_json(chapters_ids, 1)

        # convert json to chaptermodel
        chapters = []
        for chapter_raw_json in chapters_raw_json:
            chapters.append(ModelsFactory.create_chapter_model_by_json(chapter_raw_json))
        
        return chapters

    def download_pages(self, pages :ChapterModel, processes :int):
        '''
        param pages is list containing PageModel objects
        param processes is number of python processes, this arg for pool 
        returns: nothing, it just download chapters in pdf format (self.fileoutput is file where it will save it)
        '''
        self.image_parser.parse_images(pages, processes, 10)
        
        self.collector.collect_pages()

    def collect_pages(self):
        self.collector.collect_pages()


    # method for friendly-user experience
    def attach_to_chapter_json_process_event(self, observer :Observer):
        self.json_parser.chapter_progress_event.attach(observer)
    
    def detach_to_chapter_json_process_event(self, observer :Observer):
        self.json_parser.chapter_progress_event.detach(observer)
    
    def attach_to_manga_json_process_event(self, observer :Observer):
        self.json_parser.manga_progress_event.attach(observer)

    def detach_to_manga_json_process_event(self, observer :Observer):
        self.json_parser.manga_progress_event.detach(observer)
    
    def attach_to_image_parser_process_event(self, observer :Observer):
        self.image_parser.progress_event.attach(observer)

    def detach_to_image_parser_process_event(self, observer :Observer):
        self.image_parser.progress_event.detach(observer)

    def attach_to_collector_process_event (self, observer :Observer):
        self.collector.progress_event.attach(observer)

    def detach_to_collector_process_event (self, observer :Observer):
        self.collector.progress_event.detach(observer)

    
