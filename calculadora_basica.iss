; Script generado por el Asistente de Inno Setup.
; ¡Consulta la documentación para obtener detalles sobre cómo crear archivos de script de Inno Setup!

#define MyAppName "Calculadora básica"
#define MyAppVersion "1.0"
#define MyAppPublisher "Rayoscompany"
#define MyAppURL "https://rayoscompany.com"
#define MyAppExeName "basic_calculathor1.0.exe"

[Setup]
; El valor de AppId identifica de forma única esta aplicación. No utilices el mismo valor de AppId en instaladores para otras aplicaciones.
; (Para generar un nuevo GUID, haz clic en Herramientas | Generar GUID en el IDE.)
AppId={{26032CA3-9213-438F-9A8A-3EA067D060A3}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Configurar la carpeta de instalación en el directorio local del usuario
DefaultDirName={localappdata}\{#MyAppName}
DefaultGroupName={#MyAppName}
CreateAppDir=yes

; Mostrar información antes de la instalación
InfoBeforeFile=C:\Users\angel\OneDrive\git\calculadora\dist\basic_calculathor1.0\_internal\documentacion.html

; Requerir privilegios mínimos (no requiere administrador)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Configuración de salida del instalador
OutputDir=Calculadora_básica_setup
OutputBaseFilename=calculadora_básica_installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
; Copiar el ejecutable principal
Source: "C:\Users\angel\OneDrive\git\calculadora\dist\basic_calculathor1.0\basic_calculathor1.0.exe"; DestDir: "{app}"; Flags: ignoreversion

; Copiar el actualizador
Source: "C:\Users\angel\OneDrive\git\calculadora\dist\basic_calculathor1.0\update.exe"; DestDir: "{app}"; Flags: ignoreversion

; Copiar la carpeta "_internal" y su contenido
Source: "C:\Users\angel\OneDrive\git\calculadora\dist\basic_calculathor1.0\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

; Nota: No utilices "Flags: ignoreversion" en archivos de sistema compartidos

[Icons]
; Crear un acceso directo en el Menú Inicio
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

; Crear un acceso directo en el Escritorio (opcional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Ejecutar la aplicación después de la instalación
Filename: "{app}\{#MyAppExeName}"; Description: "Ejecutar {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Tasks]
; Opción para crear un icono en el Escritorio
Name: "desktopicon"; Description: "Crear un icono en el Escritorio"; GroupDescription: "Opciones adicionales"; Flags: unchecked

