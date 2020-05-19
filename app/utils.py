from clients.analeyezer import AnalEyeZerClient


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


def remove_dump_skills(skills_df):
    """This function is used to remove dump skills extracted from Dobie"""
    remove_skills = skills_df.loc[~skills_df['skill'].isin(
        ['Assurance', 'LeSS', 'Computer Science', 'Development', 'Programming'])]
    return remove_skills


def create_joined_table_index(**kwargs):
    """
    This function is used to load the joined data source to elasticsearch
    """
    analeyezer = AnalEyeZerClient()
    response = analeyezer.commit_data_source(**kwargs)
    if response.status_code == 400:
        print('Index creation to Elasticsearch failed.')
    else:
        print('Index successfully created')
