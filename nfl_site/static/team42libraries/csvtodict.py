import re


def csv_to_dict(file_name):
    # regex to get data from each line of the csv file
    row_regex = re.compile(r'(?:,|\n|^)("(?:(?:"")*[^"]*)*"|[^",\n]*|(?:\n|$))')

    csv_dict = {}  # dictionary to contain all the columns of a csv file
    misses = 0  # count how many records in a file where not extractable

    with open(file_name) as f:

        line = f.readline()  # read in fist line that should contain csv headers

        # get the headers of the csv file from first line using regex
        csv_headers = row_regex.findall(line.strip())

        lines = f.readlines()  # get all lines after the header line in the csv

    # create dictionary of arrays with csv headers (column names) as keys
    for header in csv_headers:
        csv_dict[header] = []

    # loop through each line extracted from the csv and get data
    for line in lines:
        counter = 0  # counter to cycle through values extracted from a line
        temp_list = row_regex.findall(line.strip())  # grab all values for a line

        # in the number of values extracted from the line is equal to the number of csv headers (columns)
        # data is valid and can be added to csv dictionary
        if len(csv_headers) == len(temp_list):
            for header in csv_headers:
                # if the value in a field was not empty add it to proper column else insert None
                if temp_list[counter]:
                    csv_dict[header].append(temp_list[counter])
                else:
                    csv_dict[header].append(None)
                counter += 1
        else:
            # increment counter to indicate that a line could not be added to csv dictionary
            misses += 1

    print('missed rows:', misses)

    return csv_dict


def get_player_id(firstname, lastname):
    # get columns of values
    list1 = player_dict['nameFirst']
    list2 = player_dict['nameLast']

    id_list = []  # list to hold player ids

    fullname = firstname + ' ' + lastname

    # if column length is not the same there is a problem with data
    if len(list1) == len(list1):
        # iterate through first and last name columns
        for i in range(len(list2)):
            list_name = list1[i] + ' ' + list2[i]
            # if name is found add id to list
            if fullname == list_name:
                player_id = player_dict['playerId'][i]
                id_list.append(player_id)

        # return list of ids
        return id_list
    else:
        print('Something is wrong with data')
        return None


if __name__ == '__main__':
    player_dict = csv_to_dict("archive/players.csv")

    print(get_player_id('Tom', 'Brady'))
    print(get_player_id('Jerry', 'Rice'))
    print(get_player_id('Samus', 'Aran'))
    print(get_player_id('A.J.', 'Jenkins'))


