"""
Python Desktop File Organizer Automation Tool
=============================================
Developer: Binay Chandra
GitHub: Binay-10
Assignment: Tech Internships — File Organizer
Environment: Windows 11, VS Code, PowerShell
Python Version: Python 3.10+

Description:
    A robust, beginner-friendly yet professionally structured file organization
    automation tool that inspects a user-specified directory and classifies files
    into categorized folders (Documents, Images, Audio, Videos, Archives, Others)
    based on their extensions.

Technical Highlights:
    - os.listdir() for inspecting directory contents.
    - os.path.splitext() and compound extension parsing for extension extraction.
    - shutil.move() for safe atomic file transfers.
    - pathlib.Path for cross-platform path validation and manipulation.
    - os.makedirs(..., exist_ok=True) for safe directory creation.
    - time.perf_counter() for precision benchmark timing.
    - Non-destructive collision handling (e.g., report_1.pdf).
    - Protection against moving the running script or category folders into themselves.
"""

from __future__ import annotations

import os
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Final

# Predefined Category Mapping as specified by the assignment requirements
CATEGORY_MAPPING: Final[dict[str, list[str]]] = {
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Images": [".jpg", ".png", ".gif", ".webp"],
    "Audio": [".mp3"],
    "Videos": [".mp4", ".mkv"],
    "Archives": [".zip", ".rar", ".tar.gz"],
}

DEFAULT_CATEGORY: Final[str] = "Others"

# Compound extensions that cannot be extracted purely by standard single-split splitext
KNOWN_COMPOUND_EXTENSIONS: Final[tuple[str, ...]] = (
    ".tar.gz",
    ".tar.bz2",
    ".tar.xz",
)


@dataclass
class OrganizationSummary:
    """
    Data class representing the execution metrics of the file organization process.
    """
    files_scanned: int = 0
    files_organized: int = 0
    files_skipped: int = 0
    errors_encountered: int = 0
    execution_time: float = 0.0


