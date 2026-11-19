"""Read OBJ records that span multiple physical lines."""


def obj_records(lines):
    parts = []
    for line in lines:
        line = line.rstrip()
        if line.endswith("\\"):
            parts.append(line[:-1])
        elif parts:
            parts.append(line)
            yield " ".join(parts)
            parts.clear()
        else:
            yield line
    if parts:
        raise ValueError("Unterminated OBJ continuation.")
