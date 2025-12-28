def scour(dictionary):
    string = '{'
    for key, item in dictionary.items():
        if isinstance(item, dict):
            string += scour(item)
        else:
            string += f"{key}: {item},"
    return string + '}'

def read(dictionary):
    di = str(dictionary)[1:-1]
    string = ''
    indention = ''
    QUOTES = ['"', "'"]
    r = True
    for letter in di:
        if letter in QUOTES:
            r = not r
        if r:
            if letter == '{':
                indention += '  '
                string += '\n' + indention + letter
            elif letter == '}':
                indention = indention[:-2]
                string += letter + '\n' + indention
            elif letter == ',':
                 string += letter + '\n' + indention
            else:
                string += letter
        else:
                string += letter
    return str('{' + string + '}')
#print(read({"scour":{"igsher":{"shower":{"tower":{"of":{"extreme":{"power"}}}}}}}))