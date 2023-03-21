from imports import *




now = datetime.now()
def pre_process_phone(num):
    if num.startswith("0"):
        num = num.replace("0", "84", 1)
    elif num.startswith("+84"):
        num = num.replace("+84", "84", 1)
    elif num.startswith("84"):
        pass
    else:
        num = "84" + num
    return num


if __name__ == "__main__":
    # Call get_transactions each 5 mins to get data
    while now < datetime(now.year, now.month, now.day, 20, 0, 0):

        start = datetime.now()
    
        # get transaction with reason fail = "Số điện thoại không chính xác" 
        print("-"*50)
        print("Get data at {}: Started".format(now))
        data = get_transactions.run_query(802)
        print("Done get data at {}".format(now))
        df = pd.json_normalize(data.json()['query_result']['data']['rows'])

        # if file not exist, create new file
        if not os.path.exists('./data_/transaction_fail_{}.csv'.format(now.strftime("%Y-%m-%d"))):
            df.to_csv('./data_/transaction_fail_{}.csv'.format(now.strftime("%Y-%m-%d")), index=False)
            continue
        # read old data
        old_df = pd.read_csv('./data_/transaction_fail_{}.csv'.format(now.strftime("%Y-%m-%d")))
        # concat new data with old data
        df = pd.concat([old_df, df], ignore_index=True)
        # drop duplicate
        df = df.drop_duplicates(subset=['callee', 'transaction_id'], keep='first')
        
        # Make call list: 1 call = 1 phone number
        print("Make call list at {}: Started".format(now))
        
        # if column call_id not exist, create new column
        if 'checked' not in df.columns:
            print("Create new column 'checked' at {}".format(now))
            df['checked'] = 0
        df['checked'].fillna(0, inplace=True)


        # print total transaction
        print("Total transaction will be called: {}".format(df.loc[df['checked']==0 ,'transaction_id'].nunique()))
        
        # Call each phone number
        for i in df.loc[df['checked']==0 ,'transaction_id'].unique():
            
            to_phone = df.loc[df['transaction_id']==i, 'callee'].values[0]
            to_phone = pre_process_phone(to_phone)
            # retry request if error

            res = call_.outbound_call('842473001571', to_phone)
            try:
                df.loc[df['transaction_id']==i, 'call_id'] =  res.json()['call_id']
                df.loc[df['transaction_id']==i, 'call_status'] =  res.json()['r']
                df.loc[df['transaction_id']==i, 'checked'] = 1
            except:
                df.loc[df['transaction_id']==i, 'call_id'] =  'Error'
                df.loc[df['transaction_id']==i, 'call_status'] =  'Error'
                df.loc[df['transaction_id']==i, 'checked'] = 1
            
            # save to csv
            df.to_csv('./data_/transaction_fail_{}.csv'.format(now.strftime("%Y-%m-%d")), index=False)
            print("TransactionID [{}]: Call to {} at {}: Done!".format(i, to_phone, now.strftime("%Y-%m-%d %H:%M")))

    

        # Sleep for 5 mins
        time_diff = (datetime.now() - start).total_seconds()
        if time_diff <= 300:
            print("Sleeping for {} seconds".format(300 - time_diff))
            time.sleep(300 - time_diff)
            # Get call log
            print("Get call log at {}: Started".format(now))
            call_log = call_.get_call_log()
            call_log.to_csv('./data_/call_log_{}.csv'.format(now.strftime("%Y-%m-%d")), index=False)
            print("Get call log at {}: Done".format(now))



    print(df)




