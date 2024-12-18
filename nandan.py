from utils import *
# import streamlit as st
import os
from constant import *



def nandan_live2(stock_name):

    final_df2 = pd.DataFrame()

    df = fetch_data_from_tru_data(stock_name ,'1 Y')
    time.sleep(0.1)
    # df.drop(df.tail(1).index,inplace=True)
    df1 = fetch_data_from_tru_data_nandan(stock_name,df['date'].iloc[0],365,'EOD')
    df_final = pd.concat([df1,df],axis=0).reset_index(drop=True)
    # print(df)
    new = calculate_stock_indicators(df.copy(),'atr_14','ATR_14')
    # print(new)
    new = new.drop(['atr_14'],axis=1)
    new2 = calculate_stock_indicators(new.copy(),'close_50_sma','SMA')

    df_new  = new2[['date','open','close','high','low','atr_14','SMA']]
   
    lst = []
    date_entry = "NA"
    exit_date = datetime(2010,2,20,0,0,0)
    for i in range(df_new.shape[0]-10,df_new.shape[0]):
        start_date_identify = df_new['date'].iloc[i]
        if start_date_identify  >= exit_date:
            supp,resis = get_support_and_resis(df_final,df_new['date'].iloc[i],df_new.iloc[i],stock_name)
            close_price_sma = df_new['close'].iloc[i]
            numbers_below_target = [num for num in supp if num < close_price_sma]
        
            if len(numbers_below_target) > 0:
                closest_below_target = max(numbers_below_target)
                df_new1= df_new[df_new['date'] > start_date_identify].reset_index(drop=True)
                for j in range(0,df_new1.shape[0]):
                    if closest_below_target > df_new1['close'].iloc[j]:
                        support_date_identify = df_new1['date'].iloc[j]
                        df_new2= df_new1[df_new1['date'] > support_date_identify]
                        for k in range(0,df_new2.shape[0]):
                            if ((1.5*df_new2['atr_14'].iloc[k]) < abs(df_new2['close'].iloc[k]-df_new2['open'].iloc[k])) and (df_new2['SMA'].iloc[k] < df_new2['close'].iloc[k]):
                                entry_price = df_new2['close'].iloc[k]
                                entry_date = df_new2['date'].iloc[k]
                                sma_value = df_new2['SMA'].iloc[k]
                                exit_date = entry_date + timedelta(days=10)

                                dict_list = {'start_date': start_date_identify,'close_price_start':close_price_sma,
                                            'support':supp,'nearest_support':closest_below_target,
                                            'date_below_support':support_date_identify,'atr':df_new2['atr_14'].iloc[k],
                                            'entry':entry_price,'entry_date':entry_date,'Buy/Sell':'Buy','sma_value':sma_value,
                                            'exit_date':exit_date
                                            }
                                # dict_list.update(abc)
                                lst.append(dict_list)
                                break
                        break

    final_df = pd.DataFrame(lst)

    lst = []
    date_entry = "NA"
    exit_date = datetime(2010,2,20,0,0,0)
    for i in range(df_new.shape[0]-7,df_new.shape[0]):
        start_date_identify = df_new['date'].iloc[i]
        if start_date_identify >= exit_date:
            supp,resis = get_support_and_resis(df_final,df_new['date'].iloc[i],df_new.iloc[i],stock_name)
            close_price_sma = df_new['close'].iloc[i]
            numbers_below_target = [num for num in resis if num > close_price_sma]

            if len(numbers_below_target) > 0:
                closest_above_target = min(numbers_below_target)
                df_new1= df_new[df_new['date'] > start_date_identify].reset_index(drop=True)
                for j in range(0,df_new1.shape[0]):
                    if closest_above_target > df_new1['close'].iloc[j]:
                        support_date_identify = df_new1['date'].iloc[j]
                        df_new2= df_new1[df_new1['date'] > support_date_identify]
                        for k in range(0,df_new2.shape[0]):
                            if ((1.5*df_new2['atr_14'].iloc[k]) < abs(df_new2['close'].iloc[k]-df_new2['open'].iloc[k])) and (df_new2['SMA'].iloc[k] > df_new2['close'].iloc[k]):
                                entry_price = df_new2['close'].iloc[k]
                                entry_date = df_new2['date'].iloc[k]
                                sma_value = df_new2['SMA'].iloc[k]
                                exit_date = entry_date + timedelta(days=10)

                                dict_list = {'start_date': start_date_identify,'close_price_start':close_price_sma,
                                            'support':resis,'nearest_support':closest_above_target,
                                            'date_below_support':support_date_identify,'atr':df_new2['atr_14'].iloc[k],
                                            'entry':entry_price,'entry_date':entry_date,'Buy/Sell':'Sell',
                                            'sma_value':sma_value,'exit_date':exit_date
                                            }
                                # dict_list.update(abc)
                                lst.append(dict_list)
                                break
                        break

    final_df1 = pd.DataFrame(lst)
    
    final_df2 = pd.concat([final_df1,final_df]).reset_index(drop=True)
    
    return final_df2


