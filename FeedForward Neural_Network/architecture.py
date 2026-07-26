import torch
import torch.nn as nn

class BaseballEvaluatorNet(nn.Module):
    """
    A Feedforward Neural Network to predict MLB Run Differential 
    based on team and opponent box score statistics.
    """
    def __init__(self, num_features):
        super(BaseballEvaluatorNet, self).__init__()
        
        # Start with 64 nodes
        self.hidden1 = nn.Linear(num_features, 64)

        self.hidden2 = nn.Linear(64, 16)


        # Activation function
        self.relu = nn.ReLU()
        
        # Output layer
        self.output_layer = nn.Linear(16, 1)


    def forward(self, x):
        """
        This method dictates the flow of data. It takes the input features (x)
        and passes them through the layers defined in __init__.
        """
        # Pass data through hidden layer 1, then apply ReLU
        x = self.hidden1(x)
        x = self.relu(x)
        
        # Pass data through hidden layer 2, then apply ReLU
        x = self.hidden2(x)
        x = self.relu(x)
        
        # Pass data through the output layer and return the final prediction
        x = self.output_layer(x)

        return x