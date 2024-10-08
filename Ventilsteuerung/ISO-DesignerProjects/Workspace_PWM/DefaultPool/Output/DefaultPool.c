// ISO-Designer ISO 11783   Version 5.6.2.5533 Jetter AG
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
		XYREF(OutputString_WS, 0, 40),
		'e', 'n',
		'd', 'e',
	ID(Macro_100_perc), TYPEID_MACRO, WORD(8),
		CMD_CHANGE_NUMERIC_VALUE, ID(NumberVariable_PWM_Value), 0, LONG(8191UL),
	ID(Macro_050_perc), TYPEID_MACRO, WORD(8),
		CMD_CHANGE_NUMERIC_VALUE, ID(NumberVariable_PWM_Value), 0, LONG(4095UL),
	ID(Macro_075_perc), TYPEID_MACRO, WORD(8),
		CMD_CHANGE_NUMERIC_VALUE, ID(NumberVariable_PWM_Value), 0, LONG(6143UL),
	ID(Macro_000_perc), TYPEID_MACRO, WORD(8),
		CMD_CHANGE_NUMERIC_VALUE, ID(NumberVariable_PWM_Value), 0, LONG(0UL),
	ID(Macro_025_perc), TYPEID_MACRO, WORD(8),
		CMD_CHANGE_NUMERIC_VALUE, ID(NumberVariable_PWM_Value), 0, LONG(2047UL),
	ID(DataMask_1000), TYPEID_DATAMASK, COLOR_SILVER, ID(ID_NULL), 14, 0, 
		XYREF(InputNumber_PWM_DUTY, 240, 240),
		XYREF(InputNumber_PWM_Value, 40, 240),
		XYREF(OutputString_percent, 400, 240),
		XYREF(OutputNumber_8129, 40, 320),
		XYREF(OutputString_percent, 400, 320),
		XYREF(OutputNumber_100, 240, 320),
		XYREF(LinearBargraph_18000, 0, 400),
		XYREF(Meter_17000, 40, 15),
		XYREF(ArchedBargraph_19000, 200, 15),
		XYREF(Button_100_perc, 400, 120),
		XYREF(Button_075_perc, 320, 120),
		XYREF(Button_050_perc, 240, 120),
		XYREF(Button_025_perc, 160, 120),
		XYREF(Button_000_perc, 80, 120),
	ID(Button_050_perc), TYPEID_BUTTON, WORD(80), WORD(80), 8, 8, 1, 0, 2, 1, 
		XYREF(OutputString_percent, 0, 40),
		XYREF(OutputNumber_050, 0, 0),
		MACRO(EV_KEYRELEASE, Macro_050_perc),
	ID(Button_075_perc), TYPEID_BUTTON, WORD(80), WORD(80), 8, 8, 1, 0, 2, 1, 
		XYREF(OutputString_percent, 0, 40),
		XYREF(OutputNumber_075, 0, 0),
		MACRO(EV_KEYRELEASE, Macro_075_perc),
	ID(Button_000_perc), TYPEID_BUTTON, WORD(80), WORD(80), 8, 8, 1, 0, 2, 1, 
		XYREF(OutputString_percent, 0, 40),
		XYREF(OutputNumber_000, 0, 0),
		MACRO(EV_KEYRELEASE, Macro_000_perc),
	ID(Button_025_perc), TYPEID_BUTTON, WORD(80), WORD(80), 8, 8, 1, 0, 2, 1, 
		XYREF(OutputString_percent, 0, 40),
		XYREF(OutputNumber_025, 0, 0),
		MACRO(EV_KEYRELEASE, Macro_025_perc),
	ID(Button_100_perc), TYPEID_BUTTON, WORD(80), WORD(80), 8, 8, 1, 0, 2, 1, 
		XYREF(OutputString_percent, 0, 40),
		XYREF(OutputNumber_100, 0, 0),
		MACRO(EV_KEYRELEASE, Macro_100_perc),
	ID(InputNumber_PWM_DUTY), TYPEID_INNUM, WORD(150), WORD(30), COLOR(193), ID(FontAttributes_16x16), 0, 
		ID(NumberVariable_PWM_Value), LONG(123UL), LONG(0UL), LONG(8191UL), LONG(0L), 0x40, 0x06, 0x48, 0x3C, 3, 0, 1, 1, 0, 
	ID(InputNumber_PWM_Value), TYPEID_INNUM, WORD(150), WORD(30), COLOR(193), ID(FontAttributes_16x16), 0, 
		ID(NumberVariable_PWM_Value), LONG(123UL), LONG(0UL), LONG(8191UL), LONG(0L), FLOAT_1, 0, 0, 1, 1, 0, 
	ID(OutputString_percent), TYPEID_OUTSTR, WORD(66), WORD(36), COLOR_WHITE, ID(FontAttributes_12x16_B), 1,
		ID(ID_NULL), 1, WORD(4), ' ', '%', ' ', ' ', 0,
	ID(OutputString_WS), TYPEID_OUTSTR, WORD(80), WORD(40), COLOR_WHITE, ID(FontAttributes_WS), 1,
		ID(ID_NULL), 1, WORD(4), 'P', 'W', 'M', ' ', 0,
	ID(OutputNumber_100), TYPEID_OUTNUM, WORD(72), WORD(40), COLOR_WHITE, ID(FontAttributes_12x16), 1,
		ID(ID_NULL), LONG(100UL), LONG(0L), FLOAT_1, 0, 0, 1, 0,
	ID(OutputNumber_8129), TYPEID_OUTNUM, WORD(150), WORD(40), COLOR_WHITE, ID(FontAttributes_12x16), 1,
		ID(ID_NULL), LONG(8191UL), LONG(0L), FLOAT_1, 0, 0, 1, 0,
	ID(OutputNumber_050), TYPEID_OUTNUM, WORD(72), WORD(40), COLOR_WHITE, ID(FontAttributes_12x16), 1,
		ID(ID_NULL), LONG(50UL), LONG(0L), FLOAT_1, 0, 0, 1, 0,
	ID(OutputNumber_075), TYPEID_OUTNUM, WORD(72), WORD(40), COLOR_WHITE, ID(FontAttributes_12x16), 1,
		ID(ID_NULL), LONG(75UL), LONG(0L), FLOAT_1, 0, 0, 1, 0,
	ID(OutputNumber_000), TYPEID_OUTNUM, WORD(72), WORD(40), COLOR_WHITE, ID(FontAttributes_12x16), 1,
		ID(ID_NULL), LONG(0UL), LONG(0L), FLOAT_1, 0, 0, 1, 0,
	ID(OutputNumber_025), TYPEID_OUTNUM, WORD(72), WORD(40), COLOR_WHITE, ID(FontAttributes_12x16), 1,
		ID(ID_NULL), LONG(25UL), LONG(0L), FLOAT_1, 0, 0, 1, 0,
	ID(Meter_17000), TYPEID_OUTMETER, WORD(120), COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, 13, 9, 165, 105, 
		WORD(0), WORD(8191), ID(NumberVariable_PWM_Value), WORD(0), 0, 
	ID(LinearBargraph_18000), TYPEID_OUTLINBAR, WORD(480), WORD(40), COLOR_BLACK, COLOR_RED, 55, 9, 
		WORD(0), WORD(8191), ID(NumberVariable_PWM_Value), WORD(0), ID(ID_NULL), WORD(4095), 0, 
	ID(ArchedBargraph_19000), TYPEID_OUTARCBAR, WORD(120), WORD(120), COLOR_BLACK, COLOR_RED, 19, 165, 105, 
		WORD(15), WORD(0), WORD(8191), ID(NumberVariable_PWM_Value), WORD(0), ID(ID_NULL), WORD(4095), 0, 
	ID(NumberVariable_PWM_Value), TYPEID_VARNUM, LONG(0UL), 
	ID(FontAttributes_12x16), TYPEID_FONTATTR, COLOR_BLACK, 3, 0, 0, 0, 
	ID(FontAttributes_12x16_B), TYPEID_FONTATTR, COLOR_BLACK, 3, 0, 1, 0, 
	ID(FontAttributes_16x16), TYPEID_FONTATTR, COLOR_BLACK, 4, 0, 0, 0, 
	ID(FontAttributes_WS), TYPEID_FONTATTR, COLOR_BLACK, 3, 0, 0, 0, 
}; // isoOP_DefaultPool
