<?xml version="1.0" encoding="UTF-8"?>
<AdapterType Name="Callback" Comment="Message Callback">
	<Identification Standard="61499-1">
	</Identification>
	<VersionInfo Version="1.0" Author="franz" Date="2025-09-06">
	</VersionInfo>
	<CompilerInfo packageName="isobus::pgn::tx">
	</CompilerInfo>
	<InterfaceList>
		<EventInputs>
			<Event Name="REQ" Type="Event" Comment="Request from Socket">
			</Event>
		</EventInputs>
		<EventOutputs>
			<Event Name="CNF" Type="Event" Comment="Confirmation from Plug">
				<With Var="DO1"/>
			</Event>
		</EventOutputs>
		<OutputVars>
			<VarDeclaration Name="DO1" Type="isobus::pgn::CAN_MSG"/>
		</OutputVars>
	</InterfaceList>
</AdapterType>
