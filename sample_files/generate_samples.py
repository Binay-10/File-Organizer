"""
Sample Test Files Generator
===========================
Developer: Binay Chandra
Assignment: Tech Internships — File Organizer

Utility script to populate a disposable test directory with realistic sample files
covering all required extensions, compound extensions, and edge cases.
"""

from pathlib import Path


def generate_samples(target_folder: str = "test_workspace") -> Path:
    """
    Creates a disposable directory filled with sample files for organizer testing.
    """
    dest = Path(target_folder).resolve()
    dest.mkdir(parents=True, exist_ok=True)

    samples = {
        "assignment.pdf": "Sample PDF Document for testing",
        "notes.txt": "Meeting notes text file",
        "quarterly_report.docx": "Word Document content placeholder",
        "financials.xlsx": "Excel spreadsheet content placeholder",
        "photo.jpg": "JPEG image binary placeholder",
        "PHOTO.JPG": "Uppercase JPEG image for case-insensitivity and collision test",
        "banner.png": "PNG image data",
        "animation.gif": "GIF animation data",
        "vector_graphic.webp": "Modern WEBP image data",
        "podcast_track.mp3": "MP3 audio data",
        "presentation.mp4": "MP4 video content",
        "screencast.mkv": "MKV video file",
        "archive_backup.zip": "ZIP archive content",
        "dataset.rar": "RAR archive content",
        "server_logs.tar.gz": "Compound extension tar.gz archive",
        "my.project.v2.pdf": "Filename with multiple dots and standard extension",
        "unknown_data.xyz": "File with unknown extension for Others folder",
        "README": "File without any extension for Others folder",
        "empty_file.txt": "",  # Empty file test
    }

    print(f"Creating sample test files in: {dest}")
    for filename, content in samples.items():
        file_path = dest / filename
        file_path.write_text(content, encoding="utf-8")
        print(f"  + Created: {filename}")

    print(f"\nSuccessfully generated {len(samples)} sample files in '{target_folder}'.")
    return dest


if __name__ == "__main__":
    generate_samples()
