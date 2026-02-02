# Main entry point
# Uses storage.py for save/load
# Uses ui.py for user interaction
# Uses services.py for logic (iindirectly via UI)

from errors import StorageError # imports from errors.py
from storage import load_inventory, save_inventory # imports from storage.py
from ui import print_menu, get_actions # imports from ui.py

# Main application loop
def main() -> None:
    try:
        # Load existing inventory
        inventory = load_inventory()
    except StorageError as ex:
        print(f"Error loading inventory: {ex}")
        # Start fresh if load fails
        from models import Inventory
        inventory = Inventory()

    actions = get_actions() # Get available UI actions

    # Application loop
    while True:
        print_menu() # Display menu options
        choice = input("Select an option: ").strip()

        if choice == "0": # Exit option
            break

        handler = actions.get(choice) # Get handler function
        if handler is None:
            print("Invalid option. Please try again.")
            continue

        handler(inventory) # Call the selected action

    # Save inventory on exit
    try:
        save_inventory(inventory)
    except StorageError as ex: # Handle save errors
        print(f"Error saving inventory: {ex}")

if __name__ == "__main__": # Run main if executed directly
        main()