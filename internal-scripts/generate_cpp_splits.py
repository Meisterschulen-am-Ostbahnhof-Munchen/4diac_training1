import os
import xml.etree.ElementTree as ET

# Paths
base_types_dir = "Ventilsteuerung/4diacIDE-workspace/.lib/adapter-3.0.0/typelib/types/unidirectional"
src_out_dir = "adapter/src/adapter/events/unidirectional"
inc_out_dir = "adapter/include/forte/adapter/events/unidirectional"

# Ensure output dirs exist
os.makedirs(src_out_dir, exist_ok=True)
os.makedirs(inc_out_dir, exist_ok=True)

# Main Class Header Template
main_h_template = """/*************************************************************************
 *** FORTE Library Element
 ***
 *** Name: GEN_{adapter_name}_SPLIT
 *** Description: SPLIT 1 {adapter_name} into N {adapter_name} (generic FB)
 *** Version:
 ***     1.1: 2025-01-24/Franz Höpfinger - HR Agrartechnik GmbH - Refactored to Template Base
 *************************************************************************/

#pragma once

#include "genunidirectsplitbase.h"
#include "forte/adapter/types/unidirectional/{adapter_name}_adp.h"

namespace forte::adapter::events::unidirectional {{
  class GEN_{adapter_name}_SPLIT : public CGenUnidirectSplitBase<forte::adapter::types::unidirectional::FORTE_{adapter_name}_Plug, forte::adapter::types::unidirectional::FORTE_{adapter_name}_Socket> {{
      DECLARE_GENERIC_FIRMWARE_FB(GEN_{adapter_name}_SPLIT)

    private:
      void executeEvent(TEventID paEIID, CEventChainExecutionThread *const paECET) override;

    public:
      GEN_{adapter_name}_SPLIT(StringId paInstanceNameId, CFBContainer &paContainer) : 
        CGenUnidirectSplitBase(paInstanceNameId, paContainer) {{ }}
  }};
}} // namespace forte::adapter::events::unidirectional
"""

# Main Class CPP Template
main_cpp_template = """/*************************************************************************
 *** FORTE Library Element
 ***
 *** Name: GEN_{adapter_name}_SPLIT
 *** Description: SPLIT 1 {adapter_name} into N {adapter_name} (generic FB)
 *** Version:
 ***     1.1: 2025-01-24/Franz Höpfinger - HR Agrartechnik GmbH - Refactored to Template Base
 *************************************************************************/

#include "forte/adapter/events/unidirectional/GEN_{adapter_name}_SPLIT_fbt.h"

using namespace forte::literals;

namespace forte::adapter::events::unidirectional {{
  DEFINE_GENERIC_FIRMWARE_FB(GEN_{adapter_name}_SPLIT, "adapter::events::unidirectional::GEN_{adapter_name}_SPLIT"_STRID)

  void GEN_{adapter_name}_SPLIT::executeEvent(TEventID paEIID, CEventChainExecutionThread *const paECET) {{
{execute_event_body}
  }}
}} // namespace forte::adapter::events::unidirectional
"""

# Logic to parse ADP
def parse_adp(path):
    tree = ET.parse(path)
    root = tree.getroot()
    name = root.attrib['Name']
    events = []
    for event in root.findall(".//EventOutputs/Event"):
        e_name = event.attrib['Name']
        vars = []
        for w in event.findall("With"):
            vars.append(w.attrib['Var'])
        events.append((e_name, vars))
    return name, events

# Logic to generate executeEvent body
def generate_execute_event_body(adapter_name, events):
    body = ""
    for e_name, vars in events:
        body += '    // Ein Event kann nur vom Eingangs-Socket "IN" kommen\n'
        body += f'    if (var_IN->evt_{e_name}() == paEIID) {{\n'
        for v in vars:
            body += f'      const auto &in_val_{v} = var_IN->var_{v};\n'
        body += '      const size_t numPlugs = getFBInterfaceSpec().getNumPlugs();\n\n'
        body += '      for (size_t i = 0; i < numPlugs; ++i) {\n'
        for v in vars:
            body += f'        var_OUT(i)->var_{v} = in_val_{v};\n'
        body += f'        sendAdapterEvent(*var_OUT(i), forte::adapter::types::unidirectional::FORTE_{adapter_name}::scmEvent{e_name}ID, paECET);\n'
        body += '      }\n'
        body += '    }\n'
    return body

# Main loop
generated_adapters = []
for root_dir, dirs, files in os.walk(base_types_dir):
    for file in files:
        if file.endswith(".adp"):
            path = os.path.join(root_dir, file)
            adapter_name, events = parse_adp(path)
            adapter_name_lower = adapter_name.lower()
            generated_adapters.append(adapter_name)
            
            # Generate content
            main_h = main_h_template.format(adapter_name=adapter_name)
            exec_body = generate_execute_event_body(adapter_name, events)
            main_cpp = main_cpp_template.format(adapter_name=adapter_name, execute_event_body=exec_body)
            
            # Write Main files
            with open(os.path.join(inc_out_dir, f"GEN_{adapter_name}_SPLIT_fbt.h"), "w", encoding="utf-8") as f:
                f.write(main_h)
            with open(os.path.join(src_out_dir, f"GEN_{adapter_name}_SPLIT_fbt.cpp"), "w", encoding="utf-8") as f:
                f.write(main_cpp)
            
            # Cleanup old base files if they exist
            base_h_old = os.path.join(inc_out_dir, f"gen{adapter_name_lower}splitbase_fbt.h")
            base_cpp_old = os.path.join(src_out_dir, f"gen{adapter_name_lower}splitbase_fbt.cpp")
            if os.path.exists(base_h_old): os.remove(base_h_old)
            if os.path.exists(base_cpp_old): os.remove(base_cpp_old)
            
            print(f"Refactored files for {adapter_name}")

print("Done.")
