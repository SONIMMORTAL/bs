import argparse
import sys
from typing import List, Optional

def main():
    parser = argparse.ArgumentParser(
        description="Your Custom CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create command parser
    create_parser = subparsers.add_parser("create", help="Create something new")
    create_parser.add_argument("--name", required=True, help="Name of the item to create")
    create_parser.add_argument("--type", choices=["file", "directory"], default="file", help="Type of item to create")
    
    # List command parser
    list_parser = subparsers.add_parser("list", help="List items")
    list_parser.add_argument("--path", default=".", help="Path to list items from")
    
    # Delete command parser
    delete_parser = subparsers.add_parser("delete", help="Delete something")
    delete_parser.add_argument("--name", required=True, help="Name of the item to delete")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Handle commands
    if args.command == "create":
        handle_create(args.name, args.type)
    elif args.command == "list":
        handle_list(args.path)
    elif args.command == "delete":
        handle_delete(args.name)

def handle_create(name: str, type: str) -> None:
    """Handle the create command"""
    print(f"Creating {type} with name: {name}")
    # Add your create logic here

def handle_list(path: str) -> None:
    """Handle the list command"""
    print(f"Listing items in path: {path}")
    # Add your list logic here

def handle_delete(name: str) -> None:
    """Handle the delete command"""
    print(f"Deleting item with name: {name}")
    # Add your delete logic here

if __name__ == "__main__":
    main() 