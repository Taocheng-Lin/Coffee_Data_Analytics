import pandas as pd 
import numpy as np

robusta=pd.read_csv('C:/Users/Acer/Desktop/Python/crawler_pratice/cqi/coffeedata/robusta.csv')
arabica=pd.read_csv('C:/Users/Acer/Desktop/Python/crawler_pratice/cqi/coffeedata/arabica.csv')
data=pd.concat([robusta,arabica],join='inner')
data.reset_index(inplace=True, drop=True)

#尋找遺失值欄位
cols_with_missing_value=[col for col in data.columns if data[col].isnull().any()]
#print(data)
#print(cols_with_missing_value)

#處理Color未知值
data.Color.replace('None','Unknown',inplace=True)

#處理'Farm.Name','Mill','Region','Producer','Variety','Processing.Method'遺失值
cols_values_unknown=['Farm.Name','Mill','Region','Producer','Variety','Processing.Method']
data.fillna({col:'Unknown' for col in cols_values_unknown},inplace=True)

#處理'ICO.Number'遺失值
data.fillna({'ICO.Number':'None'},inplace=True)

#處理Harvest.Year值
data['Harvest.Year']=data['Harvest.Year'].map(lambda a:str(a)[-4:])

#處理Altitude特殊符號
#special=data['Altitude'].str.contains(pat='\D',na=False,regex=True)
data.Altitude=data.Altitude.str.replace('A','')
data.Altitude=data.Altitude.str.replace(',','')
data.Altitude=data.Altitude.str.replace('above','')
data.Altitude=data.Altitude.str.replace('－','-')
data.Altitude=data.Altitude.str.replace('  ','-')
data.Altitude=data.Altitude.str.replace(' ','')
data.Altitude=data.Altitude.str.replace('–','-')
special_hyphen=data['Altitude'].str.contains(pat='\D',na=False,regex=True)
#計算平均值、修正欄位類型
data.loc[special_hyphen,'Altitude']=data[special_hyphen]['Altitude'].str.split('-')
data.loc[special_hyphen,'Altitude']=data.loc[special_hyphen,'Altitude'].map(lambda x:int((int(x[0])+int(x[1]))/2))
data.loc[data['Altitude'].str.contains(pat='\d',na=False,regex=True),'Altitude']=data.loc[data['Altitude'].str.contains(pat='\d',na=False,regex=True),'Altitude'].map(lambda x:int(x))
#處理Altitude遺失值、用同一國家平均值填補遺失值、沒資料的用整體平均值
country_altitude_mean=data.groupby('Country.of.Origin').Altitude.mean().to_dict()
for i in data[data['Altitude'].isnull()].index:
    data.loc[i,'Altitude']=country_altitude_mean[data.loc[i,'Country.of.Origin']]
data.loc[data['Altitude'].isnull(),'Altitude']=data.Altitude.mean()
#依Altitude分類高度
for i in range(len(data)):
    if data.loc[i,'Altitude']>3000:
        data.loc[i,'Altitude_classfy']='3000+'
    elif data.loc[i,'Altitude']>2000:
        data.loc[i,'Altitude_classfy']='2001-3000'
    elif data.loc[i,'Altitude']>1000:
        data.loc[i,'Altitude_classfy']='1001-2000' 
    else:
        data.loc[i,'Altitude_classfy']='0-1000' 

#更改Altitude欄位名稱為altitude_mean_meters
data.rename(columns={'Altitude':'altitude_mean_meters'},inplace=True)

#因要合併之前的資料，因此修改id
data.loc[:,'id']=data.loc[:,'id'].map(lambda x:x+1340)

#輸出資料
data.to_csv('C:/Users/Acer/Desktop/Python/crawler_pratice/cqi/coffeedata/all_coffee_data.csv',index=False)
print(data.shape)
