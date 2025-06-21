import shutil

from pathlib import Path
from domain.services.session_service import SessionService


def apply_changes(state: dict) -> dict:
    from di import container

    session_service = container.resolve(SessionService)

    session_id = session_service.get_active_session_id()
    generated_dir = Path(f".openddd/sessions/{session_id}/generated")
    generated_files = list(generated_dir.rglob("*.cs"))

    # Copy generated files
    for src_path in generated_files:
        rel_path = src_path.relative_to(generated_dir)
        dest_path = Path(rel_path)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(src_path.read_text())

    # Handle deletions
    deleted_paths = []
    for plan_item in state.get("plan", []):
        if plan_item["type"] == "delete_directory":
            dir_path = Path(plan_item["path"])
            if dir_path.exists() and dir_path.is_dir():
                shutil.rmtree(dir_path)
                deleted_paths.append(dir_path)
        elif plan_item["type"] == "delete_file":
            file_path = Path(plan_item["path"])
            if file_path.exists() and file_path.is_file():
                file_path.unlink()
                deleted_paths.append(file_path)

    file_list = "\n".join([
        f"✅ {str(f.relative_to(generated_dir))}" for f in generated_files
    ] + [
        f"❌️ {str(p)}" for p in deleted_paths
    ])

    state["final_output"] = f"Applied changes:\n\n{file_list}"
    return state
