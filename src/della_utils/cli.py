import argparse
import pathlib
import sys

def parse_args():
    """Parse command line arguments for pretty printing files."""
    parser = argparse.ArgumentParser(
        prog="della",
        description="Della utility to help with common tasks."
    )
    subparsers = parser.add_subparsers(
        help="sub command help",
        dest="command",
    )

    # members command to get members of the group
    member_parser = subparsers.add_parser(
        "members", help="List group members."
    )

    # ls command tabular output subparser
    table_parser = subparsers.add_parser(
        "ls", help="List files in a directory."
    )

    table_parser.add_argument(
        "dir",
        help="Directory at which to list files, by default current directory.",
        nargs="?",
        default=".",
    )
    table_parser.add_argument(
        "-l", "--limit", 
        help="Limit the number of files to print.",
        type=int,
        default=1000,
    )
    table_parser.add_argument(
        "-s", "--sort", 
        help="Sort files by size.",
        action="store_true",
    )
    return parser.parse_args()

def list_files(args):
    """List files in a directory."""
    #get a list of files
    f_paths = [p for p in pathlib.Path(args.dir).iterdir() if p.is_file()]
    f_sizes_bytes = [f.stat().st_size for f in f_paths]

    #sort files by size
    if args.sort:
        f_paths,f_sizes_bytes = zip(*[(f,s) for s,f in sorted(zip(f_sizes_bytes, f_paths), reverse=True)])

    #limit the number of files
    f_paths = f_paths[:args.limit]
    f_sizes_bytes = f_sizes_bytes[:args.limit]

    #convert file sizes to human readable format
    f_sizes = []
    for size in f_sizes_bytes:
        if size < 1024:
            f_sizes.append(f"{size}  B")
        elif size < 1024**2:
            f_sizes.append(f"{size/1024:.2f} KB")
        elif size < 1024**3:
            f_sizes.append(f"{size/1024**2:.2f} MB")
        else:
            f_sizes.append(f"{size/1024**3:.2f} GB")

    #create tabular output of file names and sizes
    f_names = [f"{f.name:<30}" for f in f_paths]
    f_sizes = [f"{f:>10}" for f in f_sizes]
    table = "\n".join([f"{f[0]} {f[1]}" for f in zip(f_names, f_sizes)])+"\n"

    return table

def main():
    """Main entry point for the CLI."""
    args = parse_args()

    if args.command is None:
        sys.stderr.write("No command given. use -h for help.\n")
    elif args.command == "ls":
        sys.stdout.write(list_files(args))
    elif args.command == "members":
        group_members = [
            'limingli', 'huixinx', 'rb3242', 'jakey',
            'luc', 'csaadroy', 'tcomi', 'lparsons',
            'kaiqianz', 'yushit', 'wat2', 'emmarg',
            'cweisman', 'dt8441', 'ck5658', 'mr7123',
        ]
        sys.stdout.write("\n".join(group_members)+"\n")
        
    else:
        sys.stderr.write(f"Unknown command {args.command}. use -h for help.\n")
