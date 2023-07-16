from abc import ABCMeta, abstractmethod

# pylint: disable=unused-argument


class AbstractExtractor:
    """Abstract class for article extractors."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        self.name = None

    def _name(self):
        """Returns the name of the article extractor."""
        return self.name

    def _language(self, item):
        """Returns the language of the extracted article."""

    def _title(self, item):
        """Returns the title of the extracted article."""

    def _description(self, item):
        """Returns the description/lead paragraph of the extracted article."""

    def _text(self, item):
        """Returns the main text of the extracted article."""

    def _topimage(self, item):
        """Returns the top image of the extracted article."""

    def _author(self, item):
        """Returns the authors of the extracted article."""

    def _publish_date(self, item):
        """Returns the publish date of the extracted article."""

    def extract(self, item):
        """Executes all implemented functions on the given article and returns an
        object containing the recovered data.

        :param item: A NewscrawlerItem to parse.
        :return: ArticleCandidate containing the recovered article data.
        """
