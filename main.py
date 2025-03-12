
import sys
from hosts import host_list
import logging
from result_handle import result_handeling
from ssh_setup import setup_keys
from args_handle import arg_handler
from host_class import REMOTE_HOST

def main(username, exclude_list, commands_map, args):
    host_not_in_inv = []
    client, keys = setup_keys() # setup ssh-agent keys
    host_limiter, limit_hosts, verbose = arg_handler(args) # handle arguments
    
    if verbose >= 4:
        logging.basicConfig(level=logging.DEBUG)
    
    if host_limiter and limit_hosts: # check if limited hosts have been specified
        for l_host in limit_hosts: #loop trough specified hosts
            for i in host_list:
                if i[0] == l_host:
                    host_not_in_inv.append(l_host)
        # exit if any specified hosts in limiter are not configured in host list
        if not host_not_in_inv:
            for missing_host in host_not_in_inv:
                print(f"host not found in inventory: {missing_host}")
            sys.exit(1)
    
    for host in host_list: #loop trough hosts list
        if host_limiter and limit_hosts: # if host limit specified
            if host[0] not in limit_hosts: # if host configured host is not specified in limiter skip
                continue
        if host[0] not in exclude_list: # if host is not specified in exclude list
            host_obj = REMOTE_HOST(host[0], host[1], host[2], username, keys, client, host_results) # create host object
            host_distro = host_obj.get_distro() # get the distro of current host
            
            #loop trough list of commands for each distro
            for command_list in commands_map:
                for command in commands_map[command_list]:
                    expected_distro = command[0]
                    command_exec = command[1] #command to execute
                    ok_code = command[2]
                    warn_code = command[3]
                    fail_code = command[4]
                    host_obj.set_exit_codes(ok_code, warn_code, fail_code) # set codes in host object

                    if host_distro == "UNKNOWN": # if failed to retrieve distro
                        break
                    elif host_distro == expected_distro:
                        host_obj.run_command(command_exec, command_list, ok_code, warn_code, fail_code, verbose) # run commmand on remote host
        else:
            host_results.append([host[0], host[1], host[2], "INFO", 3, "EXCLUDED", ok_code, warn_code, fail_code]) # host was in exclude list
    client.close()
    result_handeling(verbose, host_results)


if __name__ != "__main__":
    host_results = []