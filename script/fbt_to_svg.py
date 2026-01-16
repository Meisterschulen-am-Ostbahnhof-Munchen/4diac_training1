import xml.etree.ElementTree as ET
import drawsvg as draw

class FbtToSvgConverter:
    def __init__(self, fbt_path, output_path):
        self.fbt_path = fbt_path
        self.output_path = output_path
        
        # Design-Konfiguration (Angepasst an IEC 61499 Standard)
        self.cfg = {
            'font_family': 'Verdana, sans-serif',
            'font_mono': 'Consolas, monospace',
            'font_size_label': 12,
            'font_size_meta': 10,
            'row_h': 24,         # Zeilenhöhe
            'header_h': 35,      # Höhe Header
            'neck_indent': 12,   # Einzug für den Datenbereich
            'pin_len': 15,       # Länge der Pins
            'colors': {
                'bg': '#f2f2f2',
                'border': '#505050',
                'event': '#5cb85c', # Grün
                'data': '#0275d8',  # Blau
                'text': '#000000',
                'meta': '#666666',  # Kommentare/Typen
                'line': '#000000'   # Verbindungslinien
            }
        }

    def parse(self):
        """Liest XML und extrahiert Struktur + Metadaten"""
        tree = ET.parse(self.fbt_path)
        root = tree.getroot()
        
        self.block_name = root.get('Name', 'BLOCK')
        
        # Version auslesen (Nimmt die erste gefundene)
        v_info = root.find('VersionInfo')
        self.version = v_info.get('Version', '1.0') if v_info is not None else ''

        interface = root.find('InterfaceList')
        
        def parse_items(tag):
            items = []
            section = interface.find(tag)
            if section is not None:
                for child in section:
                    items.append({
                        'name': child.get('Name'),
                        'type': child.get('Type', 'Event'),
                        'comment': child.get('Comment', ''),
                        'with': [w.get('Var') for w in child.findall('With')]
                    })
            return items

        self.inputs = {
            'events': parse_items('EventInputs'),
            'vars': parse_items('InputVars')
        }
        self.outputs = {
            'events': parse_items('EventOutputs'),
            'vars': parse_items('OutputVars')
        }

    def layout(self):
        """Berechnet Positionen VOR dem Zeichnen"""
        # Anzahl Zeilen bestimmen
        rows_top = max(len(self.inputs['events']), len(self.outputs['events']))
        rows_bot = max(len(self.inputs['vars']), len(self.outputs['vars']))
        
        # Höhen
        self.h_head = self.cfg['header_h'] + (rows_top * self.cfg['row_h']) + 5
        self.h_body = (rows_bot * self.cfg['row_h']) + 10
        self.h_total = self.h_head + self.h_body
        
        # Breite basierend auf Textlänge im Block
        max_len = len(self.block_name) * 9
        for group in [self.inputs, self.outputs]:
            for kind in ['events', 'vars']:
                for item in group[kind]:
                    max_len = max(max_len, len(item['name']) * 10)
        
        self.w_block = max(110, max_len + 40)
        
        # Y-Positionen speichern (Wichtig für WITH-Linien)
        self.y_map = {'in': {}, 'out': {}}
        
        current_y = self.cfg['header_h'] + 12
        for item in self.inputs['events']:
            self.y_map['in'][item['name']] = current_y
            item['y'] = current_y
            current_y += self.cfg['row_h']
            
        current_y = self.h_head + 12 # Reset für Variablen-Teil
        for item in self.inputs['vars']:
            self.y_map['in'][item['name']] = current_y
            item['y'] = current_y
            current_y += self.cfg['row_h']
            
        # Gleiches für Outputs
        current_y = self.cfg['header_h'] + 12
        for item in self.outputs['events']:
            self.y_map['out'][item['name']] = current_y
            item['y'] = current_y
            current_y += self.cfg['row_h']
            
        current_y = self.h_head + 12
        for item in self.outputs['vars']:
            self.y_map['out'][item['name']] = current_y
            item['y'] = current_y
            current_y += self.cfg['row_h']

    def draw(self):
        # Canvas Setup (Breit genug für Texte links/rechts)
        w_canvas = self.w_block + 600
        d = draw.Drawing(w_canvas, self.h_total + 40, origin=(-300, -20))
        
        # 1. Hauptform (Pfad für IEC 61499 Shape)
        x, y, w, h = 0, 0, self.w_block, self.h_total
        indent = self.cfg['neck_indent']
        neck_y = self.h_head
        
        path = draw.Path(fill=self.cfg['colors']['bg'], stroke=self.cfg['colors']['border'], stroke_width=2)
        path.M(x, y).H(x+w).V(neck_y).H(x+w-indent).V(h).H(x+indent).V(neck_y).H(x).Z()
        d.append(path)
        
        # Header Linie
        d.append(draw.Line(x, self.cfg['header_h'], x+w, self.cfg['header_h'], stroke=self.cfg['colors']['border'], stroke_width=1))
        
        # Name & Version
        d.append(draw.Text(self.block_name, font_size=14, x=w/2, y=22, center=True, fontWeight='bold', font_family=self.cfg['font_family']))
        if self.version:
            d.append(draw.Text(self.version, font_size=10, x=w/2, y=self.cfg['header_h'] + 15, center=True, fill='#888', font_family=self.cfg['font_mono']))

        # 2. Pins & Labels
        def draw_pins(group, is_input):
            side_x = 0 if is_input else w
            text_anchor = 'start' if is_input else 'end'
            
            for kind in ['events', 'vars']:
                is_event = (kind == 'events')
                color = self.cfg['colors']['event'] if is_event else self.cfg['colors']['data']
                
                # Korrektur für "Neck" Einzug
                if not is_event:
                    pin_root_x = indent if is_input else w - indent
                else:
                    pin_root_x = 0 if is_input else w
                
                for item in group[kind]:
                    y_pos = item['y']
                    
                    # Pin Linie
                    pin_end_x = pin_root_x - self.cfg['pin_len'] if is_input else pin_root_x + self.cfg['pin_len']
                    d.append(draw.Line(pin_root_x, y_pos, pin_end_x, y_pos, stroke=color, stroke_width=2))
                    
                    # Kleines Quadrat am Block
                    sq_x = pin_root_x - 5 if is_input else pin_root_x
                    d.append(draw.Rectangle(sq_x, y_pos - 2.5, 5, 5, fill=color))
                    
                    # Label im Block
                    label_x = pin_root_x + 8 if is_input else pin_root_x - 8
                    d.append(draw.Text(item['name'], font_size=self.cfg['font_size_label'], x=label_x, y=y_pos + 4, 
                                       text_anchor=text_anchor, font_family=self.cfg['font_mono']))
                    
                    # Externe Infos (Typ, Kommentar)
                    meta_x = pin_end_x - 10 if is_input else pin_end_x + 10
                    meta_anchor = 'end' if is_input else 'start'
                    
                    # Typ anzeigen (außer bei Events)
                    if not is_event:
                         d.append(draw.Text(item['type'], font_size=10, x=meta_x, y=y_pos + 3, 
                                           text_anchor=meta_anchor, fill=self.cfg['colors']['data'], font_style='italic', font_family=self.cfg['font_family']))
                    else:
                         d.append(draw.Text("Event", font_size=10, x=meta_x, y=y_pos + 3, 
                                           text_anchor=meta_anchor, fill='#999', font_style='italic', font_family=self.cfg['font_family']))

                    # Kommentar
                    if item['comment']:
                        comm_x = meta_x - 60 if is_input else meta_x + 60
                        d.append(draw.Text(item['comment'], font_size=10, x=comm_x, y=y_pos + 3, 
                                           text_anchor=meta_anchor, fill=self.cfg['colors']['meta'], font_family=self.cfg['font_family']))

        draw_pins(self.inputs, True)
        draw_pins(self.outputs, False)

        # 3. WITH Verbindungen zeichnen
        def draw_with(group, is_input):
            # Vertikale Linie X-Position
            base_x = -20 if is_input else self.w_block + 20
            
            for item in group['events']:
                if not item['with']: continue
                
                event_y = item['y']
                # Finde min und max Y für die Linie
                target_ys = [event_y]
                
                # Wir suchen die Y-Pos der verknüpften Variablen
                mapping = self.y_map['in'] if is_input else self.y_map['out']
                
                for var_name in item['with']:
                    if var_name in mapping:
                        var_y = mapping[var_name]
                        target_ys.append(var_y)
                        # Horizontaler Connector zur Variable
                        d.append(draw.Circle(base_x, var_y, 2, fill='black'))
                
                min_y, max_y = min(target_ys), max(target_ys)
                
                # Vertikale Linie
                d.append(draw.Line(base_x, min_y, base_x, max_y, stroke='black', stroke_width=1, stroke_dasharray='3,3'))
                # Connector zum Event
                d.append(draw.Circle(base_x, event_y, 2, fill='black'))
                d.append(draw.Line(base_x, event_y, base_x + (5 if is_input else -5), event_y, stroke='black', stroke_width=1))

        draw_with(self.inputs, True)
        draw_with(self.outputs, False)

        d.save_svg(self.output_path)
        print(f"SVG gespeichert: {self.output_path}")

import sys
import os

# --- Hauptprogramm ---
if __name__ == "__main__":
    # Datei aus Argumenten oder Default
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "E_CTUD.fbt"

    if not os.path.exists(input_file):
        print(f"Fehler: Datei '{input_file}' nicht gefunden.")
        sys.exit(1)

    # Output Dateiname ableiten
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}.svg"

    converter = FbtToSvgConverter(input_file, output_file)
    converter.parse()
    converter.layout()
    converter.draw()