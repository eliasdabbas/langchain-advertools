import advertools as adv
import pandas as pd
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader


class WebsiteLoader(BaseLoader):
    """Convert an advertools-crawled website to the langchain Document format

    This uses a website that has already been written to a jsonlines file.
    """

    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        df = pd.read_json(self.filepath, lines=True, chunksize=1)
        docs = []
        for line in df:
            doc = Document(
                page_content=line.get("body_text").iloc[0],
                id=line["url"].iloc[0],
                metadata={
                    k: v
                    for k, v in line.to_dict("records")[0].items()
                    if k not in ["url", "body_text"]
                },
            )
            docs.append(doc)
        return docs

    def lazy_load(self):
        df = pd.read_json(self.filepath, lines=True, chunksize=1)
        for line in df:
            yield Document(
                page_content=line.get("body_text").iloc[0],
                id=line["url"].iloc[0],
                metadata={
                    k: v
                    for k, v in line.to_dict("records")[0].items()
                    if k not in ["url", "body_text"]
                },
            )
