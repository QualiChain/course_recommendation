def filter_extracted_skills(**kwargs):
    """
    This function is used to transform extracted skill table

    :param kwargs: provided kwargs
    :return: filtered skill
    """
    skill = kwargs['skill']

    split_skill = skill.split(" ")
    bins_len = len(split_skill)

    if bins_len > 2 or bins_len == 1:
        filtered_skill = skill
    else:
        first_bin = split_skill[0]
        second_bin = split_skill[1]

        if len(second_bin) <= 3 or len(first_bin) <= 2:
            filtered_skill = "".join(split_skill)
        elif skill == "Java Script":
            filtered_skill = "JavaScript"
        else:
            filtered_skill = skill

    return filtered_skill
