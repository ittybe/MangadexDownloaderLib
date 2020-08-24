import requests
import json
from Parsing.parsing_logger import parsing_logger
import multiprocessing
from typing import Union

class MangadexJsonParser:

    def __init__(self, url_api_manga = "https://mangadex.org/api/manga", url_api_chapter = "https://mangadex.org/api/chapter"):
        self.url_api_manga = url_api_manga
        self.url_api_chapter = url_api_chapter

    def get_chapter_json(self, chapter_id : Union[int, str]): 
        chapter_json = None
        try:
            url_json = f"{self.url_api_chapter}/{chapter_id}"
            
            r = requests.get(url_json)
            
            if r.status_code == 404:
                raise Exception(f"chapter with id {chapter_id} on url {url_json} not found")

            # read chapter json 
            raw_json = r.content
            chapter_json = json.loads(raw_json)

        except Exception:
            parsing_logger.error("unknown exception has occured", exc_info=True)
        else:
            parsing_logger.debug(f"chapter json parsing finished {id(chapter_json)}")

        return chapter_json
    
    def get_manga_json(self, manga_id :Union[int, str]):
        manga_json = None
        try:
            url_json = f"{self.url_api_manga}/{manga_id}"
            
            r = requests.get(url_json)
            
            if r.status_code == 404:
                raise Exception(f"chapter with id {manga_id} on url {url_json} not found")

            # read chapter json 
            raw_json = r.content
            manga_json = json.loads(raw_json)

        except Exception:
            parsing_logger.error("unknown exception has occured", exc_info=True)
        else:
            parsing_logger.debug(f"manga json parsing finished {id(manga_json)}")

        return manga_json

    def get_chapters_json(self, chapters_ids :list, processes :int):
        '''

        param processes: is number of processes for pool
        param chapters_ids: list of int numbers
        '''
        chapterModels = None
        with multiprocessing.Pool(processes) as p:
            chapterModels = p.map(self.get_chapter_json, chapters_ids)

        return chapterModels

    def get_mangas_json(self, mangas_ids :list, processes :int):
        '''

        '''
        mangaModels = None
        with multiprocessing.Pool(processes) as p:
            mangaModels = p.map(self.get_manga_json, mangas_ids)

        return mangaModels

    