from utils import *
from nandan import *



def final_run_aws(list_of_company):
    df9 = pd.DataFrame()
    df1_filtered = pd.DataFrame()
    df = pd.DataFrame()
    df = nandan_live2(list_of_company)
    if df.shape[0]:
        df['Company'] = list_of_company
        df9 = pd.concat([df9,df]).reset_index(drop=True)
        df9['start_date'] = df9['start_date'].dt.strftime('%Y-%m-%d')
        df9['date_below_support'] = df9['date_below_support'].dt.strftime('%Y-%m-%d')
        df9['exit_date'] = df9['exit_date'].dt.strftime('%Y-%m-%d')
        if df9.shape[0]:
            df9['support'] = df9['support'].astype(str)
            df9['date_of_run'] = datetime.now().strftime('%Y-%m-%d')
            df9['time_of_run'] = datetime.now().strftime('%H:%M:%S')

            columns_to_compare = ['entry_date','Buy/Sell','Company']
            df10 = fetch_and_rename("select * from live")
            df10 = df10.drop(['id'],axis=1,errors='ignore')
            if df10.shape[0]:
                df10['date_of_run'] = pd.to_datetime(df10['date_of_run'], format='%Y-%m-%d').dt.date
                df10['entry_date'] = pd.to_datetime(df10['entry_date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
                df9['entry_date'] = pd.to_datetime(df9['entry_date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
                mask = df9[columns_to_compare].apply(tuple, 1).isin(df10[columns_to_compare].apply(tuple, 1))
                df1_filtered = df9[~mask]

                if df1_filtered.shape[0]:
                    insert_dataframe_to_db(df1_filtered,'live')
            else:
                out = insert_dataframe_to_db(df9,'live')


    return 'True'




def final_run_single_stock(list_of_company):
    df9 = pd.DataFrame()
    df1_filtered = pd.DataFrame()
    df = pd.DataFrame()
    df = nandan_live2(list_of_company)
    if df.shape[0]:
        df['Company'] = list_of_company
        df9 = pd.concat([df9,df]).reset_index(drop=True)
        df9['start_date'] = df9['start_date'].dt.strftime('%Y-%m-%d')
        df9['date_below_support'] = df9['date_below_support'].dt.strftime('%Y-%m-%d')
        df9['exit_date'] = df9['exit_date'].dt.strftime('%Y-%m-%d')
        if df9.shape[0]:
            df9['support'] = df9['support'].astype(str)
        


    return df9
