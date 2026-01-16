import xml.etree.ElementTree as ET
import drawsvg as draw

class FbtRendererV8:
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
            'row_h': 26,            # Etwas mehr Luft
            'header_h': 30,         
            'neck_indent': 6,       
            'neck_height': 40,      
            'track_width': 8,       
            'colors': {
                'bg': '#ffffff',
                'border': '#606060',
                'event_pin': '#5cb85c', # Grün
                'data_pin': '#0066cc',  # Blau
                'adapter_pin': '#985ec9', # Helles Violett (wie im Screenshot)
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
                    # Namespace bereinigen (adapter::types::AX -> AX)
                    raw_type = child.get('Type', '')
                    display_type = raw_type.split('::')[-1]

                    items.append({
                        'name': child.get('Name'),
                        'type': display_type,
                        'kind': kind_label, 
                        'comment': child.get('Comment', ''),
                        'with': [w.get('Var') for w in child.findall('With')]
                    })
            return items

        self.inputs = {
            'events': get_items('EventInputs', 'event'),
            'adapters': get_items('Sockets', 'adapter'), # Sockets sind Inputs
            'vars': get_items('InputVars', 'var')
        }
        
        self.outputs = {
            'events': get_items('EventOutputs', 'event'),
            'adapters': get_items('Plugs', 'adapter'),   # Plugs sind Outputs
            'vars': get_items('OutputVars', 'var')
        }

    def layout(self):
        # 1. Zeilen zählen
        n_ev_in, n_ev_out = len(self.inputs['events']), len(self.outputs['events'])
        rows_head = max(n_ev_in, n_ev_out)
        
        # Body: Adapter + Vars
        n_body_in = len(self.inputs['adapters']) + len(self.inputs['vars'])
        n_body_out = len(self.outputs['adapters']) + len(self.outputs['vars'])
        rows_body = max(n_body_in, n_body_out)
        
        # 2. Vertikale Struktur
        self.y_head_end = self.cfg['header_h'] + (rows_head * self.cfg['row_h']) + (10 if rows_head > 0 else 0)
        
        self.y_neck_start = self.y_head_end
        self.y_neck_end = self.y_neck_start + self.cfg['neck_height']
        
        self.y_body_start = self.y_neck_end + 5 
        
        self.h_total = self.y_body_start + (rows_body * self.cfg['row_h']) + 10
        
        # 3. Breite berechnen
        max_txt = len(self.block_name) * 10
        for grp in [self.inputs, self.outputs]:
            for kind in ['events', 'adapters', 'vars']:
                for it in grp[kind]:
                    max_txt = max(max_txt, len(it['name']) * 9)
        self.w_block = max(130, max_txt + 40)

        # 4. Y-Positionen
        self.y_map = {'in': {}, 'out': {}}
        
        def set_y(items, start_y, mapping):
            y = start_y
            for item in items:
                item['y'] = y
                mapping[item['name']] = y
                y += self.cfg['row_h']
            return y
        
        # Head
        evt_start = self.cfg['header_h'] + 12
        set_y(self.inputs['events'], evt_start, self.y_map['in'])
        set_y(self.outputs['events'], evt_start, self.y_map['out'])
        
        # Body
        body_curr_in = self.y_body_start + 12
        body_curr_in = set_y(self.inputs['adapters'], body_curr_in, self.y_map['in'])
        set_y(self.inputs['vars'], body_curr_in, self.y_map['in'])
        
        body_curr_out = self.y_body_start + 12
        body_curr_out = set_y(self.outputs['adapters'], body_curr_out, self.y_map['out'])
        set_y(self.outputs['vars'], body_curr_out, self.y_map['out'])

        # 5. Tracks
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

    def draw_adapter_icon(self, d, center_x, y, color, is_socket):
        """
        Zeichnet Socket (Hohl) oder Plug (Gefüllt).
        is_socket=True -> Socket (IN, Links, Hohl)
        is_socket=False -> Plug (OUT, Rechts, Gefüllt)
        """
        size = 10  # Größe des Quadrats
        half = size / 2
        
        if is_socket:
            # SOCKET: Weiß gefüllt mit farbigem Rand (wie eine Buchse)
            # Zuerst ein weißes Rechteck um die Linie dahinter zu verdecken
            d.append(draw.Rectangle(center_x - half, y - half, size, size, 
                                    fill='white', stroke=color, stroke_width=2.5))
            
            # Optional: Kleines Detail innen, um es "technischer" zu machen (wie im Screenshot H-Form)
            # d.append(draw.Line(center_x, y - 2, center_x, y + 2, stroke=color, stroke_width=2))
        else:
            # PLUG: Voll gefüllt (wie ein Stecker)
            d.append(draw.Rectangle(center_x - half, y - half, size, size, 
                                    fill=color, stroke='none'))

    def draw(self):
        pad_l = 40 + ((self.max_tracks_in + 1) * self.cfg['track_width']) + 250
        pad_r = 40 + ((self.max_tracks_out + 1) * self.cfg['track_width']) + 250
        
        d = draw.Drawing(self.w_block + pad_l + pad_r, self.h_total + 50, origin=(-pad_l, -20))
        
        # --- Block Shape ---
        x, y, w, h = 0, 0, self.w_block, self.h_total
        neck_y1 = self.y_neck_start
        neck_y2 = self.y_neck_end
        ind = self.cfg['neck_indent']
        
        # Schatten
        d.append(draw.Rectangle(x+3, y+3, w, h, fill='#000000', fill_opacity=0.1, rx=2, ry=2))

        # Main Path
        p = draw.Path(fill=self.cfg['colors']['bg'], stroke=self.cfg['colors']['border'], stroke_width=2)
        p.M(x, y).H(x + w).V(neck_y1).H(x + w - ind).V(neck_y2).H(x + w).V(h).H(x).V(neck_y2).H(x + ind).V(neck_y1).H(x).Z()
        d.append(p)
        
        # Header Line
        d.append(draw.Line(x, self.cfg['header_h'], x+w, self.cfg['header_h'], 
                           stroke=self.cfg['colors']['border'], stroke_width=1))
        
        # --- Titel ---
        neck_cy = (neck_y1 + neck_y2) / 2
        d.append(draw.Text(self.block_name, font_size=self.cfg['font_size_title'], 
                           x=w/2, y=neck_cy - 2, 
                           center=True, fontWeight='bold', font_family=self.cfg['font_family'], font_style='italic'))
        
        if self.version:
            d.append(draw.Text(self.version, font_size=10, 
                               x=w/2, y=neck_cy + 12, 
                               center=True, fill='#000', font_family=self.cfg['font_mono']))

        # --- Pins ---
        self._draw_side(d, self.inputs, True, 0)
        self._draw_side(d, self.outputs, False, self.w_block)
        
        # --- WITH Lines ---
        self._draw_conns(d, self.inputs, True, 0)
        self._draw_conns(d, self.outputs, False, self.w_block)

        d.save_svg(self.output_path)
        print(f"Generiert: {self.output_path}")

    def _draw_side(self, d, group, is_input, x_edge):
        track_cnt = self.max_tracks_in if is_input else self.max_tracks_out
        txt_offset = ((track_cnt + 1) * self.cfg['track_width']) + 15
        
        for kind in ['events', 'adapters', 'vars']:
            if kind == 'events':
                color = self.cfg['colors']['event_pin']
                meta_color = '#888'
            elif kind == 'adapters':
                color = self.cfg['colors']['adapter_pin']
                meta_color = '#000'
            else:
                color = self.cfg['colors']['data_pin']
                meta_color = self.cfg['colors']['meta_type']

            pin_x = x_edge
            
            for item in group[kind]:
                y = item['y']
                
                # A. ICON
                if kind == 'adapters':
                    # Socket (Input) vs Plug (Output)
                    # Wir gehen davon aus: Input-Seite = Socket, Output-Seite = Plug
                    is_socket = is_input 
                    
                    # Position: Genau auf der Kante (pin_x)
                    self.draw_adapter_icon(d, pin_x, y, color, is_socket)
                else:
                    # Dreiecke für Events/Vars
                    if is_input:
                        self.draw_triangle_right(d, pin_x, y, color)
                    else:
                        self.draw_triangle_right(d, pin_x + 5, y, color)
                
                # B. LABEL
                if is_input:
                    d.append(draw.Text(item['name'], font_size=12, x=pin_x + 12, y=y+4, 
                                       text_anchor='start', font_family=self.cfg['font_mono']))
                else:
                    d.append(draw.Text(item['name'], font_size=12, x=pin_x - 12, y=y+4, 
                                       text_anchor='end', font_family=self.cfg['font_mono']))

                # C. META
                if is_input:
                    meta_x = pin_x - txt_offset
                    anchor = 'end'
                else:
                    meta_x = pin_x + txt_offset
                    anchor = 'start'
                
                t_txt = item['type'] if kind != 'events' else 'Event'
                font_style = 'italic' if kind in ['adapters', 'events', 'vars'] else 'normal'
                
                d.append(draw.Text(t_txt, font_size=11, x=meta_x, y=y+3, 
                                   text_anchor=anchor, fill=meta_color, font_style=font_style, font_family=self.cfg['font_family']))
                
                if item['comment']:
                    comm_x = meta_x - 70 if is_input else meta_x + 70
                    d.append(draw.Text(item['comment'], font_size=11, x=comm_x, y=y+3,
                                       text_anchor=anchor, fill=self.cfg['colors']['meta_comm'], font_family=self.cfg['font_family']))

    def _draw_conns(self, d, group, is_input, x_edge):
        # Unverändert (nur für Events relevant)
        tracks = self.tracks_in if is_input else self.tracks_out
        y_map = self.y_map['in'] if is_input else self.y_map['out']
        for item in group['events']:
            if not item['with']: continue
            t_idx = tracks.get(item['name'], 0)
            offset = 12 + (t_idx * self.cfg['track_width'])
            line_x = x_edge - offset if is_input else x_edge + offset
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
                end_x = x_edge - 5 if is_input else x_edge + 5
                d.append(draw.Line(line_x, y_v, end_x, y_v, stroke=self.cfg['colors']['line']))
                d.append(draw.Rectangle(line_x-2, y_v-2, 4, 4, fill='white', stroke='black', stroke_width=1))

if __name__ == "__main__":
    r = FbtRendererV8("AX_SPLIT_4.fbt", "AX_SPLIT_4_Final.svg")
    r.parse()
    r.layout()
    r.draw()