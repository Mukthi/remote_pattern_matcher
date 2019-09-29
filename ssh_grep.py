import csv
import os
import paramiko
import sys


if len(sys.argv) < 3:
    print ("args missing")
    sys.exit(1)

hostname = sys.argv[1]
password = sys.argv[2]

username = "workmachine"
port = 22

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)

    client.connect(hostname, port=port, username=username, password=password)

    for dirs in os.listdir(os.getcwd()):
        if dirs.startswith('output') and os.path.isdir(dirs):
            results = []
            with open(os.path.join(dirs, 'myinputfile.ini')) as fr:
                for lines in fr:
                    hash_filename = lines.split('|')[1].strip('\n')
                    filepath = lines.split('|')[0]
                    cmd = 'cat /home/workmachine/database/files/{} | grep -i mypattern'.format(hash_filename)
                    stdin, stdout, stderr = client.exec_command(cmd)
                    match = str(stdout.read())
                    if 'olkswagen' in match:
                        print (filepath, hash_filename, match)
                        results.append([filepath, hash_filename, match])
                    print ("*"*20)

            with open('myresults.csv', 'a', newline='') as csvfile:
                mywriter = csv.writer(csvfile, delimiter='|',
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for result in results:
                    mywriter.writerow(result)

except Exception as e:
    print (e)

finally:
    client.close()
