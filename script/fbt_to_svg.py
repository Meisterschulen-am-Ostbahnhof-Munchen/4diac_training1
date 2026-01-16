import xml.etree.ElementTree as ET
import drawsvg as draw

class UniversalFbtRenderer:
    def __init__(self, fbt_path, output_path):
        self.fbt_path = fbt_path
        self.output_path = output_path
        
        # Design-System
        self.cfg = {
            'font_family': 'Verdana, sans-serif',
            'font_mono': 'Consolas, monospace',
            'font_size_label': 12,
            'font_size_meta': 11,
            'font_size_title': 14,
            'row_h': 24,            
            'header_h': 30,         
            'neck_indent': 6,       
            'neck_height': 40,      
            'track_width': 8,       
            'colors': {
                'bg': '#ffffff',        # Weißer Hintergrund (wie im neuen Screenshot)
                'border': '#808080',    # Etwas weicherer Rahmen
                'event_pin': '#5cb85c', # Grün
                'data_pin': '#0066cc',  # Blau
                'adapter_pin': '#884488', # Lila (Adapter)
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
        
        def get_items(tag, kind_label):
            items = []
            sec = interface.find(tag)
            if sec is not None:
                for child in sec:
                    # Typ-Handling: Adapter haben den Typ oft im 'Type'-Attribut, 
                    # aber manchmal muss man Namespaces entfernen (z.B. adapter::types::AX -> AX)
                    raw_type = child.get('Type', '')
                    display_type = raw_type.split('::')[-1] # Nimmt nur den letzten Teil

                    items.append({
                        'name': child.get('Name'),
                        'type': display_type,
                        'kind': kind_label, # 'event', 'var', 'adapter'
                        'comment': child.get('Comment', ''),
                        'with': [w.get('Var') for w in child.findall('With')]
                    })
            return items

        # INPUTS (Links)
        # Sockets (Adapter) landen üblicherweise links
        self.inputs = {
            'events': get_items('EventInputs', 'event'),
            'adapters': get_items('Sockets', 'adapter'),
            'vars': get_items('InputVars', 'var')
        }
        
        # OUTPUTS (Rechts)
        # Plugs (Adapter) landen üblicherweise rechts
        self.outputs = {
            'events': get_items('EventOutputs', 'event'),
            'adapters': get_items('Plugs', 'adapter'),
            'vars': get_items('OutputVars', 'var')
        }

    def layout(self):
        # 1. Zeilenhöhen bestimmen
        # Head: Nur Events
        n_ev_in, n_ev_out = len(self.inputs['events']), len(self.outputs['events'])
        rows_head = max(n_ev_in, n_ev_out)
        
        # Body: Adapter + Vars
        # Wir stapeln Adapter ZUERST, dann Variablen (Standard 4diac Layout)
        n_body_in = len(self.inputs['adapters']) + len(self.inputs['vars'])
        n_body_out = len(self.outputs['adapters']) + len(self.outputs['vars'])
        rows_body = max(n_body_in, n_body_out)
        
        # 2. Vertikale Struktur
        self.y_head_end = self.cfg['header_h'] + (rows_head * self.cfg['row_h']) + (10 if rows_head > 0 else 0)
        
        # Neck
        self.y_neck_start = self.y_head_end
        self.y_neck_end = self.y_neck_start + self.cfg['neck_height']
        
        # Body Start
        self.y_body_start = self.y_neck_end + 5 
        
        # Gesamt Höhe
        self.h_total = self.y_body_start + (rows_body * self.cfg['row_h']) + 10
        
        # 3. Breite berechnen
        max_txt = len(self.block_name) * 10
        for grp in [self.inputs, self.outputs]:
            for kind in ['events', 'adapters', 'vars']:
                for it in grp[kind]:
                    max_txt = max(max_txt, len(it['name']) * 9)
        self.w_block = max(130, max_txt + 40)

        # 4. Y-Positionen setzen
        self.y_map = {'in': {}, 'out': {}}
        
        def set_y(items, start_y, mapping):
            y = start_y
            for item in items:
                item['y'] = y
                mapping[item['name']] = y
                y += self.cfg['row_h']
            return y
        
        # Events (Oben)
        evt_start = self.cfg['header_h'] + 12
        set_y(self.inputs['events'], evt_start, self.y_map['in'])
        set_y(self.outputs['events'], evt_start, self.y_map['out'])
        
        # Body (Adapter zuerst, dann Variablen)
        body_curr_in = self.y_body_start + 12
        body_curr_in = set_y(self.inputs['adapters'], body_curr_in, self.y_map['in'])
        set_y(self.inputs['vars'], body_curr_in, self.y_map['in'])
        
        body_curr_out = self.y_body_start + 12
        body_curr_out = set_y(self.outputs['adapters'], body_curr_out, self.y_map['out'])
        set_y(self.outputs['vars'], body_curr_out, self.y_map['out'])

        # 5. Tracks (Nur Events haben WITH)
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
        size = 5
        points = [tip_x - size, y - size, tip_x - size, y + size, tip_x, y]
        d.append(draw.Lines(*points, close=True, fill=color, stroke='none'))

    def draw_adapter_square(self, d, center_x, y, color):
        """Zeichnet das quadratische Icon für Adapter"""
        size = 8
        # Ein einfaches Quadrat mit kleiner Struktur (Puzzle-Look angedeutet durch Border)
        d.append(draw.Rectangle(center_x - size/2, y - size/2, size, size, 
                                fill=color, stroke='none'))
        # Optional: Kleines weißes Detail innen für "Socket"-Look
        d.append(draw.Rectangle(center_x - 2, y - 4, 4, 8, fill='none', stroke='white', stroke_width=1))

    def draw(self):
        # Canvas Setup
        pad_l = 40 + ((self.max_tracks_in + 1) * self.cfg['track_width']) + 250
        pad_r = 40 + ((self.max_tracks_out + 1) * self.cfg['track_width']) + 250
        
        d = draw.Drawing(self.w_block + pad_l + pad_r, self.h_total + 50, origin=(-pad_l, -20))
        
        # --- 1. Der Block (Notched Rectangle) ---
        x, y, w, h = 0, 0, self.w_block, self.h_total
        neck_y1 = self.y_neck_start
        neck_y2 = self.y_neck_end
        ind = self.cfg['neck_indent']
        
        # Schatten (Optional, macht es plastischer wie im Screenshot)
        d.append(draw.Rectangle(x+3, y+3, w, h, fill='#000000', fill_opacity=0.2, rx=2, ry=2))

        # Main Shape
        p = draw.Path(fill=self.cfg['colors']['bg'], stroke=self.cfg['colors']['border'], stroke_width=2)
        p.M(x, y).H(x + w)              # Top
        p.V(neck_y1).H(x + w - ind)     # Notch Rein Rechts
        p.V(neck_y2).H(x + w)           # Notch Raus Rechts
        p.V(h).H(x)                     # Bottom
        p.V(neck_y2).H(x + ind)         # Notch Rein Links
        p.V(neck_y1).H(x).Z()           # Notch Raus Links
        d.append(p)
        
        # Header Linie (nur wenn Events da sind oder als Abschluss)
        # Wenn keine Events da sind, ist die Header-Höhe trotzdem da (für den Titel)
        d.append(draw.Line(x, self.cfg['header_h'], x+w, self.cfg['header_h'], 
                           stroke=self.cfg['colors']['border'], stroke_width=1))
        
        # --- TEXT IM HALS ---
        neck_center_y = (neck_y1 + neck_y2) / 2
        d.append(draw.Text(self.block_name, font_size=self.cfg['font_size_title'], 
                           x=w/2, y=neck_center_y - 2, 
                           center=True, fontWeight='bold', font_family=self.cfg['font_family'], fill=self.cfg['colors']['text'], font_style='italic'))
        
        if self.version:
            d.append(draw.Text(self.version, font_size=10, 
                               x=w/2, y=neck_center_y + 12, 
                               center=True, fill='#000', font_family=self.cfg['font_mono']))

        # --- 2. Pins & Labels ---
        self._draw_side(d, self.inputs, True, 0)
        self._draw_side(d, self.outputs, False, self.w_block)
        
        # --- 3. WITH Linien (Nur Events) ---
        self._draw_conns(d, self.inputs, True, 0)
        self._draw_conns(d, self.outputs, False, self.w_block)

        d.save_svg(self.output_path)
        print(f"Generiert: {self.output_path}")

    def _draw_side(self, d, group, is_input, x_edge):
        track_cnt = self.max_tracks_in if is_input else self.max_tracks_out
        txt_offset = ((track_cnt + 1) * self.cfg['track_width']) + 15
        
        # Reihenfolge: Events -> Adapter -> Vars
        for kind in ['events', 'adapters', 'vars']:
            
            # Farbe und Pin-Form bestimmen
            if kind == 'events':
                color = self.cfg['colors']['event_pin']
                meta_color = '#888'
            elif kind == 'adapters':
                color = self.cfg['colors']['adapter_pin']
                meta_color = '#000' # Adapter Type oft schwarz oder dunkel
            else: # vars
                color = self.cfg['colors']['data_pin']
                meta_color = self.cfg['colors']['meta_type']

            pin_x = x_edge
            
            for item in group[kind]:
                y = item['y']
                
                # A. Pin Icon (Dreieck oder Quadrat)
                if kind == 'adapters':
                    # Quadrat an der Kante
                    # Bei Input liegt Quadrat etwas Links, bei Output etwas Rechts vom Strich?
                    # Im Bild: Quadrat liegt AUF der Linie/Kante.
                    center_offset = -4 if is_input else 4
                    self.draw_adapter_square(d, pin_x + center_offset, y, color)
                else:
                    # Dreiecke
                    if is_input:
                        self.draw_triangle_right(d, pin_x, y, color)
                    else:
                        self.draw_triangle_right(d, pin_x + 5, y, color)
                
                # B. Label (Name)
                if is_input:
                    d.append(draw.Text(item['name'], font_size=12, x=pin_x + 10, y=y+4, 
                                       text_anchor='start', font_family=self.cfg['font_mono']))
                else:
                    d.append(draw.Text(item['name'], font_size=12, x=pin_x - 10, y=y+4, 
                                       text_anchor='end', font_family=self.cfg['font_mono']))

                # C. Metadaten (Typ, Comment)
                if is_input:
                    meta_x = pin_x - txt_offset
                    anchor = 'end'
                else:
                    meta_x = pin_x + txt_offset
                    anchor = 'start'
                
                t_txt = item['type'] if kind != 'events' else 'Event'
                
                # Adapter Typen sind oft Kursiv dargestellt im Bild
                font_style = 'italic' if kind == 'adapters' or kind == 'events' or kind == 'vars' else 'normal'
                
                d.append(draw.Text(t_txt, font_size=11, x=meta_x, y=y+3, 
                                   text_anchor=anchor, fill=meta_color, font_style=font_style, font_family=self.cfg['font_family']))
                
                if item['comment']:
                    comm_x = meta_x - 70 if is_input else meta_x + 70
                    d.append(draw.Text(item['comment'], font_size=11, x=comm_x, y=y+3,
                                       text_anchor=anchor, fill=self.cfg['colors']['meta_comm'], font_family=self.cfg['font_family']))

    def _draw_conns(self, d, group, is_input, x_edge):
        # ... (Identisch zur Vorversion, nur für Events relevant) ...
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
            t_ys = [y_evt]
            valid_vars = []
            for v in item['with']:
                if v in y_map:
                    y_v = y_map[v]
                    t_ys.append(y_v)
                    valid_vars.append(y_v)
            
            if not valid_vars: continue

            d.append(draw.Line(line_x, min(t_ys), line_x, max(t_ys), stroke=self.cfg['colors']['line'], stroke_width=1))
            d.append(draw.Line(pin_x, y_evt, line_x, y_evt, stroke=self.cfg['colors']['line']))
            d.append(draw.Rectangle(line_x-2, y_evt-2, 4, 4, fill='white', stroke='black', stroke_width=1))
            
            for y_v in valid_vars:
                if is_input:
                    d.append(draw.Line(line_x, y_v, x_edge - 5, y_v, stroke=self.cfg['colors']['line']))
                else:
                    d.append(draw.Line(x_edge + 5, y_v, line_x, y_v, stroke=self.cfg['colors']['line']))
                d.append(draw.Rectangle(line_x-2, y_v-2, 4, 4, fill='white', stroke='black', stroke_width=1))

if __name__ == "__main__":
    # Teste es mit deiner neuen AX_SPLIT_4 Datei
    r = UniversalFbtRenderer("AX_SPLIT_4.fbt", "AX_SPLIT_4.svg")
    r.parse()
    r.layout()
    r.draw()