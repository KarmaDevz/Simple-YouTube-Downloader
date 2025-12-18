; --- Inno Setup Script para GeForce Presence ---
; Compilar con Inno Setup Compiler para generar el wizard instalador

[Setup]
AppName=YouTube Downloader
AppVersion=0.0.1
AppPublisher=KarmaDevz
AppPublisherURL=https://github.com/KarmaDevz
DefaultDirName={userappdata}\YouTubeDownloader
PrivilegesRequired=lowest
DefaultGroupName=YouTube Downloader
OutputDir=.
OutputBaseFilename=YouTubeDownloaderSetupv0.0.1
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=_internal\frontend\download.ico
; activa selector de idioma
ShowLanguageDialog=yes


[Files]
Source: "YouTubeDownloader.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs
; copiar también la carpeta locales con en.json, es.json, etc.

[Icons]
; Acceso directo en menú inicio
Name: "{group}\YouTube Downloader"; Filename: "{app}\YouTubeDownloader.exe"; IconFilename: "{app}\_internal\frontend\download.ico"
; Acceso directo en escritorio
Name: "{userdesktop}\YouTube Downloader"; Filename: "{app}\YouTubeDownloader.exe"; IconFilename: "{app}\_internal\frontend\download.ico"
; (Opcional) arranque con Windows
; Name: "{userstartup}\YouTube Downloader"; Filename: "{app}\YouTubeDownloader.exe"; WorkingDir: "{app}"


[Run]
Filename: "{app}\YouTubeDownloader.exe"; Description: "Iniciar YouTube Downloader"; Flags: nowait postinstall skipifsilent