def get_support_and_resis(df,date_for_s_r,x,stock_name):

    df2 = df[(df['date']<date_for_s_r) & (df['date']>=date_for_s_r-timedelta(days = 365))]
    df2 = df2.reset_index(drop=True)
    if date_for_s_r-timedelta(days = 365) in df['date']:
        df1 = df2.copy()
    else:
        df3 = pd.DataFrame([x]).reset_index(drop=True)
        df1 = fetch_data_from_tru_data_nandan(stock_name,df3['date'].iloc[0],365,'EOD')
        time.sleep(0.1)
    supp,resis = s_and_r(df1)

    return supp,resis


def final_run():
    df9 = pd.DataFrame()
    df1_filtered = pd.DataFrame()
    for i in NIFTY100:
        df = pd.DataFrame()
        df = nandan_live2(i)
        if df.shape[0]:
            df['Company'] = i
            df9 = pd.concat([df9,df]).reset_index(drop=True)
    if df9.shape[0]:
        df9['date_of_run'] = datetime.now().strftime('%d/%m/%y')
        df9['time_of_run'] = datetime.now().strftime('%H:%M:%S')
        # df9.to_csv('test.csv')
        # df9 = pd.read_csv('test.csv')
        if os.path.exists('live.csv'):
            columns_to_compare = ['entry_date','Buy/Sell','Company']
            df10 = pd.read_csv('live.csv')
            
            df10['date_of_run'] = pd.to_datetime(df10['date_of_run'], infer_datetime_format=True, errors='coerce')
            df10['date_of_run'] = pd.to_datetime(df10['date_of_run'], format='%d/%m/%y').dt.date

            df10['entry_date'] = pd.to_datetime(df10['entry_date'], infer_datetime_format=True, errors='coerce')
            df10['entry_date'] = pd.to_datetime(df10['entry_date'], format='%d/%m/%y').dt.strftime('%d/%m/%y')

            df9['entry_date'] = pd.to_datetime(df9['entry_date'], infer_datetime_format=True, errors='coerce')
            df9['entry_date'] = pd.to_datetime(df9['entry_date'], format='%d/%m/%y').dt.strftime('%d/%m/%y')

            mask = df9[columns_to_compare].apply(tuple, 1).isin(df10[columns_to_compare].apply(tuple, 1))
            df1_filtered = df9[~mask]

            if df1_filtered.shape[0]:
                df10 = pd.concat([df10,df1_filtered],axis=0,ignore_index=True)
                df10 = df10.drop(['Unnamed: 0'],axis=1,errors='ignore')
                df10.to_csv('live.csv',index=False)
        else:
            df9.to_csv('live.csv')
    
    df11 = pd.DataFrame()
    df11['date_of_run'] = [datetime.now().strftime('%d/%m/%y')]
    df11['time_of_run'] = [datetime.now().strftime('%H:%M:%S')]
    
    if os.path.exists('timesheet.csv'):
        df12 = pd.read_csv('timesheet.csv')
        df12 = pd.concat([df12,df11],axis=0,ignore_index=True)
        # df10 = df10.drop(['Unnamed: 0'],axis=1)
        df12.to_csv('timesheet.csv', index=False)
    else:
        df11.to_csv('timesheet.csv')


    return df1_filtered