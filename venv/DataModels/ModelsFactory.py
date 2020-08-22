from DataModels.ChapterModel import ChapterModel
from DataModels.MangaModel import MangaModel
from DataModels.PageModel import PageModel

class ModelsFactory:
    @staticmethod
    def createMangaModelByJson(json: dict, mangaId: int):
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
            mangaModel = MangaModel( mangaId, chapters)
            return mangaModel
        except KeyError:
            raise ValueError("json argument has ivalid structure!")
        
    @staticmethod
    def createChapterModelByJson(json):
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

            for page in json["page_array"]:
                for pageNumber, fileName in enumerate(page):
                    # url on image 
                    urlImage = f"{url}/{fileName}"
                    
                    pageModel = PageModel(pageNumber, urlImage)
                    
                    pages.append(pageModel)
            
            chapterModel = ChapterModel(chapterId, pages, chapter, volume, langCode)
            return chapterModel
        except KeyError:
            raise ValueError("json argument has ivalid structure!")
        


if __name__ == "__main__":
    import json
    with open(r'C:\Users\Lenovo\Downloads\something\454.json') as json_file:
        mangaRaw = json.load(json_file)
        manga = ModelsFactory.createMangaModelByJson(mangaRaw, 454)
        print(manga.MangaId)
        for i in manga.Chapters:
            print(i.ChapterId)
    with open(r'C:\Users\Lenovo\Downloads\something\21737.json') as json_file:
        mangaRaw = json.load(json_file)
        manga = ModelsFactory.createChapterModelByJson(mangaRaw)
        print(manga.ChapterId)
        print(manga.LangCode)