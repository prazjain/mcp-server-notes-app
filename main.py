from mcp.server.fastmcp import FastMCP
import os 

# Create an MCP server
mcp = FastMCP("NotesApp", "1.0.0")

NOTES_FILE = os.path.join(os.path.dirname(__file__),"notes.txt")

def ensure_file():
    """Ensure the notes file exists."""
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'w') as f:
            f.write("")

@mcp.tool("add_note")
def add_note(note: str):
    """Add a note to the notes file."""
    ensure_file()
    with open(NOTES_FILE, 'a') as f:
        f.write(note + "\n")
    return {"status": "success", "message": "Note added successfully."}

@mcp.tool("get_notes")
def get_notes():
    """Retrieve all notes from the notes file."""
    ensure_file()
    with open(NOTES_FILE, 'r') as f:
        notes = f.readlines()
    return {"status": "success", "notes": [note.strip() for note in notes]}

@mcp.tool("clear_notes")
def clear_notes():
    """Clear all notes from the notes file."""
    ensure_file()
    with open(NOTES_FILE, 'w') as f:
        f.write("")
    return {"status": "success", "message": "All notes cleared."}

@mcp.resource("notes://latest")
def latest_note():
    """Resource to get the latest note."""
    ensure_file()
    with open(NOTES_FILE, 'r') as f:
        notes = f.readlines()
    return {"status": "success", "note": [notes[-1].strip() if notes else "No notes available."]}

@mcp.prompt()
def note_summary_prompt() -> str:
    """Prompt to summarize the notes."""
    ensure_file()
    with open(NOTES_FILE, 'r') as f:
        notes = f.readlines()
    if not notes:
        return "No notes available."
    summary = "Summarize the current notes:\n" + "\n".join([note.strip() for note in notes])
    return summary