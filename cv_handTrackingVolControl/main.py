from customModules import handDetector

def main() -> None:
    
    ### change the detection confidence to a higher value to make sure, while controlling the volume it doesnt flicker too much
    detectorObj = handDetector()
    detectorObj.showImage(fps=True, volControlSwitch=True)


if __name__=='__main__':
    main()