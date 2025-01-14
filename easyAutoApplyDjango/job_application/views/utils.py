
import re

def generate_download_resume_link( resume_hash):
    # Extract the file name using regular expressions
    wix_link_hash = ""
    match = re.search(r'/([^/]+\.pdf)', resume_hash)
    if match:
        file_name = match.group(1)
        # Create the link using the URL template
        link = f"https://{wix_link_hash}.usrfiles.com/ugd/{file_name}"
        return link
    else:
        return None
    

