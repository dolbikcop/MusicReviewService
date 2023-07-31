from enum import StrEnum, Enum


class ReactionType(Enum):
    none = 0
    like = 1
    dislike = 2


class ReactionContent(Enum):
    review = 0
    comment = 1
