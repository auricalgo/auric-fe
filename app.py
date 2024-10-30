import logging
from flask import Flask, jsonify, request
from aws import *

app = Flask(__name__)

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/api/health', methods=['GET'])
def run_health():

    return 'True'


@app.route('/api/get_data', methods=['GET'])
def get_data_api():

    df= fetch_and_rename('select * from live')

    return df.to_json(orient='records')


@app.route('/api/get_today_data', methods=['GET'])
def get_td_data_api():

    df= fetch_and_rename("""SELECT * FROM masteradmin.live
                         WHERE date_of_run = (SELECT MAX(date_of_run) FROM masteradmin.live);""")
    
    df = df.drop(['date'],axis=1,errors='ignore')


    return df.to_json(orient='records')


@app.route('/api/max_time', methods=['GET'])
def get_max_timesheet_api():

    df= fetch_and_rename("""SELECT * FROM masteradmin.timesheet
                         WHERE id = (SELECT MAX(id) FROM masteradmin.timesheet); """)

    return df.to_json(orient='records')



@app.route('/api/run', methods=['GET'])
def run_api():
    
    for i in NIFTY100:
        final_run_aws(i)
    
    df11 = pd.DataFrame()
    df11['date_of_run'] = [datetime.now().strftime('%Y-%m-%d')]
    df11['time_of_run'] = [datetime.now().strftime('%H:%M:%S')]
    
    df12 = fetch_and_rename("select * from timesheet")
    df12 = pd.concat([df12,df11],axis=0,ignore_index=True)
    insert_dataframe_to_db(df12,'timesheet')


    return 'True'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5020 ,debug=False)
