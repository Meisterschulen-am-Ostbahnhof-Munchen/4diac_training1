# ELF-Libs-Manifest-Logik (OSCAT/OSCAT_adapter), uebertragen aus
# Krauternter/Ventilsteuerung/elf_libs_manifest_lib.sh. Format/Kanonisierung
# sind seit 2026-10-09 durch den Firmware-Code (elf_libs_loader,
# LOGIBUS_integration_datapanel feature/elf-loader) festgelegt - siehe dortige
# Datei fuer die ausfuehrliche Begruendung/Firmware-Verhalten.
#
# Genutzt von make_libs_manifest.sh (rein lokal, kein Netzwerk) und
# make_4diac_training1_deploy.sh (laedt bei ENABLE_ELF_LIBS=1 zusaetzlich ELFs
# + Manifest hoch).
#
# Firmware-Verhalten (SO IMPLEMENTIERT in main.c, von Franz NICHT ausdruecklich
# bestaetigt): existiert eine *.libs.json und ist sie nicht ladbar, startet
# FORTE NICHT, Netzwerk/Dateiserver bleiben aktiv. 192.168.178.55 (AX) wurde
# 2026-10-09 live erfolgreich mit riscv32-ELFs + Manifest getestet - das ist
# also bestaetigt ein S31 mit dieser Firmware. Fuer jeden weiteren Knoten (z.B.
# B) erst SoC + Firmware-Branch mit Franz klaeren, bevor ENABLE_ELF_LIBS dafuer
# eingeschaltet wird - auf S3 fehlt noch die Host-Symboltabelle
# (elf_libs/host/elf_host_symbols_xtensa.cpp), auf P4 sind die riscv32-ELFs
# ungetestet.

# Architektur je Knoten - UNBESTAETIGTER PLATZHALTER (ausser 192.168.178.55,
# siehe oben), muss vor dem ersten echten Einsatz mit Franz gegen die reale
# Hardware abgeglichen werden.
declare -A NODE_ARCH=(
    ["192.168.178.55"]="riscv32"
)

# forte_abi: von Hand erhoehte Nummer, wenn sich FORTE-Basisklassen aendern.
# Quelle: Datei elf_libs/FORTE_ABI im Repo LOGIBUS_integration_datapanel.
FORTE_ABI=3

# Namensraum-Praefix -> Lib-Name. Key ist entweder ein Einzelsegment (z.B.
# "OSCAT", "OSCAT_adapter") oder "Segment1::Segment2" fuer Libs, die aus einem
# gemeinsamen Namensraum herausgeloest wurden (z.B. "adapter::net" ->
# net_adapter).
#
# WICHTIG (2026-10-10, Bestandsaufnahme ueber alle 53 .lib/*/MANIFEST.MF +
# CompilerInfo/packageName der echten .fbt-Dateien, nach den isobus_UT_io_adapter/
# isobus_signalprocessing_adapter-Splits): mehrere 2-Segment-Praefixe werden von
# MEHR ALS EINER Lib gleichzeitig benutzt, der Praefix allein genuegt dort NICHT
# zur Zuordnung - am kritischsten "isobus::UT": isobus_UT, isobus_UT_adapter,
# isobus_UT_io, isobus_UT_io_adapter, isobus_signalprocessing UND
# isobus_signalprocessing_adapter liegen ALLE unter packageName="isobus::UT::...".
# PREFIX_TO_LIB traegt fuer diese Faelle nur die mengenmaessig groesste/
# "Default"-Lib ein, die echten Ausnahmen stehen exakt per Typname in
# TYPE_NAME_TO_LIB (hat in resolve_required_libs() IMMER Vorrang vor dem
# Praefix-Fallback hier).
#
# 2026-10-10 (Franz, Bestandsaufnahme der 82, dann 46 gebauten riscv32-ELFs):
# ALLE Libs unten in LIB_VERSIONS sind bestaetigt echte ladbare Module, inkl.
# "adapter" selbst und net_adapter - die fruehere Annahme "adapter bleibt fest
# in die Firmware gelinkt" gilt NICHT mehr. Nachtrag selben Tags: SafeArithmetic,
# logiBUS_safety, logiBUS_schieber sind nachgezogen (ELF jetzt vorhanden,
# urspruenglich als "kommt noch" angekuendigt), ebenso iec61131-3-bool und
# quarter (vorher Firmware-Basis ohne ELF, jetzt auch gebaut).
# logiBUS_stations braucht dagegen GRUNDSAETZLICH KEIN ELF (reine
# GlobalConstants, kein FORTE-Typecode) - das ist kein offener Punkt, bleibt
# dauerhaft aussen vor. core, events, net, system bleiben Firmware-Basis ohne
# eigenes ELF. Fuer logiBUS_stations/core/events/net/system bewusst KEIN
# PREFIX_TO_LIB-Eintrag.
declare -A PREFIX_TO_LIB=(
    ["BlinkMarine::io"]="BlinkMarine"
    ["DataPanel::Status"]="DataPanel"
    ["DataPanel::io"]="DataPanel"
    ["Funk::io"]="Funk"
    ["OSCAT::Basic"]="OSCAT_Basic"
    ["OSCAT::Building"]="OSCAT_Building"
    ["OSCAT::Network"]="OSCAT_Network"
    ["OSCAT_adapter"]="OSCAT_adapter"
    ["adapter::net"]="net_adapter"
    ["adapter::conversion"]="adapter_conversion"
    ["adapter::events"]="adapter_events"
    ["adapter::iec61131"]="adapter_iec61131-3"
    ["adapter::iec61499"]="adapter_events"
    ["adapter::selection"]="adapter_selection"
    ["adapter::signalprocessing"]="logiBUS_signalprocessing_adapter"
    ["adapter::types"]="adapter_types"
    ["adapter::utils"]="utils_adapter"
    ["adapter::Engineering"]="adapter"
    ["adapter::OverrideK"]="adapter"
    ["adapter::assembling"]="adapter"
    ["adapter::bistableElements"]="adapter"
    ["adapter::bitwiseOperators"]="adapter"
    ["adapter::booleanOperators"]="adapter"
    ["adapter::monostableElements"]="adapter"
    ["adapter::splitting"]="adapter"
    ["eclipse4diac::convert"]="convert"
    ["eclipse4diac::rtevents"]="rtevents"
    ["eclipse4diac::signalprocessing"]="signalprocessing"
    ["eclipse4diac::storage"]="logiBUS_storage"
    ["eclipse4diac::utils"]="utils"
    ["SafeArithmetic::arithmetic"]="SafeArithmetic"
    ["iec61131::arithmetic"]="iec61131-3"
    ["iec61131::arrays"]="iec61131-3"
    ["iec61131::bistableElements"]="iec61131-3"
    ["iec61131::bitwiseOperators"]="iec61131-3"
    ["iec61131::booleanOperators"]="iec61131-3-bool"
    ["iec61131::charString"]="iec61131-3"
    ["iec61131::comparison"]="iec61131-3"
    ["iec61131::conversion"]="iec61131-3"
    ["iec61131::counters"]="iec61131-3"
    ["iec61131::edgeDetection"]="iec61131-3"
    ["iec61131::numerical"]="iec61131-3"
    ["iec61131::selection"]="iec61131-3"
    ["iec61131::timers"]="iec61131-3"
    ["isobus::TC"]="isobus_TC"
    ["isobus::UT"]="isobus_UT"
    ["isobus::pgn"]="isobus_pgn"
    ["isobus::tecu"]="isobus_tecu"
    ["logiBUS::bistableElements"]="logiBUS_utils"
    ["logiBUS::bosch"]="logiBUS_bosch"
    ["logiBUS::drives"]="logiBUS_utils"
    ["logiBUS::esp32"]="logiBUS_esp32"
    ["logiBUS::io"]="logiBUS_io"
    ["logiBUS::safety"]="logiBUS_safety"
    ["logiBUS::signalprocessing"]="logiBUS_signalprocessing_adapter"
    ["logiBUS::storage"]="logiBUS_storage_esp32"
    ["logiBUS::utils"]="logiBUS_utils"
    ["logiBUS::version"]="logiBUS_version"
)

