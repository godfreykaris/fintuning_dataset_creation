from datasets import load_dataset

def load_custom_dataset(train_path, val_path, test_path):
    """Load the custom dataset."""
    dataset = load_dataset('json', data_files={'train': train_path, 'validation': val_path, 'test': test_path})
    return dataset
