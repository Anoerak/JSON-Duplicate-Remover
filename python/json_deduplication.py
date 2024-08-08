import json
import argparse
import logging
from logging.handlers import RotatingFileHandler
from collections.abc import Hashable

def setup_logging(log_file):
    """Set up logging with rotation and categorize logs."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Set up a rotating file handler
    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

def make_hashable(item):
    """Recursively convert nested structures into hashable types."""
    if isinstance(item, dict):
        return tuple(sorted((key, make_hashable(value)) for key, value in item.items()))
    elif isinstance(item, list):
        return tuple(make_hashable(x) for x in item)
    elif isinstance(item, set):
        return tuple(sorted(make_hashable(x) for x in item))
    elif isinstance(item, (tuple, int, float, str, bool)) or item is None:
        return item
    else:
        logging.error(f"Unhashable type encountered: {type(item)}")
        raise TypeError(f"Unhashable type: {type(item)}")

def remove_duplicates(data, path="root", line_num=1):
    """Recursively remove duplicates in a JSON-like structure, with logging."""
    unique_items = []
    seen_hashes = set()
    duplicates_count = 0

    for idx, item in enumerate(data):
        item_hashable = make_hashable(item)
        item_path = f"{path}[{idx}]"

        # Estimate line number by incrementing for each item (this is approximate)
        current_line = line_num + idx

        if item_hashable not in seen_hashes:
            seen_hashes.add(item_hashable)
            if isinstance(item, dict):
                logging.info(f"Retaining unique item at {item_path} (Line {current_line})")
                unique_items.append({k: remove_duplicates([v], path=f"{item_path}.{k}", line_num=current_line) if isinstance(v, list) else v for k, v in item.items()})
            elif isinstance(item, list):
                logging.info(f"Retaining unique list at {item_path} (Line {current_line})")
                unique_items.append(remove_duplicates(item, path=item_path, line_num=current_line))
            else:
                logging.info(f"Retaining unique value at {item_path}: {item} (Line {current_line})")
                unique_items.append(item)
        else:
            logging.warning(f"Removing duplicate item at {item_path} (Line {current_line})")
            duplicates_count += 1

    return unique_items, duplicates_count

def process_json(input_file, output_file, log_file):
    setup_logging(log_file)
    
    try:
        with open(input_file, 'r') as file:
            data = json.load(file)
    except Exception as e:
        logging.error(f"Failed to read JSON file: {input_file} - {e}")
        return

    total_duplicates = 0

    if isinstance(data, dict):
        for key in data.keys():
            if isinstance(data[key], list):
                data[key], duplicates = remove_duplicates(data[key], path=f"root.{key}", line_num=1)
                total_duplicates += duplicates
    elif isinstance(data, list):
        data, total_duplicates = remove_duplicates(data, path="root", line_num=1)

    try:
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=4)
        logging.info(f"Cleaned JSON saved to {output_file}")
    except Exception as e:
        logging.error(f"Failed to write JSON file: {output_file} - {e}")
        return

    logging.info("\nDeduplication Complete")
    logging.info("=======================")
    logging.info(f"Total duplicates removed: {total_duplicates}")

def main():
    parser = argparse.ArgumentParser(description="Remove duplicate objects from a JSON file, including nested structures, with categorized logging and log rotation.")
    parser.add_argument('input_file', help="Path to the input JSON file")
    parser.add_argument('output_file', help="Path to save the cleaned JSON file")
    parser.add_argument('log_file', help="Path to save the log file")

    args = parser.parse_args()

    process_json(args.input_file, args.output_file, args.log_file)

if __name__ == "__main__":
    main()
