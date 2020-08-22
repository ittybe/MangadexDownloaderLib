from DataModels.ChapterModel import ChapterModel
from DataModels.MangaModel import MangaModel
from DataModels.PageModel import PageModel
import re
from DataModels.models_logger import models_logger

class ModelsFactory:
    @staticmethod
    def create_manga_model_by_json(json: dict, mangaId: int):
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
    def create_chapter_model_by_json(json :dict):
        chapterModel = None
        try:
            # get data from json 
            chapterId = json["id"]
            volume = json["volume"]
            chapter = json["chapter"]
            langCode = json["lang_code"]

            # server where placed all chapters images
            server = json["server"]
            
            # folder where placed all images on server
            hash_server = json["hash"]

            # contains all pages 
            url = f"{server}/{hash_server}/"

            # pages
            pages = []

            # fill pages with pages
            for pageNumber, fileName in enumerate(json["page_array"]):
                # url on image 
                urlImage = f"{url}/{fileName}"
                    
                # suggested filename for page (if you will save this on disk)
                pageFilename = f"{hash_server}_{pageNumber}_{fileName}"
                    
                # warning in logger if pageFilename not match pattern in ChapterModel
                pattern = ChapterModel.get_pattern_for_filename()
                if (re.match(pattern, pageFilename) == None):
                    models_logger.warning(f"{pageFilename} not match pattern {pattern}")
                else:
                    models_logger.debug(f"{pageFilename} match pattern {pattern}")

                pageModel = PageModel(pageNumber, urlImage, pageFilename)
                    
                pages.append(pageModel)

            chapterModel = ChapterModel(chapterId, pages, chapter, volume, langCode)
        except KeyError:
            raise ValueError("json argument has ivalid structure!")
        else: 
            models_logger.debug(f"chapter parsed succesfully, {id(chapterModel)}")
        return chapterModel