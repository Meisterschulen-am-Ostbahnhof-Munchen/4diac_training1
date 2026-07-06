import os
import subprocess
import sys

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    templates_dir = os.path.abspath(os.path.join(script_dir, '..', 'templates'))
    validate_script = os.path.join(script_dir, 'validate.py')
    
    valid_ext = {'.fbt', '.adp', '.sub', '.dtp', '.atp', '.fct', '.gcf'}
    if not os.path.isdir(templates_dir):
        print(f"Error: Templates directory does not exist: {templates_dir}")
        sys.exit(1)
        
    files = sorted([f for f in os.listdir(templates_dir) if os.path.isfile(os.path.join(templates_dir, f)) and os.path.splitext(f)[1].lower() in valid_ext])
    
    if not files:
        print(f"Error: No templates found in {templates_dir}")
        sys.exit(1)
        
    all_success = True
    for file in files:
        full_path = os.path.join(templates_dir, file)
        print(f"--- Validating {file} ---")
        res = subprocess.run([sys.executable, validate_script, full_path], capture_output=True, text=True)
        if res.returncode == 0:
            print("SUCCESS")
        else:
            all_success = False
            print("FAILED")
            print(res.stdout)
            print(res.stderr)
            
    if not all_success:
        sys.exit(1)
    print("All templates validated successfully.")
    sys.exit(0)

if __name__ == '__main__':
    main()
