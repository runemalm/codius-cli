from pathlib import Path
import shutil
import logging

from domain.services.session_service import get_active_session

logger = logging.getLogger(__name__)


class ProjectMetadataService:
    def __init__(self):
        self.workdir = Path(".").resolve()
        self.metadata_root = self.workdir / ".openddd"

    def get_config_path(self) -> Path:
        """Returns the full path to the global config.yaml."""
        return self.metadata_root / "config.yaml"

    def ensure_session_dir_exists(self, session_id: str = None):
        """Ensures the session directory exists."""
        if session_id is None:
            session_id = get_active_session().id
        session_dir = self._get_session_dir(session_id)
        session_dir.mkdir(parents=True, exist_ok=True)

    def get_sessions_path(self) -> Path:
        """Returns the path to the sessions directory (.openddd/sessions)."""
        return self.metadata_root / "sessions"

    def get_state_path(self, session_id: str = None) -> Path:
        """Returns the full path to state.json for the given session."""
        if session_id is None:
            session_id = get_active_session().id
        return self._get_session_dir(session_id) / "state.json"

    def _get_session_dir(self, session_id: str) -> Path:
        return self.get_sessions_path() / session_id

    def clear_generated_files(self, session_id: str = None):
        """Deletes and recreates the generated/ directory for the given session."""
        if session_id is None:
            session_id = get_active_session().id

        generated_dir = self._get_session_dir(session_id) / "generated"

        if generated_dir.exists():
            try:
                shutil.rmtree(generated_dir)
                logger.info("Deleted generated directory: %s", generated_dir)
            except Exception as e:
                logger.warning("Failed to delete generated directory: %s", e)

        try:
            generated_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Recreated generated directory: %s", generated_dir)
        except Exception as e:
            logger.error("Failed to recreate generated directory: %s", e)
