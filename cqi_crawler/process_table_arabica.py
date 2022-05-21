import pandas as pd

df_list = []
"""
arabica
"""

for i in range(29,209):
    df1 = pd.read_csv('C:/Users/Acer/Desktop/Python/crawler_pratice/cqi/coffeedata/arabica/coffee_data_arabica_{}_table_0.csv'.format(i) ,header=None)
    df2 = pd.read_csv('C:/Users/Acer/Desktop/Python/crawler_pratice/cqi/coffeedata/arabica/coffee_data_arabica_{}_table_1.csv'.format(i))
    df3 = pd.read_csv('C:/Users/Acer/Desktop/Python/crawler_pratice/cqi/coffeedata/arabica/coffee_data_arabica_{}_table_2.csv'.format(i))
    df4 = pd.read_csv('C:/Users/Acer/Desktop/Python/crawler_pratice/cqi/coffeedata/arabica/coffee_data_arabica_{}_table_3.csv'.format(i))
    df5 = pd.read_csv('C:/Users/Acer/Desktop/Python/crawler_pratice/cqi/coffeedata/arabica/coffee_data_arabica_{}_table_4.csv'.format(i))
    
    #處理df0
    df0_processed = pd.DataFrame([i],columns=['id'])

    #處理df1
    df1.iloc[-2,1]=df1.iloc[-2,1].replace('Species ','')
    df1.iloc[-1,1]=df1.iloc[-1,1].replace('Owner ','')
    data1=df1.iloc[-2:,1].to_list()
    df1_processed = pd.DataFrame([data1],columns=['Species','Owner'])

    #處理df2
    df2.columns = [0,1,2,3,4]
    colnames1 = df2[1].tolist()
    colnames2 = df2[3].tolist()
    colnames2[5]='Owner.1'
    data1 = df2[2].tolist()
    data2 = df2[4].tolist()
    df2_processed = pd.DataFrame([(data1+data2)],columns=(colnames1+colnames2))
    
    #處理df3
    df3.columns = [0,1,2,3,4]
    colnames1 = df3[1].tolist()
    colnames2 = df3[3].tolist()
    data1 = df3[2].tolist()
    data2 = df3[4].tolist()
    df3_processed = pd.DataFrame([(data1+data2)],columns=(colnames1+colnames2))
        
    #處理df4
    df4.columns = [0,1,2,3,4]
    colnames1 = df4[1].tolist()
    colnames2 = df4[3].tolist()[:-1]
    data1 = df4[2].tolist()
    data2 = df4[4].tolist()[:-1]
    df4_processed = pd.DataFrame([(data1+data2)],columns=(colnames1+colnames2))
    
    #處理df5
    df5.columns = [0,1,2]
    colnames1 = df5[1].tolist()
    data1 = df5[2].tolist()
    df5_processed = pd.DataFrame([data1],columns=colnames1)

    #合併資料表
    df=pd.concat([df0_processed,df1_processed,df2_processed,df3_processed,df4_processed,df5_processed],axis=1)
    df.drop(['Status','Defects'],axis=1,inplace=True)
    df.rename(columns={'Country of Origin':'Country.of.Origin','Farm Name':'Farm.Name','Lot Number':'Lot.Number',\
            'ICO Number':'Lot.Number','ICO Number':'ICO.Number','Number of Bags':'Number.of.Bags','Bag Weight':'Bag.Weight',\
                'In-Country Partner':'In.Country.Partner','Harvest Year':'Harvest.Year','Grading Date':'Grading.Date','Processing Method':'Processing.Method',\
                    'Clean Cup':'Clean.Cup','Overall':'Cupper.Points','Total Cup Points':'Total.Cup.Points','Category One Defects':'Category.One.Defects',\
                        'Category Two Defects':'Category.Two.Defects','Certification Body':'Certification.Body','Certification Address':'Certification.Address',\
                            'Certification Contact':'Certification.Contact'}, inplace=True)
    df=df.reindex(columns=['id','Species', 'Owner', 'Country.of.Origin', 'Farm.Name', 'Lot.Number',
       'Mill', 'ICO.Number', 'Company', 'Region', 'Producer',
       'Number.of.Bags', 'Bag.Weight', 'In.Country.Partner', 'Harvest.Year',
       'Grading.Date', 'Owner.1', 'Variety', 'Processing.Method', 'Aroma',
       'Flavor', 'Aftertaste', 'Acidity', 'Body', 'Balance', 'Uniformity',
       'Clean.Cup', 'Sweetness', 'Cupper.Points', 'Total.Cup.Points', 'Moisture',
       'Category.One.Defects', 'Quakers', 'Color', 'Category.Two.Defects',
       'Expiration', 'Certification.Body', 'Certification.Address',
       'Certification.Contact', 'Altitude'])

    df_list.append(df)
    print('coffee number: ',i)

df_final=pd.concat(df_list,axis=0)
df_final=df_final.reset_index(drop=True)
df_final.to_csv('C:/Users/Acer/Desktop/Python/crawler_pratice/cqi/coffeedata/arabica.csv',index = False)
