from re import T
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from streamlit.proto.TextInput_pb2 import _TEXTINPUT_TYPE
warnings.filterwarnings("ignore")
import streamlit as st
import pickle
from sklearn.preprocessing import OrdinalEncoder
encoder=OrdinalEncoder()
from PIL import Image
from sklearn.utils import resample
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report

st.set_page_config(layout="wide")
# Load data
file_path = "data/bank-additional-full.csv"
na_lst = ["NA","","#NA","unknown"]
marketing_df = pd.read_csv(file_path, sep=';')
marketing_null = pd.read_csv(file_path, sep=';', na_values = na_lst, keep_default_na = True) 
# Def Visualization
na_lst = ["NA","","#NA","unknown"]
def missing_exploration(data):
    total = data.isnull().sum().sort_values(ascending=False)
    percent = round((data.isnull().sum()/data.isnull().count()*100),2).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent %'])
    return missing_data
def visualize_numerical(df, column, target = 'y'):
    fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20,4)) # Create 2 charts in 1 row
    
    sns.histplot(df[column], ax=ax1, kde=True);
    ax1.set_xlabel(column);
    ax1.set_ylabel('Density');
    ax1.set_title(f'{column}  Distribution');

    sns.boxplot(x=target, y=column, data=df, showmeans=True, ax=ax2);
    ax2.set_xlabel('Target');
    ax2.set_ylabel(column);
    plt.show()

def visualize_numerical_lst(df, numerical = ['age', 'duration', 'campaign', 'pdays', 'previous', 'emp.var.rate',\
                            'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed'], target = 'y'):
    for column in numerical:
        visualize_numerical(df,column)
        print();
        
def visualize_categorical(df, column, target = 'y'):
        fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20,4)) 
        data1 = df.groupby(column).size()
        ax1.pie(x=data1 , autopct="%.2f%%",textprops=dict(color='black'), explode=[0.05]*len(data1) , labels=data1.index.tolist(),      pctdistance=0.7, radius=1.1,  startangle=90)
        ax1.set_title(f'{column}  Distribution', loc='center')

        data2 = get_col_target(column, target,df)   
        data2.plot(kind='bar',stacked = True, ax=ax2);
        plt.xticks(rotation=45);        
        plt.show()

def visualize_categorical_w_success_percent(df, column, target = 'y'):
    
        fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20,4)) 
        data1 = df[df['y']=='yes'].groupby(column).size()
        ax1.pie(x=data1 , autopct="%.2f%%",textprops=dict(color='black'), explode=[0.05]*len(data1) , labels=data1.index.tolist(),      pctdistance=0.7, radius=1.1,  startangle=90)
        ax1.set_title(f'Distribution of each field in {column} on total success rate', loc='center')

        data2 = get_col_target(column, target,df)   
        data2.plot(kind='bar',stacked = True, ax=ax2);
        ax2.set_title(f' Quantity distribution by {column}')
        plt.xticks(rotation=45);        
        plt.show()

def visualize_categorical_w_success(df, column, target = 'y'):
    
        fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20,4))    
        #chart number
        data2 = get_col_target(column, target,df)   
        ax1 = data2.plot(kind='bar',stacked = True, ax=ax1);
        ax1.set_title(f' Quantity distribution by {column}', loc='center')
    
        #chart successing rate
        data = get_col_target(column, target,df)
        data['yes_rate'] = round(data['yes']*100/(data['yes'] + data['no']),2)
        yes_rate_df =  data['yes_rate'].sort_values(ascending = False)

        #Rotation
        sns.barplot(y = yes_rate_df.values, x = yes_rate_df.index, ax=ax2)
        ax2.set_title(f' Successing rate by {column}')
        for ax in fig.axes:
            ax.tick_params(labelrotation=45)
    
