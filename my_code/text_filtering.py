banished_characters_for_ocr = [
    '.', '-', '_', '=', '<', '>', '"', '#', '|', '/', ':', ';', ',', '^', '§', '(', ')', '[', ']', '{', '}', ' ', '?',
    '!', '$', '«', '—', '%', '*', "\\"
]
banished_characters_for_cell_management = [
    '.', '...', '_', '=', '<', '>', '"', '#', '|', '/', ':', ';', ',', '^', '§', '(', ')', '[', ']', '{', '}', '-'
]


def out_string_noise(string, banished_characters):
    stri = string.replace('\f', '')
    stri = stri.replace('\n', '')
    stri = remove_banish_character(stri, banished_characters)
    return stri


def remove_banish_character(string, banished_characters):
    new_string = string
    for ban in banished_characters:
        new_string = new_string.replace(ban, '')
    return new_string


def remove_small_ward(string, size_threshold):
    if len(string) > size_threshold:
        return string
    else:
        return ""

