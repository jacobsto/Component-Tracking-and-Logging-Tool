# Components, LogEntry, Inventory created as classes with simple methods.

from datetime import datetime
from typing import Dict, List

# Define allowed statuses for components.
ALLOWED_STATUSES = ["IN_STOCK", "IN_USE", "QUARANTINED", "DISPOSED"]

# Component model representing an inventory item.
class Component:

    # Class variable to track last used ID.
    _last_id = 0
     
    # Initialize component with attributes.
    def __init__(self, name, quantity, threshold, status, tags):
        Component._last_id += 1
        self.component_id = Component._last_id
        self.name = name
        self.quantity = quantity
        self.threshold = threshold
        self.status = status
        self.tags = tags

    # Replenishment needed when quantity <= threshold.    
    def needs_replenishment(self) -> bool:
        return self.quantity <= self.threshold
    
    # Send component data as a dictionary.
    def to_dict(self) -> dict:
        return{
            "component_id": self.component_id,
            "name": self.name,
            "quantity": self.quantity,
            "threshold": self.threshold,
            "status": self.status,
            "tags": self.tags,
        }
    
    @staticmethod
    # Create component from dictionary data.
    def from_dict(data: dict) -> "Component":
        return Component(
            name=data["name"],
            quantity=int(data["quantity"]),
            threshold=int(data["threshold"]),
            status=data["status"],
            tags=list(data.get("tags", [])),
        )
        component.component_id = int(data["component_id"])
        if component.component_id > Component._last_id:
            Component._last_id = component.component_id
        return component
    
# Log entry for actions taken on components.
class LogEntry:

    # Initialize log entry with attributes.
    def __init__(self, timestamp: str, component_id: str, action: str, details: str):
        self.timestamp = timestamp
        self.component_id = component_id
        self.action = action
        self.details = details

    @staticmethod
    # Create a log entry with current timestamp.
    def now(component_id: str, action: str, details: str) -> "LogEntry":
        ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        return LogEntry(ts, component_id, action, details)
    
    # Convert log entry to dictionary.
    def to_dict(self) -> dict:
        return{
            "timestamp": self.timestamp,
            "component_id": self.component_id,
            "action": self.action,
            "details": self.details,
        }
    
    @staticmethod
    # Create log entry from dictionary data.
    def from_dict(data:dict) -> "LogEntry":
        return LogEntry(
            timestamp=data["timestamp"],
            component_id=data["component_id"],
            action=data["action"],
            details=data["details"],
        )

# Inventory holding components and logs.    
class Inventory:

    # Initialize inventory with empty components and logs.
    def __init__(self):
        # Dict for fast lookup by component_id.
        self.components: Dict[int, Component] = {}
        self.logs: List[LogEntry] = []

    # Add a log entry to the inventory.
    def add_log(self, component_id: str, action: str, details: str) -> None:
        self.logs.append(LogEntry.now(component_id, action, details))   

    # Convert inventory to dictionary.
    def to_dict(self) -> dict:
        return{
            "components": {cid: comp.to_dict() for cid, comp in self.components.items()},
            "logs": [log.to_dict() for log in self.logs],
        }
    
    @staticmethod
    # Create inventory from dictionary data.
    def from_dict(data: dict) -> "Inventory":
        inv = Inventory()
        raw_components = data.get("components", {})
        for cid, cdict in raw_components.items():
            inv.components[cid] = Component.from_dict(cdict)

        raw_logs = data.get("logs", [])
        inv.logs = [LogEntry.from_dict(ld) for ld in raw_logs]
        return inv