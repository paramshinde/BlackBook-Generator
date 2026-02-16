from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    @abstractmethod
    def improve_section(self, section_title: str, content: str, target_words: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def generate_diagram_spec(self, project_title: str) -> dict:
        raise NotImplementedError
