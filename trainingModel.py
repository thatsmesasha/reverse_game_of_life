import numpy as np

class TrainingModel:
    def __init__(self, steps=0, size=0, modelHash=0, fields=None, row=None):
        """
            Initiate training model, which stores predictions of the start grid
            and number of occurrences of this model in the testing.
        """
        if fields and row:
            self.parseRow(fields, row)
        else:
            self.occurrences = 0
            self.data = np.zeros((size, size))
            self.size = size
            self.steps = steps
            self.modelHash = modelHash

    def addPrediction(self, window): #TODO if size is not needed, can change window to data
        """
            Add start grid values of this model to predictions.
        """
        self.occurrences += 1
        self.data += window.data

    def predict(self, transformation, position, height, width):
        """
            Return predictions grid, that was formed on the training data.
            Grid has shape (height, width, 2), where every [height, width] cell
            represents set [countCellAlive, occurrencesOfCell]: countCellAlive indicates
            how many times cell was alive in total of occurrencesOfCell cases
            during training.
        """
        # Create empty prediction grid with shape (height, width, 2)
        predictionGrid = np.zeros(height * width * 2).reshape(height, width, 2)

        # Transform model according to transformation needed
        model = Transformation.do[transformation](self.data)

        # Create model3d that stores [countCellAlive, occurrencesOfCell] for each element of model,
        # where occurrencesOfCell == self.occurrences
        model3d = np.array([model[h,w] if isCellAliveElem == 0 else self.occurrences for h in range(self.size) for w in range(self.size) for isCellAliveElem in range(2)]).reshape(self.size, self.size, 2)

        # Add model on the prediction grid at the position
        predictionGrid[position[0]:position[0] + self.size, position[1]: position[1] + self.size] = model3d

        return predictionGrid

    def parseRow(self, fields, row):
        # Retrieve data from row
        try:
            #TODO can just read values as hash,steps,sie,occurrences,models.1,models.2,... without reading field names
            data = {fields[index]: row[index] for index in range(len(fields))}
            self.modelHash = int(data['hash'])
            del(data['hash'])
            self.steps = int(data['steps'])
            del(data['steps'])
            self.size = int(data['size'])
            del(data['size'])
            self.occurrences = int(data['occurrences'])
            del(data['occurrences'])
        except:
            raise Exception("CSV file is not valid.")

        # Create data for the model
        window = []
        try:
            # Read values from the file
            for index in range(size ** 2):
                window.append(int(data['models.' + str(index + 1)]))

            # Creade NumPy array from obtained values
            self.data = np.array(window).reshape(self.size, self.size)
        except Exception as e:
            raise Exception("Unable to create model #%d for #%d steps" % (self.modelHash, self.steps))

    def createRow(self):
        """
            Create row of CSV that will store data from the model.
        """
        return [self.modelHash, self.steps, self.size, self.occurrences] + list(self.data.resize(self.size ** 2))