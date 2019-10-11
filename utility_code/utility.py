def has_valid_input_range(input_to_check, range_to_check):
    has_valid_input = True
    int_input = 0
    try:
        int_input = int(input_to_check)
    except ValueError:
        has_valid_input = False

    if has_valid_input:
        if int_input < range_to_check[0]:
            has_valid_input = False
        if int_input > range_to_check[1]:
            has_valid_input = False

    return has_valid_input


def make_valid_filename(filename):
    keep_characters = (' ', '.', '_')
    out_file_name = "".join(c for c in filename if c.isalnum() or c in keep_characters).rstrip()
    return out_file_name
