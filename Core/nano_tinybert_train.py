"""
Nano TinyBERT training script for question classification.
Trains on nano_tinybert_train.tsv (20 examples, <3KB).
Saves model as nano_tinybert_classifier_trained.pt (<1MB).
"""
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.utils.data import Dataset, DataLoader
import os

TRAIN_FILE = os.path.join(os.path.dirname(__file__), "nano_tinybert_train.tsv")
MODEL_NAME = "distilbert-base-uncased"
LABELS = ["Physics", "Health", "Culture", "Tech"]

class NanoDataset(Dataset):
    def __init__(self, path):
        self.samples = []
        with open(path, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    q, label = line.strip().split("\t")
                    self.samples.append((q, LABELS.index(label)))
    def __len__(self):
        return len(self.samples)
    def __getitem__(self, idx):
        return self.samples[idx]

def collate_fn(batch):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    questions, labels = zip(*batch)
    enc = tokenizer(list(questions), return_tensors="pt", padding=True, truncation=True, max_length=32)
    return enc, torch.tensor(labels)

def train():
    dataset = NanoDataset(TRAIN_FILE)
    loader = DataLoader(dataset, batch_size=4, shuffle=True, collate_fn=collate_fn)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=len(LABELS))
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    model.train()
    for epoch in range(5):
        for enc, labels in loader:
            outputs = model(**enc, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
    torch.save(model.state_dict(), os.path.join(os.path.dirname(__file__), "nano_tinybert_classifier_trained.pt"))
    print("Training complete. Model saved as nano_tinybert_classifier_trained.pt")

if __name__ == "__main__":
    train()
