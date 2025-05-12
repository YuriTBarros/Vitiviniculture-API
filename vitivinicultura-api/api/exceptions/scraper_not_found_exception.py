class ScraperNotFoundException(Exception):
    """
    Exception raised when attempting to retrieve a scraper for an
        unsupported category.

    Attributes:
        message (str): Description of the error.
    """

    def __init__(self, message: str = "Category not supported."):
        self.message = message
        super().__init__(self.message)
