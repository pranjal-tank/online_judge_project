import os
import subprocess
from django.shortcuts import render
from datetime import datetime
from homescr.models import Problems,Testcases,Solutions
from django.core.files.storage import FileSystemStorage
import docker
from django.conf import settings
#problem page url request
def problem_page(request,problem_id):
    problem_detail=Problems.objects.get(id=problem_id)
    problem_testcase=Testcases.objects.get(id=problem_id)
    context={'problem_detail':problem_detail, 'problem_testcase':problem_testcase}
    return render(request,'problempg/problem_page.html',context)

#user code evaluation
def usercode(request,problem_id):
    if request.method == "POST":
        #setting docker client
        docker_client=docker.from_env()
        Running="running"

        problem_testcase=Testcases.objects.get(id=problem_id)
        problem_detail=Problems.objects.get(id=problem_id)
        problem_testcase.problem_output=problem_testcase.problem_output.replace('\r\n','\n').strip() #replacing \r\n by \n in original output to compare it with the usercode output
        testcase_input=bytes(problem_testcase.problem_input,'utf-8') #converting input testcases to bytes to give them as input in subprocess
        output="WA" #setting verdict to WA by default
        lang=""
        res=""

        # if user submitted code in textarea
        if request.POST['user_problem_code']:
            user_problem_code=request.POST['user_problem_code']
            user_problem_code=user_problem_code.replace('\r\n','\n').strip() #replacing \r\n by \n in original output to compare it with the usercode output
            language=request.POST['language']
            lang=str(language)
            #if user code is in python language
            if language == "PYTH3":

                # copying user code in .py file
                filepath = settings.FILES_DIR + "/forpy.py" 
                py_code=open(filepath,"w")
                py_code.write(user_problem_code)
                py_code.close()
                
                # checking if the docker container is running or not
                try:
                    container=docker_client.containers.get('oj-py')
                    container_state=container.attrs['State']
                    container_is_running=container_state['Status']==Running
                    if not container_is_running:
                        subprocess.run(["docker","start","oj-py"],shell=False)
                except docker.errors.NotFound:
                    subprocess.run(["docker","run","-dt","--name","oj-py","python"],shell=False)
                
                # copy/paste the .py file in docker container
                subprocess.run(["docker","cp",filepath,"oj-py:/forpy.py"])
                # interpreting and running the code on given input and taking the output in a variable in bytes
                res=subprocess.run(["docker","exec","-i","oj-py","python","forpy.py"],input=testcase_input,capture_output=True,shell=False)
                # removing the .py file form the docker container
                subprocess.run(["docker","exec","oj-py","rm","forpy.py"],shell=False)

                # checking if the code have errors
                if res.stderr.decode('utf-8') != "":
                   output="CE"
            
            #if user code is in C++ language
            elif language == "C++":

                # copying user code in .cpp file
                filepath = settings.FILES_DIR + "/forcpp.cpp"
                cpp_code=open(filepath,"w")
                cpp_code.write(user_problem_code)
                cpp_code.close()
                
                # checking if the docker container is running or not
                try:
                    container=docker_client.containers.get('oj-cpp')
                    container_state=container.attrs['State']
                    container_is_running=container_state['Status']==Running
                    if not container_is_running:
                        subprocess.run(["docker","start","oj-cpp"],shell=False)
                except docker.errors.NotFound:
                    subprocess.run(["docker","run","-dt","--name","oj-cpp","gcc"],shell=False)
                
                
                # copy/paste the .cpp file in docker container 
                subprocess.run(["docker","cp",filepath,"oj-cpp:/forcpp.cpp"])
                # compiling the code
                res=subprocess.run(["docker","exec","oj-cpp","g++","-o","output","forcpp.cpp"],capture_output=True,shell=False)
                # checking if the code have errors
                if res.stderr.decode('utf-8') != "":
                   output='CE'
                # running the code on given input and taking the output in a variable in bytes
                res=subprocess.run(["docker","exec","-i","oj-cpp","./output"],input=testcase_input,capture_output=True,shell=False)
                # removing the .cpp and .output file form the container
                subprocess.run(["docker","exec","oj-cpp","rm","forcpp.cpp"])
                subprocess.run(["docker","exec","oj-cpp","rm","output"])
                 
            elif language == "C":
                filepath = settings.FILES_DIR + "/forc.c"
                c_code=open(filepath,"w")
                c_code.write(user_problem_code)
                c_code.close()
                 
                try:
                    container=docker_client.containers.get('oj-c')
                    container_state=container.attrs['State']
                    container_is_running=container_state['Status']==Running
                    if not container_is_running:
                        subprocess.run(["docker","start","oj-c"],shell=False)
                except docker.errors.NotFound:
                    subprocess.run(["docker","run","-dt","--name","oj-c","gcc"],shell=False)

                subprocess.run(["docker","cp",filepath,"oj-c:/forc.c"],shell=False)
                res=subprocess.run(["docker","exec","oj-c","g++","-o","output","forc.c"],capture_output=True,shell=False)
                if res.stderr.decode('utf-8') != "":
                   output="CE"
                res=subprocess.run(["docker","exec","-i","oj-c","./output"],input=testcase_input,capture_output=True,shell=False)
                subprocess.run(["docker","exec","oj-c","rm","forc.c"])
                subprocess.run(["docker","exec","oj-c","rm","output"])
        
        elif request.FILES['codefile']:
            user_code_file=request.FILES['codefile']
            fs=FileSystemStorage()
            fs.save(user_code_file.name,user_code_file)
            file_type=str(user_code_file.name)
            py_lan=file_type.find(".py")
            cpp_lan=file_type.find(".cpp")
            c_lan=file_type.find(".c")
            file_path="media/" + user_code_file.name

            if py_lan != -1:
                lang="PYTH3"

                try:
                    container=docker_client.containers.get('oj-py')
                    container_state=container.attrs['State']
                    container_is_running=container_state['Status']==Running
                    if not container_is_running:
                        subprocess.run(["docker","start","oj-py"])
                except docker.errors.NotFound:
                    subprocess.run(["docker","run","-dt","--name","oj-py","python"])

                subprocess.run(["docker","cp",file_path,"oj-py:/forpy.py"])
                res=subprocess.run(["docker","exec","-i","oj-py","python","forpy.py"],input=testcase_input,capture_output=True)
                subprocess.run(["docker","exec","oj-py","rm","forpy.py"])
                os.remove(file_path)
                if res.stderr.decode('utf-8') != "":
                   output="CE"
            
            elif cpp_lan != -1:
                lang="C++"

                try:
                    container=docker_client.containers.get('oj-cpp')
                    container_state=container.attrs['State']
                    container_is_running=container_state['Status']==Running
                    if not container_is_running:
                        subprocess.run(["docker","start","oj-cpp"])
                except docker.errors.NotFound:
                    subprocess.run(["docker","run","-dt","--name","oj-cpp","gcc"])

                subprocess.run(["docker","cp",file_path,"oj-cpp:/forcpp.cpp"])
                res=subprocess.run(["docker","exec","oj-cpp","g++","-o","output","forcpp.cpp"],capture_output=True)
                if res.stderr.decode('utf-8') != "":
                   output="CE" 
                res=subprocess.run(["docker","exec","-i","oj-cpp","./output"],input=testcase_input,capture_output=True)
                subprocess.run(["docker","exec","oj-cpp","rm","forcpp.cpp"])
                subprocess.run(["docker","exec","oj-cpp","rm","output"])
                os.remove(file_path)
            
            elif c_lan != -1:
                lang="C"

                try:
                    container=docker_client.containers.get('oj-c')
                    container_state=container.attrs['State']
                    container_is_running=container_state['Status']==Running
                    if not container_is_running:
                        subprocess.run(["docker","start","oj-c"])
                except docker.errors.NotFound:
                    subprocess.run(["docker","run","-dt","--name","oj-c","gcc"])

                subprocess.run(["docker","cp",file_path,"oj-c:/forc.c"])
                res=subprocess.run(["docker","exec","oj-c","g++","-o","output","forc.c"],capture_output=True)
                if res.stderr.decode('utf-8') != "":
                   output="CE"
                res=subprocess.run(["docker","exec","-i","oj-c","./output"],input=testcase_input,capture_output=True)
                subprocess.run(["docker","exec","oj-c","rm","forc.c"])
                subprocess.run(["docker","exec","oj-c","rm","output"])
                os.remove(file_path)
            else:
                os.remove(file_path)
                context={'problem_detail':problem_detail, 'problem_testcase':problem_testcase,'invalid_file':'Invalid file'}
                return render(request,'problempg/problem_page.html',context)


        res=res.stdout.decode('utf-8') # converting the res variable from bytes to string
        if str(res)==str(problem_testcase.problem_output):
            output="AC" 
        problem_testcase.problem_output+='\n' # added extra line to compare user output having extra ling at the end of their output
        if str(res)==str(problem_testcase.problem_output):
            output="AC"
        
        # creating Solution class objects and showing it on leaderboard
        sol=Solutions()
        sol.problem=Problems.objects.get(id=problem_id)
        sol.solution_problem=problem_detail.problem_nm
        sol.problem_code=problem_detail.problem_code
        sol.problem_diff=problem_detail.problem_diff
        sol.solution_lang=lang
        sol.verdict=output
        sol.uname=request.user.username
        sol.submission_time=datetime.now()
        sol.save()
        latest_lb=Solutions.objects.order_by('-submission_time')[:30]
        context={'verdict':latest_lb,}

    return render(request,'problempg/leaderboard.html',context)
    

        
        

        
     
            


