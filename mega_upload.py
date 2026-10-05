#!/usr/bin/env python3
"""
Upload video file to MEGA using mega.py library
"""

import sys
from pathlib import Path
from mega import Mega

def upload_to_mega(file_path, mega_email, mega_password):
    """
    Upload a file to MEGA cloud storage
    """
    print(f"Uploading {file_path} to MEGA...")
    
    # Initialize MEGA client
    m = Mega()
    
    try:
        # Login to MEGA
        m.login(mega_email, mega_password)
        print("Successfully logged in to MEGA")
        
        # Upload file
        file_path = Path(file_path)
        uploaded_file = m.upload(str(file_path))
        
        # Get download link
        download_link = m.get_upload_link(uploaded_file)
        
        print(f"✅ Successfully uploaded to MEGA!")
        print(f"Download link: {download_link}")
        
        return download_link
        
    except Exception as e:
        print(f"Error uploading to MEGA: {e}")
        return None

def main():
    if len(sys.argv) < 4:
        print("Usage: python mega_upload.py <file_path> <mega_email> <mega_password>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    mega_email = sys.argv[2]
    mega_password = sys.argv[3]
    
    download_link = upload_to_mega(file_path, mega_email, mega_password)
    
    if download_link:
        # Output for GitHub Actions
        print(f"DOWNLOAD_LINK={download_link}")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
