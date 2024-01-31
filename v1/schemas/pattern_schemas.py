import re

USER_NAME_PATTERN = re.compile(r'^[^\d\s][^\d]*$')
NAME_PATTERN = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9\s]*$')