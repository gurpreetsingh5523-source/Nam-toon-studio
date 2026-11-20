[Setup]
AppId=NaamToonStudio
AppName=Naam Toon Studio
AppVersion={#StudioVersion}
DefaultDirName={localappdata}\Programs\Naam Toon Studio
DefaultGroupName=Naam Toon Studio
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
OutputDir=output
OutputBaseFilename=Naam-Toon-Studio-{#StudioVersion}-Windows-x64-Setup
SetupIconFile=output\studio.ico
UninstallDisplayIcon={app}\NaamToonStudio.exe
Compression=lzma2
SolidCompression=yes

[Files]
Source: "..\dist\NaamToonStudio\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{autoprograms}\Naam Toon Studio"; Filename: "{app}\NaamToonStudio.exe"
