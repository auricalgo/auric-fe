from utils import *
# import streamlit as st




def nandan_live2(stock_name):

    final_df2 = pd.DataFrame()

    df = fetch_data_from_tru_data(stock_name ,'1 Y')
    # df.drop(df.tail(1).index,inplace=True)
    df1 = fetch_data_from_tru_data_nandan(stock_name,df['date'].iloc[0],365,'EOD')
    df_final = pd.concat([df1,df],axis=0).reset_index(drop=True)

    new = calculate_stock_indicators(df.copy(),'atr_14','ATR_14')
    new = new.drop(['atr_14'],axis=1)
    new2 = calculate_stock_indicators(new.copy(),'close_50_sma','SMA')

    df_new  = new2[['date','open','close','high','low','atr_14','SMA']]
   
    lst = []
    date_entry = "NA"
    exit_date = date(2010,2,20)
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
    exit_date = date(2010,2,20)
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
    supp,resis = s_and_r(df1)

    return supp,resis


def final_run():
    df9 = pd.DataFrame()
    for i in NIFTY100:
        # start_time = time.time()
        df = pd.DataFrame()
        df = nandan_live2(i)
        if df.shape[0]:
            df['Company'] = i
            df9 = pd.concat([df9,df]).reset_index(drop=True)
        # end = time.time() - start_time
    # df9.to_csv('old_live.csv')
    if df9.shape[0]:
        df9['date_of_run'] = datetime.now().strftime('%Y-%m-%d')
        df9['time_of_run'] = datetime.now().strftime('%H:%M:%S')
        print(df9)
        print(df9.columns)
        df9.to_csv('live.csv', mode='a', header=False, index=False)
    return df9