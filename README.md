# Tachibk JSON Tools

This project provides utilities for converting Tachiyomi backup files (`.tachibk`) to JSON and vice versa, as well as marking all chapters as read in exported JSON files.

## Features

- **Convert** `.tachibk` files to readable `.json` format and back.
- **Mark all chapters as read** in JSON backup files.

## Requirements

- Python 3.8+
- [protobuf](https://pypi.org/project/protobuf/) (`google.protobuf`)

Install dependencies:
```sh
pip install -r requirements.txt
```

## Usage

### 1. Prepare Input Files

- Place your `.tachibk` or `.json` files in the `.input` directory.

### 2. Convert Files

Run the conversion script:
```sh
python conv.py
```
- If `.tachibk` files are found in `.input`, they will be converted to `.json` in `.output`.
- If `.json` files are found in `.input`, they will be converted to `.tachibk` in `.output`.

### 3. Mark Chapters as Read (Optional)

To set all chapters as read in all JSON files in `.output`, run:
```sh
python .output/setread.py
```

## File Structure

```
tachibk-json/
├── .input/         # Place your .tachibk or .json files here
├── .output/        # Output files and setread.py script
│   └── setread.py
├── conv.py         # Main conversion script
├── schema_pb2.py   # Protobuf schema (generated)
├── requirements.txt
└── README.md
```

## Notes

- The `schema_pb2.py` file must be generated from your Tachiyomi protobuf schema.
- Only non-standard dependency is `protobuf`.
