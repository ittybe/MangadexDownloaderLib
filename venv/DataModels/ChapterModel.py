class ChapterModel:
    """
    
    """
    def __init__(self, ChapterId: int, Pages: list, Chapter: str, Volume: str, LangCode: str):
        """

        """
        self.ChapterId = ChapterId
        self.Pages = Pages
        self.Volume = Volume
        self.Chapter = Chapter
        self.LangCode = LangCode

    def get_chapter_number(self):
        """

        """
        return float(self.Chapter)

    def get_volume_number(self):
        """
        
        """
        return float(self.Volume)


