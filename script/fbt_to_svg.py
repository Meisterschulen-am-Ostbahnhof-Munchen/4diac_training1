import xml.etree.ElementTree as ET
import drawsvg as draw

class AdvancedFbtRenderer:
    def __init__(self, fbt_path, output_path):
        self.fbt_path = fbt_path
        self.output_path = output_path
        
        # Styling basierend auf deinem Screenshot
        self.style = {
            'font_family': 'Consolas, monospace', # Monospace wirkt technischer
            'font_size': 12,
            'comment_size': 10,
            'header_height': 30,
            'row_height': 24,
            'neck_indent': 10,  # Wie tief der Einzug ist
            'pin_len': 10,
            'col_gap': 10,      # Abstand zwischen Typ und Pin
            'colors': {
                'bg_body': '#f5f5f5',
                'border': '#404040',
                'event_pin': '#5cb85c', # Das Grün aus dem Bild
                'data_pin': '#0275d8',  # Blau
                'text_main': '#000000',
                'text_type': '#0275d8', # Blau für Typen
                'text_comment': '#666666'
            }
        }

    def parse_fbt(self):
        tree = ET.parse(self.fbt_path)
        root = tree.getroot()
        
        interface = root.find('InterfaceList')
        self.name = root.get('Name', 'BLOCK')
        
        # Hilfsfunktion zum sauberen Parsen
        def parse_section(tag_name):
            items = []
            section = interface.find(tag_name)
            if section:
                for child in section:
                    items.append({
                        'name': child.get('Name'),
                        'type': child.get('Type', 'Event'), # Events haben keinen Type im Tag
                        'comment': child.get('Comment', ''),
                        # Hier würde man auch 'With' parsen
                        'with': [w.get('Var') for w in child.findall('With')] 
                    })
            return items

        self.inputs = {
            'events': parse_section('EventInputs'),
            'vars': parse_section('InputVars')
        }
        self.outputs = {
            'events': parse_section('EventOutputs'),
            'vars': parse_section('OutputVars')
        }

    def calculate_dimensions(self):
        # Zeilen berechnen
        self.n_event_in = len(self.inputs['events'])
        self.n_var_in = len(self.inputs['vars'])
        self.n_event_out = len(self.outputs['events'])
        self.n_var_out = len(self.outputs['vars'])
        
        # Höhe des oberen Teils (Events) und unteren Teils (Vars)
        self.head_rows = max(self.n_event_in, self.n_event_out)
        self.body_rows = max(self.n_var_in, self.n_var_out)
        
        self.head_h = self.style['header_height'] + (self.head_rows * self.style['row_height'])
        self.body_h = (self.body_rows * self.style['row_height']) + 10 # +10 padding unten
        self.total_h = self.head_h + self.body_h
        
        # Breite des Blocks berechnen (Textabhängig)
        # Einfache Schätzung: 9px pro Zeichen
        max_len = len(self.name)
        for i in [self.inputs, self.outputs]:
            for group in i.values():
                for item in group:
                    max_len = max(max_len, len(item['name']) + 2)
        
        self.block_w = max(100, max_len * 9)
        
        # Gesamtbreite für SVG (inkl. Kommentare links/rechts)
        self.total_w = self.block_w + 500 # Puffer für externe Spalten

    def draw_path_shape(self, d, x, y, width, head_h, total_h, indent):
        """Zeichnet die typische IEC 61499 Form mit dem Einzug (Neck)"""
        p = draw.Path(fill=self.style['colors']['bg_body'], 
                      stroke=self.style['colors']['border'], 
                      stroke_width=2)
        
        # Start Oben Links
        p.M(x, y) 
        p.H(x + width) # Oben
        p.V(y + head_h) # Rechts runter bis zum Hals
        p.H(x + width - indent) # Einzug rein
        p.V(y + total_h) # Runter zum Boden
        p.H(x + indent) # Boden nach links
        p.V(y + head_h) # Hoch zum Hals
        p.H(x) # Auszug raus
        p.Z() # Schließen
        
        d.append(p)
        
        # Header Trennlinie
        d.append(draw.Line(x, y + 30, x + width, y + 30, stroke=self.style['colors']['border'], stroke_width=1))

    def draw_arrow(self, d, x, y, direction='right', color='#000'):
        """Zeichnet ein kleines Dreieck als Pfeil"""
        size = 5
        if direction == 'right':
            points = [x, y-size, x+size, y, x, y+size]
        else: # left (für Inputs)
            points = [x, y-size, x-size, y, x, y+size]
            
        d.append(draw.Lines(*points, close=True, fill=color, stroke='none'))

    def draw(self):
        d = draw.Drawing(self.total_w, self.total_h + 20, origin=(-250, -10))
        
        # Zentrierung des Blocks
        block_x = 0
        block_y = 0
        
        # 1. Den Block-Körper zeichnen (Custom Shape)
        self.draw_path_shape(d, block_x, block_y, self.block_w, self.head_h, self.total_h, self.style['neck_indent'])
        
        # 2. Block Name
        d.append(draw.Text(self.name, fontSize=14, x=block_x + self.block_w/2, y=block_y+20, 
                           center=True, fontWeight='bold', fill=self.style['colors']['text_main'], font_family=self.style['font_family']))

        # 3. Pins Zeichnen
        
        # Helper zum Zeichnen einer Seite
        def draw_side(items, is_input, start_y):
            y = start_y
            indent_adjust = 0 if is_input else -self.style['neck_indent']
            if not is_input: indent_adjust = 0 # Output side logic varies based on indent

            for item in items:
                # Koordinaten
                if is_input:
                    pin_x = block_x
                    text_anchor = 'start'
                    label_x = pin_x + 5
                    # External Layout
                    type_x = pin_x - 20
                    comment_x = type_x - 60
                else:
                    pin_x = block_x + self.block_w
                    # Korrektur für den "Hals" bei Data-Outputs ist komplexer, 
                    # vereinfachen wir hier: Wir zeichnen am Rand des Rechtecks
                    if start_y > self.head_h: # Wir sind im Body
                        pin_x -= self.style['neck_indent']
                    
                    text_anchor = 'end'
                    label_x = pin_x - 5
                    type_x = pin_x + 20
                    comment_x = type_x + 60

                # Farbe bestimmen
                is_event = item['type'] == 'Event'
                color = self.style['colors']['event_pin'] if is_event else self.style['colors']['data_pin']
                
                # Pin Linie & Pfeil
                if is_input:
                    d.append(draw.Line(pin_x - 10, y, pin_x, y, stroke=color, stroke_width=2))
                    self.draw_arrow(d, pin_x, y, 'right', color)
                else:
                    d.append(draw.Line(pin_x, y, pin_x + 10, y, stroke=color, stroke_width=2))
                    self.draw_arrow(d, pin_x, y, 'left', color) # Output arrow points out? Usually just a pin.
                
                # Label im Block
                d.append(draw.Text(item['name'], fontSize=self.style['font_size'], x=label_x, y=y+4, 
                                   text_anchor=text_anchor, fill=self.style['colors']['text_main'], font_family=self.style['font_family']))
                
                # Typ (Außerhalb)
                type_anchor = 'end' if is_input else 'start'
                if item['type'] != 'Event':
                    d.append(draw.Text(item['type'], fontSize=11, x=type_x, y=y+4,
                                       text_anchor=type_anchor, fill=self.style['colors']['text_type'], font_family=self.style['font_family'], font_style='italic'))
                else:
                    d.append(draw.Text("Event", fontSize=11, x=type_x, y=y+4,
                                       text_anchor=type_anchor, fill=self.style['colors']['text_comment'], font_family=self.style['font_family'], font_style='italic'))

                # Kommentar (Ganz außen)
                if item['comment']:
                    comment_pos = comment_x - 10 if is_input else comment_x + 10
                    d.append(draw.Text(item['comment'], fontSize=self.style['comment_size'], x=comment_pos, y=y+4,
                                       text_anchor=type_anchor, fill=self.style['colors']['text_comment'], font_family=self.style['font_family']))

                y += self.style['row_height']
            return y

        # Zeichnen Events (Oben)
        draw_side(self.inputs['events'], True, self.style['header_height'] + 15)
        draw_side(self.outputs['events'], False, self.style['header_height'] + 15)
        
        # Zeichnen Vars (Unten - Startet nach dem Head)
        draw_side(self.inputs['vars'], True, self.head_h + 15)
        draw_side(self.outputs['vars'], False, self.head_h + 15)

        d.save_svg(self.output_path)
        print(f"Erweitertes SVG erstellt: {self.output_path}")

# --- Test ---
# Wir nutzen die gleiche Testdatei wie vorher oder deine echte .fbt
renderer = AdvancedFbtRenderer("test_block.fbt", "E_CTUD_v2.svg")
renderer.parse_fbt()
renderer.calculate_dimensions()
renderer.draw()