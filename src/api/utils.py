import re


def handle_integrity_error(e):
    pattern = r"\"(.*?)\""
    matches = re.findall(pattern, str(e))
    if matches:
        return {"Error": f"{matches[0]}"}, 409