from typing import Optional, Union, List

from pydantic import BaseModel

from .enums import ContentType


class Content(BaseModel):
    """
       Схема, представляющая результат поиска.

       Attributes:
           type(:obj:`ContentType`): Тип контента.
           name(:obj:`str`): Название.
           id(:obj:`int` | :obj:`str`): Уникальный идентификатор.
    """

    type: ContentType
    name: str
    id: Union[int, str]


class SearchResponse(BaseModel):
    """
       Схема, представляющая результат поиска.

       Attributes:
           text(:obj:`str`): Текст запроса, исправленный. если correct = True.
           type(:obj:`ContentType`), optional: Желаемый тип искомых значений.
           correct(:obj:`bool`), optional: Была ли включено исправление в запросе.
           page(:obj:`int`): Номер страницы запроса.
           results(:obj:`list` из :obj:`Content`), optional: Результаты запроса.
    """

    text: str = ''
    type: Optional[ContentType] = None
    correct: Optional[bool] = True,
    page: int = 0
    results: Optional[List[Content]] = []
    message: Optional[str] = ''

