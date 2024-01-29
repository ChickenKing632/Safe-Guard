## SafeGuardAntivirus

SafeGuardAntivirus is an open-source antivirus solution with an integrated firewall to provide comprehensive protection against malware threats.

## Features

- Multi-layered defense system
- Easy to use and customizable
- Proactive threat detection
- Quarantine capabilities

## Installation

### Using PyInstaller (Standalone Executable)

1. Clone the repository:
   ```bash
   git clone https://github.com/ChickenWithACrown/SafeGuardAntivirus.git
   cd SafeGuardAntivirus
   ```

2. Run PyInstaller to create the standalone executable:
   ```bash
   pyinstaller --onefile SafeGuardAntivirusWithFirewall.py
   ```

3. Navigate to the `dist` directory and run the executable:
   ```bash
   cd dist
   ./SafeGuardAntivirusWithFirewall  # On Linux or macOS
   ```

### Using setuptools

1. Clone the repository:
   ```bash
   git clone https://github.com/ChickenWithACrown/SafeGuardAntivirus.git
   cd SafeGuardAntivirus
   ```

2. Install the package:
   ```bash
   pip install .
   ```

3. Run the antivirus program:
   ```bash
   safeguard
   ```

## Usage

- Customize configuration settings in the source code if needed.
- Run the antivirus program based on the chosen installation method.

## Contributing

Feel free to contribute by opening issues, proposing features, or submitting pull requests. Your contributions are welcome!

## Public Domain Dedication (Unlicensed)

This project is dedicated to the public domain using the [Unlicense](LICENSE).
```

This addition makes it clear that your project is dedicated to the public domain using the Unlicense. Adjust any other sections as needed.
