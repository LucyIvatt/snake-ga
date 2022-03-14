from enum import Enum


class Experiment(Enum):
    TEST = "test"
    CXINDPB = "cx-indpb"
    INPUT = "input"
    FINAL_ALGORITHM = "final-algorithm"


class ExperimentType(Enum):
    EXPLORATION = "exploration"
    FINAL = "final"
    FINAL_ALGORITHM = ""
