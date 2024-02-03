from typing import List, Generator, TypeVar

T = TypeVar('T')  # Generic type variable

class ListChunker:
    @staticmethod
    def chunks(lst: List[T], n: int) -> Generator[List[T], None, None]:
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]