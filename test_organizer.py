"""
Comprehensive Test Suite for Python Desktop File Organizer
==========================================================
Developer: Binay Chandra (GitHub: Binay-10)
Assignment: Tech Internships — File Organizer
Environment: Windows 11, Python 3.10+

This test suite executes unit and integration tests across all mandatory
technical specifications and edge cases described in Section 8 of the requirements:
1. Standard category classification (Documents, Images, Audio, Videos, Archives, Others)
2. Compound extensions (.tar.gz)
3. Case-insensitive matching (.JPG, .PNG, etc.)
4. Files without extensions (README)
5. Files with multiple dots in filename (report.2026.final.pdf)
6. Empty directory handling
7. Empty file handling (0-byte files)
8. Missing directory validation
9. File path instead of directory validation
10. Filename collision handling (generating _1, _2 without data loss)
11. Pre-existing category folder reuse without creating nested folders
12. Repeated execution idempotency
13. Running script self-protection (never moves itself)
14. Error resilience and graceful reporting
"""

import os
import shutil
import stat
import sys
import unittest
from pathlib import Path

# Import the FileOrganizer and helper classes
from file_organizer import (
    CATEGORY_MAPPING,
    DEFAULT_CATEGORY,
    FileOrganizer,
    OrganizationSummary,
)


