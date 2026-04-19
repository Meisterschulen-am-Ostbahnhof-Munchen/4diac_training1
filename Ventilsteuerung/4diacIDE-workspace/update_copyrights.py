import os
import re

extensions = ('.fbt', '.SUB', '.adp', '.itp', '.dtp')
lib_dir = '.lib'

patterns_to_exclude = ["HR Agrartechnik", "HR Agratechnik", "Meisterschulen"]
copyright_pattern = re.compile(r'Copyright\s+\(c\)\s+(?:(\d{4}(?:-\d{4})?)\s+)?([^&#\n]+)', re.IGNORECASE)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find Identification tag and its Description attribute
    ident_match = re.search(r'(<Identification\s+[^>]*Description=")([^"]*)(")', content, re.DOTALL)
    if not ident_match:
        return False

    prefix, description, suffix = ident_match.groups()
    
    if "Copyright (c)" not in description:
        return False
    
    for pattern in patterns_to_exclude:
        if pattern in description:
            return False

    # Find the last copyright holder. 
    # Usually it looks like: Copyright (c) 2011 TU Wien ACIN
    # We want to append after the holder.
    # The holder is usually everything after the year until the first newline or &#10; or similar.
    
    # Let's find all occurrences of Copyright (c)
    matches = list(re.finditer(r'Copyright\s+\(c\)\s+(?:(\d{4}(?:-\d{4})?)\s+)?([^&#\n]+)', description, re.IGNORECASE))
    if not matches:
        return False
    
    last_match = matches[-1]
    holder = last_match.group(2).rstrip()
    
    # We want to insert ", HR Agrartechnik GmbH" after the holder.
    # The holder ends at last_match.end(2).
    
    new_description = description[:last_match.end(2)].rstrip() + ", HR Agrartechnik GmbH" + description[last_match.end(2):]
    
    new_content = content[:ident_match.start(2)] + new_description + content[ident_match.end(2):]
    
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)
    
    return True, description, new_description

updated_files = []
for root, dirs, files in os.walk(lib_dir):
    for file in files:
        if file.endswith(extensions):
            file_path = os.path.join(root, file)
            try:
                result = process_file(file_path)
                if result:
                    success, old_desc, new_desc = result
                    updated_files.append((file_path, old_desc, new_desc))
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

print(f"Total updated files: {len(updated_files)}")
for path, old, new in updated_files[:5]:
    # Extract just the first line of the description for the example
    old_first = old.split('&#10;')[0].strip()
    new_first = new.split('&#10;')[0].strip()
    print(f"File: {path}")
    print(f"  Old: {old_first}")
    print(f"  New: {new_first}")
