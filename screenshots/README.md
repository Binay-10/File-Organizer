# Screenshots Guide

This directory stores authentic visual verification screenshots captured during testing of the **Python Desktop File Organizer**.

---

## 1. Required Screenshots

| File Name | Description |
| :--- | :--- |
| `before_organization.png` | Windows File Explorer or Terminal showing the unorganized, cluttered directory containing all mixed sample files. |
| `after_organization.png` | Windows File Explorer or Terminal showing the clean categorized directory with `Documents`, `Images`, `Audio`, `Videos`, `Archives`, and `Others` subdirectories. |

---

## 2. How to Capture Genuine Screenshots on Windows 11

Follow these simple steps on your Windows 11 machine:

### Step 1: Prepare the "Before" State
1. Generate sample test files by running in PowerShell:
   ```powershell
   python sample_files/generate_samples.py
   ```
2. Open the `test_workspace` folder in Windows File Explorer:
   ```powershell
   explorer.exe test_workspace
   ```
3. Press **`Win + Shift + S`** to open the Windows Snipping Tool.
4. Select the File Explorer window or region showing the mixed sample files.
5. Save the image as:
   `screenshots/before_organization.png`

### Step 2: Prepare the "After" State
1. Run the organizer tool:
   ```powershell
   python file_organizer.py test_workspace
   ```
2. Look at the `test_workspace` folder in Windows File Explorer (showing `Documents/`, `Images/`, `Audio/`, `Videos/`, `Archives/`, `Others/`).
3. Press **`Win + Shift + S`** to open the Snipping Tool.
4. Select the File Explorer window showing the organized folders.
5. Save the image as:
   `screenshots/after_organization.png`

---

## 3. Viewing in GitHub

Once these two PNG files are saved in this folder, they will automatically render inside the main project `README.md` under the **Visual Verification / Screenshots** section.
