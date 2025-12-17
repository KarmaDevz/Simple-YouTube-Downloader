; --- Inno Setup Script para GeForce Presence ---
; Compilar con Inno Setup Compiler para generar el wizard instalador

[Setup]
AppName=GeForce Presence
AppVersion=2.1.4
AppPublisher=KarmaDevz
AppPublisherURL=https://github.com/KarmaDevz
DefaultDirName={userappdata}\geforce_presence
PrivilegesRequired=lowest
DefaultGroupName=GeForce Presence
OutputDir=.
OutputBaseFilename=GeForcePresenceSetupv2.1.4
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=_internal\assets\geforce.ico
; activa selector de idioma
ShowLanguageDialog=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
Source: "geforce_presence.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs
; copiar también la carpeta locales con en.json, es.json, etc.
Source: "_internal\lang\*"; DestDir: "{app}\lang"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Acceso directo en menú inicio
Name: "{group}\GeForce Presence"; Filename: "{app}\geforce_presence.exe"; IconFilename: "{app}\_internal\assets\geforce.ico"
; Acceso directo en escritorio
Name: "{userdesktop}\GeForce Presence"; Filename: "{app}\geforce_presence.exe"; IconFilename: "{app}\_internal\assets\geforce.ico"
; (Opcional) arranque con Windows
; Name: "{userstartup}\GeForce Presence"; Filename: "{app}\geforce_presence.exe"; WorkingDir: "{app}"

[Registry]
; Guardar idioma elegido por el usuario en registro
Root: HKCU; Subkey: "Software\GeForcePresence"; ValueType: string; ValueName: "lang"; ValueData: "{language}"; Flags: uninsdeletevalue

[Run]
Filename: "{app}\geforce_presence.exe"; Description: "Iniciar GeForce Presence"; Flags: nowait postinstall skipifsilent
