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
	ID(DataMask_M1), TYPEID_DATAMASK, COLOR_SILVER, ID(ID_NULL), 6, 0, 
		XYREF(Container_Sollwertmarker, 192, 200),
		XYREF(LinearBargraph, 198, 185),
		XYREF(Bargraph_Split_links, 198, 170),
		XYREF(Bargraph_Split_rechts, 240, 170),
		XYREF(InputNumber_Sollwert, 192, 230),
		XYREF(InputNumber_Istwert, 192, 280),
	ID(Container_Sollwertmarker), TYPEID_CONTAINER, WORD(96), WORD(14), 0, 1, 0, 
		XYREF(Polygon_Bargraph_Mittelmarker, 42, 0),
	ID(InputNumber_Sollwert), TYPEID_INNUM, WORD(96), WORD(40), COLOR_WHITE, ID(FontAttributes_Werte), 0, 
		ID(NumberVariable_Sollwert), LONG(42UL), LONG(0UL), LONG(84UL), LONG(-42L), FLOAT_1, 0, 0, 1, 1, 0, 
	ID(InputNumber_Istwert), TYPEID_INNUM, WORD(96), WORD(40), COLOR_WHITE, ID(FontAttributes_Werte), 0, 
		ID(NumberVariable_Istwert), LONG(42UL), LONG(0UL), LONG(84UL), LONG(-42L), FLOAT_1, 0, 0, 1, 1, 0, 
	ID(OutputString_WorkingSet_0), TYPEID_OUTSTR, WORD(80), WORD(20), COLOR_WHITE, ID(FontAttributes_6x8), 2,
		ID(ID_NULL), 0, WORD(12), 'W', 'o', 'r', 'k', 'i', 'n', 'g', 'S', 'e', 't', '_', '0', 0,
	ID(Polygon_Bargraph_Mittelmarker), TYPEID_OUTPOLY, WORD(13), WORD(13), 
		ID(LineStyle_Bargraph_Mittelmarker_Gruen), ID(FillStyle_Bargraph_Mittelmarker_Gruen), 2, 3, 0, 
		WORD(6), WORD(0), 
		WORD(12), WORD(12), 
		WORD(0), WORD(12), 
	ID(LinearBargraph), TYPEID_OUTLINBAR, WORD(84), WORD(14), COLOR_BLACK, COLOR_RED, 55, 11, 
		WORD(0), WORD(84), ID(NumberVariable_Istwert), WORD(42), ID(NumberVariable_Sollwert), WORD(42), 0, 
	ID(Bargraph_Split_links), TYPEID_OUTLINBAR, WORD(42), WORD(14), COLOR_BLACK, COLOR_RED, 21, 11, 
		WORD(0), WORD(42), ID(ID_NULL), WORD(0), ID(ID_NULL), WORD(0), 0, 
	ID(Bargraph_Split_rechts), TYPEID_OUTLINBAR, WORD(42), WORD(14), COLOR_BLACK, COLOR_RED, 53, 11, 
		WORD(0), WORD(42), ID(ID_NULL), WORD(0), ID(ID_NULL), WORD(0), 0, 
	ID(NumberVariable_Sollwert), TYPEID_VARNUM, LONG(42UL), 
	ID(NumberVariable_Istwert), TYPEID_VARNUM, LONG(42UL), 
	ID(FontAttributes_6x8), TYPEID_FONTATTR, COLOR_BLACK, 0, 0, 0, 0, 
	ID(FontAttributes_Werte), TYPEID_FONTATTR, COLOR_BLACK, 3, 0, 0, 0, 
	ID(LineStyle_Bargraph_Mittelmarker_Gruen), TYPEID_LINEATTR, COLOR(112), 1, WORD(65535), 0, 
	ID(FillStyle_Bargraph_Mittelmarker_Gruen), TYPEID_FILLATTR, 2, COLOR(112), ID(ID_NULL), 0, 
}; // isoOP_DefaultPool
