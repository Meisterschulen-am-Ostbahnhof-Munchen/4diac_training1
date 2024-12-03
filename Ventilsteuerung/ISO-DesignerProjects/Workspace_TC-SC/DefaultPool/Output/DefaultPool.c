// ISO-Designer ISO 11783   Version 5.7.0.6283 Bucher Automation AG
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
	ID(WorkingSet_0), TYPEID_WORKSET, COLOR_SILVER, 1, ID(DataMask_1000), 1, 0, 2,
		XYREF(OutputString_TC_SC, 0, 0),
		'e', 'n',
		'd', 'e',
	ID(DataMask_1000), TYPEID_DATAMASK, COLOR_SILVER, ID(ID_NULL), 0, 0, 
	ID(OutputString_TC_SC), TYPEID_OUTSTR, WORD(72), WORD(72), COLOR_WHITE, ID(FontAttributes_SKM), 1,
		ID(ID_NULL), 0, WORD(5), 'T', 'C', '-', 'S', 'C', 0,
	ID(FontAttributes_SKM), TYPEID_FONTATTR, COLOR_BLACK, 3, 0, 0, 0, 
}; // isoOP_DefaultPool