# Exakter FBType-Name -> Lib-Name. Hat in resolve_required_libs() IMMER Vorrang
# vor PREFIX_TO_LIB. Noetig fuer jeden der oben genannten mehrdeutigen
# Praefixe: jeder Typ, der NICHT in der jeweiligen PREFIX_TO_LIB-Default-Lib
# liegt, muss hier namentlich stehen. FBType-Namen sind projektweit eindeutig
# (einzige bekannte Ausnahme: der ungenutzte Platzhalter-Typ "dummy" in
# OSCAT_Building/OSCAT_Network).
#
# isobus::UT::Q ist der dringendste Fall: Q_NumericValue_PHYSA (->
# isobus_UT_adapter) UND NumericValue_PHYSA (-> isobus_UT_io_adapter, Praefix
# isobus::UT::io) werden beide vom bereits live auf 192.168.178.55 laufenden
# boot-files/test_AX_FORTE_PC_AX.fboot benutzt. Vor diesem Eintrag war das ueber
# PREFIX_TO_LIB GAR NICHT aufloesbar (stilles Fallenlassen, kein Fehler/keine
# Warnung) - isobus_UT_adapter/isobus_UT_io_adapter fehlten dadurch komplett
# im generierten Manifest. Franz hat (2026-10-10) bestaetigt, dass alle Libs
# mit gebautem ELF echte ladbare Module sind, siehe LIB_VERSIONS - beide sind
# jetzt vollstaendig eingetragen (LIB_VERSIONS/LIB_DIR_NAME; die requires
# kommen seit 2026-10-10 ohnehin direkt aus MANIFEST.MF, siehe
# lib_requires_of()).
declare -A TYPE_NAME_TO_LIB=(
    # adapter::conversion: Default adapter_conversion, Ausnahme logiBUS_utils_adapter
    ["AQ_TO_AX"]="logiBUS_utils_adapter"
    ["AX_TO_AQ"]="logiBUS_utils_adapter"
    # adapter::events: Default adapter_events, Ausnahme logiBUS_signalprocessing_adapter (*_D_FF_HYS-Familie)
    ["ADI_D_FF_HYS"]="logiBUS_signalprocessing_adapter"
    ["ADI_D_FF_HYS_TMIN"]="logiBUS_signalprocessing_adapter"
    ["AI_D_FF_HYS"]="logiBUS_signalprocessing_adapter"
    ["AI_D_FF_HYS_TMIN"]="logiBUS_signalprocessing_adapter"
    ["ALI_D_FF_HYS"]="logiBUS_signalprocessing_adapter"
    ["ALI_D_FF_HYS_TMIN"]="logiBUS_signalprocessing_adapter"
    ["ALR_D_FF_HYS"]="logiBUS_signalprocessing_adapter"
    ["ALR_D_FF_HYS_TMIN"]="logiBUS_signalprocessing_adapter"
    ["AR_D_FF_HYS"]="logiBUS_signalprocessing_adapter"
    ["AR_D_FF_HYS_TMIN"]="logiBUS_signalprocessing_adapter"
    ["AS_D_FF_HYS"]="logiBUS_signalprocessing_adapter"
    ["AS_D_FF_HYS_TMIN"]="logiBUS_signalprocessing_adapter"
    ["AUDI_D_FF_HYS"]="logiBUS_signalprocessing_adapter"
    ["AUDI_D_FF_HYS_TMIN"]="logiBUS_signalprocessing_adapter"
    ["AUI_D_FF_HYS"]="logiBUS_signalprocessing_adapter"
    ["AUI_D_FF_HYS_TMIN"]="logiBUS_signalprocessing_adapter"
    ["AULI_D_FF_HYS"]="logiBUS_signalprocessing_adapter"
    ["AULI_D_FF_HYS_TMIN"]="logiBUS_signalprocessing_adapter"
    ["AUS_D_FF_HYS"]="logiBUS_signalprocessing_adapter"
    ["AUS_D_FF_HYS_TMIN"]="logiBUS_signalprocessing_adapter"
    # iec61131::selection: Default iec61131-3, Ausnahme iec61131-3-bool
    ["F_MUX_32"]="iec61131-3-bool"
    # isobus::UT: Default isobus_UT, Ausnahmen isobus_UT_adapter/isobus_UT_io/
    # isobus_UT_io_adapter/isobus_signalprocessing/isobus_signalprocessing_adapter
    ["Q_ActiveMask_AUI"]="isobus_UT_adapter"
    ["Q_Attribute_AUDI"]="isobus_UT_adapter"
    ["Q_BackgroundColourAux_AUS"]="isobus_UT_adapter"
    ["Q_BackgroundColour_AUS"]="isobus_UT_adapter"
    ["Q_ChildPosition_AI"]="isobus_UT_adapter"
    ["Q_ExecuteExtendedMacro_AUI"]="isobus_UT_adapter"
    ["Q_ExecuteMacro_AUI"]="isobus_UT_adapter"
    ["Q_NumericValueAux_AUDI"]="isobus_UT_adapter"
    ["Q_NumericValue_AUDI"]="isobus_UT_adapter"
    ["Q_NumericValue_PHYSA"]="isobus_UT_adapter"
    ["Q_NumericValue_PHYSA_LREAL"]="isobus_UT_adapter"
    ["Q_ObjEnableDisable_AB"]="isobus_UT_adapter"
    ["Q_ObjEnableDisable_AX"]="isobus_UT_adapter"
    ["Q_ObjHideShow_AB"]="isobus_UT_adapter"
    ["Q_ObjHideShow_AX"]="isobus_UT_adapter"
    ["Q_Priority_AUS"]="isobus_UT_adapter"
    ["Q_SelectColourMap_AUI"]="isobus_UT_adapter"
    ["Q_SetAudioVolume_AUS"]="isobus_UT_adapter"
    ["Q_SoftKeyMask_AUI"]="isobus_UT_adapter"
    ["Q_StringValue_AIS"]="isobus_UT_adapter"
    ["Attribute_ID"]="isobus_UT_io"
    ["Aux_IE"]="isobus_UT_io"
    ["Aux_IX"]="isobus_UT_io"
    ["Aux_QD"]="isobus_UT_io"
    ["Aux_QX"]="isobus_UT_io"
    ["Aux_Val1_IW"]="isobus_UT_io"
    ["Aux_Val1_QW"]="isobus_UT_io"
    ["Aux_Val2_IW"]="isobus_UT_io"
    ["Button_IE"]="isobus_UT_io"
    ["Button_IX"]="isobus_UT_io"
    ["NumericValue_ID"]="isobus_UT_io"
    ["NumericValue_PHYS"]="isobus_UT_io"
    ["Softkey_IE"]="isobus_UT_io"
    ["Softkey_IX"]="isobus_UT_io"
    ["StringValue_IS"]="isobus_UT_io"
    ["StringValue_IWS"]="isobus_UT_io"
    ["Attribute_IDA"]="isobus_UT_io_adapter"
    ["Aux_IXA"]="isobus_UT_io_adapter"
    ["Aux_QXA"]="isobus_UT_io_adapter"
    ["Button_IXA"]="isobus_UT_io_adapter"
    ["NumericValue_IDA"]="isobus_UT_io_adapter"
    ["NumericValue_PHYSA"]="isobus_UT_io_adapter"
    ["Softkey_IXA"]="isobus_UT_io_adapter"
    ["StringValue_AIS"]="isobus_UT_io_adapter"
    ["StringValue_AIWS"]="isobus_UT_io_adapter"
    ["BargraphSplitFS"]="isobus_signalprocessing"
    ["PositionMarkerFS"]="isobus_signalprocessing"
    ["ReportScrollOffset"]="isobus_signalprocessing"
    ["ScrollFS"]="isobus_signalprocessing"
    ["ScrollFS_PHYS_Button"]="isobus_signalprocessing"
    ["ScrollFS_PHYS_Softkey"]="isobus_signalprocessing"
    ["BargraphSplitFS_AR"]="isobus_signalprocessing_adapter"
    ["PositionMarkerFSA"]="isobus_signalprocessing_adapter"
    # isobus::tecu: Default isobus_tecu, Ausnahme isobus_tecu_adapter (IA_*)
    ["IA_COGSOGRapidUpdate"]="isobus_tecu_adapter"
    ["IA_FHS"]="isobus_tecu_adapter"
    ["IA_FPTO"]="isobus_tecu_adapter"
    ["IA_GBSD"]="isobus_tecu_adapter"
    ["IA_Lighting"]="isobus_tecu_adapter"
    ["IA_MSS"]="isobus_tecu_adapter"
    ["IA_PosDeltaHighPrecRapidUpd"]="isobus_tecu_adapter"
    ["IA_RHS"]="isobus_tecu_adapter"
    ["IA_RPTO"]="isobus_tecu_adapter"
    ["IA_VDS"]="isobus_tecu_adapter"
    ["IA_VP1"]="isobus_tecu_adapter"
    ["IA_WBSD"]="isobus_tecu_adapter"
    # logiBUS::io: Default logiBUS_io, Ausnahme logiBUS_DI_CAN
    ["logiBUS_2_CAN_IX"]="logiBUS_DI_CAN"
    ["logiBUS_2_CAN_IXA"]="logiBUS_DI_CAN"
    # logiBUS::signalprocessing: Default logiBUS_signalprocessing_adapter, Ausnahme logiBUS_signalprocessing (reine Nicht-Adapter-Bausteine)
    ["FIELDBUS_BYTE_TO_SIGNAL"]="logiBUS_signalprocessing"
    ["FIELDBUS_BYTE_TO_SIGNAL_SCALED"]="logiBUS_signalprocessing"
    ["FIELDBUS_DWORD_TO_SIGNAL"]="logiBUS_signalprocessing"
    ["FIELDBUS_DWORD_TO_SIGNAL_SCALED"]="logiBUS_signalprocessing"
    ["FIELDBUS_LWORD_TO_SIGNAL"]="logiBUS_signalprocessing"
    ["FIELDBUS_LWORD_TO_SIGNAL_SCALED"]="logiBUS_signalprocessing"
    ["FIELDBUS_QUARTER_TO_SIGNAL"]="logiBUS_signalprocessing"
    ["FIELDBUS_UDINT_TO_SIGNAL"]="logiBUS_signalprocessing"
    ["FIELDBUS_UDINT_TO_SIGNAL_SCALED"]="logiBUS_signalprocessing"
    ["FIELDBUS_UINT_TO_SIGNAL"]="logiBUS_signalprocessing"
    ["FIELDBUS_UINT_TO_SIGNAL_COMPOUND_SCALE"]="logiBUS_signalprocessing"
    ["FIELDBUS_UINT_TO_SIGNAL_SCALED"]="logiBUS_signalprocessing"
    ["FIELDBUS_ULINT_TO_SIGNAL"]="logiBUS_signalprocessing"
    ["FIELDBUS_ULINT_TO_SIGNAL_SCALED"]="logiBUS_signalprocessing"
    ["FIELDBUS_USINT_TO_SIGNAL"]="logiBUS_signalprocessing"
    ["FIELDBUS_USINT_TO_SIGNAL_SCALED"]="logiBUS_signalprocessing"
    ["FIELDBUS_WORD_TO_SIGNAL"]="logiBUS_signalprocessing"
    ["FIELDBUS_WORD_TO_SIGNAL_COMPOUND_SCALE"]="logiBUS_signalprocessing"
    ["FIELDBUS_WORD_TO_SIGNAL_SCALED"]="logiBUS_signalprocessing"
    ["F_FRACTION_TO_PERCENT"]="logiBUS_signalprocessing"
    ["F_PERCENT_TO_FRACTION"]="logiBUS_signalprocessing"
    ["ILOCK_2_E"]="logiBUS_signalprocessing"
    ["ILOCK_BLOCK"]="logiBUS_signalprocessing"
    ["ILOCK_BLOCK_PROTECT"]="logiBUS_signalprocessing"
    ["ILOCK_CONFLICT_TRIP"]="logiBUS_signalprocessing"
    ["ILOCK_CONFLICT_TRIP_PROTECT"]="logiBUS_signalprocessing"
    ["ILOCK_SWITCH"]="logiBUS_signalprocessing"
    ["ILOCK_SWITCH_PROTECT"]="logiBUS_signalprocessing"
    ["SYS_ONTIME"]="logiBUS_signalprocessing"
    # logiBUS::utils: Default logiBUS_utils, Ausnahmen logiBUS_utils_adapter/quarter/logiBUS_schieber
    ["AnlagenSequenz_06_ADAPTER"]="logiBUS_utils_adapter"
    ["BasicOne_AX"]="logiBUS_utils_adapter"
    ["LinksRechts_AX"]="logiBUS_utils_adapter"
    ["SchieberControl_AX"]="logiBUS_utils_adapter"
    ["SchieberVerriegelungComposite"]="logiBUS_utils_adapter"
    ["sequence_B_08_AX_AX"]="logiBUS_utils_adapter"
    ["sequence_ET_04_04_AX"]="logiBUS_utils_adapter"
    ["sequence_ET_04_AX"]="logiBUS_utils_adapter"
    ["sequence_ET_04_loop_AX"]="logiBUS_utils_adapter"
    ["sequence_ET_05_AX"]="logiBUS_utils_adapter"
    ["sequence_ET_05_loop_AX"]="logiBUS_utils_adapter"
    ["sequence_ET_08_AX"]="logiBUS_utils_adapter"
    ["sequence_ET_08_loop_AX"]="logiBUS_utils_adapter"
    ["sequence_E_04_AX"]="logiBUS_utils_adapter"
    ["sequence_E_04_AX_SR"]="logiBUS_utils_adapter"
    ["sequence_E_04_loop_AX"]="logiBUS_utils_adapter"
    ["sequence_E_05_AX"]="logiBUS_utils_adapter"
    ["sequence_E_05_loop_AX"]="logiBUS_utils_adapter"
    ["sequence_E_08_AX"]="logiBUS_utils_adapter"
    ["sequence_E_08_AX_AX"]="logiBUS_utils_adapter"
    ["sequence_E_08_AX_DM"]="logiBUS_utils_adapter"
    ["sequence_E_08_loop_AX"]="logiBUS_utils_adapter"
    ["sequence_Pattern_04_04_loop_AX"]="logiBUS_utils_adapter"
    ["sequence_Pattern_08_08_loop_AX"]="logiBUS_utils_adapter"
    ["sequence_T_04_AX"]="logiBUS_utils_adapter"
    ["sequence_T_04_loop_AX"]="logiBUS_utils_adapter"
    ["sequence_T_05_AX"]="logiBUS_utils_adapter"
    ["sequence_T_05_loop_AX"]="logiBUS_utils_adapter"
    ["sequence_T_08_ADAPTER"]="logiBUS_utils_adapter"
    ["sequence_T_08_AX"]="logiBUS_utils_adapter"
    ["sequence_T_08_loop_AX"]="logiBUS_utils_adapter"
    ["BOOLS_TO_QUARTERS"]="quarter"
    ["BOOL_TO_QUARTER"]="quarter"
    ["E_SREN"]="quarter"
    ["QUARTERS_TO_BOOLS"]="quarter"
    ["QUARTER_TO_BOOL"]="quarter"
    ["QUARTER_TO_E"]="quarter"
    ["QUARTER_TO_STR_MEASURED"]="quarter"
    ["QUARTER_TO_STR_STATUS"]="quarter"
    ["SchieberControl"]="logiBUS_schieber"
    ["SchieberVerriegelung"]="logiBUS_schieber"
)

