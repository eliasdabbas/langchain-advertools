import pytest
from langchain.docstore.document import Document
from langchain_advertools.website_loader import WebsiteLoader


class TestWebsiteLoader:
    def test_load_valid_crawl(self):
        loader = WebsiteLoader("tests/data/valid_crawl.jsonl")
        docs = loader.load()
        assert len(docs) == 3
        assert isinstance(docs[0], Document)
        assert docs[0].page_content == "This is page 1."
        assert docs[0].metadata["title"] == "Page 1 Title"
        assert docs[0].metadata["meta_desc"] == "Description for page 1."
        assert docs[1].page_content == "Content of page 2."
        assert docs[2].page_content == "Page three has some text."
        assert "meta_desc" not in docs[2].metadata  # Check for missing optional field

    def test_lazy_load_valid_crawl(self):
        loader = WebsiteLoader("tests/data/valid_crawl.jsonl")
        docs_generator = loader.lazy_load()
        docs = list(docs_generator)
        assert len(docs) == 3
        assert isinstance(docs[0], Document)
        assert docs[0].page_content == "This is page 1."
        assert docs[0].metadata["title"] == "Page 1 Title"
        assert docs[1].page_content == "Content of page 2."
        assert docs[2].page_content == "Page three has some text."

    def test_load_missing_url(self):
        loader = WebsiteLoader("tests/data/missing_url_crawl.jsonl")
        with pytest.raises(KeyError):
            loader.load()

    def test_lazy_load_missing_url(self):
        loader = WebsiteLoader("tests/data/missing_url_crawl.jsonl")
        docs_generator = loader.lazy_load()
        with pytest.raises(KeyError):
            list(docs_generator)

    def test_load_missing_body_text(self):
        loader = WebsiteLoader("tests/data/missing_body_text_crawl.jsonl")
        docs = loader.load()
        assert len(docs) == 2

        doc_without_body = None
        doc_with_body = None

        for doc in docs:
            if doc.id == "https://example.com/page1":
                doc_without_body = doc
            elif doc.id == "https://example.com/page2":
                doc_with_body = doc

        assert doc_without_body is not None, "Doc for page1 not found"
        assert doc_without_body.page_content == ""
        assert doc_without_body.metadata["title"] == "Page 1 Title"

        assert doc_with_body is not None, "Doc for page2 not found"
        assert doc_with_body.page_content == "Content of page 2."
        assert doc_with_body.metadata["title"] == "Page 2 Title"

    def test_lazy_load_missing_body_text(self):
        loader = WebsiteLoader("tests/data/missing_body_text_crawl.jsonl")
        docs_generator = loader.lazy_load()
        docs = list(docs_generator)
        assert len(docs) == 2

        doc_without_body = None
        doc_with_body = None

        for doc in docs:
            if doc.id == "https://example.com/page1":
                doc_without_body = doc
            elif doc.id == "https://example.com/page2":
                doc_with_body = doc

        assert doc_without_body is not None, "Doc for page1 not found"
        assert doc_without_body.page_content == ""
        assert doc_without_body.metadata["title"] == "Page 1 Title"

        assert doc_with_body is not None, "Doc for page2 not found"
        assert doc_with_body.page_content == "Content of page 2."
        assert doc_with_body.metadata["title"] == "Page 2 Title"

    def test_load_malformed_crawl(self):
        loader = WebsiteLoader("tests/data/malformed_crawl.jsonl")
        # pandas.read_json with lines=True might skip the malformed line
        # or raise an error depending on the nature of malformation and pandas version.
        # If it skips, the test should assert the number of valid documents.
        # If it raises, pytest.raises should be used.
        # Based on the provided file, it's likely ValueError due to
        # "this is not valid json"
        with pytest.raises(ValueError):
            loader.load()

    def test_lazy_load_malformed_crawl(self):
        loader = WebsiteLoader("tests/data/malformed_crawl.jsonl")
        docs_generator = loader.lazy_load()
        with pytest.raises(ValueError):
            list(docs_generator)
