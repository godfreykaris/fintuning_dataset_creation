import csv
import json
import random

def create_text_row(instruction, output, input):
    """Create text row."""
    text_row = f"""<s>[INST] {instruction} : {input} [/INST] \\n {output} </s>"""
    return text_row

def read_csv(csv_file):
    """Read CSV file and return data."""
    data = []
    with open(csv_file, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='|')
        for row in csv_reader:
            if len(row) != 2:
                continue  # Skip rows that don't have 2 columns

            deposition = row[0]
            summary = row[1]
            data.append((deposition, summary))
    return data

def split_data(data, val_ratio=0.2, test_ratio=0.2):
    """Split data into train, validation, and test sets."""
    random.shuffle(data)
    num_samples = len(data)
    num_val_samples = int(num_samples * val_ratio)
    num_test_samples = int(num_samples * test_ratio)

    val_data = data[:num_val_samples]
    test_data = data[num_val_samples:num_val_samples + num_test_samples]
    train_data = data[num_val_samples + num_test_samples:]

    return train_data, val_data, test_data

def write_to_jsonl(data, jsonl_file):
    """Write data to JSON Lines file."""
    with open(jsonl_file, 'w') as jsonlfile:
        for row in data:
            jsonlfile.write(json.dumps(row) + '\n')

def csv_to_jsonl(csv_file, jsonl_train, jsonl_val, jsonl_test, instruction, val_ratio=0.2, test_ratio=0.2):
    """Convert CSV to JSON Lines files."""
    data = read_csv(csv_file)
    train_data, val_data, test_data = split_data(data, val_ratio, test_ratio)

    instruction = "Provide a summary of the following"  # Possibly, this line can be removed as it's hardcoded

    train_data_formatted = [{'deposition': deposition, 'summary': summary, 'text': create_text_row(instruction, summary, deposition)} for deposition, summary in train_data]
    val_data_formatted = [{'deposition': deposition, 'summary': summary, 'text': create_text_row(instruction, summary, deposition)} for deposition, summary in val_data]
    test_data_formatted = [{'deposition': deposition, 'summary': summary, 'text': create_text_row(instruction, summary, deposition)} for deposition, summary in test_data]

    write_to_jsonl(train_data_formatted, jsonl_train)
    write_to_jsonl(val_data_formatted, jsonl_val)
    write_to_jsonl(test_data_formatted, jsonl_test)
