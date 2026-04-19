import os
import xml.etree.ElementTree as ET
import re

FILES = [
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\timed\sequence_T_08_loop_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\schieber\SchieberControl_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\combi\sequence_ET_04_04_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\combi\sequence_ET_04_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\combi\sequence_ET_04_loop_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\combi\sequence_ET_05_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\combi\sequence_ET_05_loop_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\combi\sequence_ET_08_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\combi\sequence_ET_08_loop_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\event\sequence_E_04_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\event\sequence_E_04_loop_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\event\sequence_E_05_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\event\sequence_E_05_loop_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\event\sequence_E_08_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\event\sequence_E_08_loop_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\timed\sequence_T_04_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\timed\sequence_T_04_loop_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\timed\sequence_T_05_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\timed\sequence_T_05_loop_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\timed\sequence_T_08_AX.fbt",
    r"C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\.lib\logiBUS-3.0.0\typelib\utils\sequence\verteiler\LinksRechts_AX.fbt"
]

def check_fb(filepath):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        issues = []
        
        # Pattern: Algorithm="State_NN_E" should have Output="DO_SNN.E1"
        # Pattern: Algorithm="State_NN_X" should have Output="DO_SNN.E1"
        
        for state in root.findall(".//ECState"):
            state_name = state.get("Name")
            for action in state.findall("ECAction"):
                algo = action.get("Algorithm")
                output = action.get("Output")
                
                if algo:
                    # Match State_NN_E or State_NN_X
                    m = re.match(r"State_(\d+)_([EX])", algo)
                    if m:
                        num_str = m.group(1)
                        # Normalize number: 01 -> 1
                        num = str(int(num_str))
                        expected_output = f"DO_S{num}.E1"
                        
                        if output != expected_output:
                            issues.append(f"  [State {state_name}] Action Algorithm='{algo}' has Output='{output}', expected '{expected_output}'")
        
        if issues:
            print(f"Issues in {os.path.basename(filepath)}:")
            for issue in issues:
                print(issue)
            return True
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
    return False

def main():
    found_any = False
    for f in FILES:
        if check_fb(f):
            found_any = True
    if not found_any:
        print("No issues found in checked files.")

if __name__ == "__main__":
    main()