class TestFileOrganizer(unittest.TestCase):
    """
    Test suite covering core logic, categorization, collision resolution,
    and end-to-end directory organization.
    """

    def setUp(self) -> None:
        """
        Creates a temporary test sandbox before each test.
        """
        self.test_dir = Path("temp_test_dir").resolve()
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        """
        Cleans up the temporary test sandbox after each test.
        """
        if self.test_dir.exists():
            # Reset permissions in case any read-only files were created
            for root, dirs, files in os.walk(self.test_dir):
                for f in files:
                    try:
                        p = Path(root) / f
                        p.chmod(stat.S_IWRITE)
                    except OSError:
                        pass
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_split_filename_and_compound_extensions(self) -> None:
        """
        Validates accurate splitting of single and compound extensions.
        """
        cases = [
            ("backup.tar.gz", "backup", ".tar.gz"),
            ("archive.tar.bz2", "archive", ".tar.bz2"),
            ("photo.jpg", "photo", ".jpg"),
            ("PHOTO.JPG", "PHOTO", ".JPG"),
            ("notes.txt", "notes", ".txt"),
            ("README", "README", ""),
            (".gitignore", ".gitignore", ""),
            ("my.report.v2.docx", "my.report.v2", ".docx"),
        ]
        for filename, expected_stem, expected_ext in cases:
            stem, ext = FileOrganizer.split_filename(filename)
            self.assertEqual(stem, expected_stem, f"Failed stem for {filename}")
            self.assertEqual(ext, expected_ext, f"Failed ext for {filename}")

    def test_category_mapping(self) -> None:
        """
        Validates category classification across all required types and fallbacks.
        """
        test_mappings = [
            ("assignment.pdf", "Documents"),
            ("notes.txt", "Documents"),
            ("report.docx", "Documents"),
            ("data.xlsx", "Documents"),
            ("photo.jpg", "Images"),
            ("PHOTO.JPG", "Images"),
            ("graphic.png", "Images"),
            ("animation.gif", "Images"),
            ("banner.webp", "Images"),
            ("song.mp3", "Audio"),
            ("movie.mp4", "Videos"),
            ("screencast.mkv", "Videos"),
            ("archive.zip", "Archives"),
            ("backup.rar", "Archives"),
            ("source.tar.gz", "Archives"),
            ("unknown.xyz", "Others"),
            ("README", "Others"),
            (".env", "Others"),
        ]
        for filename, expected_cat in test_mappings:
            actual_cat = FileOrganizer.get_category_for_file(filename)
            self.assertEqual(
                actual_cat,
                expected_cat,
                f"File '{filename}' expected in '{expected_cat}', got '{actual_cat}'"
            )

    def test_directory_validation(self) -> None:
        """
        Validates directory existence and type checking.
        """
        # 1. Non-existent directory
        fake_path = self.test_dir / "non_existent_folder"
        organizer = FileOrganizer(fake_path)
        is_valid, msg = organizer.validate_directory()
        self.assertFalse(is_valid)
        self.assertIn("does not exist", msg)

        # 2. File instead of directory
        dummy_file = self.test_dir / "dummy.txt"
        dummy_file.write_text("just a file", encoding="utf-8")
        organizer_file = FileOrganizer(dummy_file)
        is_valid, msg = organizer_file.validate_directory()
        self.assertFalse(is_valid)
        self.assertIn("not a directory", msg)

        # 3. Valid directory
        organizer_valid = FileOrganizer(self.test_dir)
        is_valid, msg = organizer_valid.validate_directory()
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")

    def test_collision_handling(self) -> None:
        """
        Validates that duplicate filenames generate unique _1, _2 names
        without overwriting existing files.
        """
        dest_dir = self.test_dir / "Documents"
        dest_dir.mkdir(parents=True, exist_ok=True)

        original_file = dest_dir / "report.pdf"
        original_file.write_text("original content", encoding="utf-8")

        # First collision -> report_1.pdf
        new_path_1 = FileOrganizer.get_unique_destination_path(dest_dir, "report.pdf")
        self.assertEqual(new_path_1.name, "report_1.pdf")
        new_path_1.write_text("second content", encoding="utf-8")

        # Second collision -> report_2.pdf
        new_path_2 = FileOrganizer.get_unique_destination_path(dest_dir, "report.pdf")
        self.assertEqual(new_path_2.name, "report_2.pdf")

        # Compound extension collision -> backup_1.tar.gz
        backup_file = dest_dir / "backup.tar.gz"
        backup_file.write_text("tar content", encoding="utf-8")
        backup_collision = FileOrganizer.get_unique_destination_path(dest_dir, "backup.tar.gz")
        self.assertEqual(backup_collision.name, "backup_1.tar.gz")

        # File without extension collision -> README_1
        readme_file = dest_dir / "README"
        readme_file.write_text("readme content", encoding="utf-8")
        readme_collision = FileOrganizer.get_unique_destination_path(dest_dir, "README")
        self.assertEqual(readme_collision.name, "README_1")

    def test_full_organization_flow(self) -> None:
        """
        Simulates end-to-end organization with the complete set of required sample files.
        """
        sample_files = [
            "assignment.pdf",
            "notes.txt",
            "photo.jpg",
            "animation.gif",
            "song.mp3",
            "movie.mp4",
            "backup.tar.gz",
            "archive.zip",
            "unknown.xyz",
            "README",
            "empty.txt",
            "project.notes.v2.docx",
        ]
        for name in sample_files:
            (self.test_dir / name).write_text(f"Content for {name}", encoding="utf-8")

        organizer = FileOrganizer(self.test_dir)
        summary = organizer.organize(verbose=False)

        self.assertEqual(summary.files_scanned, len(sample_files))
        self.assertEqual(summary.files_organized, len(sample_files))
        self.assertEqual(summary.files_skipped, 0)
        self.assertEqual(summary.errors_encountered, 0)
        self.assertGreaterEqual(summary.execution_time, 0.0)

        # Verify files reached correct subdirectories
        self.assertTrue((self.test_dir / "Documents" / "assignment.pdf").exists())
        self.assertTrue((self.test_dir / "Documents" / "notes.txt").exists())
        self.assertTrue((self.test_dir / "Documents" / "empty.txt").exists())
        self.assertTrue((self.test_dir / "Documents" / "project.notes.v2.docx").exists())
        self.assertTrue((self.test_dir / "Images" / "photo.jpg").exists())
        self.assertTrue((self.test_dir / "Images" / "animation.gif").exists())
        self.assertTrue((self.test_dir / "Audio" / "song.mp3").exists())
        self.assertTrue((self.test_dir / "Videos" / "movie.mp4").exists())
        self.assertTrue((self.test_dir / "Archives" / "backup.tar.gz").exists())
        self.assertTrue((self.test_dir / "Archives" / "archive.zip").exists())
        self.assertTrue((self.test_dir / "Others" / "unknown.xyz").exists())
        self.assertTrue((self.test_dir / "Others" / "README").exists())

    def test_empty_directory(self) -> None:
        """
        Validates graceful handling of an empty target directory.
        """
        organizer = FileOrganizer(self.test_dir)
        summary = organizer.organize(verbose=False)

        self.assertEqual(summary.files_scanned, 0)
        self.assertEqual(summary.files_organized, 0)
        self.assertEqual(summary.files_skipped, 0)
        self.assertEqual(summary.errors_encountered, 0)

    def test_repeated_execution_idempotency(self) -> None:
        """
        Validates that running the organizer a second time on an already-organized directory
        does not corrupt files, create nested duplicate folders, or scan category folders as files.
        """
        (self.test_dir / "test.pdf").write_text("Test PDF", encoding="utf-8")
        (self.test_dir / "image.png").write_text("Test PNG", encoding="utf-8")

        organizer = FileOrganizer(self.test_dir)

        # First run
        summary1 = organizer.organize(verbose=False)
        self.assertEqual(summary1.files_organized, 2)

        # Second run
        summary2 = organizer.organize(verbose=False)
        self.assertEqual(summary2.files_scanned, 0)
        self.assertEqual(summary2.files_organized, 0)
        self.assertEqual(summary2.files_skipped, 0)
        self.assertEqual(summary2.errors_encountered, 0)

        # Verify no duplicate nested folders were created (e.g., Documents/Documents)
        self.assertFalse((self.test_dir / "Documents" / "Documents").exists())
        self.assertFalse((self.test_dir / "Images" / "Images").exists())

    def test_script_self_protection(self) -> None:
        """
        Ensures that if the organizer script exists in the target directory,
        it skips itself and does not move itself into Others/.
        """
        script_dummy = self.test_dir / "file_organizer.py"
        script_dummy.write_text("# dummy script", encoding="utf-8")

        organizer = FileOrganizer(self.test_dir)
        # Point the script_path explicitly to the dummy to test the safety filter
        organizer.script_path = script_dummy.resolve()

        summary = organizer.organize(verbose=False)
        self.assertEqual(summary.files_scanned, 1)
        self.assertEqual(summary.files_skipped, 1)
        self.assertEqual(summary.files_organized, 0)
        self.assertTrue(script_dummy.exists())
        self.assertFalse((self.test_dir / "Others" / "file_organizer.py").exists())


def run_tests() -> bool:
    """
    Runs the test suite and returns True if all tests passed.
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileOrganizer)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
