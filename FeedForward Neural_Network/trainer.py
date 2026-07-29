import torch
import torch.nn as nn
import torch.optim as optim

class ModelTrainer:
    """
    Handles the training loop, loss calculation, and weight optimization 
    for the BaseballEvaluatorNet.
    """
    def __init__(self, model, learning_rate=0.001):
        self.model = model
        
        # 1. Define the Loss Function (The Math Setup)
        self.criterion = nn.MSELoss() 
        
        # 2. Define the Optimizer
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

    def train_step(self, features, actual_run_diffs):
        """
        Executes a single forward and backward pass for a batch of games.
        """
        # 1. Zero the gradients (clear out the math from the previous step)
        self.optimizer.zero_grad()
        
        # 2. Forward Pass: Ask the model to guess the run differentials
        predictions = self.model(features)
        
        # 3. Calculate Loss: Compare predictions against actual_run_diffs using MSE
        loss = self.criterion(predictions, actual_run_diffs)
        
        # 4. Backward Pass: Calculate the gradients (backpropagation)
        loss.backward()
        
        # 5. Optimizer Step: Update the model weights
        self.optimizer.step()
        
        # Return the actual number so we can track it in the loop
        return loss.item()

    def train_loop(self, dataloader, epochs):
        """
        The main loop that runs through the dataset multiple times (epochs).
        """
        # Ensure the model is in training mode
        self.model.train()
        
        # Loop through the total number of epochs
        for epoch in range(epochs):
            total_loss = 0.0
            
            # Loop through the batches of games in the dataloader
            for features, actual_run_diffs in dataloader:
                # Call self.train_step()
                loss = self.train_step(features, actual_run_diffs)
                total_loss += loss
            
            # (Optional) Print the loss every few epochs to monitor progress
            avg_loss = total_loss / len(dataloader)
            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch+1}/{epochs} - Avg Loss: {avg_loss:.4f}")
                
    def evaluate(self, dataloader):
         """
         Passes new games through the trained network without updating weights 
         to see how close the predicted Run Differentials are to reality.
         """
         # Set model to evaluation mode
         self.model.eval()
         total_loss = 0.0
         
         # Freeze the gradients to save memory and prevent accidental learning
         with torch.no_grad():
             # Loop through test data and calculate the final error rate
             for features, actual_run_diffs in dataloader:
                 predictions = self.model(features)
                 loss = self.criterion(predictions, actual_run_diffs)
                 total_loss += loss.item()
                 
         avg_loss = total_loss / len(dataloader)
         print(f"Final Evaluation - Average Loss (MSE): {avg_loss:.4f}")
         
         return avg_loss