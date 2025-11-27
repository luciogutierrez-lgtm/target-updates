from clients.tms import TMS
import argparse
import json
import os

def read_folders(folder):
    folders = []
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isdir(item_path):
            folders.append((item, os.listdir(item_path)))
    return folders


def import_command(args):
    tms = TMS()
    folders_and_files = read_folders(args.folder)

    filtered_folders = [(folder, files) for folder, files in folders_and_files if folder.lower() == args.source_language.lower()]

    project = tms.get_project(args.project)

    if not project['sourceLang'] == args.source_language:
        print(f"Project {args.project} does not support source language {args.source_language}")
        return

    if not filtered_folders:
        print(f"No folders found for language {args.source_language}")
        return
    
    for folder, files in filtered_folders:
        print(f"Importing {args.source_language} files from {folder} folder")
        for file in files:
            headers = {"Content-Type": "application/octet-stream",
                    "Content-Disposition": f"filename*=UTF-8''{file}",
                    "Memsource": json.dumps({"targetLangs": project['targetLangs'], "useProjectFileImportSettings": True})}
            print(f"Importing file {file}")
            tms.create_job(project, headers, os.path.join(args.folder, folder, file))


    print(f"Importing {args.source_language} files from {args.folder}")

def update_command(args):
    tms = TMS()
    folders_and_files = read_folders(args.folder)

    filtered_folders = [(folder, files) for folder, files in folders_and_files if folder.lower() != args.source_language.lower()]

    project = tms.get_project(args.project)

    jobs = tms.list_jobs(project, {"workflowLevel": "1"})

    for folder, files in filtered_folders:
        print(f"Updating '{args.source_language}' files in '{folder}' folder")
        for file in files:
            job_uid = [j for j in jobs if j['targetLang'] == folder and j['filename'] == file][0]['uid']
            headers = {"Content-Type": "application/octet-stream",
                    "Content-Disposition": f"filename*=UTF-8''{file}",
                    "Memsource": json.dumps({"jobs": [{"uid": job_uid}]})}
            print(f"Updating file '{file}' with job '{job_uid}' for language '{folder}'")
            tms.update_target(project, os.path.join(args.folder, folder, file), headers)

    print(f"Updating {args.source_language} files in {args.folder}")

def main():
    parser = argparse.ArgumentParser(description="CLI Boilerplate")
    subparsers = parser.add_subparsers(title="Available commands", dest="subcommand")

    # Import subparser
    import_parser = subparsers.add_parser("import", help="Import files")
    import_parser.add_argument("--source-language", "-s" , required=True, help="Source language (use underscore as separator)")
    import_parser.add_argument("--folder", "-f", required=True, help="Folder")
    import_parser.add_argument("--project", "-p", required=True, help="Project UID")

    # Update subparser
    update_parser = subparsers.add_parser("update", help="Update files")
    update_parser.add_argument("--source-language", "-s", required=True, help="Source language")
    update_parser.add_argument("--folder", "-f", required=True, help="Folder")
    update_parser.add_argument("--project", "-p", required=True, help="Project UID")

    args = parser.parse_args()

    if args.subcommand == "import":
        import_command(args)
    elif args.subcommand == "update":
        update_command(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()