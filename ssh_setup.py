import paramiko
import sys

def setup_keys():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    agent = paramiko.Agent()
    keys = agent.get_keys()
    if not keys:
        print("\033[31mno ssh-keys found from agent...\033[0m")
        sys.exit(1)
    return client, keys