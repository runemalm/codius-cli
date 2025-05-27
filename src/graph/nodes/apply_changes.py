from pathlib import Path

from domain.service import session_service


def apply_changes(state: dict) -> dict:
    session_id = session_service.get_active_session_id()
    generated_dir = Path(f".openddd/sessions/{session_id}/generated")
    generated_files = list(generated_dir.rglob("*.cs"))

    for src_path in generated_files:
        rel_path = src_path.relative_to(generated_dir)
        dest_path = Path(rel_path)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(src_path.read_text())

    file_list = "\n".join([f"✅ {str(f.relative_to(generated_dir))}" for f in generated_files])
    state["final_output"] = f"Applied changes:\n\n{file_list}"
    return state
