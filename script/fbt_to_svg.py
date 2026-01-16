import xml.etree.ElementTree as ET
import drawsvg as draw

class FbtRenderer:
    def __init__(self, fbt_path, output_path):
        self.fbt_path = fbt_path
        self.output_path = output_path
        
        # Konfiguration für das Styling
        self.config = {
            'font_family': 'Arial, sans-serif',
            'font_size': 12,
            'header_height': 30,
            'row_height': 20,
            'pin_width': 10,
            'pin_height': 4, # Dicke der Anschlussstriche
            'padding_x': 10,
            'bg_color': '#f0f0f0',
            'border_color': '#333333',
            'text_color': '#000000'
        }

    def parse_fbt(self):
        """Liest die XML-Datei und extrahiert die Schnittstellen."""
        tree = ET.parse(self.fbt_path)
        root = tree.getroot()
        
        interface = root.find('InterfaceList')
        if interface is None:
            raise ValueError("Keine InterfaceList in der FBT-Datei gefunden.")

        # Hilfsfunktion zum Extrahieren von Namen
        def get_names(section_name):
            section = interface.find(section_name)
            if section is None:
                return []
            # Wir holen Event Inputs/Outputs und Var Inputs/Outputs
            # Tag-Namen variieren (Event, VarDeclaration)
            return [child.get('Name') for child in section]

        self.data = {
            'name': root.get('Name', 'UnknownBlock'),
            'inputs': {
                'events': get_names('EventInputs'),
                'vars': get_names('InputVars')
            },
            'outputs': {
                'events': get_names('EventOutputs'),
                'vars': get_names('OutputVars')
            }
        }

    def calculate_layout(self):
        """Berechnet Dimensionen basierend auf dem Inhalt."""
        inputs = self.data['inputs']['events'] + self.data['inputs']['vars']
        outputs = self.data['outputs']['events'] + self.data['outputs']['vars']
        
        # Anzahl der Zeilen bestimmen (Maximum von Links oder Rechts)
        max_rows = max(len(inputs), len(outputs))
        
        # Höhe berechnen: Header + Zeilen + etwas Bodenabstand
        self.height = self.config['header_height'] + (max_rows * self.config['row_height']) + 10
        
        # Breite schätzen (grob basierend auf Zeichenlänge * Faktor)
        # Für eine präzise Berechnung bräuchte man Font-Metriken, aber das hier reicht meistens.
        max_text_len = 0
        all_texts = inputs + outputs + [self.data['name']]
        for text in all_texts:
            if len(text) > max_text_len:
                max_text_len = len(text)
        
        # Basisbreite + Textlänge (Faktor 8px pro Zeichen ist ein Schätzwert)
        self.width = 100 + (max_text_len * 8)

    def draw(self):
        """Erstellt die SVG-Grafik."""
        d = draw.Drawing(self.width + 40, self.height + 20, origin=(-20, -10))
        
        # 1. Hauptkörper (Rechteck)
        d.append(draw.Rectangle(0, 0, self.width, self.height, 
                                fill=self.config['bg_color'], 
                                stroke=self.config['border_color'], 
                                stroke_width=2, rx=5, ry=5))
        
        # 2. Header (Baustein Name)
        d.append(draw.Text(self.data['name'], 
                           self.config['font_size'] + 2, 
                           x=self.width/2, y=20, 
                           center=True, fontWeight='bold', font_family=self.config['font_family']))
        
        # Trennlinie unter dem Header
        d.append(draw.Line(0, self.config['header_height'], self.width, self.config['header_height'],
                           stroke=self.config['border_color'], stroke_width=1))

        # 3. Inputs zeichnen (Links)
        current_y = self.config['header_height'] + self.config['row_height']
        
        # Events (Oben)
        for name in self.data['inputs']['events']:
            self._draw_pin(d, name, 0, current_y, is_input=True, is_event=True)
            current_y += self.config['row_height']
            
        # Variablen (Unten) - Kleiner Abstand zur optischen Trennung
        if self.data['inputs']['events'] and self.data['inputs']['vars']:
            current_y += 5 
            
        for name in self.data['inputs']['vars']:
            self._draw_pin(d, name, 0, current_y, is_input=True, is_event=False)
            current_y += self.config['row_height']

        # 4. Outputs zeichnen (Rechts)
        current_y = self.config['header_height'] + self.config['row_height']
        
        # Events
        for name in self.data['outputs']['events']:
            self._draw_pin(d, name, self.width, current_y, is_input=False, is_event=True)
            current_y += self.config['row_height']
            
        if self.data['outputs']['events'] and self.data['outputs']['vars']:
            current_y += 5
            
        for name in self.data['outputs']['vars']:
            self._draw_pin(d, name, self.width, current_y, is_input=False, is_event=False)
            current_y += self.config['row_height']

        # Speichern
        d.save_svg(self.output_path)
        print(f"SVG erstellt: {self.output_path}")

    def _draw_pin(self, drawing, text, x_pos, y_pos, is_input, is_event):
        """Hilfsmethode zum Zeichnen eines einzelnen Pins mit Label."""
        
        # Pin-Linie
        if is_input:
            start_x = x_pos - self.config['pin_width']
            end_x = x_pos
            text_anchor = 'start'
            text_x = x_pos + 5
        else:
            start_x = x_pos
            end_x = x_pos + self.config['pin_width']
            text_anchor = 'end'
            text_x = x_pos - 5
            
        # Farbe: Events oft Rot oder anders, Vars Schwarz. Hier simpel gehalten.
        color = '#d9534f' if is_event else '#000000'
        
        # Pin zeichnen
        drawing.append(draw.Line(start_x, y_pos - 4, end_x, y_pos - 4,
                                 stroke=color, stroke_width=2))
        
        # Kleines Rechteck am Ende bei Events (IEC Stil oft Quadrat)
        if is_event:
             sq_size = 4
             sq_x = start_x if is_input else end_x - sq_size
             drawing.append(draw.Rectangle(sq_x, y_pos - 6, sq_size, sq_size, fill=color))

        # Text Label
        drawing.append(draw.Text(text, self.config['font_size'],
                                 x=text_x, y=y_pos,
                                 text_anchor=text_anchor,
                                 fill=self.config['text_color'],
                                 font_family=self.config['font_family']))

