def set_choices(choicesList):
    # 用于将选项生成CharField的choices元组
    # 参数:选项列表r
    choicesTuple = list()
    for choice in choicesList:
        singlechoicelist = list()
        singlechoicelist.append(choice)
        singlechoicelist.append(choice)
        choicesTuple.append(tuple(singlechoicelist))
    return tuple(choicesTuple)

