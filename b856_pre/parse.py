import re

# patterns

NUM = "^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+\-]?\d+)?"
UNIT = "^[a-z]+"

OP = "^[\\*/\\^]"

BRACKETS = "^\\(.+\\)"

def parse(expr):
    expr = expr.strip()
    parts = []
    while len(expr)>0:
        match = ""
        for reg in [NUM, UNIT, OP]:
            if match := re.match(reg, expr):
                break
        if match:
            parts.append(expr[:match.end()])
        elif match := re.match(BRACKETS, expr):
            parts.append(parse(expr[1:match.end()-1]))
        else:
            print("ERROR")
            return False
        expr = expr[match.end():].strip()

    return parts

INT = "^[+-]?\d+([eE][+\-]?\d+)?$"

def readfile(filename):
    units = []
    properties = []
    
    with open(filename) as f:
        properties = f.readline().strip().split(',')
        for line in f:
            spline = line.split(',')
            unit = {}
            for i in range(len(properties)):
                item = spline[i].strip()
                if re.match(INT, item):
                    item = int(item)
                elif item.isnumeric():
                    item = float(item)
                elif item == '':
                    item = 0
                unit[properties[i]] = item
            units.append(unit)

    return properties, units


