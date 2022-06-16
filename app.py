#Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

def convert_df_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def main():
    st.subheader("Upload the GWP file Excel")
    updated_file = st.file_uploader("Choose a file")
    if updated_file is not None:
        #df_raw = pd.read_csv(updated_file)
        df1 = pd.read_excel(updated_file)
         #Get overview of data
        st.write(df1.head()) 
        
        df1.to_csv ('converted.csv', index = None, header=True)
        df_raw = pd.DataFrame(pd.read_csv('converted.csv'))
    
        df_map = pd.read_csv('bcm.csv')

        drop_cols = ['OCCUPATION', 'Cancellation Type', 'POLICY TYPE', 'INTEREST', 'VESSEL NAME', 'ENDORSEMENT TYPE', 'SALES REGION', 'REMARK', 'APPROVED DATE', 'APPROVED USER', 'REFERANCE NO', 'BUSINESS SOURCE', 'Remark', 'ENGINE NUMBER', 'CHASSIS NUMBER', 'CONTACT NUMBER']
        df_raw.drop(drop_cols, axis=1, inplace=True)
        
        df_raw['FROM DATE'] = pd.to_datetime(df_raw['FROM DATE'], errors = 'coerce')
        df_raw['TO DATE'] = pd.to_datetime(df_raw['TO DATE'], errors = 'coerce')

        df_raw['TRANSACTION EFFECTIVE DATE'] = pd.to_datetime(df_raw['TRANSACTION EFFECTIVE DATE'])
        df_raw['DEBIT DATE'] = pd.to_datetime(df_raw['DEBIT DATE'])
        df_raw['FROM DATE'] = pd.to_datetime(df_raw['FROM DATE'])
        df_raw['TO DATE'] = pd.to_datetime(df_raw['TO DATE'])
        df_raw['RECEIPT DATE'] = pd.to_datetime(df_raw['RECEIPT DATE'])
        
        df_raw['Date Gap'] = df_raw['TRANSACTION EFFECTIVE DATE'] - df_raw['RECEIPT DATE']
        
        df_raw['Month'] = df_raw['TRANSACTION EFFECTIVE DATE'].dt.month
        df_raw['Year'] = df_raw['TRANSACTION EFFECTIVE DATE'].dt.year

        df_raw['Class'] = df_raw['POLICY NUMBER'].str[:1]
        df_raw['Branch Code'] = df_raw['POLICY NUMBER'].str[1:3]
        df_raw['Category'] = df_raw['POLICY NUMBER'].str[3:6]
        
        df_raw['GWP'] = df_raw['BASIC PREMIUM'] + df_raw['MANAGEMENT FEE'] + df_raw['SRCC'] + df_raw['TC']
        
        df_maped = pd.merge(df_raw, df_map, 
                        on='Branch Code', 
                        how='inner')

        df_maped.rename(columns = {'Channel':'Channel Code'}, inplace = True)

        # df_raw = df_maped
        
        # st.write(df_maped.head()) 
        st.subheader("Download the cleaned file csv")
        st.download_button(
            label="Download data as CSV",
            data=convert_df_to_csv(df_maped),
            file_name='GWP_cleaned.csv',
            mime='text/csv',
            )       
        
        # st.write(df_maped.head()) 
        
        df_nic = df_maped[df_maped.duplicated(['NIC Number'], keep=False)].sort_values(by='NIC Number')
        dup_cols_nic = ['POLICY NUMBER', 'NIC Number']
        df_nic_dup = df_nic[dup_cols_nic]
        st.subheader("Download duplicated NIC csv")
        st.download_button(
            label="Download data as CSV",
            data=convert_df_to_csv(df_nic_dup),
            file_name='nic_dup.csv',
            mime='text/csv',
            ) 
        
        # st.write(df_maped.head()) 
        df_name = df_maped[df_maped.duplicated(['NAME OF INSURED'], keep=False)].sort_values(by='NAME OF INSURED')
        dup_cols_names = ['POLICY NUMBER', 'NAME OF INSURED']
        df_name_dup = df_name[dup_cols_names]
        st.subheader("Download duplicated names csv")
        st.download_button(
            label="Download data as CSV",
            data=convert_df_to_csv(df_name_dup),
            file_name='name_dup.csv',
            mime='text/csv',
            ) 
        
        # st.write(df_maped.head()) 
        df_vhcl = df_maped[df_maped.duplicated(['VEHICLE NUMBER'], keep=False)].sort_values(by='VEHICLE NUMBER')
        dup_cols_vhcl = ['POLICY NUMBER', 'VEHICLE NUMBER']
        df_vhcl_dup = df_vhcl[dup_cols_vhcl]
        st.subheader("Download duplicated vehicles csv")
        st.download_button(
            label="Download data as CSV",
            data=convert_df_to_csv(df_vhcl_dup),
            file_name='vhcl_dup.csv',
            mime='text/csv',
            ) 
        
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
if __name__ == '__main__':
    main()