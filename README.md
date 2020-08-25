# MangadexDownloaderLib
pypi package for downloading manga from mangadex 


## Usage/Example

```
import tempfile
from MangadexDownloaderLib.PagesCollector import PagesCollector
from MangadexDownloaderLib.MangadexDownloader import MangadexDownloader
from MangadexDownloaderLib.Observer import Observer
from MangadexDownloaderLib.ChapterModel import ChapterModel
import time

def only_eng_chapters(chapterModel :ChapterModel):
    return chapterModel.lang_code == "gb"

def only_first_volume(chapterModel :ChapterModel):
    return chapterModel.volume == "1"


# this is users classes, you can remake this as you wish
class ChapterObserver(Observer):
    def __init__(self, number_of_chapters):
        self.number_of_chapters = number_of_chapters
        self.already_parsed = 0

    def update(self, **kwargs):
        message = kwargs["message"]
        chapter_id = kwargs["chapter_id"]
        self.already_parsed += 1

        print(f"message: {message}, chapter id: {chapter_id}, {self.already_parsed}/{self.number_of_chapters}")

class MangaObserver(Observer):
    def update(self, **kwargs):
        message = kwargs["message"]
        manga_id = kwargs["manga_id"]
        print(f"message: {message}, manga id: {manga_id}")

class ImageParserObserver(Observer):
    def __init__(self, number_of_pages):
        self.number_of_pages = number_of_pages
        self.already_parsed = 0

    def update(self, **kwargs):
        page = kwargs["page_model"]
        path = kwargs["path_to_image"]
        message = kwargs["message"]
        self.already_parsed += 1

        print(f"message: {message}, path to file: {path}, {self.already_parsed}/{self.number_of_pages}")

class CollectorObserver(Observer):
    def __init__(self):
        self.already_parsed = []

    def update(self, **kwargs):
        number = kwargs["number_of_pdf_files"] 
        message = kwargs["message"]
        self.already_parsed.append(1)
        print(f"message: {message}, {len(self.already_parsed)}/{number}")


if __name__ == "__main__":
    t0 = time.time()

    FILEOUTPUT = r"C:\Users\Lenovo\OneDrive\Рабочий стол\onepunchman.pdf"
    # manga id from mangadex
    MANGA_ID = 7139
    NUMBER_OF_PROCESSES_IN_ONE_TIME = 8

    with tempfile.TemporaryDirectory() as tmpdirname:
        # create downloader object
        downloader = MangadexDownloader(FILEOUTPUT, tmpdirname)
        
        # attach to manga json progress event observer object, to observe parsing progress
        downloader.attach_to_manga_json_process_event(MangaObserver())

        # get manga info by id
        manga_model = downloader.download_manga_info(MANGA_ID)
        
        # filter chapters by some criteria 
        chapters = list(filter(only_eng_chapters, manga_model.chapters))

        chapters = list(filter(only_first_volume, chapters))

        
        # get ids from chapters for MangadexDownloaders method
        chapters_ids = [chapter.chapter_id for chapter in chapters]

        # number of chapters, this is for printing remain chapters to parse        
        number_of_chapters = len(chapters_ids)
        
        # attach to chapter json progress event observer object, to observe parsing progress
        downloader.attach_to_chapter_json_process_event(ChapterObserver(number_of_chapters))

        # download info about pages and chapters that we filtered by some criteria
        chapters = downloader.download_chapters_and_pages_info(chapters_ids)

        # get all pages info from chapters
        pages = []
        for chapter in chapters:
            pages += chapter.pages
        
        # basically, it just number_of_chapter var just for pages parsing
        number_of_pages = len(pages)
        downloader.attach_to_image_parser_process_event(ImageParserObserver(number_of_pages))

        # parse pages into "tempdirname" directory
        # this uses pool from multiprocessing
        downloader.download_pages(pages, NUMBER_OF_PROCESSES_IN_ONE_TIME)

        # to observe progress in pages collector 
        downloader.attach_to_collector_process_event(CollectorObserver())
        # save all pages in one pdf file (FILEOUTPUT)
        downloader.collect_pages()

    t1 = time.time()

    total = t1-t0
    print(total)
```