# Lib-Version, die aktuell als ELF gebaut/erwartet wird. Quelle: die echten
# MANIFEST.MF unter 4diacIDE-workspace/.lib/<Lib>*/MANIFEST.MF.
#
# 2026-10-10 (Franz): alle Libs unten haben ein gebautes riscv32-ELF unter
# .lib/<Lib>*/elf/riscv32/ und sind bestaetigt echte ladbare Module.
# SafeArithmetic, logiBUS_safety, logiBUS_schieber (urspruenglich "kommt noch")
# sowie iec61131-3-bool und quarter (urspruenglich Firmware-Basis ohne ELF)
# sind noch am selben Tag nachgezogen worden, sobald ihr ELF vorlag.
# logiBUS_stations braucht dagegen GRUNDSAETZLICH KEIN ELF (reine
# GlobalConstants, kein FORTE-Typecode) und wird deshalb absichtlich nie
# eingetragen. Ebenfalls ohne eigenes ELF bleibt die Firmware-Basis core,
# events, net, system. build_libs_manifest() ueberspringt jeden Knoten, der
# einen dieser Namensraeume nutzt, bis auch dafuer ein ELF gebaut ist (bzw.
# dauerhaft bei logiBUS_stations/Firmware-Basis, da dort kein ELF vorgesehen
# ist).
declare -A LIB_VERSIONS=(
    ["BlinkMarine"]="3.0.0"
    ["DataPanel"]="3.0.0"
    ["Funk"]="3.0.0"
    ["OSCAT_Basic"]="0.1.0"
    ["OSCAT_Building"]="0.1.0"
    ["OSCAT_Network"]="0.1.0"
    ["OSCAT_adapter"]="3.0.0"
    ["SafeArithmetic"]="3.0.0"
    ["adapter"]="3.0.0"
    ["adapter_conversion"]="3.0.0"
    ["adapter_events"]="3.0.0"
    ["adapter_iec61131-3"]="3.0.0"
    ["adapter_selection"]="3.0.0"
    ["adapter_types"]="3.0.0"
    ["convert"]="3.0.0"
    ["iec61131-3"]="3.0.0"
    ["iec61131-3-bool"]="3.0.0"
    ["isobus_TC"]="3.0.0"
    ["isobus_UT"]="3.0.0"
    ["isobus_UT_adapter"]="3.0.0"
    ["isobus_UT_io"]="3.0.0"
    ["isobus_UT_io_adapter"]="3.0.0"
    ["isobus_pgn"]="3.0.0"
    ["isobus_signalprocessing"]="3.0.0"
    ["isobus_signalprocessing_adapter"]="3.0.0"
    ["isobus_tecu"]="3.0.0"
    ["isobus_tecu_adapter"]="3.0.0"
    ["logiBUS_DI_CAN"]="3.0.0"
    ["logiBUS_bosch"]="3.0.0"
    ["logiBUS_esp32"]="3.0.0"
    ["logiBUS_io"]="3.0.0"
    ["logiBUS_safety"]="3.0.0"
    ["logiBUS_schieber"]="3.0.0"
    ["logiBUS_signalprocessing"]="3.0.0"
    ["logiBUS_signalprocessing_adapter"]="3.0.0"
    ["logiBUS_storage"]="3.0.0"
    ["logiBUS_storage_esp32"]="3.0.0"
    ["logiBUS_utils"]="3.0.0"
    ["logiBUS_utils_adapter"]="3.0.0"
    ["logiBUS_version"]="3.0.0"
    ["net_adapter"]="3.0.0"
    ["quarter"]="3.0.0"
    ["rtevents"]="3.0.0"
    ["signalprocessing"]="3.0.0"
    ["utils"]="3.0.0"
    ["utils_adapter"]="3.0.0"
)

