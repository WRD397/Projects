import cv2 as cv
import pandas as pd
import numpy as np
from keras.applications.vgg16 import VGG16
from keras import Sequential
from keras.models import model_from_json
from keras.layers import Dense
import ssl
import tensorflow as tf
tf.config.run_functions_eagerly(True)
import os
import random
from sklearn.model_selection import train_test_split


class dataPreprocess :
    def __init__(self) -> None :
        print(f'class dataPreprocess initiated')
        return None
    
    def foo(self, data : pd.DataFrame) -> tuple:
        pass

    def imgResizer(self, imgPath:str, imgSize:tuple) -> cv.imread:
        img = cv.imread(imgPath)
        img = cv.resize(img, imgSize)

        return img

    def dataGenerator(self, sourceFolder:tuple) -> list[list]:
        data = []
        categories = ['Masked', 'Unmasked']
        maskedImgDir,nonMaskedImgDir = sourceFolder
        for cat in categories : 
            if categories.index(cat) == 0:
                path = maskedImgDir
                for file in os.listdir(path):
                    file_path = os.path.join(path, file)
                    label = categories.index(cat)
                    data.append([self.imgResizer(imgPath=file_path, imgSize=(224,224)), label])
            else :
                path = nonMaskedImgDir
                for file in os.listdir(path):
                    file_path = os.path.join(path, file)
                    label = categories.index(cat)
                    data.append([self.imgResizer(imgPath=file_path, imgSize=(224,224)), label])
        
        print(f'Length of Data : {len(data)}')
        random.shuffle(data)

        return data

    
    def ftTarget(self, data:list[list], finalDataFolder : str) -> tuple[list, list]:
        X = []
        y = []
        for ft, label in data:
            X.append(ft)
            y.append(label)
        print(f'X len -> {len(X)}')
        print(f'y len -> {len(y)}')
        print(f'X[:3] -> \n{X[:3]}')
        print(f'y[:3] -> \n{y[:3]}')
        X = np.array(X)
        y = np.array(y)
        ### standardizing
        X = X/255
        print('Features and Labels are generated and stored in the below location')
        print(finalDataFolder)
        pathToSaveX = os.path.join(finalDataFolder, 'feature.npy')
        pathToSaveY = os.path.join(finalDataFolder, 'label.npy')
        np.save(pathToSaveX, X)
        np.save(pathToSaveY, y)

        return (X,y)
    
    def ftLabelLoader(self, sourceFolder:str) -> tuple[list, list]:
        X_path = os.path.join(sourceFolder, 'feature.npy')
        y_path = os.path.join(sourceFolder, 'label.npy')
        X_loaded = np.load(X_path)
        y_loaded = np.load(y_path)
        print('feature and label arrays are loaded successfully.')
        return X_loaded, y_loaded
    

    def train_test(self, X:np.array, y:np.array) -> tuple:
        X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2)
        print(f"X_train shape : {X_train.shape}")
        print(f"X_test shape : {X_test.shape}")

        return X_train,X_test, y_train, y_test


class modelVGG16:
    def __init__(self) -> None:
        print('class modelVGG16 is initiated - VGG16 is ready to load.')
        return None
    
    def vggCustomised(self) -> callable:
        ### Use the next line to avoid the "CERTIFICATE_VERIFY_FAILED" error while downloading the weights of the model.
        ssl._create_default_https_context = ssl._create_unverified_context
        vgg = VGG16()
        model = Sequential()

        ### Removing the last layer of VGG16 original model.
        for layer in vgg.layers[:-1]:
            model.add(layer)

        ### Freezing the layers so that the all the trainable parameters dont get trained while training
        for layer in model.layers:
            layer.trainable = False

        ### Adding the Last Layer with one output Node
        model.add(Dense(1,activation='sigmoid'))
        print('***** Model Summary *****')
        print(model.summary())

        return model
    


    def compileFit(self,
                   model:callable, 
                   optimizer:str, 
                   learningRate:float,
                   loss:str,
                   metrics:list,
                   epochs:int,
                   train_data:tuple,
                   validation_data:tuple) -> callable:
        model = model
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        model.fit(x=train_data[0], y=train_data[1], epochs=epochs, validation_data=validation_data)

        return model


    def modelStoring(self, model:callable, folderPath:str) -> None:

        # serialize model to JSON
        model_json = model.to_json()
        modelPath = os.path.join(folderPath,'model.json')
        modelWeightsPath = os.path.join(folderPath, 'model.weights.h5')
        with open(modelPath, "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights(modelWeightsPath)
        print("Saved model to disk")

        return None
    

    def modelLoading(self, folderPath:str) -> callable:

        modelPath = os.path.join(folderPath,'model.json')
        modelWeightsPath = os.path.join(folderPath, 'model.weights.h5')

        json_file = open(modelPath, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(modelWeightsPath)
        print("Loaded model from disk")

        return loaded_model


    def modelEvaluation(self, model:callable, features:np.array, label:np.array) -> None :
        score = model.evaluate(features, label)
        print(f'Metric : {model.metrics_names[1]}')
        print(f'Score : {score[1]}') 

        return None


class faceMaskDetect:
    def __init__(self) -> None:
        pass
        return None

    def detect(self, img:cv.imread, model:callable) -> int:

        yPred = (model.predict(img.reshape(1,224,224,3)) > 0.5).astype("int32")

        return yPred


    def writeLabel(self, img, text, position, color) -> None:
        textSize = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, cv.FILLED)
        end_x = position[0] + textSize[0][0] + 2
        end_y = position[1] + textSize[0][1] - 2

        cv.rectangle(img, position, (end_x, end_y), color, 1)
        cv.putText(img, text, position, cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv.LINE_AA)

        return None
    

    def startVideo(self, model) -> None:
        captureVideo = cv.VideoCapture(0)
        print('Detection is Switched On ...')
        while True:
            _, frame = captureVideo.read()

            img = cv.resize(frame, (224,224))
            ### calling the faceDetection method
            predictedVal = self.detect(img, model=model)
            if predictedVal == 0:
                self.writeLabel(frame, "No Mask", (30,30), (0,0,255))
            else : 
                self.writeLabel(frame, "Mask On", (30,30), (0,255,0))
            cv.imshow('Window', frame)

            if cv.waitKey(1) & 0xFF == ord('x'):
                print('Detection is Switched Off')
                break
        
        cv.destroyAllWindows()

        return None



if __name__ == '__main__':
    ...
