// ISO-Designer ISO 11783   Version 5.7.2.6664 Bucher Automation AG
// Do not change!

#include "DefaultPool.iop.h"
#include "DefaultPool.c.h"

#define WORD(w)  (unsigned char)w, (unsigned char)(w >> 8)
#define LONG(l)  (unsigned char)l, \
					(unsigned char)((unsigned long)l >> 8), \
					(unsigned char)((unsigned long)l >> 16), \
					(unsigned char)((unsigned long)l >> 24)
#define ID(id)           WORD(id)
#define REF(id)          WORD(id)
#define XYREF(id, x, y)  WORD(id), WORD(x), WORD(y)
#define MACRO(ev, id)    ev, id
#define COLOR(c)         c

const unsigned char ISO_OP_MEMORY_CLASS isoOP_DefaultPool[] = {
	17,
	ID(WorkingSet), TYPEID_WORKSET, COLOR_SILVER, 1, ID(DataMask_M1), 1, 0, 2,
		XYREF(OutputString_WorkingSet_0, 0, 60),
		'e', 'n',
		'd', 'e',
	ID(DataMask_M1), TYPEID_DATAMASK, COLOR_SILVER, ID(ID_NULL), 2, 0, 
		XYREF(Bargraph_Hysterese, 50, 150),
		XYREF(Container_Schwellwerte, 38, 178),
	ID(Container_Schwellwerte), TYPEID_CONTAINER, WORD(210), WORD(28), 0, 5, 0, 
		XYREF(Polygon_MID, 93, 0),
		XYREF(Polygon_MID_PLUS_DEAD, 121, 0),
		XYREF(Polygon_MID_MINUS_DEAD, 65, 0),
		XYREF(Polygon_MID_PLUS_DEAD_HYST, 158, 0),
		XYREF(Polygon_MID_MINUS_DEAD_HYST, 28, 0),
	ID(OutputString_WorkingSet_0), TYPEID_OUTSTR, WORD(80), WORD(20), COLOR_WHITE, ID(FontAttributes_6x8), 2,
		ID(ID_NULL), 0, WORD(12), 'W', 'o', 'r', 'k', 'i', 'n', 'g', 'S', 'e', 't', '_', '0', 0,
	ID(Polygon_MID), TYPEID_OUTPOLY, WORD(25), WORD(25), 
		ID(LineStyle_Hysterese_MID_Gruen), ID(FillStyle_Hysterese_MID_Gruen), 2, 3, 0, 
		WORD(12), WORD(0), 
		WORD(24), WORD(24), 
		WORD(0), WORD(24), 
	ID(Polygon_MID_PLUS_DEAD), TYPEID_OUTPOLY, WORD(25), WORD(25), 
		ID(LineStyle_Hysterese_DEAD_Orange), ID(FillStyle_Hysterese_DEAD_Orange), 2, 3, 0, 
		WORD(12), WORD(0), 
		WORD(24), WORD(24), 
		WORD(0), WORD(24), 
	ID(Polygon_MID_MINUS_DEAD), TYPEID_OUTPOLY, WORD(25), WORD(25), 
		ID(LineStyle_Hysterese_DEAD_Orange), ID(FillStyle_Hysterese_DEAD_Orange), 2, 3, 0, 
		WORD(12), WORD(0), 
		WORD(24), WORD(24), 
		WORD(0), WORD(24), 
	ID(Polygon_MID_PLUS_DEAD_HYST), TYPEID_OUTPOLY, WORD(25), WORD(25), 
		ID(LineStyle_Hysterese_HYST_Rot), ID(FillStyle_Hysterese_HYST_Rot), 2, 3, 0, 
		WORD(12), WORD(0), 
		WORD(24), WORD(24), 
		WORD(0), WORD(24), 
	ID(Polygon_MID_MINUS_DEAD_HYST), TYPEID_OUTPOLY, WORD(25), WORD(25), 
		ID(LineStyle_Hysterese_HYST_Rot), ID(FillStyle_Hysterese_HYST_Rot), 2, 3, 0, 
		WORD(12), WORD(0), 
		WORD(24), WORD(24), 
		WORD(0), WORD(24), 
	ID(Bargraph_Hysterese), TYPEID_OUTLINBAR, WORD(186), WORD(28), COLOR_BLACK, COLOR_RED, 53, 11, 
		WORD(0), WORD(100), ID(ID_NULL), WORD(50), ID(ID_NULL), WORD(0), 0, 
	ID(FontAttributes_6x8), TYPEID_FONTATTR, COLOR_BLACK, 0, 0, 0, 0, 
	ID(LineStyle_Hysterese_MID_Gruen), TYPEID_LINEATTR, COLOR(112), 1, WORD(65535), 0, 
	ID(LineStyle_Hysterese_DEAD_Orange), TYPEID_LINEATTR, COLOR(39), 1, WORD(65535), 0, 
	ID(LineStyle_Hysterese_HYST_Rot), TYPEID_LINEATTR, COLOR_BLUE, 1, WORD(65535), 0, 
	ID(FillStyle_Hysterese_MID_Gruen), TYPEID_FILLATTR, 2, COLOR(112), ID(ID_NULL), 0, 
	ID(FillStyle_Hysterese_DEAD_Orange), TYPEID_FILLATTR, 2, COLOR(39), ID(ID_NULL), 0, 
	ID(FillStyle_Hysterese_HYST_Rot), TYPEID_FILLATTR, 2, COLOR_BLUE, ID(ID_NULL), 0, 
}; // isoOP_DefaultPool
