from torch.utils.data import DataLoader, TensorDataset
from transformers import BertTokenizerFast
import torch
import pandas as pd

def load_data(file_path,max_length=256):
    df = pd.read_csv(file_path)
    texts = df['text'].tolist()
    sentiments = df['sentiment'].tolist()
    emotions = df['emotion'].tolist()
    
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
    texts, sentiments, emotions = [], [], []
    
    input_ids = []
    attention_masks = []

    for text in texts:
        encoded = tokenizer.encode_plus(
            text,
            add_special_tokens = True,
            max_length = max_length,
            pad_to_max_length = True,
            return_attention_mask = True
        )
        input_ids.append(encoded['input_ids'])
        attention_masks.append(encoded['attention_mask'])
        
    input_ids = torch.tensor(input_ids)
    attention_masks = torch.tensor(attention_masks)
    sentiments = torch.tensor(sentiments)
    emotions = torch.tensor(emotions)
    dataset = TensorDataset(input_ids, attention_masks, sentiments, emotions)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    return dataloader


def prepare_and_save_dataset(file_path, save_path, max_length=256):
    df = pd.read_csv(file_path)
    texts = df['text'].tolist()
    sentiments = df['sentiment'].tolist()
    emotions = df['emotion'].tolist()
    
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
    
    input_ids = []
    attention_masks = []

    for text in texts:
        encoded = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=max_length,
            pad_to_max_length=True,
            return_attention_mask=True
        )
        input_ids.append(encoded['input_ids'])
        attention_masks.append(encoded['attention_mask'])
        
    input_ids = torch.tensor(input_ids)
    attention_masks = torch.tensor(attention_masks)
    sentiments = torch.tensor(sentiments)
    emotions = torch.tensor(emotions)
    
    dataset = TensorDataset(input_ids, attention_masks, sentiments, emotions)
    
    # Save TensorDataset to disk
    torch.save(dataset, save_path)

