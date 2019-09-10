# calender
### reference information
#### ref: http://www.tornadoweb.org
####      https://minzkraut.com/2016/11/23/making-a-simple-spritesheet-generator-in-python
### The default deployment path is /home/irteam/apps/, and if you want to change the deployment path, please modify the configuration file
#### nginx.conf setting.py
### Using the default irteam user to boot by default 
### python version 3.6.3

1. install miniconda2(python2.7 env) to /home1/irteam/miniconda2 and add /home1/irteam/miniconda2/bin to $PATH; install miniconda3(python3.6 env) to /home1/irteam/miniconda3

   refer https://conda.io/miniconda.html 
   
2. use pip to install supervisor, superlance (python2); install the modules in requirements.txt to python3

   pngdefry: pip install ./externals/pngdefry-0.4-fixed.tar.gz (to python3)

   refer https://pip.pypa.io/en/stable/user_guide/#installing-packages

3. clone this repository and cd calender/                               

4. sh autobuild.sh #build and install

5. cp calender/constants/constants.XXX to calender/constants.py (XXX is your run-env)

6. simple running

   ./oneapp.calender.ctl start #(./oneapp.calender.ctl stop for stop)
   
7. product running

   supervisord -c supervisord/supervisor.conf
   
   refer http://supervisord.org/running.html
   
8. static code checking

   pylint -f parseable --rcfile=./tests/pylint.rc calender
   
9. coverage
   
   coverage run --source='calender' --branch test.py
   
   coverage report
   
   refer https://coverage.readthedocs.io/en/coverage-4.5.1/cmd.html