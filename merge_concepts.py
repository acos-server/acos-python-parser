import pandas as pd
import json



def merge_concepts(smart_content_df):

    smart_content_df.loc[:,'concept'] =  smart_content_df.loc[:,'component_name']
    smart_content_df = smart_content_df[['content_name','concept']]

    