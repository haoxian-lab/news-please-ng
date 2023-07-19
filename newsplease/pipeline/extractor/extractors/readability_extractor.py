from copy import deepcopy

from readability import Document

from ..article_candidate import ArticleCandidate
from .abstract_extractor import AbstractExtractor

# pylint: disable=assignment-from-no-return


class ReadabilityExtractor(AbstractExtractor):
    """This class implements Readability as an article extractor. Readability is
    a subclass of Extractors and newspaper.Article.

    """

    def __init__(self):
        self.name = "readability"

    def extract(self, item):
        """Creates an readability document and returns an
        ArticleCandidate containing article title and text.

        :param item: A NewscrawlerItem to parse.
        :return: ArticleCandidate containing the recovered article data.
        """

        doc = Document(deepcopy(item["spider_response"].body))
        description = doc.summary()

        article_candidate = ArticleCandidate()
        article_candidate.extractor = self._name
        article_candidate.title = doc.short_title()
        article_candidate.description = description

        return article_candidate
