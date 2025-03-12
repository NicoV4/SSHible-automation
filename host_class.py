class REMOTE_HOST:
    def __init__(self, host_display_name, hostname, port, username, keys, client, host_results):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.keys = keys
        self.display_name = host_display_name
        self.global_result_list = host_results
        self.client = client
        self.distro = "UNKNOWN"
    
    def get_distro(self):
        try:
            self.distro = self.get_data('source /etc/os-release && echo "$ID"')
        except Exception as err:
            self.distro = "UNKNOWN"
            self.global_result_list.append([self.display_name, self.hostname, self.port, "Find-Distro", 1, err, "", "", "FAILED RETRIEVING OS"])
        return self.distro

    def get_data(self, command):
        for key in self.keys:
            self.client.connect(self.hostname, self.port, self.username, pkey=key)
            stdin, stdout, stderr = self.client.exec_command(command, timeout=300)
            data = stdout.read().decode().strip()
            return data

    def set_exit_codes(self, ok_code, warn_code, fail_code):
        self.ok_code = ok_code
        self.warn_code = warn_code
        self.fail_code = fail_code

    def run_command(self, command, command_name, ok_code, warn_code, fail_code, verbose=False):
        for key in self.keys: # loop trough ssh-keys
            if verbose >= 2:
                print(f"{self.username}@{self.display_name}> {command}")
            tmp_error = ""
            tmp_out = ""
            try:
                self.client.connect(self.hostname, self.port, self.username, pkey=key, timeout=300) #connect to host
                if verbose >= 3:
                    print(self.client)
                stdin, stdout, stderr = self.client.exec_command(command, timeout=300) # execute command

                for line in iter(stdout.readline, ""): # loop trough stdout of running command
                    tmp_out+=(line)
                
                for line in iter(stderr.readline, ""): # loop trough stderr of running command
                    tmp_error+=(line)
                
                if verbose >= 1:
                    if tmp_out:
                        print(f"OUTPUT:\n{tmp_out}")
                    if tmp_error:
                        print(f"ERROR:\n{tmp_error}")
                
            except Exception as err:
                if verbose >= 1:
                    print(f"[FAILED] while trying to run command -> {err}")
                tmp_error = err
            
            exit_status = stdout.channel.recv_exit_status()  # Waits for command to finish
            if exit_status == 0:
                self.global_result_list.append([self.display_name, self.hostname, self.port, command_name, 0, str(tmp_out).strip(), ok_code, warn_code, fail_code])
                return
            else:
                self.global_result_list.append([self.display_name, self.hostname, self.port, command_name, 1, str(tmp_error).strip(), ok_code, warn_code, fail_code])
                return