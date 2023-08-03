import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import pandas as pd





@dataclass
class DataIngestionConfig:
 train_data_path = os.path.join("artifacts","train.csv")
 test_data_path = os.path.join("artifacts","test.csv")
 raw_data_path = os.path.join("artifacts","raw.csv")
    
    
class DataIngestion:
    logging.info("entered data ingestion class")
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        
    def Initiate_Data_Ingestion(self):
        logging.info("data ingestion intitated")
        
        try :
            
            data = pd.read_csv(r"F:\study material\Data Science\modular coding assignment\metro interstate traffic volume prediction\notebooks\data\cleaned.csv")
            logging.info("data read successfulyy")
            
            dir_name = os.path.dirname(self.ingestion_config.raw_data_path)
            os.makedirs(dir_name,exist_ok=True)
            logging.info("directory has been made")
            
            data.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info("raw data has been saved")
            
            train_set , test_set = train_test_split(data,test_size=0.1,random_state=8)
            logging.info("train and test split done")
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info("train and test data has been saved")
            
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
            
            
            
            
        
        except Exception as e:
            logging.info("exception occurs")
            raise CustomException(e,sys)        
        
        
