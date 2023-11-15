import re

def yaml2dict(yaml_file: str) -> dict:
    """
    Converts yaml file to dict
    """
    with open(yaml_file, 'r') as f:
        lines = f.readlines()

    return parse_lines(lines)


def parse_lines(lines: str) -> dict:
    result = {}
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line or line.startswith('#'):
            i += 1
            continue
        key, value = parse_line(line)
        if value is None:
            sublines = []
            i += 1
            while i < len(lines) and is_indented(lines[i]):
                sublines.append(lines[i][2:])
                i += 1
            value = parse_lines(sublines)
        else:
            i += 1
        result[key] = value
    return result


def parse_line(line: str):
    match = re.match(r'^([^:]+):\s*(.*)$', line)
    if match:
        key = match.group(1)
        value = match.group(2).strip()
        if not value:
            value = None
        return key, value
    else:
        return line, None


def is_indented(line: str) -> bool:
    return re.match(r'^\s{2}', line) is not None


def dict2xml(data: dict, parent: str="root") -> str:
    """
    Convert dict to xml file
    """
    xml = ""
    if isinstance(data, dict):
        for tag, value in data.items():
            xml += f"<{tag}>"
            xml += dict2xml(value, tag)
            xml += f"</{tag}>"
    else:
        xml += f"{data}"
    
    return xml