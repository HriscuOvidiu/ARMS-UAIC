import os
import uuid
import pandas as pd

out_path = 'out/processed/'

def _get_id_by_name(df, name):
    for index, row in df.iterrows():
        if row["name"] == name:
            return row["id"]

    return -1

def _get_merged_df(mdf, fdf, wdf, website_list):
    column_name = "website_id"
    
    mc_id = _get_id_by_name(wdf, website_list[0])
    fly_id = _get_id_by_name(wdf, website_list[1])

    mdf.insert(1, column_name, [mc_id for i in mdf.iterrows()], True)
    fdf.insert(1, column_name, [fly_id for i in fdf.iterrows()], True)

    return pd.concat([mdf, fdf])

def process_data(folder, mc_file, fly_file):
    website_list = ["McMusic", "FlyMusic"]

    ## Create website df
    d = {'id':[uuid.uuid4() for i in website_list], "name": website_list}
    wdf = pd.DataFrame(data=d)

    ## Get the data dfs
    mdf = pd.read_csv(os.path.join(folder, mc_file))
    fdf = pd.read_csv(os.path.join(folder, fly_file))

    df = _get_merged_df(mdf, fdf, wdf, website_list)

    ## Get company name
    companies = [row['name'].split(' ')[0].lower().capitalize() for index, row in df.iterrows()]
    companiesSet = list(set(companies))
    companyIds = []

    ## Create the company DataFrame
    d = {'id':[uuid.uuid4() for i in companiesSet], 'name': companiesSet}
    cdf = pd.DataFrame(data=d)

    for index, row in df.iterrows():
        companyIds.append(_get_id_by_name(cdf, companies[index]))
    
    df.insert(0, "id", [uuid.uuid4() for i in df.iterrows()], False)
    df.insert(1, "companyId", companyIds, True)

    ## Save both DataFrames
    wdf.to_csv(os.path.join(out_path, 'websites.csv'), index=False)
    cdf.to_csv(os.path.join(out_path, 'companies.csv'), index=False)
    df.to_csv(os.path.join(out_path, 'instruments.csv'), index=False)