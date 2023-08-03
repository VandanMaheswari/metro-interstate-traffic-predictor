import os
import sys
from dataclasses import dataclass

from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")
    
    
class ModelTrainer:
    
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
    
    def initiate_model_trainer(self,train_array,test_array):
        
        try :
            logging.info("Split training and test input data")
            
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            
            
            
            # model = RandomForestRegressor()
            # the actual model is random forest but because its model.pkl is above 350mb so we won't be able to upload on github thats 
            # why we use KNeighborsRegressor right now
            model = KNeighborsRegressor(n_neighbors=10)

            
            
            
            
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            r2_square = r2_score(y_pred,y_test)
            
            
            
            if r2_square<0.55:
                raise CustomException("No best model found")
                logging.info(f"Best found model on both training and testing dataset")  
            
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=model
            )      
            
            # print(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')
            # print('\n====================================================================================\n')
            # logging.info(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')
            
            
            return r2_square
        
        
            
        
        
        
        except Exception as e :
            CustomException(e,sys)
           
        
                