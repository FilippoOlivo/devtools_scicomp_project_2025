import lightning as pl
from .model import AlexNet
import torchmetrics
import torch
import torch.nn.functional as F

class Classifier(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = AlexNet(num_classes=10)
        self.train_accuracy = torchmetrics.classification.Accuracy(task="multiclass", num_classes=10)
        self.test_accuracy = torchmetrics.classification.Accuracy(task="multiclass", num_classes=10)
        self.val_accuracy = torchmetrics.classification.Accuracy(task="multiclass", num_classes=10)

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        pred, true, loss = self._classifier_step(batch)
        acc = self.train_accuracy(pred, true)
        self.log("train_accuracy", acc, on_step=True, on_epoch=True)
        return loss
    
    def validation_step(self, batch, batch_idx):
        pred, true, loss = self._classifier_step(batch)
        self.val_accuracy(pred, true)
        self.log("val_accuracy", self.val_accuracy, on_step=True, on_epoch=True)
        return loss

    def test_step(self, batch, batch_idx):
        pred, true, loss = self._classifier_step(batch)
        self.test_accuracy(pred, true)
        self.log("test_accuracy", self.test_accuracy, on_step=True, on_epoch=True)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.0001)
    
    def _classifier_step(self, batch):
        features, true_labels = batch
        y_hat = self.model(features)
        loss = F.cross_entropy(y_hat, true_labels)
        prediction = torch.argmax(y_hat, dim=1)
        return prediction, true_labels, loss