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
    
    @staticmethod
    def get_pattern_for_filename():
        '''this is regex for filename for pages
        first [] is hash server
        second [] is page number in chapter
        third [] is filename (on server)
        forth [] is extension

        @returns regular expression for suggested filename
        '''
        return "[a-zA-Z0-9]+_[0-9]+_[a-zA-Z0-9]+.[a-zA-Z0-9]+"
