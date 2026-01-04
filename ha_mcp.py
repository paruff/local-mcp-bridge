import os
import requests
from mcp.server import Server
from mcp.types import Tool, TextContent
from dotenv import load_dotenv

load_dotenv("config.env")

HA_URL = os.environ["HA_BASE_URL"]
TOKEN = os.environ["HA_TOKEN"]
VERIFY_SSL = os.environ.get("VERIFY_SSL", "true").lower() == "true"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

def ha_get(path):
    r = requests.get(f"{HA_URL}{path}", headers=HEADERS, verify=VERIFY_SSL)
    r.raise_for_status()
    return r.json()

server = Server("home-assistant-ro")

@server.tool()
def list_entities():
    """List all Home Assistant entities (read-only)."""
    states = ha_get("/api/states")
    return TextContent(
        text="\n".join(f"{s['entity_id']}: {s['state']}" for s in states)
    )

@server.tool()
def get_entity_state(entity_id: str):
    """Get the current state of a specific entity."""
    s = ha_get(f"/api/states/{entity_id}")
    return TextContent(text=str(s))

@server.tool()
def get_areas():
    """List Home Assistant areas."""
    return TextContent(text=str(ha_get("/api/config/area_registry")))

@server.tool()
def get_devices():
    """List Home Assistant devices."""
    return TextContent(text=str(ha_get("/api/config/device_registry")))

if __name__ == "__main__":
    server.run()
