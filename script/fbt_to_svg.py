import xml.etree.ElementTree as ET
import drawsvg as draw

class PerfectShapeFbtRenderer:
    def __init__(self, fbt_path, output_path):
        self.fbt_path = fbt_path
        self.output_path = output_path
        
        # Design-System
        self.cfg = {
            'font_family': 'Verdana, sans-serif',
            'font_mono': 'Consolas, monospace',
            'font_size_label': 12,
            'font_size_meta': 11,
            'row_h': 24,            
            'header_h': 35,         
            'neck_indent': 6,       # Wie tief die Kerbe ist (dezent)
            'neck_height': 8,       # Wie hoch die Kerbe ist
            'track_width': 8,       # Platz pro WITH-Linie
            'colors': {
                'bg': '#f2f2f2',
                'border': '#404040',
                'event_pin': '#5cb85c',
                'data_pin': '#0066cc',
                'text': '#000000',
                'meta_type': '#0066cc',
                'meta_comm': '#666666',
                'line': '#404040'
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
            sec = interface.find(tag)
            if sec is not None:
                for child in sec:
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
        # 1. Zeilenhöhen bestimmen
        n_ev_in, n_ev_out = len(self.inputs['events']), len(self.outputs['events'])
        n_var_in, n_var_out = len(self.inputs['vars']), len(self.outputs['vars'])
        
        rows_head = max(n_ev_in, n_ev_out)
        rows_body = max(n_var_in, n_var_out)
        
        # 2. Vertikale Struktur berechnen
        # Head Ende
        self.y_head_end = self.cfg['header_h'] + (rows_head * self.cfg['row_h']) + 10
        
        # Neck Bereich (Start und Ende der Einkerbung)
        self.y_neck_start = self.y_head_end
        self.y_neck_end = self.y_neck_start + self.cfg['neck_height']
        
        # Body Start (Variablen)
        self.y_body_start = self.y_neck_end + 5 # Kleiner Puffer nach der Kerbe
        
        # Gesamt Höhe
        self.h_total = self.y_body_start + (rows_body * self.cfg['row_h']) + 10
        
        # 3. Breite berechnen
        max_txt = len(self.block_name) * 10
        for grp in [self.inputs, self.outputs]:
            for kind in ['events', 'vars']:
                for it in grp[kind]:
                    max_txt = max(max_txt, len(it['name']) * 9)
        self.w_block = max(120, max_txt + 40)

        # 4. Y-Positionen der Items setzen
        self.y_map = {'in': {}, 'out': {}}
        
        def set_y(items, start_y, mapping):
            y = start_y
            for item in items:
                item['y'] = y
                mapping[item['name']] = y
                y += self.cfg['row_h']
        
        # Events (Oben)
        evt_start = self.cfg['header_h'] + 12
        set_y(self.inputs['events'], evt_start, self.y_map['in'])
        set_y(self.outputs['events'], evt_start, self.y_map['out'])
        
        # Variablen (Unten, nach der Kerbe)
        var_start = self.y_body_start + 12
        set_y(self.inputs['vars'], var_start, self.y_map['in'])
        set_y(self.outputs['vars'], var_start, self.y_map['out'])

        # 5. Tracks für Linien berechnen
        self.tracks_in = self._calc_tracks(self.inputs['events'])
        self.tracks_out = self._calc_tracks(self.outputs['events'])
        
        self.max_tracks_in = max(self.tracks_in.values()) if self.tracks_in else -1
        self.max_tracks_out = max(self.tracks_out.values()) if self.tracks_out else -1

    def _calc_tracks(self, events):
        tracks = {}
        curr = 0
        for ev in events:
            if ev['with']:
                tracks[ev['name']] = curr
                curr += 1
        return tracks

    def draw_triangle_right(self, d, tip_x, y, color):
        """Zeichnet ein Dreieck das nach rechts zeigt |>"""
        size = 5
        points = [
            tip_x - size, y - size, # Oben Links
            tip_x - size, y + size, # Unten Links
            tip_x, y                # Spitze Rechts
        ]
        d.append(draw.Lines(*points, close=True, fill=color, stroke='none'))

    def draw(self):
        # Canvas Setup
        pad_l = 40 + ((self.max_tracks_in + 1) * self.cfg['track_width']) + 250
        pad_r = 40 + ((self.max_tracks_out + 1) * self.cfg['track_width']) + 250
        
        d = draw.Drawing(self.w_block + pad_l + pad_r, self.h_total + 50, origin=(-pad_l, -20))
        
        # --- 1. Der Block (Die Form: Eingekerbtes Rechteck) ---
        x, y, w, h = 0, 0, self.w_block, self.h_total
        neck_y1 = self.y_neck_start
        neck_y2 = self.y_neck_end
        ind = self.cfg['neck_indent']
        
        # Pfad Definition
        p = draw.Path(fill=self.cfg['colors']['bg'], stroke=self.cfg['colors']['border'], stroke_width=2)
        p.M(x, y)               # 0,0 Start
        p.H(x + w)              # Oben rechts
        p.V(neck_y1)            # Runter bis Hals-Start
        p.H(x + w - ind)        # REIN (Rechts)
        p.V(neck_y2)            # Runter im Hals
        p.H(x + w)              # RAUS (Rechts)
        p.V(h)                  # Runter zum Boden
        p.H(x)                  # Boden nach links
        p.V(neck_y2)            # Hoch bis Hals-Ende
        p.H(x + ind)            # REIN (Links)
        p.V(neck_y1)            # Hoch im Hals
        p.H(x)                  # RAUS (Links)
        p.Z()                   # Schließen
        d.append(p)
        
        # Header Trennlinie
        d.append(draw.Line(x, self.cfg['header_h'], x+w, self.cfg['header_h'], 
                           stroke=self.cfg['colors']['border'], stroke_width=1))
        
        # Block Text
        d.append(draw.Text(self.block_name, font_size=14, x=w/2, y=25, center=True, 
                           fontWeight='bold', font_family=self.cfg['font_family']))
        if self.version:
            d.append(draw.Text(self.version, font_size=10, x=w/2, y=self.cfg['header_h']+20, 
                           center=True, fill='#999', font_family=self.cfg['font_mono']))

        # --- 2. Pins & Labels ---
        # Jetzt sitzen BEIDE Gruppen (Events und Vars) an der Außenkante (x=0 oder x=w)
        # Der Hals ist nur Deko dazwischen.
        self._draw_side(d, self.inputs, True, 0)
        self._draw_side(d, self.outputs, False, self.w_block)
        
        # --- 3. WITH Linien ---
        self._draw_conns(d, self.inputs, True, 0)
        self._draw_conns(d, self.outputs, False, self.w_block)

        d.save_svg(self.output_path)
        print(f"Generiert: {self.output_path}")

    def _draw_side(self, d, group, is_input, x_edge):
        # Text Offset
        track_cnt = self.max_tracks_in if is_input else self.max_tracks_out
        txt_offset = ((track_cnt + 1) * self.cfg['track_width']) + 15
        
        for kind in ['events', 'vars']:
            is_evt = (kind == 'events')
            color = self.cfg['colors']['event_pin'] if is_evt else self.cfg['colors']['data_pin']
            
            # Alle Pins sitzen an der Kante x_edge
            pin_x = x_edge
            
            for item in group[kind]:
                y = item['y']
                
                # A. DREIECKE
                if is_input:
                    self.draw_triangle_right(d, pin_x, y, color)
                    # Label
                    d.append(draw.Text(item['name'], font_size=12, x=pin_x + 8, y=y+4, 
                                       text_anchor='start', font_family=self.cfg['font_mono']))
                else:
                    self.draw_triangle_right(d, pin_x + 5, y, color)
                    # Label
                    d.append(draw.Text(item['name'], font_size=12, x=pin_x - 8, y=y+4, 
                                       text_anchor='end', font_family=self.cfg['font_mono']))

                # B. METADATEN
                if is_input:
                    meta_x = pin_x - txt_offset
                    anchor = 'end'
                else:
                    meta_x = pin_x + txt_offset
                    anchor = 'start'
                
                t_col = '#888' if is_evt else self.cfg['colors']['meta_type']
                t_txt = 'Event' if is_evt else item['type']
                d.append(draw.Text(t_txt, font_size=11, x=meta_x, y=y+3, 
                                   text_anchor=anchor, fill=t_col, font_style='italic', font_family=self.cfg['font_family']))
                
                if item['comment']:
                    comm_x = meta_x - 70 if is_input else meta_x + 70
                    d.append(draw.Text(item['comment'], font_size=11, x=comm_x, y=y+3,
                                       text_anchor=anchor, fill=self.cfg['colors']['meta_comm'], font_family=self.cfg['font_family']))

    def _draw_conns(self, d, group, is_input, x_edge):
        tracks = self.tracks_in if is_input else self.tracks_out
        y_map = self.y_map['in'] if is_input else self.y_map['out']
        
        for item in group['events']:
            if not item['with']: continue
            
            t_idx = tracks.get(item['name'], 0)
            offset = 12 + (t_idx * self.cfg['track_width'])
            
            if is_input:
                line_x = x_edge - offset
                pin_x = x_edge
            else:
                line_x = x_edge + offset
                pin_x = x_edge
            
            y_evt = item['y']
            
            # Ziele finden
            t_ys = [y_evt]
            valid_vars = []
            for v in item['with']:
                if v in y_map:
                    y_v = y_map[v]
                    t_ys.append(y_v)
                    valid_vars.append(y_v)
            
            # 1. Vertikale Linie
            d.append(draw.Line(line_x, min(t_ys), line_x, max(t_ys), 
                               stroke=self.cfg['colors']['line'], stroke_width=1))
            
            # 2. Connector Event
            d.append(draw.Line(pin_x, y_evt, line_x, y_evt, stroke=self.cfg['colors']['line']))
            d.append(draw.Rectangle(line_x-2, y_evt-2, 4, 4, fill='white', stroke='black', stroke_width=1))
            
            # 3. Connectors Vars
            for y_v in valid_vars:
                # Jetzt sind die Variablen NICHT mehr eingezogen. 
                # Die Linie geht also direkt von der Vertical Line zur Edge.
                if is_input:
                    d.append(draw.Line(line_x, y_v, x_edge - 5, y_v, stroke=self.cfg['colors']['line']))
                else:
                    d.append(draw.Line(x_edge + 5, y_v, line_x, y_v, stroke=self.cfg['colors']['line']))
                
                d.append(draw.Rectangle(line_x-2, y_v-2, 4, 4, fill='white', stroke='black', stroke_width=1))

if __name__ == "__main__":
    r = PerfectShapeFbtRenderer("E_CTUD.fbt", "E_CTUD_Notched.svg")
    r.parse()
    r.layout()
    r.draw()