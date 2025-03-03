// ISO-Designer ISO 11783   Version 5.7.0.6283 Bucher Automation AG
// Do not change!

#define WorkingSet_0_Offset                                     1
#define Macro_Go_To_DataMask_M1_Offset                         21
#define Macro_Go_To_DataMask_M2_Offset                         34
#define DataMask_M1_Offset                                     47
#define DataMask_M2_Offset                                    157
#define AlarmMask_A1_low_Offset                               177
#define AlarmMask_A2_medium_Offset                            193
#define AlarmMask_A3_high_Offset                              209
#define Container_B_Offset                                    225
#define Container_low_Offset                                  247
#define Container_medium_Offset                               275
#define Container_high_Offset                                 303
#define SoftKeyMask_S1_Offset                                 331
#define SoftKey_F1_Offset                                     361
#define SoftKey_F2_Offset                                     374
#define SoftKey_F3_Offset                                     387
#define SoftKey_F4_Offset                                     400
#define SoftKey_F5_Offset                                     413
#define SoftKey_F6_Offset                                     426
#define SoftKey_F7_Offset                                     439
#define SoftKey_F8_Offset                                     452
#define SoftKey_F9_Offset                                     465
#define SoftKey_F10_Offset                                    478
#define SoftKey_F11_Offset                                    491
#define SoftKey_F12_Offset                                    504
#define Button_A1_Offset                                      517
#define Button_A2_Offset                                      544
#define InputNumber_I1_Offset                                 571
#define InputNumber_I2_Offset                                 609
#define OutputString_WorkingSet_0_Offset                      647
#define OutputString_SoftKey_F1_Offset                        676
#define OutputString_SoftKey_F2_Offset                        703
#define OutputString_SoftKey_F3_Offset                        730
#define OutputString_SoftKey_F4_Offset                        757
#define OutputString_SoftKey_F5_Offset                        784
#define OutputString_SoftKey_F6_Offset                        811
#define OutputString_SoftKey_F7_Offset                        838
#define OutputString_SoftKey_F8_Offset                        865
#define OutputString_SoftKey_F9_Offset                        892
#define OutputString_SoftKey_F10_Offset                       919
#define OutputString_SoftKey_F11_Offset                       947
#define OutputString_SoftKey_F12_Offset                       975
#define OutputString_DataMask_M1_Offset                      1003
#define OutputString_DataMask_M2_Offset                      1031
#define OutputString_Go_To_DataMask_M1_Offset                1059
#define OutputString_Go_To_DataMask_M2_Offset                1093
#define OutputString_Button_A1_Offset                        1127
#define OutputString_Button_A2_Offset                        1153
#define OutputString_OutputNumber_N1_Offset                  1179
#define OutputString_OutputNumber_N2_Offset                  1211
#define OutputString_InputNumber_I1_Offset                   1243
#define OutputString_InputNumber_I2_Offset                   1274
#define OutputNumber_N1_Offset                               1305
#define OutputNumber_N2_Offset                               1334
#define Line_W_Offset                                        1363
#define Line_S_Offset                                        1374
#define Rectangle_black_Offset                               1385
#define Rectangle_grey_Offset                                1398
#define Rectangle_yellow_Offset                              1411
#define Rectangle_red_Offset                                 1424
#define Logos_icon_Offset                                    1437
#define information_Offset                                   1966
#define alert_Offset                                         6883
#define Caution_Offset                                      11800
#define FontAttributes_6x8_Offset                           16717
#define FontAttributes_8x12_Offset                          16725
#define FontAttributes_12x16_Offset                         16733
#define FontAttributes_23003_Offset                         16741
#define LineAttributes_black_Offset                         16749
#define LineAttributes_black_3_Offset                       16757
#define LineAttributes_grey_3_Offset                        16765
#define LineAttributes_yellow_3_Offset                      16773
#define LineAttributes_red_3_Offset                         16781
#define FillAttributes_25000_Offset                         16789
#define ObjectPointer_P1_Offset                             16797
#define AuxFunction2_X1_Offset                              16802

#define ISO_OP_MEMORY_CLASS

#define ISO_OP_DefaultPool_Size  16814
extern const unsigned char ISO_OP_MEMORY_CLASS isoOP_DefaultPool[];

#define ISO_OP_DefaultPool_ObjectNumber     76
extern const unsigned long ISO_OP_MEMORY_CLASS isoOP_DefaultPool_Offset[];
extern const unsigned long ISO_OP_MEMORY_CLASS isoOP_DefaultPool_Offset_Id[];
#define ISO_OP_DefaultPool_Scale_Offset      1

#define ID_NULL  0xFFFF

