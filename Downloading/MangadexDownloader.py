from DataModels.ModelsFactory import ModelsFactory
from DataModels.PageModel import PageModel
from DataModels.MangaModel import MangaModel
from DataModels.ChapterModel import ChapterModel

from Parsing.MangadexImageParser import MangadexImageParser
from Parsing.MangadexJsonParser import MangadexJsonParser

from Collecting.PagesCollector import PagesCollector

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

    def download_chapters_and_pages_info(self, manga_model :MangaModel):
        '''
        param manga_model is MangaModel object
        returns list of ChapterModel objects
        '''
        if (type(manga_model) is not MangaModel):
            raise TypeError(f"manga_model is not {type(MangaModel)}, manga_model is {type(manga_model)}")

        # get all ids from manga model
        ids = [chapter.chapter_id for chapter in manga_model.chapters]

        # get raw json of chapters (list)
        chapters_raw_json = self.json_parser.get_chapters_json(ids, 1)

        # convert json to chaptermodel
        chapters = []
        for chapter_raw_json in chapters_raw_json:
            chapters.append(ModelsFactory.create_chapter_model_by_json(chapter_raw_json))
        
        return chapters

    def download_chapters(self, pages :ChapterModel, processes :int):
        '''
        param pages is list containing PageModel objects
        param processes is number of python processes, this arg for pool 
        returns: nothing, it just download chapters in pdf format (self.fileoutput is file where it will save it)
        '''
        self.image_parser.parse_images(pages, processes, 10)
        
        self.collector.collect_pages()


