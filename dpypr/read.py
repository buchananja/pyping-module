import pandas as pd
import dpypr as dp
import os
import sqlite3
from sqlite3 import OperationalError
import logging


'''
the 'read' module contains functionality for reading data of various datatypes
into data pipelines
'''


# creates logging instance
logger = logging.getLogger(__name__)


def read_all_json(path, messaging = True):
    '''
    - iteratively loads all json files from the data directory and assigns to 
    dataframes
    - logger.infos number of records
    '''
    
    if dp.check_path_valid(path):
        files = os.listdir(path)
        data_dictionary = dict()
    else:
        logger.info('Please enter a valid path.')
        
    for file in files:
        if file.endswith('.json'):
            df = pd.read_json(os.path.join(path, file))
            filename = os.path.splitext(file)[0]
            data_dictionary[f'df_{filename}'] = df
            
            if messaging:
                logger.info(f'read df_{filename} ({len(filename):,} records).')
                
    if not data_dictionary:
        logger.info('No files read.')
        
    return data_dictionary


def read_all_csv(path, seperator = ',', messaging = True):
    '''
    - iteratively loads all csv files from the data directory and assigns to 
    dataframes
    - logger.infos number of records
    '''
    
    if dp.check_path_valid(path):
        files = os.listdir(path)
        data_dictionary = dict()
    else:
        logger.info('Please enter a valid path.')
    
    for file in files:
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(path, file), sep = f'{seperator}')
            filename = os.path.splitext(file)[0]
            data_dictionary[f'df_{filename}'] = df
            
            if messaging:
                logger.info(f'read df_{filename} ({len(filename):,} records).')
                
    if not data_dictionary:
        logger.info('No files read.')
        
    return data_dictionary


def read_all_xlsx(path, messaging = True):
    '''
    - iteratively loads all xlsx files from the data directory and assigns to 
    dataframes
    - logger.infos number of records
    '''
    
    if dp.check_path_valid(path):
        files = os.listdir(path)
        data_dictionary = dict()
    else:
        logger.info('Please enter a valid path.')
        
    for file in files:
        if file.endswith('.xlsx'):
            df = pd.read_excel(os.path.join(path, file))
            filename = os.path.splitext(file)[0]
            data_dictionary[f'df_{filename}'] = df
            
            if messaging:
                logger.info(f'read df_{filename} ({len(filename):,} records).')
                
    if not data_dictionary:
        logger.info('No files read.')
        
    return data_dictionary


def read_all_feather(path, messaging = True):
    '''
    - iteratively loads all feather files from the data directory and assigns to 
    dataframes
    - logger.infos number of records
    '''
    
    if dp.check_path_valid(path):
        files = os.listdir(path)
        data_dictionary = dict()
    else:
        logger.info('Please enter a valid path.')
        
    for file in files:
        if file.endswith('.feather'):
            df = pd.read_feather(os.path.join(path, file))
            filename = os.path.splitext(file)[0]
            data_dictionary[f'df_{filename}'] = df
            
            if messaging:
                logger.info(f'read df_{filename} ({len(filename):,} records).')
                
    if not data_dictionary:
        logger.info('No files read.')
        
    return data_dictionary


def read_all_parquet(path, messaging = True):
    '''
    - iteratively loads all parquet files from the data directory and assigns to 
    dataframes
    - logger.infos number of records
    '''
    
    if dp.check_path_valid(path):
        files = os.listdir(path)
        data_dictionary = dict()
    else:
        logger.info('Please enter a valid path.')
        
    for file in files:
        if file.endswith('.parquet'):
            df = pd.read_parquet(os.path.join(path, file))
            filename = os.path.splitext(file)[0]
            data_dictionary[f'df_{filename}'] = df
            
            if messaging:
                logger.info(f'read df_{filename} ({len(filename):,} records).')
                
    if not data_dictionary:
        logger.info('No files read.')
        
    return data_dictionary


def read_all_pickle(path, messaging = True):
    '''
    - iteratively loads all pickle files from the data directory and assigns to 
    dataframes
    - logger.infos number of records
    '''
    
    if dp.check_path_valid(path):
        files = os.listdir(path)
        data_dictionary = dict()
    else:
        logger.info('Please enter a valid path.')
        
    for file in files:
        if file.endswith('.pickle'):
            df = pd.read_pickle(os.path.join(path, file))
            filename = os.path.splitext(file)[0]
            data_dictionary[f'df_{filename}'] = df
            
            if messaging:
                logger.info(f'read df_{filename} ({len(filename):,} records).')
                
    if not data_dictionary:
        logger.info('No files read.')
        
    return data_dictionary
     
              
def read_all_sqlite(path, messaging = True):
    '''
    - iteratively loads all tables from sqlite database and assigns to 
    dataframes
    - logger.infos number of records
    '''
    
    try:
        if dp.check_path_valid(path):
            conn = sqlite3.connect(path)
            cur = conn.cursor()
    except OperationalError:
        logger.info('WARNING: Failed to connect to database.')
    
    # queries all tables in database
    cur.execute('''
        SELECT name 
        FROM sqlite_master 
        WHERE type = 'table';
    ''')
    
    # returns list of table names
    table_names = cur.fetchall()
    
    data_dictionary = dict()
    for table_name in table_names:
        # selects everything from each table.
        query = f"SELECT * FROM {table_name[0]}"
        data_dictionary[table_name[0]] = pd.read_sql_query(query, conn)
        
        if messaging:
            logger.info(f'read df_{table_name[0]} ({len(data_dictionary[table_name[0]]):,} records).')
    
    # closes cursor and connection to database
    cur.close() 
    conn.close()
    
    if not data_dictionary:
        logger.info('No files read.')
        
    return data_dictionary     


def gather_data_dictionary(globals_dict):
    '''
    packages all dataframes in input dictionary beginning with 'df_' and 
    returns output dictionary
    '''
    
    data_dictionary = dict()
    
    for name, data in globals_dict.items():
        if name.startswith('df_') and isinstance(data, pd.DataFrame):
            data_dictionary.update({name: data})
    if not data_dictionary:
        logger.info('No files found.')
        
    return data_dictionary


def unpack_data_dictionary(
        input_dictionary, 
        output_dict = None, 
        messaging = False
    ):
    '''
    - loads all data from data_dictionary into global variables with record 
    counts
    - if output_dict is provided, output_dict will be updated and not returned
    - if output_dict is not provided, a new dictionary will be returned
    '''
    
    # checks whether output dictionary provided
    if output_dict is None:
        output_dict = dict()
        return_dict = True
    else:
        return_dict = False
    
    # unpacks all dataframes to globals are prefixes name with 'df_'
    for key, value in input_dictionary.items():
        if isinstance(value, pd.DataFrame):
            output_dict[f'df_{key}'] = value
            
            if messaging:
                logger.info(f'Loaded df_{key} ({len(value):,} records).')

    if return_dict:
        return output_dict