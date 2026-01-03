# Paramodus Anime.js Version (Executable Ready)

A high-performance, multi-agent AI productivity assistant.

## How to Build the EXE

To package this app into a single standalone `.exe` for Windows:

1. **Install Build Tools**:
   ```bash
   pip install pyinstaller
   ```

2. **Run the Build Command**:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --add-data "static;static" --name "Paramodus" launcher.py
   ```
   *Note: Use `:` instead of `;` on Linux/macOS (e.g., `--add-data "static:static"`).*

3. **Find your Program**:
   The standalone executable will be in the `dist/` folder.

## Running in Dev Mode
```bash
python launcher.py
```
This will start the FastAPI server and automatically open the UI in your browser.
