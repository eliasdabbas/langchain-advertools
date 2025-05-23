import json
from typing import Iterator, List

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader


class WebsiteLoader(BaseLoader):
    """Convert an advertools-crawled website to the langchain Document format

    This uses a website that has already been written to a jsonlines file.
    """

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def load(self) -> List[Document]:
        return list(self.lazy_load())

    def lazy_load(self) -> Iterator[Document]:
        with open(self.filepath, "r") as f:
            for line in f:
                data = json.loads(line)
                page_content = data.get("body_text", "")
                doc_id = data["url"]
                metadata = {
                    k: v for k, v in data.items() if k not in ["url", "body_text"]
                }
                yield Document(
                    page_content=page_content,
                    id=doc_id,
                    metadata=metadata,
                )
