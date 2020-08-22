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

    def getChapterNumber(self):
        """

        """
        return float(self.Chapter)

    def getVolumeNumber(self):
        """
        
        """
        return float(self.Volume)


