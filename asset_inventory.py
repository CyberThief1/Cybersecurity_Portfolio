import os
import argparse
import csv

def scan_assets(project_path):
    """
    Generator yielding unique tuples of (asset_type, relative_path)
    for all files and directories under project_path.
    """
    seen = set()
    for root, dirs, files in os.walk(project_path):
        for d in dirs:
            rel_path = os.path.relpath(os.path.join(root, d), project_path)
            if rel_path not in seen:
                seen.add(rel_path)
                yield ('directory', rel_path)
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), project_path)
            if rel_path not in seen:
                seen.add(rel_path)
                yield ('file', rel_path)

def main():
    parser = argparse.ArgumentParser(
        description="Scan a project folder and output an asset inventory CSV."
    )
    parser.add_argument('-p', '--project-path',
                        required=True,
                        help='Root path to scan')
    parser.add_argument('-o', '--output',
                        required=True,
                        help='CSV output file')
    args = parser.parse_args()

    root = os.path.abspath(args.project_path)
    if not os.path.isdir(root):
        print(f"Error: Path not found: {root}")
        return

    try:
        with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['asset_type', 'relative_path'])
            for asset_type, rel_path in scan_assets(root):
                writer.writerow([asset_type, rel_path])
        print(f"Asset inventory successfully written to {args.output}")
    except Exception as e:
        print(f"Failed to write inventory: {e}")

if __name__ == '__main__':
    main()