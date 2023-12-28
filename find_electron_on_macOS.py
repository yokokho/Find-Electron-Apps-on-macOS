import os
import subprocess

def get_app_name(app_path):
    return os.path.basename(app_path)

def get_electron_version(filename):
    try:
        output = subprocess.check_output(f"strings '{filename}' | grep 'Chrome/' | grep -i Electron | grep -v '%s' | sort -u | cut -f 3 -d '/'", shell=True)
        return output.decode().strip()
    except subprocess.CalledProcessError:
        return None

def generate_github_link(version):
    return f"https://github.com/electron/electron/releases/tag/v{version}"

def format_row(app_name, electron_version, filename):
    return f"{app_name:30s} {electron_version:20s} {filename}"

def find_electron_apps():
    try:
        apps = subprocess.check_output("mdfind 'kind:app'", shell=True).decode().splitlines()
        apps = sorted(set(apps))

        print("_" * 100)
        print(format_row("App Name", "Electron Version", "File Name"))
        print("=" * 100)

        for app in apps:
            filename = os.path.join(app, "Contents/Frameworks/Electron Framework.framework/Electron Framework")
            if os.path.isfile(filename):
                app_name = get_app_name(app)
                electron_version = get_electron_version(filename)
                print(format_row(app_name, electron_version, filename))

        print("\n")

        print("=" * 60)
        print("App Name" + " " * 24 + "GitHub Link")
        print("=" * 60)

        for app in apps:
            filename = os.path.join(app, "Contents/Frameworks/Electron Framework.framework/Electron Framework")
            if os.path.isfile(filename):
                app_name = get_app_name(app)
                electron_version = get_electron_version(filename)
                github_link = generate_github_link(electron_version) if electron_version else "Not Found"
                print(f"{app_name:30s} {github_link}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_electron_apps()
