# Business logic written as functions.
# Validate -> find -> update -> log.

from errors import NotFoundError, ValidationError # imports from errors.py
from models import Component, Inventory # imports from models.py
from validators import require_min, require_non_empty # imports from validators.py

# Add a new component to the inventory.
def add_component(inv: Inventory, comp: Component) -> None:
    cid = comp.component_id

    if cid in inv.components:
        raise ValidationError(f"Component with ID '{cid}' already exists.")
    
    inv.components[cid] = comp
    inv.add_log(cid, "ADD_COMPONENT", f"Added '{comp.name}'(qty={comp.quantity}), threshold={comp.threshold}.")

# Retrieve a component by ID, raising error if not found.
def get_component(inv: Inventory, component_id: int) -> Component:
    cid = require_non_empty(component_id, "Component ID")
    comp = inv.components.get(cid)
    if comp is None:
        raise NotFoundError(f"Component with ID '{cid}' not found.")
    return comp

# Update the status of a component.
def update_status(inv: Inventory, component_id: int, new_status: str) -> None:
    comp = get_component(inv, component_id)
    old_status = comp.status
    comp.status = new_status
    inv.add_log(comp.component_id, "UPDATE_STATUS", f"{old_status} -> {new_status}")

# Adjust the quantity of a component.
def adjust_quantity(inv: Inventory, component_id: int, delta: int, reason: str) -> None:
    comp = get_component(inv, component_id)
    reason = require_non_empty(reason, "Reason")
    new_quantity = comp.quantity + delta
    if new_quantity < 0:
        raise ValidationError("Quantity cannot be negative.")
    old_quantity = comp.quantity
    comp.quantity = new_quantity
    inv.add_log(comp.component_id, "ADJUST_QUANTITY", f"{old_quantity} -> {new_quantity} ({'+' if delta >= 0 else ''}{delta}) Reason: {reason}")


# List all components in the inventory, sorted by ID.
def list_components(inv: Inventory) -> list:
    return [inv.components[cid] for cid in sorted(inv.components.keys())]

# Get components needing replenishment, sorted by quantity.
def replenishment_list(inv: Inventory) -> list:
    needs = []
    for comp in inv.components.values():
        if comp.needs_replenishment():
            needs.append(comp)
    # Sort by lowest quantity first
    needs.sort(key=lambda c: c.quantity)
    return needs

# Get recent log entries up to the specified limit.
def recent_logs(inv: Inventory, limit: int) -> list:
    limit = require_min(limit, 1, "Log limit")
    # Sort by recent first
    logs = inv.logs[-limit:]
    logs.reverse()
    lines = []
    for l in logs:
        lines.append(f"{l.timestamp} | {l.component_id} | {l.action} | {l.details}")
    return lines