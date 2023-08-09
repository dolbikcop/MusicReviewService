from enum import Enum


class ReactionType(Enum):
    like = 1
    dislike = 2


class ReactionContent(Enum):
    review = 0
    comment = 1