# --- Verwendung ---

# Erstelle eine Dummy-Datei zum Testen, falls du keine zur Hand hast
dummy_fbt = """
<FBType Name="E_CTUD">
  <InterfaceList>
    <EventInputs>
      <Event Name="CU" Comment="Count Up"/>
      <Event Name="CD" Comment="Count Down"/>
      <Event Name="R" Comment="Reset"/>
      <Event Name="LD" Comment="Load"/>
    </EventInputs>
    <EventOutputs>
      <Event Name="CO" Comment="Carry Out"/>
      <Event Name="RO" Comment="Reset Out"/>
    </EventOutputs>
    <InputVars>
      <VarDeclaration Name="PV" Type="UINT" Comment="Preset Value"/>
    </InputVars>
    <OutputVars>
      <VarDeclaration Name="QU" Type="BOOL" Comment="Up limit reached"/>
      <VarDeclaration Name="QD" Type="BOOL" Comment="Down limit reached"/>
      <VarDeclaration Name="CV" Type="UINT" Comment="Current Value"/>
    </OutputVars>
  </InterfaceList>
</FBType>
"""

# Schreib den Dummy-Inhalt in eine Datei
with open("test_block.fbt", "w") as f:
    f.write(dummy_fbt)

# Führe den Renderer aus
renderer = FbtRenderer("test_block.fbt", "E_CTUD.svg")
renderer.parse_fbt()
renderer.calculate_layout()
renderer.draw()