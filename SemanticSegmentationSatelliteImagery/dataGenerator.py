from customModules import imagePreprocess
import numpy as np


def main()->None:
    preprocessObj = imagePreprocess()
    imageDataset,maskedDataset = preprocessObj.createDataset()
    imageDataset = np.array(imageDataset)
    maskedDataset = np.array(maskedDataset)

    ## Saving imageDataset and maskedDataset

    labels = preprocessObj.labelling(maskedDataset)
    print(np.unique(labels))
    preprocessObj.maskedPlotComparison(imageDataset,maskedDataset)
    return None

if __name__ == '__main__':
    main()