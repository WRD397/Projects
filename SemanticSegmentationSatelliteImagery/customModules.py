import os
import cv2
from PIL import Image
import numpy as np
from patchify import patchify
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import random
from tensorflow.keras.utils import to_categorical

from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, Conv2DTranspose
from keras.layers import concatenate, BatchNormalization, Dropout, Lambda
from keras import backend as kerasBackend


class mainBase:

  def __init__(self)->None:
    print("'mainBase' - Initiated.")
    return None

  # ********** USED LABELS *********  
  # building : 0
  # land:1
  # road:2
  # vegetation:3
  # water:4
  # unlabeled:5

  datasetName = "data"
  datasetRootFolder = '/content/drive/MyDrive/ProjectWorks/semanticSegmentationSatelliteImagery/'

  def foo(self)->None:
    return 'hello'


class imagePreprocess(mainBase):

  def __init__(self)->None:
    print("'imagePreprocess' - Initiated.")
    self.imageTypes = ['images', 'masks']
    self.image_patch_size=256
    self.titleIdRange=np.arange(1,8)
    self.imageIdRange=np.arange(1,20)

    self.segmentList = ['Building', 'Land', 'Road', 'Vegetation', 'Water', 'Unlabeled']
    self.hexBuilding = '3C1098'
    self.hexLand = '8429F6'
    self.hexRoad = '6EC1E4'
    self.hexVegetation = 'FEDD3A'
    self.hexWater = 'E2A929'
    self.hexUnlabeled = '9B9B9B'

    return None

  def normalize(self, individual_patched_image:list)->list:
    minmaxscaler = MinMaxScaler()
    reshapedImage = individual_patched_image.reshape(-1, individual_patched_image.shape[-1])
    scaledImage = minmaxscaler.fit_transform(reshapedImage)
    scaledImage = scaledImage.reshape(individual_patched_image.shape)
    return scaledImage

  def patchifyImg(self,image:list) -> list:
    size_x = (image.shape[1]//self.image_patch_size)*self.image_patch_size
    size_y = (image.shape[0]//self.image_patch_size)*self.image_patch_size
    image = Image.fromarray(image)
    image = image.crop((0,0, size_x, size_y))
    image = np.array(image)
    patched_images = patchify(image, (self.image_patch_size, self.image_patch_size, 3), step=self.image_patch_size)

    return patched_images

  def createDataset(self)->tuple[list]:
    imageDataset = []
    maskedDataset = []
    ### Deciding the extensions
    for image_type in self.imageTypes:
      if image_type == 'images':
        image_extension = 'jpg'
      elif image_type == 'masks':
        image_extension = 'png'

      for tile_id in self.titleIdRange:
        for image_id in self.imageIdRange:
          image = cv2.imread(f'{self.datasetRootFolder}/{self.datasetName}/Tile {tile_id}/{image_type}/image_part_00{image_id}.{image_extension}',1)

          if image is not None:

            if image_type == 'masks':
              image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            patched_images = self.patchifyImg(image)
            for i in range(patched_images.shape[0]):
              for j in range(patched_images.shape[1]):
                if image_type == 'images':
                  individual_patched_image = patched_images[i,j,:,:]
                  individual_patched_image = self.normalize(individual_patched_image)
                  individual_patched_image = individual_patched_image[0]
                  imageDataset.append(individual_patched_image)
                elif image_type == 'masks':
                  individual_patched_mask = patched_images[i,j,:,:]
                  individual_patched_mask = individual_patched_mask[0]
                  maskedDataset.append(individual_patched_mask)

    return imageDataset, maskedDataset


  def hex2RGB(self)->dict:
    segmentRGBDict = {}

    segmentRGBDict['buildingRGB'] = np.array(tuple(int(self.hexBuilding[i:i+2], 16) for i in (0,2,4)))
    segmentRGBDict['landRGB'] = np.array(tuple(int(self.hexLand[i:i+2], 16) for i in (0,2,4)))
    segmentRGBDict['roadRGB'] = np.array(tuple(int(self.hexRoad[i:i+2], 16) for i in (0,2,4)))
    segmentRGBDict['vegetationRGB'] = np.array(tuple(int(self.hexVegetation[i:i+2], 16) for i in (0,2,4)))
    segmentRGBDict['waterRGB']= np.array(tuple(int(self.hexWater[i:i+2], 16) for i in (0,2,4)))
    segmentRGBDict['unlabeledRGB'] = np.array(tuple(int(self.hexUnlabeled[i:i+2], 16) for i in (0,2,4)))
    return segmentRGBDict

  def RGB2labelSeg(self, label:list):
    segmentRGBDict = self.hex2RGB()
    labelSegment = np.zeros(label.shape, dtype=np.uint8)

    for i,(key,value) in enumerate(segmentRGBDict.items()):
      labelSegment[np.all(label == value, axis=-1)] = i

    labelSegment = labelSegment[:,:,0]
    return labelSegment

  def labelling(self,maskedDataset:list)->list:
    labelList = []
    for i in range(maskedDataset.shape[0]):
      labelSegment = self.RGB2labelSeg(label=maskedDataset[i])
      labelList.append(labelSegment)

    labelList = np.array(labelList) 
    labelList = np.expand_dims(labelList, axis=3)
    print('labelList length : ',len(labelList))

    return labelList

  def maskedPlotComparison(self, imageDataset:list, maskedDataset:list)->None:   
    randomImage= random.randint(0, len(imageDataset))
    plt.figure(figsize=(15,10))
    plt.subplot(121)
    plt.imshow(imageDataset[randomImage])
    plt.subplot(122)
    plt.imshow(maskedDataset[randomImage])

    return None


class modelBuilding(mainBase):

  def __init__(self)->None:
    print("'modelBuilding' - Initiated")
    self.testSize = 0.15

    return None


  def trainTestSplit(self, imageDataset, maskedDataset):
    labelsCategorical = to_categorical(labels, num_classes=total_classes)
    X_train, X_test, y_train, y_test = train_test_split(imageDataset, labels_categorical_dataset, test_size=self.testSize,shuffle=True ,random_state=0)
    print('X_train : ',X_train.shape)
    print('X_test : ',X_test.shape)
    print('y_train : ',y_train.shape)
    print('y_test : ',y_test.shape)
    
    return X_train, X_test, y_train, y_test
  

  def trainTestLoader(self) -> tuple[list]:
    X_train = np.load(os.path.join(self.trainTestRootDir, 'X_train.npy'))
    X_test = np.load(os.path.join(self.trainTestRootDir, 'X_test.npy'))
    y_train = np.load(os.path.join(self.trainTestRootDir, 'y_train.npy'))
    y_test = np.load(os.path.join(self.trainTestRootDir, 'y_test.npy'))
    print('X_train : ',X_train.shape)
    print('X_test : ',X_test.shape)
    print('y_train : ',y_train.shape)
    print('y_test : ',y_test.shape)

    return X_train, X_test, y_train, y_test
  
  def jaccardCoef(self, y_pred:list, y_test:list)->float:
    y_pred_flat = kerasBackend.flatten(y_pred)
    y_true_flat = kerasBackend.flatten(y_test)
    intersection = kerasBackend.sum(y_pred_flat*y_true_flat)
    union = kerasBackend.sum(y_pred_flat) + kerasBackend.sum(y_true_flat) - intersection

    jCoef = intersection + 1.0 / (union + 1.0)

    return jCoef
  
  def unetMulti(self):
    """
    Trying to replicate the original model architecture, proposed in the U-NET Paper
    The original paper was written in the regards of Biomedical images, so for satellite images, the hyperparameters won't be same - experimentations needed
    """

    nClasses=5
    imageHeight = self.image_patch_size
    imageWidth = self.image_patch_size
    imageChannels = 1
    
    ### Layes
    ############# Max Pooling
    #### 1st Chunk
    input=Input((imageHeight, imageWidth, imageChannels))
    sourceInput = input
    c1=Conv2D(filters=16, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(sourceInput)
    c1=Dropout(0.2)(c1)
    c1=Conv2D(filters=16, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
    pool1 = MaxPooling2D(c1)

    #### 2nd Chunk
    c2=Conv2D(filters=32, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(pool1)
    c2=Dropout(0.2)(c2)
    c2=Conv2D(filters=32, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(c2)
    pool2 = MaxPooling2D(c2)

    #### 3rd Chunk
    c3=Conv2D(filters=64, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(pool2)
    c3=Dropout(0.2)(c3)
    c3=Conv2D(filters=64, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(c3)
    pool3 = MaxPooling2D(c3)

    #### 4th Chunk
    c4=Conv2D(filters=128, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(pool3)
    c4=Dropout(0.2)(c4)
    c4=Conv2D(filters=128, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(c4)
    pool4 = MaxPooling2D(c4)


    ############# Base
    #### 5th Chunk
    b=Conv2D(filters=256, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(pool4)
    b=Dropout(0.2)(b)
    b=Conv2D(filters=256, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(b)


    ############# Up Conversion
    #### 6th Chunk
    u1=Conv2DTranspose(128, (2,2), strides=(2,2), padding='same')(b)
    u1 = concatenate([u1, c4])
    u1 = Conv2D(filters=128, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(u1)
    u1 = Dropout(0.2)(u1)
    u1 = Conv2D(filters=128, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(u1)

    #### 7th Chunk
    u2 = Conv2DTranspose(64, (2,2), strides=(2,2), padding='same')(u1)
    u2 = concatenate([u2, c3])
    u2 = Conv2D(filters=64, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(u2)
    u2 = Dropout(0.2)(u2)
    u2 = Conv2D(filters=64, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(u2)

    #### 7th Chunk
    u3 = Conv2DTranspose(64, (2,2), strides=(2,2), padding='same')(u2)
    u3 = concatenate([u3, c2])
    u3 = Conv2D(filters=32, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(u3)
    u3 = Dropout(0.2)(u3)
    u3 = Conv2D(filters=32, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(u3)

    #### 7th Chunk
    u4 = Conv2DTranspose(16, (2,2), strides=(2,2), padding='same')(u3)
    u4 = concatenate([u4, c1], axis=3)
    u4 = Conv2D(filters=16, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(u4)
    u4 = Dropout(0.2)(u4)
    u4 = Conv2D(filters=16, kernel_size=(3,3), activation='relu', kernel_initializer='he_normal', padding='same')(u4)


    ############# Output Layer
    output = Conv2D(nClasses, (1,1), activation="softmax")(u4)

    model = Model(inputs=[input], outputs=[output])

    return model




if __name__=='__main__':
  pass