# Abhaengigkeiten je Lib werden NICHT mehr aus einer von Hand gepflegten
# Tabelle genommen, sondern direkt aus der echten MANIFEST.MF gelesen (siehe
# lib_requires_of() unten) - Range-Format seit 2026-10-09 durch die Firmware
# festgelegt: "^MAJOR.MINOR" (gleiche Major, bei Major 0 zusaetzlich gleiche
# Minor).
#
# 2026-10-10 (Franz, nach echtem Geraete-Fehler auf 192.168.178.55): adapter-
# 3.0.0 scheiterte zur Laufzeit mit "Can't find common
# _ZTVN5forte8iec6113116booleanOperators16FORTE_F_NOT_BOOLE" (die Vtable
# liegt in iec61131-3-bool), weil die bisherige LIB_REQUIRES-Tabelle diese
# Abhaengigkeit fuer "adapter" nicht enthielt - sie war schlicht nicht
# mitgepflegt worden, obwohl adapter-3.0.0/MANIFEST.MF sie schon lange
# deklariert. Eine Tabelle gegen die MANIFEST.MF manuell synchron zu halten
# ist fehleranfaellig, siehe auch 10 WEITERE Libs mit dem gleichen
# Synchronisationsfehler, die dieselbe Pruefung aufdeckte. MANIFEST.MF ist
# jetzt die einzige Quelle.

