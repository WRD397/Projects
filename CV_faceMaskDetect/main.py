import os
from customModule import dataPreprocess,modelVGG16, faceMaskDetect

def main() -> None:
    ### Object Initiation
    preprocessObj = dataPreprocess()
    modelObj = modelVGG16()
    detectObj = faceMaskDetect()

    print('Loading to X and y to test the model once.')
    finalDataFolder = os.getenv("FINAL_DATASET_FOLDER")
    X_loaded, y_loaded = preprocessObj.ftLabelLoader(sourceFolder=finalDataFolder)
    _, X_test, _, y_test = preprocessObj.train_test(X=X_loaded, y=y_loaded)

    print('Model is getting loaded')
    folderPath = os.getenv('MODEL_COMPONENT_PATH')
    loadedModel = modelObj.modelLoading(folderPath=folderPath)
    print('Loaded Model Evaluation')
    modelObj.modelEvaluation(model=loadedModel, features=X_test, label=y_test)

    print('******* Start Capturing Video to Detect Mask/NonMask condition ********')
    detectObj.startVideo(model=loadedModel)

    return None



if __name__ == '__main__':
    try :
        main()
        print('main() ran successfully.')
    except Exception as e:
        print('********')
        print('main() failed to run due to the below error -> ')
        print(e)