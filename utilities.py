def load_data(file_name):
    with open(file_name, 'r') as input_file:
        lines_read = input_file.readlines()
        # Read all the data from the 5th index until before the last index
        # Parse the line into index numbers and coordinates
        # Convert coordinates to float
    name = ''
    data = []
    for text in lines_read:
        if len(text) > 0 and text[0].isdigit():
            data.append(tuple(map(float, text.strip().split(' ')[1:3])))
        elif 'NAME: ' in text:
            name = text[6:-1]
    return name, data
