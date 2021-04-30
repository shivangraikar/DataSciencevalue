def treat_input(data):
    """
    Treats the input json to keep it in the same format as the coeficcients
    """
    treated_data = dict()
    for key, value in data.items():
        if key[0] == 'Q':
            treated_data[value] = 1
        else:
            treated_data[key] = 1
    return treated_data