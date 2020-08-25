from MangadexDownloaderLib.ChapterModel import ChapterModel
from MangadexDownloaderLib.MangaModel import MangaModel
from MangadexDownloaderLib.PageModel import PageModel
from MangadexDownloaderLib.models_logger import models_logger

import re
import urllib.parse
class ModelsFactory:
    @staticmethod
    def create_manga_model_by_json(json: dict, mangaId: int):
        '''
        WARNING! this method do NOT fill pages list in chapters
        '''
        mangaModel = None
        try:
            chapterRaw = json["chapter"]

            # contains all ids 
            chapters = []
            
            # fill chapters
            for key in chapterRaw:
                # get info about chapter
                chapterInfo= chapterRaw[key]

                # data for chapter
                chapterNumber = chapterInfo["chapter"]
                volumeNumber = chapterInfo["volume"]
                langCode = chapterInfo["lang_code"]

                chapter = ChapterModel(
                    key,
                    None,
                    chapterNumber,
                    volumeNumber,
                    langCode)

                # append chapter in chapters
                chapters.append(chapter)

            # result
            mangaModel = MangaModel(mangaId, chapters)
        except KeyError:
            raise ValueError("json argument has ivalid structure!")
        else: 
            models_logger.debug(f"mangaModel parsed succesfully, {id(mangaModel)}")
        return mangaModel
    @staticmethod
    def _string_to_float(string):
        '''
        for chapter/volume parsing to float
        '''
        result = None
        try:
            result = float(string)
        except Exception:
            result = 0
        return result


    @staticmethod
    def create_chapter_model_by_json(json :dict):
        chapterModel = None
        try:
            # get data from json 
            chapterId = json["id"]
            volume_number = json["volume"]
            chapter_number = json["chapter"]
            langCode = json["lang_code"]

            # server where placed all chapters images
            server = json["server"] 
            
            # folder where placed all images on server
            hash_chapter = json["hash"]   # this is really stupid but I hope it will work 

            # pages
            pages = []

            # fill pages with pages
            for pageNumber, filename in enumerate(json["page_array"]):
                # init page 
                page = PageModel(
                    pageNumber,
                    ModelsFactory._string_to_float(chapter_number),
                    ModelsFactory._string_to_float(volume_number),
                    hash_chapter,
                    server,
                    filename)
                
                # warning in logger if pageFilename not match pattern in ChapterModel
                pattern = PageModel.get_pattern_for_filename()
                if (re.match(pattern, page.get_filename()) == None):
                    models_logger.warning(f"{page.get_filename()} not match pattern {pattern}")
                    
                pages.append(page)

            chapterModel = ChapterModel(chapterId, pages, chapter_number, volume_number, langCode)
        except KeyError:
            raise ValueError("json argument has invalid structure!")
        else: 
            models_logger.debug(f"chapter parsed succesfully, {id(chapterModel)}")
        return chapterModel