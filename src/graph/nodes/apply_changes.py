from pathlib import Path


def apply_changes(state: dict) -> dict:
    session_id = state.get("session_id", "unknown_session")
    generated_files = state.get("generated_files", [])

    for file in generated_files:
        path = Path(f".openddd/sessions/{session_id}/generated/{file['path']}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(file["content"])

    # Update final output
    file_list = "\n".join([f"✅ {f['path']}" for f in generated_files])
    state["final_output"] = f"Applied changes:\n\n{file_list}"
    return state
