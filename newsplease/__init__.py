import datetime
import os
import sys
from typing import Optional
import urllib
from bs4.dammit import EncodingDetector
from dotmap import DotMap


from newsplease.crawler.items import NewscrawlerItem
from newsplease.crawler.simple_crawler import SimpleCrawler
from newsplease.pipeline.extractor import article_extractor
from newsplease.pipeline.pipelines import ExtractedInformationStorage
from newsplease.news_article import NewsArticle


sys.path.append(os.path.dirname(os.path.realpath(__file__)))


class EmptyResponseError(ValueError):
    pass


class NewsPlease:
    """
    Access news-please functionality via this interface
    """

    @staticmethod
    def from_warc(warc_record, decode_errors="replace", fetch_images=True):
        """
        Extracts relevant information from a WARC record. This function does not invoke scrapy but only uses the article
        extractor.
        :return:
        """
        raw_stream = warc_record.raw_stream.read()
        encoding = None
        try:
            encoding = (
                warc_record.http_headers.get_header("Content-Type")
                .split(";")[1]
                .split("=")[1]
            )
        except:
            pass
        if not encoding:
            encoding = EncodingDetector.find_declared_encoding(raw_stream, is_html=True)
        if not encoding:
            # assume utf-8
            encoding = "utf-8"

        try:
            html = raw_stream.decode(encoding, errors=decode_errors)
        except LookupError:
            # non-existent encoding: fallback to utf-9
            html = raw_stream.decode("utf-8", errors=decode_errors)
        if not html:
            raise EmptyResponseError()
        url = warc_record.rec_headers.get_header("WARC-Target-URI")
        download_date = warc_record.rec_headers.get_header("WARC-Date")
        article = NewsPlease.from_html(
            html, url=url, download_date=download_date, fetch_images=fetch_images
        )
        return article

    @staticmethod
    def from_html(html, url=None, download_date=None, fetch_images=True):
        """
        Extracts relevant information from an HTML page given as a string. This function does not invoke scrapy but only
        uses the article extractor. If you have the original URL make sure to provide it as this helps NewsPlease
        to extract the publishing date and title.
        :param html:
        :param url:
        :return:
        """
        extractor = article_extractor.Extractor(
            (
                ["newspaper_extractor"]
                if fetch_images
                else [("newspaper_extractor_no_images", "NewspaperExtractorNoImages")]
            )
            + ["readability_extractor", "date_extractor", "lang_detect_extractor"]
        )

        title_encoded = "".encode()
        if not url:
            url = ""

        # if an url was given, we can use that as the filename
        filename = urllib.parse.quote_plus(url) + ".json"

        item = NewscrawlerItem()
        item["spider_response"] = DotMap()
        item["spider_response"].body = html
        item["url"] = url
        item["source_domain"] = (
            urllib.parse.urlparse(url).hostname.encode() if url != "" else "".encode()
        )
        item["html_title"] = title_encoded
        item["rss_title"] = title_encoded
        item["local_path"] = None
        item["filename"] = filename
        item["download_date"] = download_date
        item["modified_date"] = None
        item = extractor.extract(item)

        tmp_article = ExtractedInformationStorage.extract_relevant_info(item)
        final_article = ExtractedInformationStorage.convert_to_class(tmp_article)
        return final_article

    @staticmethod
    def from_url(url, timeout=None) -> Optional[NewsArticle]:
        """
        Crawls the article from the url and extracts relevant information.
        :param url:
        :param timeout: in seconds, if None, the urllib default is used
        :return: A NewsArticle object containing all the information of the article. Else, None.
        :rtype: NewsArticle, None
        """
        articles = NewsPlease.from_urls([url], timeout=timeout)
        if url in articles.keys():
            return articles[url]
        else:
            return None

    @staticmethod
    def from_urls(urls, timeout=None):
        """
        Crawls articles from the urls and extracts relevant information.
        :param urls:
        :param timeout: in seconds, if None, the urllib default is used
        :return: A dict containing given URLs as keys, and extracted information as corresponding values.
        """
        results = {}
        download_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if len(urls) == 0:
            pass
        elif len(urls) == 1:
            url = urls[0]
            html = SimpleCrawler.fetch_url(url, timeout=timeout)
            if html:
                results[url] = NewsPlease.from_html(html, url, download_date)
        else:
            results = SimpleCrawler.fetch_urls(urls)
            for url in results:
                results[url] = NewsPlease.from_html(results[url], url, download_date)

        return results

    @staticmethod
    def from_file(path):
        """
        Crawls articles from the urls and extracts relevant information.
        :param path: path to file containing urls (each line contains one URL)
        :return: A dict containing given URLs as keys, and extracted information as corresponding values.
        """
        with open(path) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        urls = list(filter(None, content))

        return NewsPlease.from_urls(urls)
