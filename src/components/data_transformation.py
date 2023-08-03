import os
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object




@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')



class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    
    def get_data_transformer_object(self):
        
        try :
            categorical_columns = ['holiday', 'weather_main', 'weekday', 'hour', 'month']
            numerical_columns = ['temp', 'clouds_all']
            
            
            # holiday = ['no holiday', 'yes holiday']
            # hour = ['Morning', 'Afternoon', 'Evening', 'Night', 'Late Night','Early Morning']
            # month = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            # weather_main = ['Clouds', 'Clear', 'Rain', 'Drizzle', 'Mist', 'Haze', 'Fog','Thunderstorm', 'Snow', 'Squall', 'Smoke']
            # weekday = [1, 2, 3, 4, 5, 6, 0]
            
            
        
            holiday = ['no holiday', 'yes holiday']
            hour = ['Early Morning', 'Morning', 'Afternoon', 'Evening', 'Night', 'Late Night']
            month = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
            weather_main = ['Clouds', 'Clear', 'Rain', 'Drizzle', 'Mist', 'Haze', 'Fog', 'Thunderstorm', 'Snow', 'Squall', 'Smoke']
            weekday = ['0', '1', '2', '3', '4', '5', '6']

            
            
            num_pipeline = Pipeline(
                steps=[
                    ("scaler" , StandardScaler())
                ]
            )
            
            cat_pipeline = Pipeline(
                steps=[
                    ("one_hot_encoder",OrdinalEncoder(categories=[holiday,weather_main,weekday,hour,month])),
                    ("scaler" , StandardScaler())
                ]
            )
            
            
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")
            
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns),
                ]
            )
            
            
            
            
            
            return preprocessor
            
            
        except Exception as e:
            raise CustomException(e,sys)   
        
        
    
    
    def initiate_data_tranformation(self,train_path,test_path):
        
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("reading test and train data completed")
            logging.info("obtaining pre-processor object")
            
            preprocessor_obj = self.get_data_transformer_object()
            
            target_column_name="traffic_volume"
            
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]
            
            # logging.info(
            #     f"Applying preprocessing object on training dataframe and testing dataframe."
            # )

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr  = preprocessor_obj.transform(input_feature_test_df)
           
           
            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]
            
            logging.info(f"Saved preprocessing object.")
            
            
            save_object(
                file_path =  self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
                )
            
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
            
        except Exception as e:
            raise CustomException(e,sys)    
    
    


            
            
    