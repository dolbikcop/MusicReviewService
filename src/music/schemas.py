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


class SearchRequest(BaseModel):
    """
        Схема, представляющая тело запроса на поиск.

        Attributes:
            text(:obj:`str`): Текст запроса.
            type(:obj:`ContentType`), optional: Желаемый тип искомых значений.
            correct(:obj:`bool`), optional: Будет ли включено исправление в запросе.
            page(:obj:`int`): Номер страницы запроса.
    """

    text: str = ''
    type: Optional[ContentType] = None
    correct: Optional[bool] = True,
    page: int = 0


class SearchResponse(SearchRequest):
    """
       Схема, представляющая результат поиска.

       Attributes:
           results(:obj:`list` из :obj:`Content`), optional: Результаты запроса.
           message(:obj:`str`), optional: Комментарий к результату запроса.
    """

    results: Optional[List[Content]]
    message: Optional[str]

