# CLI Script Instructions

This is a command-line interface (CLI) script for managing translation projects. It provides two main functionalities: importing files into a project and updating files in a project. This can be used to upload translated files to a project to align them an create TM. The script assumes that the source and target files are named the same and stored in language folders that match the locale ID used in the Phrase TMS project.

A project must be created in Phrase TMS manually which contains the correct parsing/file import and segmentation rules for the files that will be imported/updated/aligned. The locales used in the project must match the language folder names used in the folder argument. The folder argument should be the parent of the language folders (i.e. c:\alignment_test and not c:\alignment_test\en or c:\alignment_test\ja). Note, avoid putting a trailing \ in the path, as this may lead to errors.

The script will assume that any language folder that is not the source (-s <source_language>) is a target language and try to import it to the corresponding job with the matching file name and target langauge.

## Requirements

- Python 3.x
- Pipenv

## Installation

```
cd <repository-directory>
```

Install the required Python packages using Pipenv:
```
pipenv install requests
```

## Usage
The script provides two commands: import and update.
Before running any of them, add your TMS credentials into `config.py`.

##### Import Command
The `import` command is used to import the source files into a project.
```
python cli.py import --source-language <source_language> --folder <folder_path> --project <project_uid>
python cli.py import -s <source_language> -f <folder_path> -p <project_uid>
```

##### Update Command
The `update` command is used to update target translations for the files in a project.
```
python cli.py update --source-language <source_language> --folder <folder_path> --project <project_uid>
python cli.py update -s <source_language> -f <folder_path> -p <project_uid>
```