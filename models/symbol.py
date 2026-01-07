from enum import Enum
import operator

class Symbol(Enum):
    NONE = "None"
    GREATER_THAN = operator.ge  #gt is greater than, ge is greater equal
    LESS_THAN = operator.le     #lt is less than, le is less equal
    EQUAL_TO = operator.eq