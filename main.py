from data_preprocessing import csv_to_jsonl, txt_to_jsonl
from data_loading import load_custom_dataset
from dataset_exploration import explore_dataset


if __name__ == "__main__":
    csv_file = 'dataset_sample.csv'
    jsonl_train = 'dataset/train.jsonl'
    jsonl_val = 'dataset/validation.jsonl'
    jsonl_test = 'dataset/test.jsonl'
    instruction = "Provide a summary of the following"
    
    # csv_to_jsonl(csv_file, jsonl_train, jsonl_val, jsonl_test, instruction)

    txt_folder = "sample_source"

    txt_to_jsonl(txt_folder, jsonl_train, jsonl_val, jsonl_test, instruction)

    # Load the dataset
    train_dataset = load_custom_dataset(jsonl_train, jsonl_val, jsonl_test)
    
    # Explore the dataset
    explore_dataset(train_dataset)
