# Sample Test Files Guide

This directory guides you in creating safe, disposable sample files to test the **Python Desktop File Organizer** without touching or committing any personal or sensitive files.

---

## 1. Why Disposable Sample Files?

During development and evaluation, it is critical **never** to run experimental automation scripts directly on personal folders like your actual `Downloads`, `Documents`, or `Desktop`.

Using disposable test files ensures:
- Safe, non-destructive testing.
- Predictable and repeatable evaluation runs.
- Clean Git commit history without private files or accidental data leaks.

---

## 2. Recommended Test File Set

To thoroughly test all file categories and edge cases specified in the assignment, use this sample collection:

| Filename | Expected Category | Reason / Test Objective |
| :--- | :--- | :--- |
| `assignment.pdf` | **Documents** | Standard document extension |
| `notes.txt` | **Documents** | Standard text file |
| `quarterly_report.docx` | **Documents** | Microsoft Word format |
| `financials.xlsx` | **Documents** | Microsoft Excel spreadsheet |
| `photo.jpg` | **Images** | Standard JPEG image |
| `PHOTO.JPG` | **Images** | Uppercase extension handling & collision |
| `banner.png` | **Images** | Portable Network Graphics |
| `animation.gif` | **Images** | Graphics Interchange Format |
| `vector_graphic.webp`| **Images** | Modern web image format |
| `podcast_track.mp3` | **Audio** | Audio format |
| `presentation.mp4` | **Videos** | Standard video container |
| `screencast.mkv` | **Videos** | Matroska video container |
| `archive_backup.zip`| **Archives** | ZIP compressed file |
| `dataset.rar` | **Archives** | Roshal ARchive format |
| `server_logs.tar.gz` | **Archives** | Compound extension (`.tar.gz`) test |
| `my.project.v2.pdf` | **Documents** | Multiple dots in filename |
| `unknown_data.xyz` | **Others** | Unrecognized extension fallback |
| `README` | **Others** | File without any extension |
| `empty_file.txt` | **Documents** | Zero-byte empty file handling |

---

## 3. Method A — Automated Generation (Recommended)

Run the included generation script from the project root using PowerShell:

```powershell
python sample_files/generate_samples.py
```

This will automatically create a dedicated folder named `test_workspace` in the project root filled with all the sample files listed above.

---

## 4. Method B — Manual Generation via PowerShell

If you prefer to create the files manually in a folder called `test_workspace`, run the following commands in PowerShell:

```powershell
# Create test directory
New-Item -ItemType Directory -Force -Path "test_workspace"

# Create standard sample files
Set-Content -Path "test_workspace/assignment.pdf" -Value "Sample PDF assignment"
Set-Content -Path "test_workspace/notes.txt" -Value "Sample lecture notes"
Set-Content -Path "test_workspace/quarterly_report.docx" -Value "Sample docx"
Set-Content -Path "test_workspace/financials.xlsx" -Value "Sample xlsx"
Set-Content -Path "test_workspace/photo.jpg" -Value "Sample image content"
Set-Content -Path "test_workspace/banner.png" -Value "Sample PNG content"
Set-Content -Path "test_workspace/animation.gif" -Value "Sample GIF content"
Set-Content -Path "test_workspace/vector_graphic.webp" -Value "Sample WEBP content"
Set-Content -Path "test_workspace/podcast_track.mp3" -Value "Sample audio content"
Set-Content -Path "test_workspace/presentation.mp4" -Value "Sample video content"
Set-Content -Path "test_workspace/screencast.mkv" -Value "Sample MKV content"
Set-Content -Path "test_workspace/archive_backup.zip" -Value "Sample ZIP archive"
Set-Content -Path "test_workspace/dataset.rar" -Value "Sample RAR archive"
Set-Content -Path "test_workspace/server_logs.tar.gz" -Value "Sample tar.gz archive"
Set-Content -Path "test_workspace/my.project.v2.pdf" -Value "Sample multi-dot file"
Set-Content -Path "test_workspace/unknown_data.xyz" -Value "Sample unknown extension"
Set-Content -Path "test_workspace/README" -Value "Sample file with no extension"
New-Item -ItemType File -Force -Path "test_workspace/empty_file.txt"
```

---

## 5. Cleaning Up Test Data

Because `test_workspace/` is included in `.gitignore`, it will not be committed to Git. To remove the test folder once testing is complete, run:

```powershell
Remove-Item -Recurse -Force "test_workspace"
```
