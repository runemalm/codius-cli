from domain.service.config_service import ensure_project_config_exists
from ui.shell import run_shell


def main():
    ensure_project_config_exists()
    run_shell()

if __name__ == "__main__":
    main()
