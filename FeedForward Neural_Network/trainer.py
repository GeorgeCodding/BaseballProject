import torch.optim as optim

class ModelTrainer:
    """
    Handles the training loop, loss calculation, and weight optimization 
    for the BaseballEvaluatorNet.
    """
    def __init__(self, model, learning_rate=0.001):
        self.model = model
        
        # 1. Define the Loss Function (The Math Setup)
        # Since we are predicting a continuous number (Run Differential), 
        # we tell the model to use Mean Squared Error (MSE) to measure accuracy.
        self.criterion = nn.MSELoss() 
        
        # 2. Define the Optimizer
        # The algorithm (like Adam or SGD) that updates the network's weights 
        # based on the calculated error.
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

    def train_step(self, features, actual_run_diffs):
        """
        Executes a single forward and backward pass for a batch of games.
        """
        # 1. Zero the gradients (clear out the math from the previous step)
        
        # 2. Forward Pass: Ask the model to guess the run differentials
        
        # 3. Calculate Loss: Compare predictions against actual_run_diffs using MSE
        
        # 4. Backward Pass: Calculate the gradients (backpropagation)
        
        # 5. Optimizer Step: Update the model weights
        pass

    def train_loop(self, dataloader, epochs):
        """
        The main loop that runs through the dataset multiple times (epochs).
        """
        # Loop through the total number of epochs
            # Loop through the batches of games in the dataloader
                # Call self.train_step()
            
            # (Optional) Print the loss every few epochs to monitor progress
        pass
        
    def evaluate(self, dataloader):
         """
         Passes new games through the trained network without updating weights 
         to see how close the predicted Run Differentials are to reality.
         """
         # Set model to evaluation mode
         # Loop through test data and calculate the final error rate
         pass