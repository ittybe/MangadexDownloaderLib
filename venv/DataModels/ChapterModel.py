class ChapterModel:
    """
    
    """
    def __init__(self, ChapterId: int, Pages: list, Chapter: str, Volume: str, LangCode: str):
        """

        """
        self.chapter_id = ChapterId
        self.pages = Pages
        self.volume = Volume
        self.chapter = Chapter
        self.lang_code = LangCode

    def get_chapter_number(self):
        """

        """
        result = None
        try:
            result = float(self.chapter)
        except Exception:
            result = 0
        return result

    def get_volume_number(self):
        """
        
        """
        result = None
        try:
            result = float(self.volume)
        except Exception:
            result = 0
        return result
    
    
