import torch
import torch.nn as nn

class BaseballEvaluatorNet(nn.Module):
    """
    A Feedforward Neural Network to predict MLB Run Differential 
    based on team and opponent box score statistics.
    """
    def __init__(self, num_features):
        super(BaseballEvaluatorNet, self).__init__()
        
        # 1. Define the Hidden Layers
        # These are the "brain" of the network that find the non-linear patterns.
        # We start with the input size (num_features) and compress it down.
        # e.g., self.hidden1 = nn.Linear(num_features, 64)
        
        # 2. Define the Activation Functions
        # We need ReLU activations to handle the non-linear relationships 
        # between hitting well and pitching poorly.
        # e.g., self.relu = nn.ReLU()
        
        # 3. Define the Output Layer
        # Exactly 1 node with no activation (Linear) to output any number 
        # representing the Run Differential (e.g., -1.2, +4.8).
        # e.g., self.output_layer = nn.Linear(16, 1)

    def forward(self, x):
        """
        This method dictates the flow of data. It takes the input features (x)
        and passes them through the layers defined in __init__.
        """
        # Pass data through hidden layer 1, then apply ReLU
        
        # Pass data through hidden layer 2, then apply ReLU
        
        # Pass data through the output layer and return the final prediction
        pass