# Lib-Ordnername unter 4diacIDE-workspace/.lib/ (nicht einheitlich).
declare -A LIB_DIR_NAME=(
    ["BlinkMarine"]="BlinkMarine-3.0.0"
    ["DataPanel"]="DataPanel-3.0.0"
    ["Funk"]="Funk-3.0.0"
    ["OSCAT_Basic"]="OSCAT_Basic-0.1.0"
    ["OSCAT_Building"]="OSCAT_Building-0.1.0"
    ["OSCAT_Network"]="OSCAT_Network-0.1.0"
    ["OSCAT_adapter"]="OSCAT_adapter-3.0.0"
    ["SafeArithmetic"]="SafeArithmetic-3.0.0"
    ["adapter"]="adapter-3.0.0"
    ["adapter_conversion"]="adapter_conversion-3.0.0"
    ["adapter_events"]="adapter_events-3.0.0"
    ["adapter_iec61131-3"]="adapter_iec61131-3-3.0.0"
    ["adapter_selection"]="adapter_selection-3.0.0"
    ["adapter_types"]="adapter_types-3.0.0"
    ["convert"]="convert-3.0.0"
    ["iec61131-3"]="iec61131-3-3.0.0"
    ["iec61131-3-bool"]="iec61131-3-bool-3.0.0"
    ["isobus_TC"]="isobus_TC-3.0.0"
    ["isobus_UT"]="isobus_UT-3.0.0"
    ["isobus_UT_adapter"]="isobus_UT_adapter-3.0.0"
    ["isobus_UT_io"]="isobus_UT_io-3.0.0"
    ["isobus_UT_io_adapter"]="isobus_UT_io_adapter-3.0.0"
    ["isobus_pgn"]="isobus_pgn-3.0.0"
    ["isobus_signalprocessing"]="isobus_signalprocessing-3.0.0"
    ["isobus_signalprocessing_adapter"]="isobus_signalprocessing_adapter-3.0.0"
    ["isobus_tecu"]="isobus_tecu-3.0.0"
    ["isobus_tecu_adapter"]="isobus_tecu_adapter-3.0.0"
    ["logiBUS_DI_CAN"]="logiBUS_DI_CAN-3.0.0"
    ["logiBUS_bosch"]="logiBUS_bosch-3.0.0"
    ["logiBUS_esp32"]="logiBUS_esp32-3.0.0"
    ["logiBUS_io"]="logiBUS_io-3.0.0"
    ["logiBUS_safety"]="logiBUS_safety-3.0.0"
    ["logiBUS_schieber"]="logiBUS_schieber-3.0.0"
    ["logiBUS_signalprocessing"]="logiBUS_signalprocessing-3.0.0"
    ["logiBUS_signalprocessing_adapter"]="logiBUS_signalprocessing_adapter-3.0.0"
    ["logiBUS_storage"]="logiBUS_storage-3.0.0"
    ["logiBUS_storage_esp32"]="logiBUS_storage_esp32-3.0.0"
    ["logiBUS_utils"]="logiBUS_utils-3.0.0"
    ["logiBUS_utils_adapter"]="logiBUS_utils_adapter-3.0.0"
    ["logiBUS_version"]="logiBUS_version-3.0.0"
    ["net_adapter"]="net_adapter-3.0.0"
    ["quarter"]="quarter-3.0.0"
    ["rtevents"]="rtevents-3.0.0"
    ["signalprocessing"]="signalprocessing-3.0.0"
    ["utils"]="utils-3.0.0"
    ["utils_adapter"]="utils_adapter-3.0.0"
)