class FileOrganizer:
    """
    Automates the classification, collision resolution, and moving of files
    within a target directory into organized category directories.
    """

    def __init__(self, target_directory: str | Path) -> None:
        """
        Initialize the FileOrganizer with a target directory path.

        Args:
            target_directory: Absolute or relative path to the folder to organize.
        """
        self.target_path: Path = Path(target_directory).expanduser().resolve()
        
        # Safely resolve the running script's own path to prevent self-moving
        try:
            self.script_path: Path | None = Path(__file__).resolve()
        except (NameError, TypeError):
            self.script_path = None

    def validate_directory(self) -> tuple[bool, str]:
        """
        Verifies that the target directory exists and is a valid directory.

        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        if not self.target_path.exists():
            return False, f"Target directory does not exist: '{self.target_path}'"
        if not self.target_path.is_dir():
            return False, f"Target path is not a directory: '{self.target_path}'"
        return True, ""

    @staticmethod
    def split_filename(filename: str) -> tuple[str, str]:
        """
        Splits a filename into its stem and extension.
        Accurately recognizes multi-part compound extensions like '.tar.gz'
        while utilizing os.path.splitext() for all standard extensions.

        Args:
            filename: The name of the file (e.g. 'backup.tar.gz', 'report.pdf', 'README')

        Returns:
            A tuple of (stem, extension) where extension includes the leading dot if present.
        """
        lower_name = filename.lower()
        for compound in KNOWN_COMPOUND_EXTENSIONS:
            # Check if filename ends with known compound extension and is not just the extension itself
            if lower_name.endswith(compound) and len(filename) > len(compound):
                stem = filename[:-len(compound)]
                ext = filename[-len(compound):]
                return stem, ext

        # Fall back to standard os.path.splitext()
        stem, ext = os.path.splitext(filename)
        return stem, ext

    @classmethod
    def get_category_for_file(cls, filename: str) -> str:
        """
        Determines the target folder category based on file extension.
        Performs case-insensitive matching. Unrecognized extensions or files
        without extensions default to 'Others'.

        Args:
            filename: Name of the file to evaluate.

        Returns:
            The category name (e.g., 'Documents', 'Images', 'Others').
        """
        _, ext = cls.split_filename(filename)
        ext_lower = ext.lower()

        for category, extensions in CATEGORY_MAPPING.items():
            if ext_lower in extensions:
                return category

        return DEFAULT_CATEGORY

    @classmethod
    def get_unique_destination_path(cls, destination_dir: Path, filename: str) -> Path:
        """
        Checks whether the destination filename already exists in the destination folder.
        If a collision occurs, generates a unique incremental name (e.g., 'report_1.pdf')
        while strictly preserving original file extensions.

        Args:
            destination_dir: Path to the category directory.
            filename: Original filename to be moved.

        Returns:
            A Path object representing an unused, collision-free destination path.
        """
        candidate_path = destination_dir / filename
        if not candidate_path.exists():
            return candidate_path

        stem, ext = cls.split_filename(filename)
        counter = 1
        while True:
            unique_filename = f"{stem}_{counter}{ext}"
            candidate_path = destination_dir / unique_filename
            if not candidate_path.exists():
                return candidate_path
            counter += 1

    def scan_files(self) -> list[str]:
        """
        Inspects the target directory using os.listdir() and identifies regular files.
        Subdirectories (including pre-existing category folders) are explicitly ignored
        to prevent duplicate nesting and unwanted traversal.

        Returns:
            A list of filenames representing files discovered in the target directory.
        """
        try:
            entries = os.listdir(self.target_path)
        except OSError as err:
            raise OSError(f"Unable to read directory '{self.target_path}': {err}") from err

        discovered_files: list[str] = []
        for entry in entries:
            entry_path = self.target_path / entry
            # Rule: Never treat directories as regular files
            if entry_path.is_dir():
                continue
            if entry_path.is_file():
                discovered_files.append(entry)

        return discovered_files

    def organize(self, verbose: bool = True) -> OrganizationSummary:
        """
        Coordinates the entire file organization workflow:
        1. Validates directory accessibility.
        2. Scans files using os.listdir().
        3. Classifies files into categories.
        4. Safely creates category directories using os.makedirs(..., exist_ok=True).
        5. Handles filename collisions cleanly.
        6. Transfers files via shutil.move().
        7. Calculates execution benchmark via time.perf_counter().
        8. Outputs formatted execution log and summary.

        Args:
            verbose: If True, prints real-time logs and the final summary.

        Returns:
            OrganizationSummary containing the final execution counts and duration.
        """
        # Feature A: Directory Validation
        is_valid, error_msg = self.validate_directory()
        if not is_valid:
            raise ValueError(error_msg)

        # Feature D: Precise benchmark timing
        start_time = time.perf_counter()
        summary = OrganizationSummary()

        if verbose:
            print("=== PYTHON DESKTOP FILE ORGANIZER ===\n")
            # Present path with forward slashes for clean, readable terminal display
            print(f"Target Folder: {self.target_path.as_posix()}\n")

        # Feature A: Directory Inspection using os.listdir()
        files_to_process = self.scan_files()
        summary.files_scanned = len(files_to_process)

        if verbose:
            print(f"Scanning {summary.files_scanned} files...\n")
            print("[ORGANIZING IN PROGRESS]\n")

        # Feature B & C: Classification, Collision Handling & Safe Transfer
        for filename in files_to_process:
            source_path = self.target_path / filename

            # Safety Rule: Never move the running script itself
            if self.script_path and source_path.resolve() == self.script_path:
                if verbose:
                    print(f"Skipping '{filename}' (running Python script)")
                summary.files_skipped += 1
                continue

            # Determine category based on extension
            category = self.get_category_for_file(filename)
            category_dir = self.target_path / category

            # Feature B: Safe category directory creation
            try:
                os.makedirs(category_dir, exist_ok=True)
            except OSError as err:
                if verbose:
                    print(f"Error creating category directory '{category_dir}': {err}")
                summary.errors_encountered += 1
                continue

            # Feature C: Safe Collision Resolution
            destination_path = self.get_unique_destination_path(category_dir, filename)

            # Safety Rule: Do not move if source and destination resolve to the same location
            try:
                if source_path.resolve() == destination_path.resolve():
                    if verbose:
                        print(f"Skipping '{filename}' (already in destination location)")
                    summary.files_skipped += 1
                    continue
            except OSError as err:
                if verbose:
                    print(f"Error checking file path '{filename}': {err}")
                summary.errors_encountered += 1
                continue

            # Feature C: Move file using shutil.move() with isolated exception handling
            try:
                shutil.move(str(source_path), str(destination_path))
                if verbose:
                    if destination_path.name != filename:
                        print(f"Moving '{filename}' -> {category}/ (renamed to '{destination_path.name}')")
                    else:
                        print(f"Moving '{filename}' -> {category}/")
                summary.files_organized += 1
            except PermissionError as err:
                if verbose:
                    print(f"Permission denied while moving '{filename}': {err}")
                summary.errors_encountered += 1
            except shutil.SameFileError as err:
                if verbose:
                    print(f"Skipping identical file '{filename}': {err}")
                summary.files_skipped += 1
            except OSError as err:
                if verbose:
                    print(f"Filesystem error moving '{filename}': {err}")
                summary.errors_encountered += 1
            except Exception as err:
                if verbose:
                    print(f"Unexpected error moving '{filename}': {err}")
                summary.errors_encountered += 1

        # Stop timer
        summary.execution_time = time.perf_counter() - start_time

        # Feature D: Execution Log Summary
        if verbose:
            print("\n[SUMMARY]\n")
            print(f"Files scanned: {summary.files_scanned}")
            print(f"Files successfully organized: {summary.files_organized}")
            print(f"Files skipped: {summary.files_skipped}")
            print(f"Errors encountered: {summary.errors_encountered}\n")
            print(f"Execution time: {summary.execution_time:.2f} seconds")
            if summary.errors_encountered == 0:
                print("Organization completed successfully!")
            else:
                print("Organization completed with errors encountered.")

        return summary


def main() -> None:
    """
    Main entry point for interactive user execution.
    Accepts an optional command-line path or prompts user for target directory.
    Supports clean cancellation, quote-stripping on Windows, and error reporting.
    """
    try:
        if len(sys.argv) > 1:
            raw_input_path = sys.argv[1]
        else:
            print("=========================================")
            print("===   PYTHON DESKTOP FILE ORGANIZER   ===")
            print("=========================================")
            print("Developer : Binay Chandra (GitHub: Binay-10)")
            print("Project   : File-Organizer (Tech Internships)")
            print("Platform  : Windows 11 | Python 3.10+\n")
            print("Instructions: Enter an absolute or relative directory path to organize.")
            print("              Type 'q' or press Ctrl+C to cancel at any time.\n")
            raw_input_path = input("Target directory path: ").strip()

        # Handle user cancellation
        if not raw_input_path or raw_input_path.lower() in ("q", "quit", "exit"):
            print("\nOperation cancelled. Exiting without modifying any files.")
            sys.exit(0)

        # Clean Windows pasted paths (which might be enclosed in single or double quotes)
        cleaned_path = raw_input_path.strip("\"'")

        organizer = FileOrganizer(cleaned_path)
        is_valid, error_message = organizer.validate_directory()

        if not is_valid:
            print(f"\n[ERROR] {error_message}")
            print("Please check the path and try again.")
            sys.exit(1)

        print()
        organizer.organize(verbose=True)

    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Operation aborted by user. Exiting safely.")
        sys.exit(0)
    except Exception as err:
        print(f"\n[FATAL ERROR] An unexpected error occurred: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
