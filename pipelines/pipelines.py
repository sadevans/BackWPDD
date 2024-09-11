import numpy as np

class DetectDefectsPipeline():
    def __init__(self):
        super(DetectDefectsPipeline, self).__init__()
        """there will be init method of pipelina class"""


    def call(image):
        """here model is called"""
        if_defect = np.random.choice([0, 1])

        return (if_defect, image)