ELF_DIR="elf-libs"

sha256_of() {
    local f="$1"
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$f" | awk '{print $1}'
    else
        shasum -a 256 "$f" | awk '{print $1}'
    fi
}

sha256_stdin() {
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum | awk '{print $1}'
    else
        shasum -a 256 | awk '{print $1}'
    fi
}

# Liest die benoetigten Lib-Namen aus einem .fboot: zu jedem Type="..."
# zuerst den letzten Segment (den eigentlichen FBType-Namen) exakt gegen
# TYPE_NAME_TO_LIB pruefen (deckt die unter PREFIX_TO_LIB dokumentierten
# Namensraum-Mehrdeutigkeiten ab), erst wenn das nichts liefert den
# Zwei-Segment-Namensraum-Key gegen PREFIX_TO_LIB pruefen (z.B. "adapter::net"),
# dann als Fallback den Einzelsegment-Key (z.B. "OSCAT"), dann transitiv per
# lib_requires_of() (liest MANIFEST.MF) erweitern.
resolve_required_libs() {
    local fboot_file="$1" full name seg1 rest seg2 ns lib req
    declare -A seen=()
    local -a queue=()

    while IFS= read -r full; do
        name="${full##*::}"
        lib="${TYPE_NAME_TO_LIB[$name]:-}"
        if [ -z "$lib" ]; then
            seg1="${full%%::*}"
            rest="${full#*::}"
            if [ "$rest" != "$full" ] && [ "$rest" != "$name" ]; then
                seg2="${rest%%::*}"
                lib="${PREFIX_TO_LIB[${seg1}::${seg2}]:-}"
            fi
            if [ -z "$lib" ]; then
                lib="${PREFIX_TO_LIB[$seg1]:-}"
            fi
        fi
        if [ -n "$lib" ] && [ -z "${seen[$lib]:-}" ]; then
            seen[$lib]=1
            queue+=("$lib")
        fi
    done < <(grep -oE 'Type="[A-Za-z0-9_]+(::[A-Za-z0-9_]+)+"' "$fboot_file" | sed -E 's/^Type="(.*)"$/\1/' | sort -u)

    local i=0
    while [ "$i" -lt "${#queue[@]}" ]; do
        lib="${queue[$i]}"
        i=$((i + 1))
        for req in $(lib_requires_of "$lib"); do
            name="${req%%:*}"
            if [ -z "${seen[$name]:-}" ]; then
                seen[$name]=1
                queue+=("$name")
            fi
        done
    done

    # "${queue[@]}" bei leerem Array nicht einfach an printf uebergeben: ohne
    # Argumente gibt printf trotzdem EINE Leerzeile aus, mapfile liest das als
    # ein Element "" statt eines leeren Arrays.
    if [ "${#queue[@]}" -gt 0 ]; then
        printf '%s\n' "${queue[@]}"
    fi
}

