import xml.etree.ElementTree as ET
import drawsvg as draw

class FbtToProfessionalSvg:
    def __init__(self, fbt_path, output_path):
        self.fbt_path = fbt_path
        self.output_path = output_path
        
        # Design-System (Exakt auf Screenshot abgestimmt)
        self.cfg = {
            'font_family': 'Verdana, sans-serif',
            'font_mono': 'Consolas, monospace',
            'font_size_label': 12,
            'font_size_meta': 11,
            'row_h': 24,
            'header_h': 35,
            'neck_indent': 12,   # Einzug
            'pin_len_inner': 5,  # Kurzer Strich direkt am Block
            'track_width': 6,    # Abstand zwischen den vertikalen Linien
            'text_gap': 15,      # Abstand von Linien zum Text
            'colors': {
                'bg': '#f5f5f5',        # Heller Hintergrund
                'border': '#606060',    # Rahmen
                'event': '#5cb85c',     # Grün
                'data': '#0066cc',      # Blau
                'text': '#000000',
                'meta_type': '#0066cc', # Blau kursiv
                'meta_comm': '#404040', # Grau
                'conn_line': '#404040'  # Dunkelgrau für WITH-Linien
            }
        }

    def parse(self):
        tree = ET.parse(self.fbt_path)
        root = tree.getroot()
        
        self.block_name = root.get('Name', 'BLOCK')
        v_info = root.find('VersionInfo')
        self.version = v_info.get('Version', '1.0') if v_info is not None else ''

        interface = root.find('InterfaceList')
        
        def get_items(tag):
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
            'events': get_items('EventInputs'),
            'vars': get_items('InputVars')
        }
        self.outputs = {
            'events': get_items('EventOutputs'),
            'vars': get_items('OutputVars')
        }

    def layout(self):
        # 1. Grundhöhen
        rows_top = max(len(self.inputs['events']), len(self.outputs['events']))
        rows_bot = max(len(self.inputs['vars']), len(self.outputs['vars']))
        
        self.h_head = self.cfg['header_h'] + (rows_top * self.cfg['row_h']) + 8
        self.h_body = (rows_bot * self.cfg['row_h']) + 10
        self.h_total = self.h_head + self.h_body
        
        # 2. Blockbreite (Textabhängig)
        max_len = len(self.block_name) * 9
        # Wir schauen nur auf die inneren Labels
        for group in [self.inputs, self.outputs]:
            for k in ['events', 'vars']:
                for item in group[k]:
                    max_len = max(max_len, len(item['name']) * 9)
        self.w_block = max(110, max_len + 30)

        # 3. Y-Positionen berechnen
        self.y_map = {'in': {}, 'out': {}}
        
        def assign_y(items, start_y, mapping):
            y = start_y
            for item in items:
                item['y'] = y
                mapping[item['name']] = y
                y += self.cfg['row_h']
            return y

        # Inputs
        y = assign_y(self.inputs['events'], self.cfg['header_h'] + 12, self.y_map['in'])
        assign_y(self.inputs['vars'], self.h_head + 12, self.y_map['in'])
        
        # Outputs
        y = assign_y(self.outputs['events'], self.cfg['header_h'] + 12, self.y_map['out'])
        assign_y(self.outputs['vars'], self.h_head + 12, self.y_map['out'])

        # 4. TRACK CALCULATOR (Die Magie für die Linien)
        # Wir berechnen, wie viele "Spuren" wir links und rechts brauchen
        self.tracks_in = self._calculate_tracks(self.inputs['events'])
        self.tracks_out = self._calculate_tracks(self.outputs['events'])
        
        # Maximale Anzahl an Tracks bestimmt den Abstand zum Text
        self.max_tracks_in = max(self.tracks_in.values()) if self.tracks_in else 0
        self.max_tracks_out = max(self.tracks_out.values()) if self.tracks_out else 0

    def _calculate_tracks(self, events):
        """Weist jedem Event mit WITH-Verbindungen eine Spur-Nummer zu (0, 1, 2...)"""
        tracks = {}
        current_track = 0
        for item in events:
            if item['with']:
                tracks[item['name']] = current_track
                current_track += 1
        return tracks

    def draw(self):
        # Abstände berechnen basierend auf Anzahl der Linien
        padding_left = 20 + (self.max_tracks_in * self.cfg['track_width']) + 250
        padding_right = 20 + (self.max_tracks_out * self.cfg['track_width']) + 250
        
        w_canvas = self.w_block + padding_left + padding_right
        h_canvas = self.h_total + 40
        
        d = draw.Drawing(w_canvas, h_canvas, origin=(-padding_left, -20))
        
        # --- 1. Block Body ---
        x, y, w, h = 0, 0, self.w_block, self.h_total
        indent = self.cfg['neck_indent']
        neck_y = self.h_head
        
        # Shape
        path = draw.Path(fill=self.cfg['colors']['bg'], stroke=self.cfg['colors']['border'], stroke_width=2)
        path.M(x, y).H(x+w).V(neck_y).H(x+w-indent).V(h).H(x+indent).V(neck_y).H(x).Z()
        d.append(path)
        
        # Header Line
        d.append(draw.Line(x, self.cfg['header_h'], x+w, self.cfg['header_h'], stroke=self.cfg['colors']['border'], stroke_width=1))
        
        # Text im Block
        d.append(draw.Text(self.block_name, font_size=14, x=w/2, y=22, center=True, fontWeight='bold', font_family=self.cfg['font_family']))
        if self.version:
            d.append(draw.Text(self.version, font_size=11, x=w/2, y=self.cfg['header_h'] + 20, center=True, fill='#888', font_family=self.cfg['font_mono']))

        # --- 2. Pins & Metadaten ---
        self._draw_side(d, self.inputs, True, 0)
        self._draw_side(d, self.outputs, False, self.w_block)
        
        # --- 3. WITH Verbindungen (Lines) ---
        self._draw_connections(d, self.inputs, True, 0)
        self._draw_connections(d, self.outputs, False, self.w_block)

        d.save_svg(self.output_path)
        print(f"SVG gespeichert: {self.output_path}")

    def _draw_side(self, d, group, is_input, x_block_edge):
        """Zeichnet Pins und Texte für eine Seite"""
        indent = self.cfg['neck_indent']
        
        # Wo fängt der Text an? (Abhängig von Tracks)
        track_count = self.max_tracks_in if is_input else self.max_tracks_out
        extra_space = (track_count * self.cfg['track_width']) + self.cfg['text_gap']
        
        for kind in ['events', 'vars']:
            is_event = (kind == 'events')
            color = self.cfg['colors']['event'] if is_event else self.cfg['colors']['data']
            
            # X-Korrektur für Einzug (Neck)
            if not is_event:
                pin_root = x_block_edge + indent if is_input else x_block_edge - indent
            else:
                pin_root = x_block_edge
            
            for item in group[kind]:
                y = item['y']
                
                # 1. Kleiner Pin am Block
                pin_end = pin_root - 5 if is_input else pin_root + 5
                d.append(draw.Line(pin_root, y, pin_end, y, stroke=color, stroke_width=2))
                
                # Quadrat am Pin-Start
                sq_x = pin_root - 5 if is_input else pin_root
                d.append(draw.Rectangle(sq_x, y - 2.5, 5, 5, fill=color))
                
                # 2. Label INNERHALB des Blocks
                lbl_x = pin_root + 8 if is_input else pin_root - 8
                lbl_anchor = 'start' if is_input else 'end'
                d.append(draw.Text(item['name'], font_size=self.cfg['font_size_label'], 
                                   x=lbl_x, y=y+4, text_anchor=lbl_anchor, font_family=self.cfg['font_mono']))
                
                # 3. Metadaten AUSSERHALB (Type, Comment)
                # Position: Pin-Ende + Platz für Linien
                meta_x = (pin_root - extra_space) if is_input else (pin_root + extra_space)
                meta_anchor = 'end' if is_input else 'start'
                
                # Typ
                type_txt = "Event" if is_event else item['type']
                type_col = '#666' if is_event else self.cfg['colors']['meta_type']
                d.append(draw.Text(type_txt, font_size=self.cfg['font_size_meta'], 
                                   x=meta_x, y=y+3, text_anchor=meta_anchor, 
                                   fill=type_col, font_style='italic', font_family=self.cfg['font_family']))
                
                # Kommentar (weiter außen)
                if item['comment']:
                    comm_x = meta_x - 70 if is_input else meta_x + 70
                    d.append(draw.Text(item['comment'], font_size=self.cfg['font_size_meta'], 
                                       x=comm_x, y=y+3, text_anchor=meta_anchor, 
                                       fill=self.cfg['colors']['meta_comm'], font_family=self.cfg['font_family']))
                
                # Verbindungslinie vom Pin zum Text (nur wenn keine WITH linie dazwischen kommt, optisch nett)
                # Hier lassen wir es erstmal sauber leer wie im Screenshot

    def _draw_connections(self, d, group, is_input, x_edge):
        """Zeichnet die komplexen WITH-Linien in Tracks"""
        mapping = self.y_map['in'] if is_input else self.y_map['out']
        track_map = self.tracks_in if is_input else self.tracks_out
        
        indent = self.cfg['neck_indent']
        
        for item in group['events']:
            if not item['with']: continue
            
            # Welchen Track hat dieses Event?
            track_idx = track_map.get(item['name'], 0)
            
            # X-Position der vertikalen Linie berechnen
            # Wir fangen nah am Block an und gehen nach außen
            offset = 10 + (track_idx * self.cfg['track_width'])
            
            if is_input:
                line_x = x_edge - offset
                pin_x = x_edge # Event pin root
            else:
                line_x = x_edge + offset
                pin_x = x_edge
            
            y_event = item['y']
            
            # Alle verknüpften Variablen finden
            target_ys = [y_event]
            valid_targets = []
            
            for var_name in item['with']:
                if var_name in mapping:
                    y_var = mapping[var_name]
                    target_ys.append(y_var)
                    valid_targets.append(y_var)
            
            min_y, max_y = min(target_ys), max(target_ys)
            
            # 1. Vertikale Linie (Solid!)
            d.append(draw.Line(line_x, min_y, line_x, max_y, 
                               stroke=self.cfg['colors']['conn_line'], stroke_width=1))
            
            # 2. Horizontaler Connector vom Event zur Linie
            d.append(draw.Line(pin_x, y_event, line_x, y_event, stroke=self.cfg['colors']['conn_line'], stroke_width=1))
            
            # Kleines Quadrat am Kreuzungspunkt Event/Linie
            d.append(draw.Rectangle(line_x - 2, y_event - 2, 4, 4, fill='white', stroke=self.cfg['colors']['conn_line'], stroke_width=1))

            # 3. Horizontale Connectors zu den Variablen
            for y_var in valid_targets:
                # Wo startet die Variable? (Achtung Neck indent)
                if is_input:
                    var_pin_x = x_edge + indent
                    # Linie muss von links (line_x) nach rechts (var_pin_x)
                    d.append(draw.Line(line_x, y_var, var_pin_x - 5, y_var, stroke=self.cfg['colors']['conn_line'], stroke_width=1))
                else:
                    var_pin_x = x_edge - indent
                    # Linie von rechts (line_x) nach links (var_pin_x)
                    d.append(draw.Line(var_pin_x + 5, y_var, line_x, y_var, stroke=self.cfg['colors']['conn_line'], stroke_width=1))
                
                # Kleines Quadrat am Kreuzungspunkt Variable/Linie
                d.append(draw.Rectangle(line_x - 2, y_var - 2, 4, 4, fill='white', stroke=self.cfg['colors']['conn_line'], stroke_width=1))


# --- Ausführung ---
if __name__ == "__main__":
    converter = FbtToProfessionalSvg("E_CTUD.fbt", "E_CTUD_PixelPerfect.svg")
    converter.parse()
    converter.layout()
    converter.draw()