# Event-driven menu for user interactions.
# UI collects input and prints outputs.
# Calls services for actual logic.

from errors import AppError, ValidationError # imports from errors.py
from models import Inventory, Component, ALLOWED_STATUSES # imports from models.py
from services import ( # imports from services.py
    add_component,
    adjust_quantity,
    list_components,
    recent_logs,
    replenishment_list,
    update_status,
)
from validators import ( # imports from validators.py
    parse_tags,
    require_non_empty,
    to_int,
    require_min,
    validate_status,
)

# Display the main menu options.
def print_menu() -> None:
    print("\nComponent Tracking and Logging Tool")
    print("1. Add Component")
    print("2. Update Component Status")
    print("3. Adjust Component Quantity")
    print("4. List All Components")
    print("5. Show Replenishment List")
    print("6. Show Recent Logs")
    print("0. Exit")

# Prompt user for input.
def ask(prompt: str) -> str:
    return input(prompt).strip()

# Prompt user for integer input with optional minimum constraint.
def ask_int(promt: str, field_name: str, minimum: int = None) -> int:
    while True:
        raw = ask(promt)
        try:
            value = to_int(raw, field_name)
            if minimum is not None:
                value = require_min(value, minimum, field_name)
            return value
        except ValidationError as ex:
            print(f"Input error: {ex}")

# Handle adding a new component.
def handle_add(inv: Inventory) -> None:
    try:
        cid = require_non_empty(ask("Component ID: "), "Component ID")
        name = require_non_empty(ask("Name: "), "Name")
        quantity = ask_int("Quantity (>=0): ", "Quantity", minimum=0)
        threshold = ask_int("Reorder Threshold (>=0): ", "Reorderhreshold", minimum=0)
        status = validate_status(ask(f"Status ({', '.join(ALLOWED_STATUSES)}): "))
        tags = parse_tags(ask("Tags (comma-separated, optional): "))
        
        comp = Component(cid, name, quantity, threshold, status, tags)
        add_component(inv, comp)
        print(f"Component '{cid}' added successfully.")
    except AppError as ex:
        print(f"Error: {ex}")

# Handle updating component status.
def handle_status(inv: Inventory) -> None:
    try:
        cid = require_non_empty(ask("Component ID: "), "Component ID")
        status = validate_status(ask(f"New Status {ALLOWED_STATUSES}: "))
        update_status(inv, cid, status)
        print(f"Component '{cid}' status updated to '{status}'.")
    except AppError as ex:
        print(f"Error: {ex}")

# Handle adjusting component quantity.
def handle_adjust(inv: Inventory) -> None:
    try:
        cid = require_non_empty(ask("Component ID: "), "Component ID")
        delta = to_int(ask("Quantity Adjustment (positive or negative): "), "Quantity Adjustment")
        reason = require_non_empty(ask("Reason for adjustment: "), "Reason")
        adjust_quantity(inv, cid, delta, reason)
        
        comp = inv.components[cid]
        if comp.needs_replenishment():
            print(f"Warning: Component '{cid}' needs replenishment (qty={comp.quantity}, threshold={comp.threshold}).")
        else:
            print("Quantity updated successfully.")
    except AppError as ex:
        print(f"Error: {ex}")

# Handle listing all components.
def handle_list(inv: Inventory) -> None:
    comps = list_components(inv)
    if not comps:
        print("No components in inventory.")
        return
    print("\nComponents in Inventory:")
    for c in comps:
        flag = " **REPLENISH**" if c.needs_replenishment() else ""
        tags = ",".join(c.tags) if c.tags else "-"
        print(f"{c.component_id}: {c.name} | {c.quantity} | {c.threshold} | {c.status} | tags={tags}{flag}")

# Handle showing replenishment list.
def handle_replenishment(inv: Inventory) -> None:
    needs = replenishment_list(inv)
    if not needs:
        print("No components need replenishment.")
        return
    
    print ("\nComponents Needing Replenishment:")
    for c in needs:
        tags = ",".join(c.tags) if c.tags else "-"
        print(f"{c.component_id}: {c.name} | {c.quantity} <= {c.threshold}")

# Handle showing recent logs.
def handle_logs(inv: Inventory) -> None:
    limit = ask_int("How many recent logs to show? ", "Log limit", minimum=1)
    logs = recent_logs(inv, limit)
    if not logs:
        print("No log entries found.")
        return
    print("\nRecent Log Entries:")
    for l in logs:
        print(l)

# Map menu options to handler functions.
def get_actions():
    return {
        "1": handle_add,
        "2": handle_status,
        "3": handle_adjust,
        "4": handle_list,
        "5": handle_replenishment,
        "6": handle_logs,
    }