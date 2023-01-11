from django import template # 追記 必須
register = template.Library() # 追記 必須

@register.filter
def getval(dictionary, key):
    return dictionary.get(key)

@register.filter
def url_fst(string):
    return str(string).split('/')[1]

@register.filter
def sum_dic(dic):
    a = 0
    for key in dic:
        a += int(dic[key])
    return a

@register.simple_tag
def access_list(some_list: list, index: int):
    """
    リストの要素のうち、インデックスで指定した要素を返す
    :param some_list: 要素を取得したいリスト
    :param index: 取得したいリストのインデックス
    :return: 指定したインデックスに格納されているリストの要素
    """
    try:
        result = some_list[int(index)]
        return result
    except:
        return ""