from enum import Enum


class Experiment(Enum):
    """Enum used to determine which experiment is being ran when saving and plotting data. Helps to determine file paths & labels."""
    TEST = "test"
    CXINDPB = "cx-indpb"
    INPUT = "input"
    FINAL_ALGORITHM = "final-algorithm"


class ExperimentType(Enum):
    """Enum used to determine which experiment type is being ran when saving and plotting data. Helps to determine file paths, labels, and iteration numbers."""
    EXPLORATION = "exploration"
    FINAL = "final"
    FINAL_ALGORITHM = ""
