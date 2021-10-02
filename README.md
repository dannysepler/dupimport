dupimport
=========

Find things you imported twice in your python code, when you probably only needed to import once.

## Installation

`pip install dupimport`

## Usage

Use on a file: `dupimport path/to/file.py`

or use on a folder:
- `dupimport .`
- `dupimport path/to/folder/`

## Caveats

Imports in an `if` statement may be okay
