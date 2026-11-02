def main() -> None:
    """Inicia a interface visual local feita com Streamlit."""
    import subprocess
    import sys
    from pathlib import Path

    app_file = Path(__file__).with_name("app.py")
    result = subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(app_file)],
        check=False,
    )
    raise SystemExit(result.returncode)
