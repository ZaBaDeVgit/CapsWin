[Setup]
AppName=CapsWin
AppVersion=1.0
AppPublisher=CapsWin
DefaultDirName={autopf}\CapsWin
DefaultGroupName=CapsWin
OutputDir={tmp}
OutputBaseFilename=CapsWin_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Files]
Source: "CapsWin.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CapsWin"; Filename: "{app}\CapsWin.exe"
Name: "{commondesktop}\CapsWin"; Filename: "{app}\CapsWin.exe"

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "CapsWin"; ValueData: "{app}\CapsWin.exe"; Flags: uninsdeletevalue
