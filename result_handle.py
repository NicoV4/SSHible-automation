import re
import sys

def result_handeling(verbose, host_results):
    #result handeling
    failed = False
    print("\n")
    for host_data in host_results:
        warn_regex_inverted = False
        fail_regex_inverted = False
        warn_regex = None
        fail_regex = None
        display_name = host_data[0]
        ip = host_data[1]
        port = host_data[2]
        command_name = host_data[3]
        exit_status = host_data[4]

        result = host_data[5]
        ok_code = host_data[6]
        if type(host_data[7]) == type([]): # check if warning has regex specified
            warn_code = host_data[7][0]
            warn_regex = host_data[7][1]
            warn_regex_inverted = host_data[7][2]
        else:
            warn_code = host_data[7]
            
        if type(host_data[8]) == type([]): # check if fail command has regex specified
            fail_code = host_data[8][0]
            fail_regex = host_data[8][1]
            fail_regex_inverted = host_data[8][2]
        else:
            fail_code = host_data[8]
        
        if verbose >= 5:
            print(f"ok_code: {ok_code}")
            print(f"warn_code: {warn_code}")
            print(f"fail_code: {fail_code}")
            print(f"warn_regex: {warn_regex}")
            print(f"warn_code_inverted: {warn_regex_inverted}")
            print(f"fail_regex: {fail_regex}")
            print(f"fail_regex_inverted: {fail_regex_inverted}")
            print(f"result: {result}")
            
        # logic for result status
        if not fail_regex_inverted and fail_regex != None and re.search(fail_regex, result, re.MULTILINE):
            print(f"\033[31m[{command_name}] {display_name} ({ip}:{port}): {fail_code} --> {str(result).strip()}\033[0m")
        elif fail_regex_inverted and fail_regex != None and not re.search(fail_regex, result, re.MULTILINE):
            print(f"\033[31m[{command_name}] {display_name} ({ip}:{port}): {fail_code} --> {str(result).strip()}\033[0m")
        elif exit_status == 0 and not warn_regex_inverted and warn_regex != None and re.search(warn_regex, result, re.MULTILINE):
            print(f"\033[38;5;214m[{command_name}] {display_name} ({ip}:{port}): {warn_code}\033[0m")
        elif exit_status == 0 and warn_regex_inverted and warn_regex != None and not re.search(warn_regex, result, re.MULTILINE):
            print(f"\033[38;5;214m[{command_name}] {display_name} ({ip}:{port}): {warn_code}\033[0m")
        elif exit_status == 0:
            print(f"\033[32m[{command_name}] {display_name} ({ip}:{port}): {ok_code}\033[0m")
        elif exit_status == 3:
            print(f"\033[90m[{command_name}] {display_name} ({ip}:{port}): {result.strip()}\033[0m")
        else:
            failed = True
            print(f"\033[31m[{command_name}] {display_name} ({ip}:{port}): {fail_code} --> {str(result).strip()}\033[0m")

    if failed:
        sys.exit(1)
    else:
        sys.exit(0)