#define TYPEID_WORKSET        0
#define TYPEID_DATAMASK       1
#define TYPEID_ALARMMASK      2
#define TYPEID_CONTAINER      3
#define TYPEID_SKEYMASK       4
#define TYPEID_SOFTKEY        5
#define TYPEID_BUTTON         6
#define TYPEID_INBOOL         7
#define TYPEID_INSTR          8
#define TYPEID_INNUM          9
#define TYPEID_INLIST        10
#define TYPEID_OUTSTR        11
#define TYPEID_OUTNUM        12
#define TYPEID_OUTLINE       13
#define TYPEID_OUTRECT       14
#define TYPEID_OUTELLIPSE    15
#define TYPEID_OUTPOLY       16
#define TYPEID_OUTMETER      17
#define TYPEID_OUTLINBAR     18
#define TYPEID_OUTARCBAR     19
#define TYPEID_OUTPICT       20
#define TYPEID_VARNUM        21
#define TYPEID_VARSTR        22
#define TYPEID_FONTATTR      23
#define TYPEID_LINEATTR      24
#define TYPEID_FILLATTR      25
#define TYPEID_INPATTR       26
#define TYPEID_OBJPTR        27
#define TYPEID_MACRO         28
#define TYPEID_AUXFUNC       29
#define TYPEID_AUXINP        30
#define TYPEID_AUXFUNC2      31
#define TYPEID_AUXINP2       32
#define TYPEID_AUXPTR        33
#define TYPEID_WINMASK       34
#define TYPEID_KEYGROUP      35
#define TYPEID_GRPHCTXT      36
#define TYPEID_OUTLIST       37
#define TYPEID_EXTINPATTR    38
#define TYPEID_COLORMAP      39
#define TYPEID_OBJLBLREF     40
#define TYPEID_EXTOBJDEF     41
#define TYPEID_EXTREFNAME    42
#define TYPEID_EXTOBJPTR     43
#define TYPEID_ANIMATION     44
#define TYPEID_COLORPAL      45
#define TYPEID_GRAPHDATA     46
#define TYPEID_WSSPECIAL     47
#define TYPEID_SCALEGRAPH    48

#define EV_REFRESH            0
#define EV_ACT                1
#define EV_DEACT              2
#define EV_SHOW               3
#define EV_HIDE               4
#define EV_ENABLE             5
#define EV_DISABLE            6
#define EV_CHGACTMASK         7
#define EV_CHGSKEYMASK        8
#define EV_CHGATTR            9
#define EV_CHGBKCOLOR        10
#define EV_CHGFONTATTR       11
#define EV_CHGLINEATTR       12
#define EV_CHGFILLATTR       13
#define EV_CHGCHILDLOC       14
#define EV_CHGSIZE           15
#define EV_CHGVAL            16
#define EV_CHGPRIOR          17
#define EV_CHGENDPNT         18
#define EV_SELINPUT          19
#define EV_DESELINPUT        20
#define EV_ESC               21
#define EV_ENTERVAL          22
#define EV_ENTERCHGVAL       23
#define EV_KEYPRESS          24
#define EV_KEYRELEASE        25
#define EV_CHGCHILDPOS       26

#define CMD_HIDE_SHOW               160
#define CMD_ENABLE_DISABLE          161
#define CMD_SELECT_INPUT_OBJECT     162
#define CMD_CONTROL_AUDIO_DEVICE    163
#define CMD_SET_AUDIO_VOLUME        164
#define CMD_CHANGE_CHILD_LOCATION   165
#define CMD_CHANGE_SIZE             166
#define CMD_CHANGE_BACKGROUND_COLOR 167
#define CMD_CHANGE_NUMERIC_VALUE    168
#define CMD_CHANGE_END_POINT        169
#define CMD_CHANGE_FONT_ATTRIBUTES  170
#define CMD_CHANGE_LINE_ATTRIBUTES  171
#define CMD_CHANGE_FILL_ATTRIBUTES  172
#define CMD_CHANGE_ACTIVE_MASK      173
#define CMD_CHANGE_SOFT_KEY_MASK    174
#define CMD_CHANGE_ATTRIBUTE        175
#define CMD_CHANGE_PRIORITY         176
#define CMD_CHANGE_LIST_ITEM        177
#define CMD_CHANGE_STRING_VALUE     179
#define CMD_CHANGE_CHILD_POSITION   180
#define CMD_SET_OBJECT_LABEL        181
#define CMD_CHANGE_POLYGON_POINT    182
#define CMD_CHANGE_POLYGON_SCALE    183
#define CMD_GRAPHICS_CONTEXT        184
#define CMD_GET_ATTRIBUTE           185
#define CMD_SELECT_COLOURMAP_OR_PALETTE 186
#define CMD_EXECUTE_EXTENDED_MACRO  188
#define CMD_LOCK_UNLOCK_MASK        189
#define CMD_EXECUTE_MACRO           190

#define COLOR_BLACK       0
#define COLOR_WHITE       1
#define COLOR_GREEN       2
#define COLOR_TEAL        3
#define COLOR_MAROON      4
#define COLOR_PURPLE      5
#define COLOR_OLIVE       6
#define COLOR_SILVER      7
#define COLOR_GREY        8
#define COLOR_BLUE        9
#define COLOR_LIME       10
#define COLOR_CYAN       11
#define COLOR_RED        12
#define COLOR_MAGENTA    13
#define COLOR_YELLOW     14
#define COLOR_NAVY       15

#define FLOAT_1      0x00, 0x00, 0x80, 0x3F
#define FLOAT_10     0x00, 0x00, 0x20, 0x41
#define FLOAT_100    0x00, 0x00, 0xC8, 0x42
#define FLOAT_1000   0x00, 0x00, 0x7A, 0x44
#define FLOAT_0_1    0xCD, 0xCC, 0xCC, 0x3D
#define FLOAT_0_01   0x0A, 0xD7, 0x23, 0x3C
#define FLOAT_0_001  0x6F, 0x12, 0x83, 0x3A
