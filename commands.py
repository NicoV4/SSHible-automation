#!/usr/bin/env python3

from main import *

if __name__ == "__main__":
    username = "admin" #your username that will be used to log into hosts
    exclude_list = [] #list of hosts that will be excluded

    commands_map = {
        # job_name : ["distro", "command", "exit status 0 output", ["warning output", "regex filter", "regex inverted"], ["exit 1 status output", "regex filter", "regex inverted"]]
        "update": [
            ["alpine", "sudo apk update", "Aldready up to date", "Updated", "Error updating"],
            ["arch", "sudo pacman -Syy && sudo yum -Syy", "Aldready up to date", "Updated", "Error updating"],
            ["debian", "sudo apt update", "Aldready up to date", "Updated", ["Error updating", "^Err", False]],
            ["ubuntu", 'sudo apt update', "Aldready up to date", "Updated", ["Error updating", "^Err", False]],
            ["almalinux", "sudo yum update -y", "Aldready up to date", ["Updated", r"Nothing to do", True], "Error updating"],
            ],
        
        "upgrade": [
            ["alpine", "sudo apk upgrade --no-interactive -vv", "Aldready up to date", "Upgraded", "Error upgrading"],
            ["arch", "sudo pacman -Syu --no-confirm && sudo yay -Syu --no-confirm", "Aldready up to date", "Upgraded", "Error upgrading"],
            ["ubuntu", "sudo apt upgrade -y", "Aldready up to date", ["Upgraded", "^Unpacking", False], "Error upgrading"],
            ["debian", "sudo apt upgrade -y", "Aldready up to date", ["Upgraded", "^Unpacking", False], "Error upgrading"],
            ["almalinux", "sudo yum upgrade -y", "Aldready up to date", ["Upgraded", r"Nothing to do", True], "Error upgrading"],
            ],
        
        "reboot_if_req": [
            ["alpine", "apk list --upgradable | grep -E 'linux-lts|musl|busybox' && sudo reboot && echo 'rebooting...'; exit 0", "No reboot needed", ["Rebooting", "rebooting...", False], "Failed rebooting system"],
            ["arch", "checkupdates | grep -E 'linux|glibc|systemd' && sudo reboot && echo 'rebooting...'; exit 0", "No reboot needed", ["Rebooting", "rebooting...", False], "Failed rebooting system"],
            ["ubuntu", "test -f /var/run/reboot-required && sudo reboot && echo 'rebooting...'; exit 0", "No reboot needed", ["Rebooting", "rebooting...", False], "Failed rebooting system"],
            ["debian", "test -f /var/run/reboot-required && sudo reboot && echo 'rebooting...'; exit 0", "No reboot needed", ["Rebooting", "rebooting...", False], "Failed rebooting system"],
            ["almalinux", "needs-restarting -r && sudo reboot && echo 'rebooting...'; exit 0", "No reboot needed", ["Rebooting", "rebooting...", False], "Failed rebooting system"],
        ]

    }

    main(username, exclude_list, commands_map, sys.argv)
