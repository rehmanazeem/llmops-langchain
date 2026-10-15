from llmops.document_loader import DocumentLoader, ParsingMethod


class StubMethod(ParsingMethod):
    def read_document(self, file_path):
        return [file_path]


def test_loader_delegates_to_method():
    assert DocumentLoader(StubMethod()).get_document("a.pdf") == ["a.pdf"]
