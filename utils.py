
def longest_string(list_string):
    # find the longest string
    # create a new list of string lengths using a list comprehension
    lengths = [len(s) for s in list_string]
    # find the index of the longest string in the original list
    longest_index = lengths.index(max(lengths))
    # use the index to get the longest string from the original list
    longest_string = list_string[longest_index]
    return longest_string


def concatenate_name(name_list):
    name_list_len = len(name_list)
    if name_list_len > 3:

        division = name_list_len // 3

        if (name_list_len % 3 != 0):
            division += 1

        temp_name_list = [""] * division
        idx = 0
        num = 0
        for name in name_list:
            if (num % 3 == 0 and num != 0):
                idx += 1
                num = 0
            temp_name_list[idx] = temp_name_list[idx] + str(name) + " "
            num += 1
        return temp_name_list
    else:
        return name_list

def convert_fdoc(docs):
    return docs.to_dict()

def convert_django_querydict(djangoDict):
    djangoDict = djangoDict.dict()
    for key, values in djangoDict.items():
        djangoDict[key] = values[0]
    return djangoDict

