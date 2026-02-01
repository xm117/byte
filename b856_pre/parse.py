import re

# patterns

NUM = "^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+\-]?\d+)?"
UNIT = "^(?:°)?[A-Za-zµΩ]+"

OP = "^[\\*/\\^]"

_OPENING_BRACKETS = "([{"
_BRACKET_PAIRS = {"(": ")", "[": "]", "{": "}"}
_CLOSING_BRACKETS = set(_BRACKET_PAIRS.values())

def _find_matching_bracket(expr):
    opener = expr[0]
    if opener not in _BRACKET_PAIRS:
        raise ValueError(f"Not a bracketed expression: {expr[:20]}")

    stack = [opener]
    i = 1
    while i < len(expr):
        ch = expr[i]
        if ch in _BRACKET_PAIRS:
            stack.append(ch)
        elif ch in _CLOSING_BRACKETS:
            if not stack or _BRACKET_PAIRS[stack[-1]] != ch:
                raise ValueError(f"Mismatched brackets near: {expr[:max(20, i+1)]}")
            stack.pop()
            if not stack:
                return i
        i += 1

    raise ValueError(f"Unclosed bracket near: {expr[:20]}")

def parse(expr):
    expr = expr.strip()
    parts = []
    while len(expr) > 0:
        expr = expr.lstrip()
        if not expr:
            break

        if expr[0] in _OPENING_BRACKETS:
            end = _find_matching_bracket(expr)
            parts.append(parse(expr[1:end]))
            expr = expr[end + 1:]
            continue

        match = None
        for reg in (NUM, UNIT, OP):
            match = re.match(reg, expr)
            if match:
                break

        if not match:
            raise ValueError(f"Cannot parse near: {expr[:20]}")

        parts.append(expr[:match.end()])
        expr = expr[match.end():]

    return parts

INT = "^[+-]?\d+([eE][+\-]?\d+)?$"

def readfile(filename):
    units = []
    properties = []
    
    with open(filename, encoding="utf-8-sig") as f:
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


