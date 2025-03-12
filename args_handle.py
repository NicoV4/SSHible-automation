import sys
import re

def arg_handler(args):
    verbose = 0
    host_limiter = False
    hosts = ""
    skip_arg = False
    
    for i in range(len(args)):
        if i != 0 and not skip_arg:
            if args[i] == "-l":
                host_limiter = True
                try:
                    hosts = args[i+1]
                except IndexError:
                    print("No hosts given")
                if "," in hosts:
                    hosts = hosts.split(",")
                else:
                    hosts = [hosts]
                skip_arg = True
            elif args[i] == "--help" or args[i] == "-help" or args[i] == "-h":
                print("""Usage: main.py [options]
-v\t|\tuse verbosity, add more 'v' for extra verbosity
-l\t|\tlimit hosts, example: -l host1,host2,host3""")
                sys.exit(1)
            elif args[i][:2] == "-v":
                if bool(re.fullmatch(r'v*-v*', args[i])):
                    verbose = args[i].count("v")
            else:
                print(f"parameter not found: {args[i]}\tuse --help for options")
                sys.exit(1)
        elif skip_arg:
            skip_arg = False
        
        
    return host_limiter, hosts, verbose