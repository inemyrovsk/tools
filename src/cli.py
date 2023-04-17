import os
import distro
import logging
import platform
import argparse
import subprocess

logging.basicConfig(level=logging.INFO)


def get_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--install', choices=["base", "infra-tools"], help='install')
    args = parser.parse_args()
    return args


def zip_name(archive_url):
    return archive_url.split('/')[-1]


def wget_download_url(archive_url):
    archive_name = zip_name(archive_url)
    subprocess.call(["wget", "-O", archive_name, archive_url])

    # return obj_name


def env_path():
    return os.environ["PATH"].split(':')[3]  # TODO set path dynamically

def install_packages():
    destination = env_path()
    source = "tools"
    for tool in os.listdir(source):
        subprocess.run(["chmod", "+x", f"./{source}/{tool}"])
        os.rename(f"./{source}/{tool}", f"{destination}/{tool}")

def unzip_archive(archive_url):
    import zipfile
    achive_name = zip_name(archive_url)
    target_folder = env_path()
    with zipfile.ZipFile(achive_name, "r") as zip_ref:
        zip_ref.extractall("tools")



def install_infra_tools():
    terraform_url = "https://releases.hashicorp.com/terraform/1.3.5/terraform_1.3.5_linux_amd64.zip"
    wget_download_url(terraform_url)
    unzip_archive(terraform_url)
    install_packages()


def install_base():
    base_packages = ["wget", "zip", "unzip"]
    # base_packages = ["git", "vim", "zsh", "tmux", "htop", "curl", "wget", "tree", "zip", "unzip"]
    package_manager = installation_method()
    for package in base_packages:
        subprocess.run([package_manager, "install", package, "-y"])


def install_docker():
    pass


def install_ansible():
    pass


def installation_method():
    os_name = os.uname().sysname
    if os_name == 'Linux':
        distribution_name = distro.name()
        if distribution_name == 'Fedora Linux':
            install_method = "dnf"
            return install_method
        elif distribution_name == 'Ubuntu':
            install_method = "apt"
            return install_method


def run_install():
    args = get_args()
    if args.install == "base":
        install_base()
    if args.install == "infra-tools":
        install_infra_tools()


def main():
    args = get_args()
    if args.install:
        run_install()

    # minimal_packages = ["terraform", "wget", "zsh", "tmux", "htop", "curl", "wget", "tree"]
    # if args.minimal:
    #     cmd = "where" if platform.system() == "Windows" else "which"
    #     try:
    #         subprocess.call([cmd, your_executable_to_check_here])
    #     except:
    #         print("No executable")
    #     for package in minimal_packages:
    #         subprocess.run([package_manager, "install", package, "-y"])


if __name__ == '__main__':
    main()
