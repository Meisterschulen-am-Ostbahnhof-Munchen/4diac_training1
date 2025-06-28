<?xml version="1.0" encoding="UTF-8"?>
<AdapterType Name="ASR2" Comment="bidirectional Adapter Interface for 2 Events">
	<Identification Standard="61499-1">
	</Identification>
	<VersionInfo Version="1.0" Author="franz" Date="2025-05-27">
	</VersionInfo>
	<CompilerInfo>
	</CompilerInfo>
	<InterfaceList>
		<EventInputs>
			<Event Name="EI_SET" Type="Event" Comment="Set / Switch on">
			</Event>
			<Event Name="EI_RESET" Type="Event" Comment="Reset / Switch off">
			</Event>
		</EventInputs>
		<EventOutputs>
			<Event Name="EO_SET" Type="Event" Comment="Set / Switch on">
			</Event>
			<Event Name="EO_RESET" Type="Event" Comment="Reset / Switch off">
			</Event>
		</EventOutputs>
	</InterfaceList>
</AdapterType>
