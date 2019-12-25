import commands
import time
import subprocess


def run_cmd_wait(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    return process.returncode


def dump_hprof(pid,count):
    run_cmd_wait("adb shell am dumpheap {} /tmp/map.hprof".format(pid))
    time.sleep(5)
    run_cmd_wait("adb pull /tmp/map.hprof /tmp/memdebug/map{}.hprof".format(count))


def dump_app_info(app,count):
    pid = commands.getstatusoutput("adb shell ps -A | grep {} ".format(app) + "| awk '{print $2}'")[1]
    print "{} pid:".format(app),pid
    commands.getstatusoutput("adb shell lsof -p {} > /tmp/memdebug/app_lsof{}".format(pid,count))




pid = commands.getstatusoutput("adb shell pgrep system_server")[1]
print "system_server_pid:",pid

leak_app = "com.android.systemui"
unleak_app = "com.microsoft.windowsintune.companyportal"
maps_path = "/proc/{}/maps".format(pid)
back_commands = "adb shell input keyevent BACK"
start_settings_commands = "adb shell am start -n {}/.MainActivity".format(leak_app)
#start_settings_commands = "adb shell am start -n com.microsoft.windowsintune.companyportal/.views.SplashActivity"
memdump_commands = "adb shell cat {}".format(maps_path)
meminfo_commands = "adb shell dumpsys meminfo system_server"


commands.getstatusoutput("mv /tmp/memdebug/ /tmp/memdebug_old/")
commands.getstatusoutput("rm -rf /tmp/memdebug/")
commands.getstatusoutput("mkdir /tmp/memdebug/")


for x in range(2):
    commands.getstatusoutput(back_commands)
    time.sleep(0.5)

count = 0

for x in range(600):
    commands.getstatusoutput(start_settings_commands)
    time.sleep(1)
    commands.getstatusoutput(back_commands)
    time.sleep(0.5)
    commands.getstatusoutput(back_commands)
    if(x%50 == 0):
        time.sleep(10)
        count = count + 1
        commands.getstatusoutput(memdump_commands + " > /tmp/memdebug/maps{}".format(count))
        commands.getstatusoutput(meminfo_commands + " > /tmp/memdebug/meminfo{}".format(count))
        commands.getstatusoutput("adb shell procmem {} > /tmp/memdebug/promem{}".format(pid,count))
        commands.getstatusoutput("adb shell lsof -p {} > /tmp/memdebug/lsof{}".format(pid,count))
        #dump_hprof(pid,count)
        dump_app_info(leak_app,count)

    




