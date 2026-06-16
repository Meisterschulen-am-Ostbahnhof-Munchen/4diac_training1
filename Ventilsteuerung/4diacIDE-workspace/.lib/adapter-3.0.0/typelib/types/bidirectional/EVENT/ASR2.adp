<?xml version="1.0" encoding="UTF-8"?>
<AdapterType Name="ASR2" Comment="bidirectional Adapter Interface for 2 Events">
	<Identification Standard="61499-1" Description="Copyright (c) 2025 HR Agrartechnik GmbH &#10; &#10;This program and the accompanying materials are made &#10;available under the terms of the Eclipse Public License 2.0 &#10;which is available at https://www.eclipse.org/legal/epl-2.0/ &#10; &#10;SPDX-License-Identifier: EPL-2.0"/>
	<VersionInfo Organization="HR Agrartechnik GmbH" Version="1.0" Author="Franz Höpfinger" Date="2025-05-27"/>
	<CompilerInfo packageName="adapter::types::bidirectional">
		<Import declaration="eclipse4diac::core::TypeHash"/>
	</CompilerInfo>
	<InterfaceList>
		<EventInputs>
			<Event Name="EI_SET" Type="Event" Comment="Set / Switch on"/>
			<Event Name="EI_RESET" Type="Event" Comment="Reset / Switch off"/>
		</EventInputs>
		<EventOutputs>
			<Event Name="EO_SET" Type="Event" Comment="Set / Switch on"/>
			<Event Name="EO_RESET" Type="Event" Comment="Reset / Switch off"/>
		</EventOutputs>
	</InterfaceList>
	<Attribute Name="eclipse4diac::core::TypeHash" Value="''"/>
</AdapterType>
