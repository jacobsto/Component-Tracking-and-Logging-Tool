# JSON Storage for Inventory and Logs

import json
import os
from pathlib import Path 
from errors import StorageError # imports from errors.py
from models import Inventory # imports from models.py

# Path to the JSON database file.
DB_FILE = Path.cwd()/ "inventory_db.json"

# Load inventory from JSON file, or create new if not found.
def load_inventory() -> Inventory:
    # Return new inventory if file missing 
    if not DB_FILE.exists():
        return Inventory()
    
    try:
        # Load and parse JSON data
        raw = DB_FILE.read_text(encoding="utf-8") # Read file content
        data = json.loads(raw) # Parse JSON to dict
        return Inventory.from_dict(data) # Create Inventory from dict
    # Handle file read/parse errors
    except (OSError, json.JSONDecodeError) as ex:
        raise StorageError(f"Failed to load inventory from {DB_FILE}: {ex}") from ex

# Save inventory to JSON file.    
def save_inventory(inv: Inventory) -> None:
    try:
        # Convert inventory to JSON and write to file
        DB_FILE.write_text(json.dumps(inv.to_dict(), indent=2), encoding="utf-8")
    # Handle file write errors
    except OSError as ex:
        raise StorageError(f"Failed to save inventory to {DB_FILE}: {ex}") from ex