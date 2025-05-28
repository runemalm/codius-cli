from enum import Enum


class IntentType(str, Enum):
    ADD_AGGREGATE = "add_aggregate"
    ADD_REPOSITORY = "add_repository"
    UNSURE = "unsure"