def visualize_categorical_lst(df,categorical = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact',\
                                          'month', 'day_of_week', 'poutcome'], target = 'y'):
    for column in categorical:
        visualize_categorical(df, column)
        
def visualize_success_rate(df,categorical = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact',\
                                          'month', 'day_of_week', 'poutcome'], target = 'y'):
    
    for column in categorical:
        data = get_col_target(column, target,df)
        data['yes_rate'] = round(data['yes']*100/(data['yes'] + data['no']),2)
        yes_rate_df =  data['yes_rate'].sort_values(ascending = False)


        plt.figure(figsize = (8,5))
        sns.barplot(y = yes_rate_df.values, x = yes_rate_df.index)
        plt.xticks(rotation = 45)
        plt.ylabel('Successful rate by '+ column)
        
def get_col_target(rows, cols,data):
    
    cols_lst = data[cols].unique().tolist()
    rows_lst = data.groupby(rows)[rows].count().sort_values(ascending = False).index.tolist()

    group_df = data.groupby([rows,cols]).size()
    dic = {}
    for item in cols_lst:
        vals = []
        for i in rows_lst:
            try:
                vals.append(group_df.loc[(i, item)])
            except:
                vals.append(0)
            finally:
                continue
        dic[item] = vals

    df = pd.DataFrame(dic,index = rows_lst)
    return(df)

# Text describe
general = """
        <p style="margin: 0in; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="font-size: 14px; font-family: Calibri, sans-serif;">Nh???n x&eacute;t:</span></p>
        <ul style="list-style-type: square;">
        <li style="margin-top: 0in; margin-right: 0in; margin-bottom: 0in; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="font-size: 14px;"><span style="font-family: Calibri, sans-serif;">B??? d??? li???u c&oacute; 41188 d&ograve;ng v&agrave; 21 c???t, trong ??&oacute; c&oacute; 10 bi???n s??? v&agrave; 11 bi???n ph&acirc;n lo???i.&nbsp;</span></span></li>
        <li style="margin-top: 0in; margin-right: 0in; margin-bottom: 0in; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="font-size: 14px; font-family: Calibri, sans-serif;">B??? d??? li???u c&oacute; 88.7% nh&atilde;n &apos;no&apos; v&agrave; 11.3% nh&atilde;n &apos;yes&apos;, ??i???u n&agrave;y ch??? ra r???ng b??? d??? li???u nghi&ecirc;n c???u kh&ocirc;ng c&acirc;n b???ng gi???a t??? l??? c&aacute;c k???t qu??? thu ???????c. N&oacute; ?????ng th???i c??ng cho th???y r???ng ng&acirc;n h&agrave;ng n&agrave;y ??&atilde; th???c hi???n chi???n d???ch call marketing n&agrave;y m???t c&aacute;ch kh&ocirc;ng t&iacute;nh to&aacute;n n&ecirc;n t??? l??? th&agrave;nh c&ocirc;ng th???t s??? th???p.</span></li>
        </ul>
        """
age = """
    <p style='box-sizing: border-box; margin: 0px 0px 1rem; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-family: "IBM Plex Sans", sans-serif; font-style: normal; font-variant-caps: normal; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; line-height: 1.5;'><span style="box-sizing: border-box; font-size: 14px; font-family: Calibri, sans-serif;">Nh???n x&eacute;t:&nbsp;</span></p>
<ul style='box-sizing: border-box; margin: 0px 0px 1rem; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-family: "IBM Plex Sans", sans-serif; font-style: normal; font-variant-caps: normal; letter-spacing: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; list-style-type: square;'>
    <li style="box-sizing: border-box; margin: 0.2em 0px 0.2em 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;"><span style="box-sizing: border-box; font-family: Calibri, sans-serif;">Trong chi???n d???ch n&agrave;y ng&acirc;n h&agrave;ng t???p trung v&agrave;o nh&oacute;m ?????i t?????ng t??? 25-60 tu???i, nh&oacute;m tu???i target trong chi???n d???ch n&agrave;y l&agrave; t??? 30-40 tu???i.&nbsp;</span></span></li>
    <li style="box-sizing: border-box; margin: 0.2em 0px 0.2em 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;"><span style="box-sizing: border-box; font-family: Calibri, sans-serif;">Nh???ng kh&aacute;ch h&agrave;ng ?????ng &yacute; g???i ti???n t???p trung ??? ????? tu???i 30-50. Nh???ng ng?????i ?????ng &yacute; g???i ti???n m???c d&ugrave; bi&ecirc;n ?????ng r???ng h??n nh???ng ng?????i t??? ch???i, nh??ng nh&igrave;n chung h??? c&oacute; ????? tu???i trung b&igrave;nh tr??? h??n nh???ng ng?????i kh&ocirc;ng ?????ng &yacute;. &nbsp;??i???u n&agrave;y ch???ng t??? nh???ng ng?????i tr??? ??? giai ??o???n s??? nghi???p b???t ?????u ???n ?????nh th&igrave; c&oacute; xu h?????ng g???i ti???n nhi???u h??n so v???i nh???ng ng?????i gi&agrave; ho???c ng?????i m???i b???t ?????u s??? nghi???p.</span></span></li>
</ul>
<p style='box-sizing: border-box; margin: 0px 0px 1rem; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-family: "IBM Plex Sans", sans-serif; font-style: normal; font-variant-caps: normal; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; line-height: 1.5;'><span style="box-sizing: border-box; font-family: Calibri, sans-serif; font-size: 14px;">L??u &yacute;: Bi???n age c&oacute; ph???n outlier t??? kho???ng 70 tu???i tr??? l&ecirc;n, n&ecirc;n c&oacute; th??? c&acirc;n nh???c lo???i b??? c&aacute;c gi&aacute; tr??? n&agrave;y trong ph???n model training.</span></p>
    """


job = """<p style="box-sizing: border-box; margin: 0in; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-style: normal; font-variant-caps: normal; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Nh???n x&eacute;t:</span></p>
<ul style='box-sizing: border-box; margin: 0px 0px 1rem; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-family: "IBM Plex Sans", sans-serif; font-style: normal; font-variant-caps: normal; letter-spacing: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; list-style-type: square;'>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Chi???n d???ch n&agrave;y t???p trung v&agrave;o g???i ??i???n cho ?????i t?????ng l&agrave; admin, ng?????i lao ?????ng ch&acirc;n tay v&agrave; nh???ng ng?????i l&agrave;m k?? thu???t l&agrave; ch&iacute;nh.</span></li>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">M???c d&ugrave; 3 nh&oacute;m m&agrave; chi???n d???ch t???p trung v&agrave;o ch&iacute;nh chi???m s??? l?????ng th&agrave;nh c&ocirc;ng g???i ti???n cao nh???t, t??? l??? th&agrave;nh c&ocirc;ng ch??? n???m ??? m???c th???p ch???ng t??? ?????i t?????ng ng&agrave;nh ngh??? chi???n d???ch t???p trung ch??a th???c s??? hi???u qu???.</span></li>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Th&agrave;nh ph???n sinh vi&ecirc;n v&agrave; ng?????i ngh??? h??u tuy chi???m s??? l?????ng kh&ocirc;ng nhi???u nh??ng l???i c&oacute; t??? l??? th&agrave;nh c&ocirc;ng cao v?????t tr???i so v???i ng&agrave;nh ngh??? kh&aacute;c, ng&acirc;n h&agrave;ng n&ecirc;n c&acirc;n nh???c li&ecirc;n h??? th&ecirc;m v???i nh???ng ng?????i thu???c nh&oacute;m ?????i t?????ng n&agrave;y trong chi???n d???ch t???i.</span></li>
</ul>
"""


marital = """
<p style="box-sizing: border-box; margin: 0in; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-style: normal; font-variant-caps: normal; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Nh???n x&eacute;t:</span></p>
<ul style='box-sizing: border-box; margin: 0px 0px 1rem; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-family: "IBM Plex Sans", sans-serif; font-style: normal; font-variant-caps: normal; letter-spacing: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; list-style-type: square;'>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">?????i t?????ng ch&iacute;nh trong chi???n d???ch n&agrave;y ??a s??? l&agrave; nh???ng ng?????i ??&atilde; l???p gia ??&igrave;nh.</span></li>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">M???c d&ugrave; t&iacute;nh v??? s??? l?????ng th&agrave;nh c&ocirc;ng th&igrave; nh???ng ng?????i k???t h&ocirc;n c&oacute; s??? l?????ng k&iacute; g???i ti???n nhi???u nh???t, tuy nhi&ecirc;n x&eacute;t v??? t??? l??? th&agrave;nh c&ocirc;ng th&igrave; nh???ng ng?????i thu???c nh&oacute;m ?????c th&acirc;n chi???m t??? l??? cao h??n. ??i???u n&agrave;y ch???ng t??? nh???ng ng?????i ch??a k???t h&ocirc;n c&oacute; xu h?????ng g???i ti???n ti???t ki???m nhi???u h??n nh???ng ng?????i ??&atilde; k???t h&ocirc;n v&agrave; li d???, ng&acirc;n h&agrave;ng n&ecirc;n c&acirc;n nh???c ?????i t?????ng n&agrave;y trong chi???n d???ch ti???p theo..</span><span style="box-sizing: border-box; font-size: 14px;"><br></span><span style="box-sizing: border-box; font-size: 14px;">L??u &yacute;: S??? l?????ng &iacute;t data l&agrave; unknown, tuy nhi&ecirc;n l???i c&oacute; t??? l??? th&agrave;nh c&ocirc;ng cao nh???t -&gt; c&oacute; kh??? n??ng d??? b??? bias khi train model n???u train v???i d??? li???u n&agrave;y.</span></li>
</ul>
"""

education = """
<p style="box-sizing: border-box; margin: 0in; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-style: normal; font-variant-caps: normal; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Nh???n x&eacute;t:</span></p>
<ul style='box-sizing: border-box; margin: 0px 0px 1rem; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-family: "IBM Plex Sans", sans-serif; font-style: normal; font-variant-caps: normal; letter-spacing: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; list-style-type: square;'>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Trong chi???n d???ch marketing l???n n&agrave;y, kh&aacute;ch h&agrave;ng t???p trung ch&iacute;nh v&agrave;o ?????i t?????ng c&oacute; b???ng c???p ?????i h???c v&agrave; c???p ba l&agrave; ch&iacute;nh.</span></li>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">?????ng th???i khi x&eacute;t v??? t??? l??? kh&aacute;ch h&agrave;ng g???i ti???n, nh&oacute;m kh&aacute;ch h&agrave;ng c&oacute; tr&igrave;nh ????? ?????i h???c, h???c sinh c???p ba v&agrave; professional course l&agrave; ba nh&oacute;m chi???m t??? l??? cao nh???t.&nbsp;</span><span style="box-sizing: border-box; font-size: 14px;">??i???u n&agrave;y ch???ng t??? kh&ocirc;ng ph???i nh???ng ng?????i c&oacute; b???ng c???p c&agrave;ng cao th&igrave; c&oacute; xu h?????ng g???i ti???n ti???t ki???m c&agrave;ng nhi???u, ng&acirc;n h&agrave;ng n&ecirc;n c&acirc;n nh???c kh&ocirc;ng t???p trung v&agrave;o nh&oacute;m ?????i t?????ng n&agrave;y trong chi???n d???ch ti???p theo.</span></li>
</ul>
"""

default = """
<p style="box-sizing: border-box; margin: 0in; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-style: normal; font-variant-caps: normal; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Nh???n x&eacute;t:</span></p>
<ul style='box-sizing: border-box; margin: 0px 0px 1rem; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-family: "IBM Plex Sans", sans-serif; font-style: normal; font-variant-caps: normal; letter-spacing: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; list-style-type: square;'>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Trong chi???n d???ch n&agrave;y, ng&acirc;n h&agrave;ng ch??? t???p trung v&agrave;o ?????i t?????ng kh&ocirc;ng c&oacute; n??? x???u n&ecirc;n nh&igrave;n chung vi???c ??&aacute;nh gi&aacute; s??? ???nh h?????ng c???a y???u t??? n&agrave;y l&ecirc;n &yacute; ?????nh quy???t ?????nh g???i ti???n c???a kh&aacute;ch h&agrave;ng r???t kh&oacute;. Tuy nhi&ecirc;n c&oacute; th??? ?????t ra gi??? thi???t d??? hi???u l&agrave; nh???ng ng?????i c&oacute; n??? th&igrave; s??? kh&ocirc;ng c&oacute; ti???n ????? g???i ti???t ki???m n&ecirc;n vi???c ng&acirc;n h&agrave;ng lo???i nh???ng kh&aacute;ch h&agrave;ng c&oacute; n??? x???u ra kh???i ?????i t?????ng m???c ti&ecirc;u l&agrave; h???p l&iacute;.</span></li>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Y???u t??? default l&agrave; y???u t??? c&oacute; ????? inbalance l???n ?????ng th???i c&oacute; s??? l?????ng missing g???n 10.000, ??i???u n&agrave;y c??ng ch???ng t??? vi???c thu th???p d??? li???u n&agrave;y t????ng ?????i kh&oacute; kh??n.</span></li>
</ul>
"""
housing = """
<p style="box-sizing: border-box; margin: 0in; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-style: normal; font-variant-caps: normal; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Nh???n x&eacute;t:</span></p>
<ul style='box-sizing: border-box; margin: 0px 0px 1rem; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-family: "IBM Plex Sans", sans-serif; font-style: normal; font-variant-caps: normal; letter-spacing: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; list-style-type: square;'>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Trong chi???n d???ch n&agrave;y, t&iacute;nh tr&ecirc;n nh???ng kh&aacute;ch h&agrave;ng m&agrave; chi???n d???ch li&ecirc;n h??? c&oacute; t??? l??? ch&ecirc;nh l???ch gi???a nh???ng ng?????i c&oacute; nh&agrave; m&agrave; kh&ocirc;ng c&oacute; nh&agrave; kh&ocirc;ng qu&aacute; nhi???u.</span></li>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Theo bi???u ????? th&igrave; t??? l??? g???i ti???n tr&ecirc;n kh&aacute;ch h&agrave;ng c&oacute; nh&agrave;, kh&ocirc;ng c&oacute; nh&agrave; v&agrave; k??? c??? m???t l?????ng nh??? data missing t????ng ?????i b???ng nhau. ??i???u n&agrave;y ch???ng t??? vi???c c&oacute; nh&agrave; hay kh&ocirc;ng c&oacute; nh&agrave; kh&ocirc;ng th???c s??? ???nh h?????ng nhi???u ?????n quy???t ?????nh g???i ti???n c???a kh&aacute;ch h&agrave;ng.</span></li>
</ul>
"""

loan = """
<p style="box-sizing: border-box; margin: 0in; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-style: normal; font-variant-caps: normal; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px; text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Nh???n x&eacute;t:</span></p>
<ul style='box-sizing: border-box; margin: 0px 0px 1rem; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-family: "IBM Plex Sans", sans-serif; font-style: normal; font-variant-caps: normal; letter-spacing: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; list-style-type: square;'>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Trong chi???n d???ch n&agrave;y, ng&acirc;n h&agrave;ng t???p trung ch??? y???u v&agrave;o nh???ng ?????i t?????ng kh&ocirc;ng c&oacute; n??? -&gt; bi???n c&oacute; ????? inbalance cao n&ecirc;n c???n c&acirc;n nh???c th&ecirc;m v??? m???i li&ecirc;n h??? v???i c&aacute;c bi???n kh&aacute;c.</span></li>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">X&eacute;t v??? t??? l??? kh&aacute;ch h&agrave;ng ?????ng &yacute; g???i ti???n ti???t ki???m th&igrave; kh&ocirc;ng c&oacute; s??? ch&ecirc;ch l???nh nhi???u gi???a nh???ng kh&aacute;ch h&agrave;ng c&oacute; n???, kh&ocirc;ng c&oacute; n??? v&agrave; k??? c??? m???t l?????ng missing value nh???. ??i???u n&agrave;y ch???ng t??? vi???c kh&aacute;ch h&agrave;ng c&oacute; n??? hay kh&ocirc;ng c&oacute; n??? kh&ocirc;ng th???c s??? ???nh h?????ng nhi???u ?????n quy???t ?????nh g???i ti???n ti???t ki???m, ng&acirc;n h&agrave;ng c&oacute; th??? c&acirc;n nh???c lo???i b??? y???u t??? n&agrave;y trong qu&aacute; tr&igrave;nh t&igrave;m ki???m kh&aacute;ch h&agrave;ng trong chi???n d???ch ti???p theo.<br></span></li>
    <li style="box-sizing: border-box; margin: 0in 0in 0in 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Bi???n n??? c&oacute; m???t s??? l?????ng missing value tuy nhi&ecirc;n kh&ocirc;ng ??&aacute;ng k???.</span></li>
</ul>
"""

contact = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">Nh???n x&eacute;t:&nbsp;</span></p>
<ul style="list-style-type: square;">
    <li style="line-height: 1.5;"><span style="font-size: 14px;">Trong chi???n d???ch n&agrave;y, ng&acirc;n h&agrave;ng ch???n ph????ng ph&aacute;p g???i ??i???n b???ng ??i???n tho???i ????? li&ecirc;n h??? v???i kh&aacute;ch h&agrave;ng. Trong ??&oacute; s??? l?????ng kh&aacute;ch h&agrave;ng ???????c li&ecirc;n h??? b???ng di ?????ng chi???m s??? ??&ocirc;ng so v???i vi???c g???i ??i???n b???ng ??i???n tho???i b&agrave;n.</span></li>
    <li style="line-height: 1.5;"><span style="font-size: 14px;">T??? l??? th&agrave;nh c&ocirc;ng ?????i v???i ph????ng th???c g???i ??i???n c??ng chi???m t??? l??? cao g???n g???p 3 l???n so v???i vi???c g???i ??i???n b???ng s??? ??i???n tho???i b&agrave;n ch???ng t??? vi???c ti???p c???n kh&aacute;ch h&agrave;ng b???ng c&aacute;ch g???i ??i???n b???ng ??i???n tho???i di ?????ng c&oacute; hi???u qu??? h??n nhi???u so v???i vi???c g???i ??i???n b???ng s??? ??i???n tho???i b&agrave;n.</span></li>
</ul>
"""

day_of_week = """
<ul style='box-sizing: border-box; margin: 0px 0px 1rem; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-family: "IBM Plex Sans", sans-serif; font-style: normal; font-variant-caps: normal; letter-spacing: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; list-style-type: square;'>
    <li><span style="box-sizing: border-box; font-size: 14px;">Nh???n x&eacute;t:</span>
        <ul style='box-sizing: border-box; margin: 0px 0px 1rem; padding: 0px; font-size: 16px; font-weight: normal; caret-color: rgb(38, 39, 48); color: rgb(38, 39, 48); font-family: "IBM Plex Sans", sans-serif; font-style: normal; font-variant-caps: normal; letter-spacing: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; list-style-type: square;'>
            <li style="box-sizing: border-box; margin: 0.2em 0px 0.2em 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Trong chi???n d???ch n&agrave;y, ng&acirc;n h&agrave;ng h???u nh?? kh&ocirc;ng t&iacute;nh to&aacute;n vi???c ph&acirc;n b??? g???i ??i???n nh?? th??? n&agrave;o m&agrave; g???i ??i???n ?????u c&aacute;c ng&agrave;y trong tu???n.&nbsp;</span></li>
            <li style="box-sizing: border-box; margin: 0.2em 0px 0.2em 1.2em; padding: 0px 0px 0px 0.6em; font-size: 1rem; line-height: 1.5;"><span style="box-sizing: border-box; font-size: 14px;">Tuy nhi&ecirc;n t&iacute;nh tr&ecirc;n t??? l??? th&agrave;nh c&ocirc;ng th&igrave; ng&agrave;y ?????u tu???n (th??? hai) v&agrave; ng&agrave;y cu???i tu???n (th??? s&aacute;u) c&oacute; t??? l??? th&agrave;nh c&ocirc;ng th???p nh???t (??i???u n&agrave;y c??ng c&oacute; th??? d??? hi???u v&igrave; th??? hai - ng&agrave;y b???t ?????u c&ocirc;ng vi???c v&agrave; th??? s&aacute;u - ng&agrave;y k???t th&uacute;c tu???n l&agrave;m vi???c th?????ng l&agrave; nh???ng ng&agrave;y b???n r???n nh???t trong tu???n).&nbsp;</span><span style="box-sizing: border-box; font-size: 14px;">Chi???n d???ch c&oacute; th??? c&acirc;n nh???c li&ecirc;n h??? kh&aacute;ch h&agrave;ng v&agrave;o c&aacute;c ng&agrave;y gi???a tu???n t??? th??? ba ?????n th??? n??m ????? c&oacute; hi???u qu??? cao h??n.</span></li>
        </ul>
    </li>
</ul>
"""

duration = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">Nh???n x&eacute;t:</span></p>
<ul style="list-style-type: square;">
    <li style="line-height: 1.5;"><span style="font-size: 14px;">Th???i gian g???i ??i???n trung b&igrave;nh cho kh&aacute;ch h&agrave;ng n???m ??? 449s</span></li>
    <li style="line-height: 1.5;"><span style="font-size: 14px;">Th???i gian c???a cu???c g???i g???n nh???t (duration) t???p trung trong kho???ng 0-200.&nbsp;</span></li>
    <li style="line-height: 1.5;"><span style="font-size: 14px;">Nh???ng ng?????i c&oacute; duration = 0 th&igrave; t??? l??? th&agrave;nh c&ocirc;ng g???n nh?? l&agrave; 0. ??? nh???ng tr?????ng h???p ti???p c???n th&agrave;nh c&ocirc;ng, th???i l?????ng trung b&igrave;nh c???a cu???c g???i g???n nh???t trong chi???n d???ch hi???n t???i kho???ng 450 (t???p trung trong kho???ng &lt; 1000)</span></li>
</ul>
"""

campaign = """
<p style="margin-bottom: 10px !important; caret-color: rgb(0, 0, 0); color: rgb(0, 0, 0); font-family: -webkit-standard; font-style: normal; font-variant-caps: normal; font-weight: normal; letter-spacing: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none;"><span style="font-size: 14px;">Nh???n x&eacute;t:&nbsp;</span></p>
<ul style="list-style-type: square;">
    <li style="margin-bottom: 10px !important; caret-color: rgb(0, 0, 0); color: rgb(0, 0, 0); font-family: -webkit-standard; font-style: normal; font-variant-caps: normal; font-weight: normal; letter-spacing: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none;"><span style="font-size: 14px;">Trong chi???n d???ch n&agrave;y, h???u h???t c&aacute;c kh&aacute;ch h&agrave;ng ???????c li&ecirc;n h??? t??? 1-3 l???n v&agrave; t??? l??? kh&aacute;ch h&agrave;ng ?????ng &yacute; g???i ti???n c??ng chi???m s??? ??&ocirc;ng trong 3 l???n li&ecirc;n h??? tr??? l???i.</span></li>
</ul>
<p style="margin: 0in; caret-color: rgb(0, 0, 0); color: rgb(0, 0, 0); font-style: normal; font-variant-caps: normal; font-weight: normal; letter-spacing: normal; orphans: auto; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; widows: auto; word-spacing: 0px; -webkit-text-size-adjust: auto; -webkit-text-stroke-width: 0px; text-decoration: none; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="font-size: 14px;">&nbsp;</span></p>
"""

pdays = """<p style="margin: 0in; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="font-size: 14px;">Nh???n x&eacute;t:</span></p>
<ul style="list-style-type: square;">
    <li style="margin-top: 0in; margin-right: 0in; margin-bottom: 0in; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="font-size: 14px;">??a s??? ch??a ???????c ti???p x&uacute;c qua ??i???n tho???i ??? chi???n d???ch qu???ng c&aacute;o trc ??&oacute; (pdays = 999).&nbsp;</span></li>
    <li style="margin-top: 0in; margin-right: 0in; margin-bottom: 0in; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="font-size: 14px;">?????i v???i nh???ng clients ??&atilde; ???????c ti???p c???n ??? chi???n d???ch tr?????c (pdays != 999), ??a s??? cu???c g???i cu???i c&ugrave;ng c???a chi???n d???ch tr?????c n???m trong kho???ng 3 - 6 ng&agrave;y (trong v&ograve;ng 1 tu???n). Trong ??&oacute;, nh???ng tr?????ng h???p th&agrave;nh c&ocirc;ng c&oacute; pdays trung b&igrave;nh l&agrave; 5 ng&agrave;y.</span></li>
</ul>
<p style="margin: 0in; font-family: Calibri, sans-serif; line-height: 1.5;"><span style="font-size: 14px;">** Note: Data th??? hi???n tr&ecirc;n bi???u ????? c&oacute; pre-process lo???i b??? c&aacute;c lo???i b??? c&aacute;c gi&aacute; tr??? &apos;999&apos; c???a pdays </span></p>
"""

previous = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">Nh???n x&eacute;t:</span></p>
<ul style="list-style-type: square;">
    <li style="line-height: 1.5;"><span style="font-size: 14px;">S??? cu???c g???i ?????n kh&aacute;ch h&agrave;ng th???c hi???n tr?????c chi???n d???ch hi???n t???i (previous) ph???n nhi???u n???m ??? 0 --&gt; ??a s??? kh&aacute;ch h&agrave;ng ??? chi???n d???ch l???n n&agrave;y l&agrave; m???i, ch??a ??c ti???p th??? l???n n&agrave;o.&nbsp;</span></li>
    <li style="line-height: 1.5;"><span style="font-size: 14px;">Trung b&igrave;nh s??? l???n g???i ?????n kh&aacute;ch h&agrave;ng tr?????c chi???n d???ch hi???n t???i ??? nh???ng ng?????i ?????ng &yacute; cao h??n ??? nh&oacute;m ng?????i kh&ocirc;ng ?????ng &yacute;, l???n l?????t l&agrave; 0.5 v&agrave; 0. C&oacute; th??? n&oacute;i s??? t????ng t&aacute;c qua ??i???n tho???i ?????n kh&aacute;ch h&agrave;ng tr?????c ??&oacute; c??ng ???nh h?????ng ?????n k???t qu??? c???a chi???n d???ch ??? l???n ti???p theo. (N???u tr?????c ??&oacute;, kh&aacute;ch h&agrave;ng ??&atilde; ???????c ch??m s&oacute;c, h??? c&oacute; xu h?????ng mua s???n ph???m s??? ???????c ti???p th???)</span></li>
</ul>
"""

poutcome = """
<p><span style="font-size: 14px;">Nh???n x&eacute;t:</span></p>
<ul style="list-style-type: square;">
    <li><span style="font-size: 14px;">Trong chi???n d???ch n&agrave;y h???u h???t c&aacute;c li&ecirc;n h??? ?????u l&agrave; kh&aacute;ch h&agrave;ng m???i.</span></li>
    <li><span style="font-size: 14px;">N???u ng&acirc;n h&agrave;ng ??&atilde; th&agrave;nh c&ocirc;ng trong vi???c thuy???t ph???c kh&aacute;ch h&agrave;ng s??? d???ng d???ch v??? tr?????c ??&oacute; th&igrave; t??? l??? kh&aacute;ch h&agrave;ng ?????ng &yacute; tham gia chi???n d???ch l???n t???i s??? cao, l&ecirc;n t???i tr&ecirc;n 60%</span></li>
</ul>
"""

emp_var_rate = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">Nh???n x&eacute;t:&nbsp;</span></p>
<ul style="list-style-type: square;">
    <li style="line-height: 1.5;"><span style="font-size: 14px;">H??? s??? em.var.rate (h??? s??? thay ?????i c&ocirc;ng vi???c)</span></li>
    <li style="line-height: 1.5;"><span style="font-size: 14px;">KH ???????c ti???p th??? c&oacute; t??? l??? thay ?????i c&ocirc;ng vi???c n???m t??? -2 ?????n 1.2. ?????c bi???t, nh???ng KH ?????ng &yacute; g???i ti???n ?????u c&oacute; t??? l??? n&agrave;y &lt;0 (hi???m khi thay ?????i c&ocirc;ng vi???c) v&agrave; t??? l??? n&agrave;y th???p h??n t??? l??? trung b&igrave;nh c???a nh???ng ng?????i kh&ocirc;ng ?????ng &yacute; g???i. Nh???ng ng?????i &iacute;t thay ?????i c&ocirc;ng vi???c c&oacute; xu h?????ng g???i ti???n ng&acirc;n h&agrave;ng nhi???u h??n ng?????i hay thay ?????i c&ocirc;ng vi???c.</span></li>
</ul>
"""

cons_price_idx = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">Nh???n x&eacute;t:</p>
<ul style="list-style-type: square;">
<li style="line-height: 1.5;"><span style="font-size: 14px;">H??? s??? cons.price.idx l&agrave; h??? s??? gi&aacute; ti&ecirc;u d&ugrave;ng.</li>
<li style="line-height: 1.5;"><span style="font-size: 14px;">H??? s??? gi&aacute; ti&ecirc;u d&ugrave;ng c???a kh&aacute;ch h&agrave;ng ???????c g???i n???m trong kho???ng 93-94. T??? l??? trung b&igrave;nh c???a ch??? s??? n&agrave;y ??? nh???ng ng?????i ?????ng &yacute; g???i th???p h??n nh???ng ng?????i ko g???i. ??i???u n&agrave;y c&oacute; ngh??a l&agrave; khi ch??? s??? gi&aacute; ti&ecirc;u d&ugrave;ng cao (gi&aacute; tr??? h&agrave;ng h&oacute;a b&aacute;n ra cao), kh&aacute;ch h&agrave;ng s??? &iacute;t c&oacute; xu h?????ng g???i ti???n.</li>
</ul>
"""

cons_conf_idx = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">Nh???n x&eacute;t:</p>
<ul style="list-style-type: square;">
<li style="line-height: 1.5;"><span style="font-size: 14px;">H??? s??? cons.conf.ind (ch??? s??? l???c quan th??? tr?????ng)</li>
<li style="line-height: 1.5;"><span style="font-size: 14px;">T??? l??? trung b&igrave;nh ??? nh???ng kh&aacute;ch h&agrave;ng ti???p th??? th&agrave;nh c&ocirc;ng l???i cao h??n. T??? l??? n&agrave;y n???m trong kho???ng t??? -45 ?????n -37. ??i???u n&agrave;y c&oacute; ngh??a Khi kh&aacute;ch h&agrave;ng tin t?????ng v&agrave;o s???c kh???e c???a n???n kinh t??? th&igrave; ng?????i ta c??ng c&oacute; xu h?????ng g???i ti???n v&agrave;o ng&acirc;n h&agrave;ng nhi???u h??n.</li>
</ul>
"""

euribor3m = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">Nh???n x&eacute;t:</p>
<ul style="list-style-type: square;">
<li style="line-height: 1.5;"><span style="font-size: 14px;">Euribo3m (l&agrave; t??? l??? tham chi???u ???????c x&acirc;y d???ng t??? l&atilde;i su???t trung b&igrave;nh m&agrave; c&aacute;c ng&acirc;n h&agrave;ng Ch&acirc;u &Acirc;u cung c???p cho vay ng???n h???n kh&ocirc;ng c&oacute; t&agrave;i s???n b???o ?????m tr&ecirc;n th??? tr?????ng li&ecirc;n ng&acirc;n h&agrave;ng): n???m trong kho???ng t??? 1-5.</li>
<li style="line-height: 1.5;"><span style="font-size: 14px;">So s&aacute;nh 2 nh&oacute;m ?????ng &yacute; g???i v&agrave; kh&ocirc;ng g???i, ta th???y trung b&igrave;nh ch??? s??? n&agrave;y ??? nh&oacute;m ng?????i ?????ng &yacute; th???p h??n nh&oacute;m kh&ocirc;ng ?????ng &yacute;.??i???u n&agrave;y c&oacute; ngh??a khi ch??? s??? euribo3m c&agrave;ng th???p th&igrave; c&agrave;ng c&oacute; nhi???u ng?????i g???i h??n.</li>
<li style="line-height: 1.5;"><span style="font-size: 14px;">S??? l?????ng ng?????i c&oacute; vi???c l&agrave;m t&iacute;nh theo qu&yacute; n???m trong kho???ng 5010 - 5210. Khi ch??? s??? n&agrave;y c&agrave;ng th???p th&igrave; client c&agrave;ng c&oacute; xu h?????ng g???i h??n.</li>
</ul>
"""

nr_employed = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">Nh???n x&eacute;t:</p>
<ul style="list-style-type: square;">
<li style="line-height: 1.5;"><span style="font-size: 14px;">Bi???n nr.employed l&agrave; bi???n x&atilde; h???i th??? hi???n s??? l?????ng ng?????i c&oacute; vi???c l&agrave;m t&iacute;nh tr&ecirc;n qu&yacute;.</li>
<li style="line-height: 1.5;"><span style="font-size: 14px;">C&oacute; th??? nh???n th???y l&agrave; s??? l?????ng ng?????i c&oacute; vi???c l&agrave;m n???m ??? 5025-5200 th&igrave; c&oacute; kh??? n??ng th&agrave;nh c&ocirc;ng cao trong chi???n d???ch, ?????ng th???i ch??? s??? n&agrave;y n???m ??? 5100 l&agrave; ch??? s??? l&iacute; t?????ng nh???t ????? ti???p c???n kh&aacute;ch h&agrave;ng.</li>
</ul>
"""

comment_1 = """
<pli style="line-height: 1.5;"><span style="font-size: 14px;">### Nh???ng ch&uacute; &yacute; cho qu&aacute; tr&igrave;nh x??? l&yacute;</p>
<p style="line-height: 1.5;"><span style="font-size: 14px;">1. L?????c b??? d??? li???u</p>
<ul style="list-style-type: square;">
<li style="line-height: 1.5;"><span style="font-size: 14px;">C???t 'duration' s??? kh&ocirc;ng ???????c quan t&acirc;m trong qu&aacute; tr&igrave;nh ph&acirc;n t&iacute;ch v&agrave; x??? l&yacute;</li>
<li style="line-height: 1.5;"><span style="font-size: 14px;">C&oacute; 12 d&ograve;ng tr&ugrave;ng nhau s??? c???t b???</li>
</ul>
<p style="line-height: 1.5;"><span style="font-size: 14px;">2. Missing:</p>
<ul style="list-style-type: square;">
<li style="line-height: 1.5;"><span style="font-size: 14px;">C&oacute; s??? missing value tr&ecirc;n c&aacute;c bi???n: default, education, loan, housing, marital, job. Trong ??&oacute; bi???n default c&oacute; t??? l??? missing value cao v&agrave; ??&aacute;ng k??? nh???t (~20%)</li>
</ul>
<p style="line-height: 1.5;"><span style="font-size: 14px;">3. Outlier:</p>
<ul style="list-style-type: square;">
<li style="line-height: 1.5;"><span style="font-size: 14px;">Age, campain, previous, cons.conf.idx</li>
</ul>
<p style="line-height: 1.5;"><span style="font-size: 14px;">4. C&aacute;c bi???n s??? c&acirc;n nh???c ph&acirc;n lo???i th&ecirc;m: age, pdays.</p>
<p style="line-height: 1.5;"><span style="font-size: 14px;">5. Clustering theo 3 ch??? s??? pdays, previous, poutcome</p>
<p>&nbsp;</p>
"""

comment_2 = """
<pli style="line-height: 1.5;"><span style="font-size: 14px;">### L??u &yacute; kh&aacute;c nh&oacute;m ghi nh???n ???????c trong qu&aacute; tr&igrave;nh ph&acirc;n t&iacute;ch ngo&agravei</p>
<p style="line-height: 1.5;"><span style="font-size: 14px;">1. Bi???n previous:</p>
<ul style="list-style-type: square;">
<li style="line-height: 1.5;"><span style="font-size: 14px;">Bi???n n&agrave;y c&oacute; t????ng quan t??? l??? ngh???ch v???i nh&oacute;m bi???n ??? m???c 1, tuy nhi&ecirc;n nh???ng h??? s??? n&agrave;y kh&ocirc;ng qu&aacute; quan tr???ng trong ph???m vi xem x&eacute;t</li>
</ul>
<p style="line-height: 1.5;"><span style="font-size: 14px;">2.&nbsp;Nh&oacute;m bi???n x&atilde; h???i:</p>
<ul style="list-style-type: square;">
<li style="line-height: 1.5;"><span style="font-size: 14px;">Nh&oacute;m ch??? s??? nr.employed, emp.var.rate, euribor3m l&agrave; nh&oacute;m c&oacute; t????ng quan t??? l??? thu???n<br />&gt; 3 bi???n n&agrave;y c&oacute; y???u t??? t????ng ?????ng r???t cao n&ecirc;n ta c&oacute; th??? ch???n 1 bi???n ????? quan s&aacute;t (????? gi???m chi???u d??? li???u)</li>
<li style="line-height: 1.5;"><span style="font-size: 14px;">3 bi???n nr.employed, emp.var.rate, euribo3m l&agrave; 3 bi???n c&oacute; t????ng quan r???t m???nh --&gt; c&oacute; th??? l???c b???t ????? gi???m chi???u d??? li???u</li>
</ul>
<p style="line-height: 1.5;"><span style="font-size: 14px;">4. T??? l??? chuy???n ?????i: T??? l??? chuy???n ?????i t??? Failure to YES l&agrave; 14% trong khi t??? l??? chuy???n ?????i t??? Success to NO g???n 35%. ??? ??&acirc;y c&oacute; s??? m???t kh&aacute;ch h&agrave;ng.</p>
<p>&nbsp;</p>
"""
pre_process_1 = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">C&aacute;c b?????c pre-processing ???????c s??? d???ng:</span></p>
<p style="line-height: 1.5;"><span style="font-size: 14px;">1. D??? li???u tr&ugrave;ng: Xo&aacute; 12 d&ograve;ng d??? li???u tr&ugrave;ng nhau</span></p>
<p style="line-height: 1.5;"><span style="font-size: 14px;">2. S??? l?????ng bi???n s??? d???ng cho training: 19 bi???n/ 21 bi???n (lo???i b??? 2 c???t duration v&agrave; nr.employed)</span></p>
<p style="line-height: 1.5;"><span style="font-size: 14px;">3. D??? li???u thi???u:</span></p>
<ul style="list-style-type: square;">
    <li><span style="font-size: 14px;">?????i v???i c&aacute;c bi???n missing th???p: V&igrave; m???c ti&ecirc;u l&agrave; ti???p th??? ???????c nhi???u kh&aacute;ch h&agrave;ng kh&aacute;ch h&agrave;ng c&agrave;ng t???t - tr&aacute;nh vi???c ??&aacute;nh m???t kh&aacute;ch h&agrave;ng ti???m n??ng, n&ecirc;n nh&oacute;m quy???t ?????nh bi???n ?????i c&aacute;c bi???n missing c&oacute; t??? l??? nh??? sang gi&aacute; tr??? c&oacute; t??? l??? th&agrave;nh c&ocirc;ng cao nh???t trong b??? d??? li???u. C??? th???:</span>
        <ul>
            <li style="line-height: 1.5;"><span style="font-size: 14px;">Bi???n education: &apos;unknown&apos; -&gt; &apos;<span style="color: rgb(184, 49, 47);">university-degree</span>&apos;&nbsp;</span></li>
            <li style="line-height: 1.5;"><span style="font-size: 14px;">Bi???n loan: &apos;unknown&apos; -&gt; &apos;<span style="color: rgb(184, 49, 47);">no</span>&apos;&nbsp;</span></li>
            <li style="line-height: 1.5;"><span style="font-size: 14px;">Bi???n housing: &apos;unknown&apos; -&gt; &apos;<span style="color: rgb(184, 49, 47);">yes</span>&apos;</span></li>
            <li style="line-height: 1.5;"><span style="font-size: 14px;">Bi???n marital: &apos;unknown&apos; -&gt; &apos;<span style="color: rgb(184, 49, 47);">single</span>&apos;</span></li>
            <li style="line-height: 1.5;"><span style="font-size: 14px;">Bi???n job: &apos;unknown&apos; -&gt; &apos;<span style="color: rgb(184, 49, 47);">student</span>&apos;</span></li>
"""
pre_process_2 = """
<ul style="list-style-type: square;">
    <li><span style="font-size: 14px;">?????i v???i bi???n c&oacute; t??? l??? missing cao &apos;default&apos; - 20%, v&igrave; bi???n n&agrave;y kh&ocirc;ng c&oacute; d???u hi???u nh???n bi???t r&otilde; r&agrave;ng n&ecirc;n nh&oacute;m quy???t ?????nh kh&ocirc;ng thay ?????i thu???c t&iacute;nh c???a bi???n n&agrave;y.</span></li>
</ul>
<p style="line-height: 1.5;"><span style="font-size: 14px;">4. Outlier:</span></p>
<ul style="list-style-type: square;">
    <li style="line-height: 1.5;"><span style="font-size: 14px;">Bi???n age: thay th??? c&aacute;c gi&aacute; tr??? outlier (t???c l???n h??n 70) b???ng 70.</span></li>
    <li style="line-height: 1.5;"><span style="font-size: 14px;">Bi???n campaign, previous, cons.conf.idx: thay th??? nh???ng gi&aacute; tr??? l???n h??n quantile_95 b???ng quantitle_95</span></li>
</ul>
<p style="line-height: 1.5;"><span style="font-size: 14px;">5. Ph&acirc;n lo???i bi???n:</span><span style="font-size: 14px;">Ph&acirc;n lo???i bi???n pdays th&agrave;nh 3 nh&oacute;m:&nbsp;</span></p>
<ul style="list-style-type: square; line-height: 1.5;">
    <li><span style="font-size: 14px;">&apos;not_previously_contacted&apos;: cho c&aacute;c gi&aacute; tr??? &ge; 999</span></li>
    <li><span style="font-size: 14px;">&apos;over_a_week&apos;: cho c&aacute;c gi&aacute; tr??? &ge; 7 v&agrave; &lt; 999</span></li>
    <li><span style="font-size: 14px;">&apos;within_a_week&apos;: cho c&aacute;c gi&aacute; tr??? &ge; 0 v&agrave; &lt; 7</span></li>
</ul>
<p><br></p>
"""
metric = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">M???c d&ugrave; nh&oacute;m s??? d???ng 04 c&ocirc;ng th???c t&iacute;nh AC ph??? bi???n nh???t l&agrave;: Accuracy, Precision, Recall v&agrave; F1. Tuy nhi&ecirc;n, v&igrave; m???c ti&ecirc;u cu???i c&ugrave;ng l&agrave; l&agrave;m th??? n&agrave;o ????? ti???p c???n ???????c nhi???u kh&aacute;ch h&agrave;ng ti???m n??ng nh???t - hay n&oacute;i c&aacute;ch kh&aacute;c l&agrave; tr&aacute;nh vi???c b??? s&oacute;t kh&aacute;ch h&agrave;ng ti???m n??ng, nh&oacute;m quy???t ?????nh s??? quan t&acirc;m nh???t ?????n k???t qu??? c???a Recall.</span></p>
"""

overview_1 = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">M???c ??&iacute;ch d??? &aacute;n: Nghi&ecirc;n c???u v??? chi???n d???ch ti???p th??? khuy???n kh&iacute;ch kh&aacute;ch h&agrave;ng g???i ti???n ti???t ki???m th&ocirc;ng qua ??i???n tho???i c???a ng&acirc;n h&agrave;ng, t??? ??&oacute; x&acirc;y d???ng m&ocirc; h&igrave;nh d??? ??o&aacute;n v??? m???c ????? th&agrave;nh c&ocirc;ng c???a chi???n d???ch ?????i v???i nh&oacute;m kh&aacute;ch h&agrave;ng m???c ti&ecirc;u v&agrave; ??&aacute;nh gi&aacute; hi???u qu??? kinh t??? n???u &aacute;p d???ng m&ocirc; h&igrave;nh ??&aacute;nh gi&aacute; v&agrave;o th???c t???.</span></p>
<p style="line-height: 1.5;"><span style="font-size: 14px;">T???p Dataset: B??? d??? li???u ???????c d&ugrave;ng l&agrave; d??? li???u c???a chi???n d???ch tele-marketing ??? Th??? Nh?? K??? (t??? 05/2008 ?????n 11/2010) tr&ecirc;n 41188 m???u v???i 20 thu???c t&iacute;nh kh&aacute;c nhau.</span></p>
<p style="line-height: 1.5;"><span style="font-size: 14px;">Ph????ng ph&aacute;p nhi&ecirc;n c???u: ?????i v???i b&agrave;i to&aacute;n n&agrave;y, nh&oacute;m ??&atilde; th???c hi???n ?????y ????? 7 b?????c/ 8 b?????c th&ocirc;ng th?????ng c???a m???t d??? &aacute;n data science th???c t??? trong doanh nghi???p nh?? b&ecirc;n d?????i:</span></p>
"""
overview_2 = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">Tuy nhi&ecirc;n, v&igrave; th???i gian ban t??? ch???c ????a ra cho d??? &aacute;n c&oacute; h???n c??ng nh?? v&igrave; l&agrave; l???n ?????u ti&ecirc;n tr???i nghi???m v???i d??? &aacute;n Data science th???c t???, nh&oacute;m kh&ocirc;ng tr&aacute;nh kh???i nhi???u sai s&oacute;t trong qu&aacute; tr&igrave;nh l&agrave;m. Nh&oacute;m r???t mong nh???n ???????c s??? th&ocirc;ng c???m, g&oacute;p &yacute; t??? qu&yacute; doanh nghi???p, ban t??? ch???c c??ng nh?? c&aacute;c b???n tham gia ch????ng tr&igrave;nh ????? nh&oacute;m c&oacute; th??? h???c t???p, s???a ch???a v&agrave; ho&agrave;n thi???n b&agrave;i h??n.</span></p>
"""

result_analysis = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">Nh???n x&eacute;t chung:</span></p>
<ul style="list-style-type: square;">
    <li style="line-height: 1.5;"><span style="font-size: 14px;">Nh&igrave;n v&agrave;o 2 c???t AC ?????u ti&ecirc;n, ta c&oacute; th??? th???y v???i 4 model ???????c ch???n l???c ????? ph&acirc;n t&iacute;ch AC ?????u cho k???t qu??? t???t tr&ecirc;n c??? t???p train v&agrave; t???p test. Ngo&agrave;i ra s??? kh&aacute;c bi???t v??? AC gi???a t???p train v&agrave; t???p test tr&ecirc;n m???i model kh&ocirc;ng kh&aacute;c bi???t nhi???u, ch???ng t??? kh&ocirc;ng c&oacute; s??? kh&aacute;c th?????ng v??? output c???a model.</span></li>
    <li style="line-height: 1.5;"><span style="font-size: 14px;">Nh&igrave;n v&agrave;o 03 c???t AC ??? cu???i, c&oacute; th??? nh???n th???y khi d&ugrave;ng XGBoost Classifier c&ugrave;ng v???i resampled data cho k???t qu??? cao nh???t tr&ecirc;n c??? 3 ch??? s??? Precision, Recall v&agrave; F1 tr&ecirc;n bi???n y = &quot;Yes&quot;, ?????ng th???i k???t qu??? Accuracy c???a model c??ng cao th??? hai so v???i c&aacute;c model kh&aacute;c..</span></li>
</ul>
<p style="line-height: 1.5;"><span style="font-size: 14px;">-&gt; Nh&oacute;m quy???t ?????nh s??? d???ng model </span><span style="color: rgb(0, 0, 0); font-family: Times; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: left; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;">XGBoost Classifier with under resampled data v&agrave;o th???c t???.</span></p>
"""

flow_source = """
<p><span style='color: rgb(44, 130, 201); font-family: sohne, "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 12px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; float: none; display: inline !important;'><em>inspired by&nbsp;</em></span><span style="color: rgb(44, 130, 201);"><a class="el gz" href="https://the-modeling-agency.com/crisp-dm.pdf" rel="noopener nofollow" style='box-sizing: inherit; color: inherit; text-decoration: underline; -webkit-tap-highlight-color: transparent; font-family: sohne, "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 14px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(255, 255, 255);'><span style="font-size: 12px;"><em>CRISP-DM 1.0</em></span></a></span></p>
"""

benefit = """
<p style="line-height: 1.5;"><span style="font-size: 14px;">V??? ???ng d???ng trong th???c t??? ?????i v???i model ch???n l???c, nh&oacute;m gi??? s???:</span></p>
<ul style="list-style-type: square;">
    <li style="line-height: 1.5;"><span style="font-size: 14px;">Kh&aacute;ch h&agrave;ng l???ng nghe 100% k???t qu??? c???a model</span></li>
    <li style="line-height: 1.5;"><span style="font-size: 14px;">Chi ph&iacute; tr&ecirc;n m???t cu???c g???i l&agrave; 10$ v&agrave; l???i nhu???n kh&aacute;ch h&agrave;ng thu ???????c tr&ecirc;n m???t cu???c g???i l&agrave; 20$</span></li>
</ul>
<p style="line-height: 1.5;"><span style="font-size: 14px;">Khi ??&oacute; kh&aacute;ch h&agrave;ng c&oacute; th??? t&iacute;nh to&aacute;n l???i nhu???n d???a v&agrave;o m&ocirc; h&igrave;nh t&iacute;nh to&aacute;n b&ecirc;n d?????i.</span></p>
"""

def main():
    
    st.title("Team 01")
    st.text(" B??i t???p cu???i kho?? ???????c ho??n th??nh b???i 04 th??nh vi??n b??n d?????i:")

    #Introduce team members
    col1, col2, col3, col4, col5, col6  = st.beta_columns(6)

    ava1 = Image.open("image/ava1.jpeg")
    ava2 = Image.open("image/ava2.jpeg")
    ava3 = Image.open("image/ava3.jpg")
    ava4 = Image.open("image/ava4.jpg")

    col1.header("Nguyen")
    col1.image(ava1, use_column_width=True)

    col2.header("Linh")
    col2.image(ava2, use_column_width=True)

    col3.header("Tuan")
    col3.image(ava3, use_column_width=True)

    col4.header("Hai")
    col4.image(ava4, use_column_width=True)

    # Tham kh???o: https://www.google.com/search?q=write+paragraph+in+streamlit+app&oq=write+paragraph+in+streamlit+app&aqs=chrome..69i57j33i160.10955j0j4&sourceid=chrome&ie=UTF-8#kpvalbx=_Dx_eYLayJ4y9rQGQ3J6YAg53

    #Title list
    h1=  """
    <div style="background-color:#004d99;padding:0px">
    <h2 style="color:white;text-align:center;">PROJECT OVERVIEW </h2>
    </div>
    """
    h2=  """
    <div style="background-color:#004d99;padding:0px">
    <h2 style="color:white;text-align:center;">DATA OVERVIEW </h2>
    </div>
    """
    h3=  """
    <div style="background-color:#004d99;padding:0px">
    <h2 style="color:white;text-align:center;">RESULT OVERVIEW </h2>
    </div>
    """
    
    # PROJECT OVERVIEW INFORMATION
    st.markdown(h1,unsafe_allow_html=True)
    st.markdown(overview_1, True)
    col1, col2, col3 = st.beta_columns((1,3,1))
    col2.image('image/analysis_flow.png')
    im1, im2, im3, im4, im5 = st.beta_columns(5)
    im4.markdown(flow_source, True)
    
    st.markdown(overview_2, True)
    

    # DATA OVERVIEW INFORMATION
    st.markdown(h2,unsafe_allow_html=True)

    #show dataframe with filter
    marketing_w_10_rows = marketing_df[0:20]
    st.subheader("DataFrame")
    filtered = st.multiselect("Filter columns", options=list(marketing_w_10_rows.columns), default=list(marketing_w_10_rows.columns))
    st.write(marketing_w_10_rows[filtered])

    # Create selected box to display chart
    st.subheader("Data Visualization")
    ax_size = 8
    title_size = 12
    an1, an2 = st.beta_columns(2)
    info_selectbox = an1.selectbox(
    "N???i dung ph??n t??ch",
    ("Th??ng tin chung", "C??c bi???n kh??ch h??ng", "C??c bi???n ph????ng ph??p ti???p c???n", "C??c bi???n x?? h???i","L??u ?? chung"))

    if info_selectbox == "Th??ng tin chung":
        # T??? l??? Missing c???a c??c bi???n
        missing_data = missing_exploration(marketing_null)

        fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2, figsize=(14,4)) 
        #Percentage of Target value
        data = marketing_df.groupby('y').size().sort_values(ascending=False)
        ax1.pie(x=data , autopct="%.1f%%", explode=[0.05]*len(data), labels=data.index.tolist());
        ax1.set_title("The percentage of Target value", fontsize=title_size);

        # Visualiza missing value percent
        sns.barplot(x=missing_data.index, y=missing_data['Percent %'], ax = ax2)
        ax2.set_title('Percent missing data by feature', fontsize=title_size)

        for ax in fig.axes:
            ax.tick_params(labelrotation=45)
        plt.tick_params(axis='both', which='major', labelsize=ax_size)
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False)

        #Text explain
        st.markdown(general, True)

    client_varible = {'age': age,'job': job, 'marital': marital,'education': education,'default': default, 'housing': housing, 'loan': loan,"emp.var.rate": emp_var_rate, "cons.price.idx" : cons_price_idx, "cons.conf.idx" : cons_conf_idx, "euribor3m" : euribor3m, "nr.employed" : nr_employed, 'contact': contact,'day_of_week': day_of_week,'duration': duration,'campaign': campaign,'pdays': pdays,'previous': previous,'poutcome': poutcome}

    if info_selectbox == "C??c bi???n kh??ch h??ng":
        varible_selectbox = an2.selectbox("T??n bi???n", ('age','job','marital','education','default', 'housing', 'loan'))
        if varible_selectbox == "age":
            visualize_numerical(marketing_df,'age',target = 'y')
            
        if varible_selectbox == "job":
            visualize_categorical_w_success(marketing_df,'job',target = 'y')

        if varible_selectbox == "marital":
            visualize_categorical_w_success(marketing_df,'marital',target = 'y')

        if varible_selectbox == "education":
            visualize_categorical_w_success_percent(marketing_df,'education',target = 'y')

        if varible_selectbox == "default":
            visualize_categorical_w_success_percent(marketing_df,'default',target = 'y')
        
        if varible_selectbox == "housing":
            visualize_categorical_w_success(marketing_df,'housing',target = 'y')
        
        if varible_selectbox == "loan":
            visualize_categorical_w_success(marketing_df,'loan',target = 'y')
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False)

        # visualization
        if varible_selectbox in client_varible.keys():
            st.markdown(client_varible[varible_selectbox], True)
    
    if info_selectbox == "C??c bi???n ph????ng ph??p ti???p c???n":
        bank_varible_selectbox = an2.selectbox("T??n bi???n",('contact','day_of_week','duration','campaign','pdays','previous','poutcome'))

        if bank_varible_selectbox == 'contact':
            visualize_categorical_w_success(marketing_df,'contact',target = 'y')

        if bank_varible_selectbox == 'day_of_week':
            visualize_categorical_w_success_percent(marketing_df,'day_of_week',target = 'y')

        if bank_varible_selectbox == 'month':
            look_up = {'jan': 1, 'feb': 2, 'mar': 3,'apr':4,'may': 5, 'jun': 6, 'jul':7, 'aug':8,'sep': 9,'oct': 10,'nov': 11,'dec':12}
            marketing_01 = marketing_df.copy()
            marketing_01['month_num']  = marketing_01.month.map(look_up)
            #visualize
            visualize_categorical_w_success(marketing_01 , 'month_num', target = 'y')

        if bank_varible_selectbox == 'duration':
            visualize_numerical(marketing_df,'duration')
        
        if bank_varible_selectbox == 'campaign':
            visualize_categorical_w_success(marketing_df,'campaign',target = 'y')

        if bank_varible_selectbox == 'pdays':
            data = marketing_df[marketing_df.pdays != 999]
            column = 'pdays'
            visualize_numerical(data,column)

        if bank_varible_selectbox == 'previous':
            visualize_numerical(marketing_df,'previous')

        if bank_varible_selectbox == 'poutcome':
            visualize_categorical_w_success(marketing_df,'poutcome',target = 'y')
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False)

        # text explaination
        if bank_varible_selectbox in client_varible.keys():
            st.markdown(client_varible[bank_varible_selectbox], True)

    if info_selectbox == "C??c bi???n x?? h???i":
        social_varible_selectbox = an2.selectbox("T??n bi???n", ("emp.var.rate", "cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed"))
        # Visualization
        visualize_numerical(marketing_df,social_varible_selectbox)
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # Explain Text
        if social_varible_selectbox in client_varible.keys():
            st.markdown(client_varible[social_varible_selectbox], True)

    if info_selectbox == "L??u ?? chung":
        col1, col2  = st.beta_columns(2)
        col1.markdown(comment_1, True)
        col2.markdown(comment_2, True)

    # Add Text in explaination
    st.set_option('deprecation.showPyplotGlobalUse', False)

    ### Model result
    st.markdown(h3,unsafe_allow_html=True)        
    result_img = Image.open("image/result_visualization.png")
    result_comparison = pd.read_csv('data/AC_result.csv',sep=',')
    
    #Description about result
    st.markdown("""<p><span style="font-size: 14px;">Trong qu&aacute; tr&igrave;nh x&acirc;y d???ng m&ocirc; h&igrave;nh d??? ??o&aacute;n v&agrave; ph&acirc;n t&iacute;ch, nh&oacute;m ??&atilde; th???c hi???n nhi???u b?????c pre-process kh&aacute;c nhau d???a v&agrave;o ph???n ph&acirc;n t&iacute;ch data c&ugrave;ng v???i vi???c th???c nghi???m tr&ecirc;n nhi???u m&ocirc; h&igrave;nh kh&aacute;c nhau ????? d??? ??o&aacute;n. Tuy nhi&ecirc;n ????? tr&aacute;nh g&acirc;y b???i r???i cho ng?????i ?????c, nh&oacute;m ch??? ch???n l???c ra b?????c pre-processing ???????c s??? d???ng ch&iacute;nh c&ugrave;ng 5 models cho ra k???t qu??? cao nh???t.</span></p>""", unsafe_allow_html=True)
    
    # 1. Pre-processing
    st.subheader("1. Ti???n x??? l?? d??? li???u")
    col1, col2  = st.beta_columns(2)
    col1.markdown(pre_process_1, True)
    col2.markdown(pre_process_2, True)

    #2. Evaluation metric
    st.subheader("2. Ph????ng ph??p ????nh gi??")
    st.markdown(metric,True)

    # 3. result
    st.subheader("3. K???t qu???")
    st.image(result_img, use_column_width=True)
    st.dataframe(result_comparison.style.highlight_max(axis=0))
    st.markdown(result_analysis, True)

    # 4 Benefit calculation
    st.subheader("3. L???i nhu???n d??? ki???n khi s??? d???ng m?? h??nh v??o th???c t???")
    st.markdown(benefit, True)   

    with st.form(key='my-form'):
        total_cus = st.number_input('T???ng s??? kh??ch h??ng li??n h???:')
        submit = st.form_submit_button(label = 'Calculate')
        save_cost = 20*int(total_cus)*0.933094 - 10*int(total_cus)
        if submit:
            st.write(f'L???i nhu???n thu ???????c l??: {save_cost}')


    df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
    
    # if add_selectbox == "Email":
    #     st.map(df)

if __name__=='__main__':
    Res=main()
 
    


    
    
   
# streamlit run apps/data_analysis.py