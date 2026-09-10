import os
import glob
import xml.etree.ElementTree as ET

ax_dir = r'C:\git\ms\4diac_training1\Ventilsteuerung\4diacIDE-workspace\test_AX\Uebungen'
files = sorted(glob.glob(os.path.join(ax_dir, '*.SUB')))

actual_violations = []

bad_types = {
    'isobus::UT::io::NumericValue::NumericValue_ID',
    'isobus::UT::io::NumericValue::NumericValue_PHYS',
    'isobus::UT::Q::Q_NumericValue',
    'isobus::UT::Q::Q_NumericValue_PHYS',
    'iec61131::arithmetic::ADD_2',
    'iec61131::arithmetic::SUB_2',
    'iec61131::arithmetic::MUL_2',
    'iec61131::arithmetic::DIV_2',
    'iec61131::arithmetic::F_MUL',
    'iec61131::arithmetic::F_DIV',
    'eclipse4diac::utils::FB_RANDOM',
    'iec61499::events::E_SR',
    'iec61499::events::E_D_FF',
    'iec61499::events::E_T_FF',
    'iec61499::events::E_PERMIT',
    'iec61499::events::E_SWITCH',
    'logiBUS::io::DI::logiBUS_IX',
    'logiBUS::io::DQ::logiBUS_QX',
    'iec61131::booleanOperators::AND_2',
    'iec61131::booleanOperators::OR_2',
    'iec61131::booleanOperators::XOR_2',
    'iec61131::booleanOperators::NOT',
    'iec61131::booleanOperators::NOT_BOOL',
}

for path in files:
    fname = os.path.basename(path)
    if fname == 'Uebung_002a4b_AX.SUB': # Known exception for negated connection test
        continue
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        net = root.find('SubAppNetwork')
        if net is None:
            continue
        
        fbs = net.findall('.//FB')
        bad_fbs = []
        for fb in fbs:
            fb_type = fb.attrib.get('Type', '')
            if fb_type in bad_types:
                bad_fbs.append((fb.attrib.get('Name'), fb_type))
            elif fb_type == 'eclipse4diac::signalprocessing::RampLimitFS':
                bad_fbs.append((fb.attrib.get('Name'), fb_type))
        
        if len(bad_fbs) > 0:
            actual_violations.append((fname, len(bad_fbs), bad_fbs))

    except Exception as e:
        print(f'Error parsing {fname}: {e}')

print(f'Total AX files scanned: {len(files)}')
print(f'Total AX files with actual non-adapter FBs needing porting: {len(actual_violations)}')
print('=' * 80)
for fname, n_bad, fbs in actual_violations:
    print(f'{fname:35s} | {n_bad} non-adapter FBs:')
    for fb_name, fb_type in fbs:
        print(f'    - {fb_name}: {fb_type}')
