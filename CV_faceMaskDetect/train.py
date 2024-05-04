import os
import random
import pandas as pd
from customModule import dataPreprocess, modelVGG16, faceMaskDetect
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

### Creating the Labels manually 
def main() -> None:
    ### Object Initiations
    dp = dataPreprocess()
    modelObj = modelVGG16()

    maskedImgDir = os.getenv('MASKED_IMG_FOLDER')
    nonMaskedImgDir = os.getenv('NON_MASKED_IMG_FOLDER')
    print('Generating the numerical data from two categories of images - Masked / Non Masked')
    data = dp.dataGenerator(sourceFolder=(maskedImgDir,nonMaskedImgDir))

    print("Creating Features and Labels from the numerical data")
    finalDataFolder = os.getenv("FINAL_DATASET_FOLDER")
    X,y = dp.ftTarget(data=data, finalDataFolder=finalDataFolder)

    ### Train Test
    print('splitting into Train Test')
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2)
    print(f"X_train shape : {X_train.shape}")
    print(f"X_test shape : {X_test.shape}")


    ### Model Training
    print('*** Model Training Started ***')
    print('Loading the model')
    model = modelObj.vggCustomised()
    print('***** Fitting started....')
    model = modelObj.compileFit(model=model,
                                optimizer='adam',
                                learningRate=0.0001,
                                loss='binary_crossentropy',
                                metrics=['accuracy'],
                                epochs=5,
                                train_data=(X_train,y_train),
                                validation_data=(X_test,y_test))
    print('Fitting complete.')
    print('Evaluation Score')
    modelObj.modelEvaluation(model=model, features=X_test, label=y_test)
    modelDestinationDir = os.getenv('MODEL_COMPONENT_PATH')
    modelObj.modelStoring(model=model, folderPath=modelDestinationDir)
    print('Model is stored in the below location :')

    return None



if __name__ == '__main__':
    try :
        main()
        print('main() ran successfully.')
    except Exception as e:
        print('********')
        print('main() failed to run due to the below error -> ')
        print(e)

