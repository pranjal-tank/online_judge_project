import subprocess
s=b"hello"
subprocess.run('docker exec oj-cpp sh -c \"cat >> temp.cpp\"',input=s,shell=True)