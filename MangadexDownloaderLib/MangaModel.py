class MangaModel:
    """
    """
    
    def __init__(self, MangaId : int, Chapters: list):
        """
        @param Chapters contains ChapterModel objects
        """
        self.manga_id = MangaId
        self.chapters = Chapters
