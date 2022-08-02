def bytes_to_str_noquotes(keyword):
    if isinstance(keyword, bytes):
        tmp = keyword
        decode_keyword = tmp.decode('utf-8')
        result = f'{decode_keyword}'
    return result

def bytes_to_str(keyword):
    if isinstance(keyword, bytes):
        tmp = keyword
        decode_keyword = tmp.decode('utf-8')
        str_keyword = '\'' + decode_keyword + '\''
        result = f'{str_keyword}'
    return result

def byteslist_to_strlist(bytes_list):
    if isinstance(bytes_list, list):
        string_list=[word.decode('utf-8') for word in bytes_list]
    return bytes_list

