import os
import re
import hashlib
from collections import defaultdict

def normalize_content(content):
    # Remove the Name attribute from SubAppType
    content = re.sub(r'<SubAppType\s+Name="[^"]*"', '<SubAppType Name="PLACEHOLDER"', content)
    # Remove the Comment attribute from SubAppType
    content = re.sub(r'Comment="[^"]*"', 'Comment="PLACEHOLDER"', content)
    # Remove VersionInfo attributes
    content = re.sub(r'Date="[^"]*"', 'Date="PLACEHOLDER"', content)
    content = re.sub(r'Remarks="[^"]*"', 'Remarks="PLACEHOLDER"', content)
    content = re.sub(r'Author="[^"]*"', 'Author="PLACEHOLDER"', content)
    content = re.sub(r'Organization="[^"]*"', 'Organization="PLACEHOLDER"', content)
    # Remove Identification Description
    content = re.sub(r'Description="[^"]*"', 'Description="PLACEHOLDER"', content)
    # Remove x and y coordinates
    content = re.sub(r'x="[^"]*"', 'x="PLACEHOLDER"', content)
    content = re.sub(r'y="[^"]*"', 'y="PLACEHOLDER"', content)
    # Remove dx and dy coordinates
    content = re.sub(r'dx[12]?="[^"]*"', 'dx="PLACEHOLDER"', content)
    content = re.sub(r'dy[12]?="[^"]*"', 'dy="PLACEHOLDER"', content)
    return content

def main():
    files = [f for f in os.listdir('.') if f.endswith('.SUB')]
    hashes = defaultdict(list)
    
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            normalized = normalize_content(content)
            h = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
            hashes[h].append(filename)
            
    for h, filenames in hashes.items():
        if len(filenames) > 1:
            print(f"Duplicate content found in:")
            for f in filenames:
                # Extract the Name attribute to show it's different
                with open(f, 'r', encoding='utf-8') as file:
                    content = file.read()
                    match = re.search(r'<SubAppType\s+Name="([^"]*)"', content)
                    sub_name = match.group(1) if match else "UNKNOWN"
                    print(f"  - {f} (SubApp Name: {sub_name})")
            print("-" * 40)

if __name__ == "__main__":
    main()