# Liest die in der echten MANIFEST.MF deklarierte Lib-Version
# (Product/VersionInfo/@Version unter 4diacIDE-workspace/.lib/<LibVerzeichnis>/
# MANIFEST.MF). Leer, wenn die Datei fehlt oder nicht geparst werden kann -
# dann wird NICHT geprueft (siehe Aufrufer), statt faelschlich abzubrechen.
mf_version_of() {
    local lib="$1" dir mf
    dir="${LIB_DIR_NAME[$lib]:-$lib}"
    mf="4diacIDE-workspace/.lib/${dir}/MANIFEST.MF"
    [ -f "$mf" ] || { echo ""; return; }
    grep -A1 '<Product ' "$mf" | grep -oE 'Version="[^"]+"' | tail -1 | sed -E 's/Version="([^"]+)"/\1/'
}

# Liest die "requires"-Liste einer Lib ("Name:Range", Leerzeichen-getrennt)
# direkt aus deren MANIFEST.MF statt aus einer von Hand gepflegten Tabelle
# (siehe Begruendung oben bei der alten LIB_REQUIRES-Deklaration). Nur
# <Required SymbolicName="X" Version="V"/>-Eintraege, zu denen es ein
# LIB_VERSIONS-Element (= gebautes ELF) gibt, werden uebernommen -
# Abhaengigkeiten auf Firmware-Basis-Libs (core, events, net, system) ohne
# eigenes ELF gibt es dafuer naturgemaess nichts zu laden. Range ist
# "^Major.Minor" der in MANIFEST.MF fuer diese Abhaengigkeit deklarierten
# Version. Ergebnis wird pro Lib gecacht (gleiche MANIFEST.MF wird sonst bei
# jedem .fboot/jeder transitiven Erweiterung erneut geparst).
declare -A _LIB_REQUIRES_CACHE=()
lib_requires_of() {
    local lib="$1" dir mf line name ver major minor
    local -a result=()
    if [ -n "${_LIB_REQUIRES_CACHE[$lib]+x}" ]; then
        printf '%s\n' "${_LIB_REQUIRES_CACHE[$lib]}"
        return
    fi
    dir="${LIB_DIR_NAME[$lib]:-$lib}"
    mf="4diacIDE-workspace/.lib/${dir}/MANIFEST.MF"
    if [ -f "$mf" ]; then
        while IFS= read -r line; do
            name="$(sed -E 's/.*SymbolicName="([^"]+)".*/\1/' <<<"$line")"
            ver="$(sed -E 's/.*Version="([^"]+)".*/\1/' <<<"$line")"
            [ -n "${LIB_VERSIONS[$name]:-}" ] || continue
            major="${ver%%.*}"
            minor="${ver#*.}"
            minor="${minor%%.*}"
            result+=("${name}:^${major}.${minor}")
        done < <(grep -oE '<Required SymbolicName="[^"]+" Version="[^"]+"' "$mf")
    fi
    # Firmware-Limit MAX_REQ=8 pro Lib (frueher 4, siehe historischer Fehler
    # "invalid requires of OSCAT_adapter" - OSCAT_adapter hat bereits 6
    # requires). Nur eine Warnung hier (build_libs_manifest() macht daraus
    # einen harten Abbruch, siehe dort) - lib_requires_of() wird auch aus der
    # reinen Namensaufloesung heraus aufgerufen, wo ein Abbruch zu frueh waere.
    if [ "${#result[@]}" -gt 8 ]; then
        echo "  WARNUNG: Lib '${lib}' hat ${#result[@]} requires, Firmware erlaubt max. 8 (MAX_REQ)." >&2
    fi
    _LIB_REQUIRES_CACHE[$lib]="${result[*]}"
    printf '%s\n' "${result[*]}"
}

# Findet den lokalen Pfad eines Lib-ELFs: ELF_DIR flach, sonst Repo-Pfad
# 4diacIDE-workspace/.lib/<LibVerzeichnis>/elf/<arch>/<Name>-<Version>-<arch>.elf.
resolve_elf_path() {
    local lib="$1" version="$2" arch="$3" fname dir repo_path
    fname="${lib}-${version}-${arch}.elf"
    if [ -f "${ELF_DIR}/${fname}" ]; then
        echo "${ELF_DIR}/${fname}"
        return
    fi
    dir="${LIB_DIR_NAME[$lib]:-$lib}"
    repo_path="4diacIDE-workspace/.lib/${dir}/elf/${arch}/${fname}"
    if [ -f "$repo_path" ]; then
        echo "$repo_path"
        return
    fi
    echo ""
}

# Baut <programm>.libs.json (Pfad in $3) fuer einen Knoten: $1=Arch,
# $2=Array-Name (nameref) der lokalen "files"-Pfade, $4=Array-Name (nameref)
# der benoetigten Lib-Namen. 0 bei Erfolg (setzt MANIFEST_ELF_PATHS), 1
# (nichts geschrieben) wenn ein ELF fehlt oder ein Firmware-Limit verletzt
# wuerde.
build_libs_manifest() {
    local arch="$1" files_ref="$2" out_path="$3" libs_ref="$4"
    local -n _files="$files_ref"
    local -n _libs="$libs_ref"
    local lib version elf_path missing=0
    declare -A elf_path_of=()

    if [ "${#_libs[@]}" -gt 16 ]; then
        echo "  WARNUNG: ${#_libs[@]} Libs benoetigt, Firmware erlaubt max. 16 - uebersprungen."
        return 1
    fi
    if [ $(( ${#_libs[@]} + ${#_files[@]} )) -gt 64 ]; then
        echo "  WARNUNG: ${#_libs[@]} Libs + ${#_files[@]} Dateien > 64 Eintraege (Firmware-Limit) - uebersprungen."
        return 1
    fi

    local req_count
    for lib in "${_libs[@]}"; do
        req_count=$(lib_requires_of "$lib" | wc -w)
        if [ "$req_count" -gt 8 ]; then
            echo "  WARNUNG: Lib '${lib}' hat ${req_count} requires, Firmware erlaubt max. 8 (MAX_REQ) - uebersprungen."
            return 1
        fi
    done

    local mf_ver
    for lib in "${_libs[@]}"; do
        version="${LIB_VERSIONS[$lib]:-}"
        if [ -z "$version" ]; then
            echo "  WARNUNG: Keine Version fuer Lib '${lib}' in LIB_VERSIONS hinterlegt - uebersprungen."
            return 1
        fi
        mf_ver="$(mf_version_of "$lib")"
        if [ -n "$mf_ver" ] && [ "$mf_ver" != "$version" ]; then
            echo "  WARNUNG: LIB_VERSIONS[${lib}]=${version} stimmt nicht mit MANIFEST.MF (${mf_ver}) ueberein - LIB_VERSIONS aktualisieren. Uebersprungen."
            return 1
        fi
        elf_path="$(resolve_elf_path "$lib" "$version" "$arch")"
        if [ -z "$elf_path" ]; then
            echo "  Hinweis: ELF fehlt lokal (${lib}-${version}-${arch}.elf, weder in ${ELF_DIR}/ noch unter 4diacIDE-workspace/.lib/${LIB_DIR_NAME[$lib]:-$lib}/elf/${arch}/) - uebersprungen."
            missing=1
            continue
        fi
        elf_path_of[$lib]="$elf_path"
    done
    if [ "$missing" = 1 ]; then
        return 1
    fi

    local -a canon_lines=()
    local -a lib_json_entries=()
    for lib in "${_libs[@]}"; do
        elf_path="${elf_path_of[$lib]}"
        version="${LIB_VERSIONS[$lib]}"
        local fname size sha requires_json="[]" req name range first=1
        fname="$(basename "$elf_path")"
        size="$(wc -c < "$elf_path" | tr -d ' ')"
        sha="$(sha256_of "$elf_path")"
        canon_lines+=("${fname}:${sha}")

        requires_json="["
        for req in $(lib_requires_of "$lib"); do
            name="${req%%:*}"
            range="${req#*:}"
            if [ "$first" = 1 ]; then first=0; else requires_json+=","; fi
            requires_json+="{\"name\":\"${name}\",\"range\":\"${range}\"}"
        done
        requires_json+="]"

        lib_json_entries+=("{\"name\":\"${lib}\",\"version\":\"${version}\",\"file\":\"${fname}\",\"size\":${size},\"sha256\":\"${sha}\",\"requires\":${requires_json}}")
    done

    local -a file_json_entries=()
    local f fname size sha
    for f in "${_files[@]}"; do
        fname="$(basename "$f")"
        size="$(wc -c < "$f" | tr -d ' ')"
        sha="$(sha256_of "$f")"
        canon_lines+=("${fname}:${sha}")
        file_json_entries+=("{\"file\":\"${fname}\",\"size\":${size},\"sha256\":\"${sha}\"}")
    done

    local dup_check
    dup_check="$(printf '%s\n' "${canon_lines[@]%%:*}" | sort | uniq -d)"
    if [ -n "$dup_check" ]; then
        echo "  WARNUNG: Doppelte Dateinamen zwischen libs[] und files[] (${dup_check}) - uebersprungen."
        return 1
    fi

    # -t: -k1,1: nach dem Dateiname-Feld sortieren (vor dem ersten ":"), nicht
    # nach der ganzen Zeile - muss exakt der Sortierung in cmp_hashed()
    # (elf_libs_loader.c, sortiert nur ueber .name) entsprechen.
    local manifest_sha
    manifest_sha="$(printf '%s\n' "${canon_lines[@]}" | LC_ALL=C sort -t: -k1,1 | sha256_stdin)"

    # manifest_sha256 haengt nur von den canon_lines (Dateiname:sha256 je
    # Lib/Datei) ab, nicht vom Text dieser JSON-Datei selbst - Pretty-Print
    # (Einrueckung/Zeilenumbrueche) aendert daran nichts und ist fuer jeden
    # konformen JSON-Parser (auch den der Firmware) bedeutungslos, macht die
    # Datei fuer Menschen aber lesbar. python3 ist ueber die restliche
    # Pipeline (GcfScript.py etc.) ohnehin Voraussetzung.
    local compact_json
    compact_json="$(
        printf '{'
        printf '"format":1,'
        printf '"forte_abi":%s,' "$FORTE_ABI"
        printf '"arch":"%s",' "$arch"
        printf '"libs":[%s],' "$(IFS=,; echo "${lib_json_entries[*]}")"
        printf '"files":[%s],' "$(IFS=,; echo "${file_json_entries[*]}")"
        printf '"manifest_sha256":"%s",' "$manifest_sha"
        printf '"signature":null'
        printf '}'
    )"
    # stdout.buffer statt print()/json.dump(): auf Windows uebersetzt
    # Text-Mode-stdout "\n" sonst automatisch zu "\r\n" (CRLF), das Repo
    # erwartet aber LF-Zeilenenden wie bei allen anderen generierten Dateien.
    if ! python3 -c 'import json, sys; sys.stdout.buffer.write((json.dumps(json.load(sys.stdin), indent=2) + "\n").encode())' <<<"$compact_json" > "$out_path"; then
        echo "  WARNUNG: Pretty-Print des Manifests fehlgeschlagen (python3) - uebersprungen."
        rm -f "$out_path"
        return 1
    fi

    local manifest_size
    manifest_size="$(wc -c < "$out_path" | tr -d ' ')"
    if [ "$manifest_size" -gt 65536 ]; then
        echo "  WARNUNG: Manifest ${manifest_size} Bytes > 64 KB (Firmware-Limit) - uebersprungen."
        rm -f "$out_path"
        return 1
    fi

    MANIFEST_ELF_PATHS=()
    for lib in "${_libs[@]}"; do
        MANIFEST_ELF_PATHS+=("${elf_path_of[$lib]}")
    done
    return 0
}
