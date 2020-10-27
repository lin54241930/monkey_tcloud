import os
import sys
import time
import traceback
import re
from multiprocessing import Pool
import multiprocessing
import prettytable
import requests
import json
from datetime import datetime
import uiautomator2 as u2
import subprocess




def getDevicesAll():
    # 获取devices数量和名称
    try:
        for dName_ in os.popen("adb devices"):
            if "\t" in dName_:
                if dName_.find("emulator") < 0:
                    devices.append(dName_.split("\t")[0])
        devices.sort(cmp=None, key=None, reverse=False)
        print(devices)
    except Exception as e:
        print(e)
    print(u"\n设备名称: %s \n总数量:%s台" % (devices, len(devices)))
    return devices


def check_screen_locked(device, d, times=1):
    devices_v = d.device_info["version"]
    devices_version = devices_v[0:3]
    try:
        if times >= 3:
            return False
        if d.device_info["brand"] == 'Honor' and float(devices_version) == 4.4:
            right_slide_unlock(device, d)
        elif d.device_info["brand"] == 'OPPO' and (float(devices_version) == 7.1 or float(devices_version) == 5.1):
            coordinate_unlock(device, d)
        elif d.device_info["brand"] == 'HUAWEI':
            coordinate_unlock(device, d)
        else:
            up_slide_unlock(device, d)
    except Exception as e:
        print(e)
        print("({}) 解锁失败，第{}次尝试".format(device, times))
        return check_screen_locked(times=times + 1)


def up_slide_unlock(device, d):
    print('({}) 关闭屏幕！'.format(device))
    d.screen_off()
    print('({}) 开启屏幕！'.format(device))
    d.screen_on()
    time.sleep(2)
    print('({}) 上滑动执行解锁'.format(device))
    d.swipe_ext("up")
    time.sleep(2)
    print('({}) 回到桌面'.format(device))
    d.press("home")


def right_slide_unlock(device, d):
    print('({}) 关闭屏幕！'.format(device))
    d.screen_off()
    print('({}) 开启屏幕！'.format(device))
    d.screen_on()
    time.sleep(2)
    print('({}) 右滑动执行解锁'.format(device))
    d.swipe_ext("right")
    time.sleep(2)
    print('({}) 回到桌面'.format(device))
    d.press("home")


def check_ordinary(device, d):
    print('({}) 关闭屏幕！'.format(device))
    d.screen_off()
    print('({}) 开启屏幕！'.format(device))
    d.screen_on()
    time.sleep(2)
    print('({}) 直接执行解锁'.format(device))
    d.unlock()
    time.sleep(2)
    print('({}) 回到桌面'.format(device))
    d.press("home")


def coordinate_unlock(device, d):
    cmd = '{} -s {} shell input swipe 350 991 379 277'.format("adb", device)
    print(cmd)
    print('({}) 关闭屏幕！'.format(device))
    d.screen_off()
    print('({}) 开启屏幕！'.format(device))
    d.screen_on()
    time.sleep(2)
    print('({}) adb命令执行滑动解锁'.format(device))
    subprocess.Popen(cmd, shell=True)
    time.sleep(2)
    print('({}) 回到桌面'.format(device))
    d.press("home")


def screen_size(d):
    display = d.device_info["display"]
    my_display = '{}*{}'.format(display["width"], display["height"])
    return my_display


def devices_version(d):
    devices_v = d.device_info["version"]
    devices_version = devices_v[0:3]
    return devices_version

def input_autoinstall(device, d):
    try:
        print('({}) 当前手机系统版本为 {}'.format(device, devices_version(d)))
        print('({}) 检测手机厂商 {}'.format(device, d.device_info["brand"]))
        print('({}) 屏幕分辨率为 {}'.format(device, screen_size(d)))
        if d.device_info["brand"] == 'vivo':
            print('({}) 检测到vivo手机'.format(device))
            if float(devices_version(d)) < 8:
                try:
                    d(resourceId="vivo:id/vivo_adb_install_ok_button").click()
                    print("({}) 成功点击安装按钮".format(device))
                except Exception as e:
                    print(e)
                    print("({}) 未找到安装按钮".format(device))
                    return False
            elif d(resourceId="android:id/button1").exists:
                print('({}) 开始输入密码'.format(device))
                d.xpath(
                    '//*[@resource-id="com.bbk.account:id/dialog_pwd"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').set_text(
                    "Pokercity2019")
                print('({}) 点击确认按钮'.format(device))
                d(resourceId="android:id/button1").click()
                print('({}) 等待10s检测应用安全性'.format(device))
                d(resourceId="com.sohu.inputmethod.sogou.vivo:id/imeview_keyboard").wait(timeout=10.0)
                print('({}) 点击安装按钮'.format(device))
                d.click(0.497, 0.858)
                return True
            else:
                d.click(0.493, 0.885)
                time.sleep(2)
                d.click(0.493, 0.885)
        elif d.device_info["brand"] == 'OPPO' and float(devices_version(d)) > 4.4:
            print('({}) 检测到OPPO手机'.format(device))
            print('({}) 开始输入密码'.format(device))
            time.sleep(2)
            d(resourceId="com.coloros.safecenter:id/et_login_passwd_edit").set_text("******")
            print('({}) 点击确认按钮'.format(device))
            d(resourceId="android:id/button1").click()
            print('({}) 等待8s检测应用安全性'.format(device))
            time.sleep(8)
            if d(text="发现广告插件").exists:
                d.click(0.686, 0.929)
                time.sleep(2)
                d.click(0.482, 0.84)
                return True
            else:
                if float(devices_version(d)) > 5 and float(devices_version(d)) < 7:
                    print("({}) 点击确认按钮".format(device))
                    d.click(0.718, 0.957)
                    return True
                elif float(devices_version(d)) == 7.1:
                    print("({}) 点击确认按钮".format(device))
                    d.click(0.495, 0.841)
                elif float(devices_version(d)) > 8 and float(devices_version(d)) < 11:
                    print("({}) 点击确认按钮".format(device))
                    d.click(0.495, 0.954)
                    return True
                elif float(devices_version(d)) < 5.3 and float(devices_version(d)) >= 5:
                    print("({}) 点击确认按钮".format(device))
                    d.click(0.498, 0.793)
                    return True
                else:
                    return True
        elif d.device_info["brand"] == "xiaomi":
            print('({}) 检测到小米手机'.format(device))
            print('({}) 手机系统版本为{}'.format(device, devices_version(d)))
            if d(text="USB安装提示").exists:
                print('({}) 检测到弹出窗口，点击继续安装按钮'.format(device))
                d.click(0.26, 0.953)
            else:
                print('({}) 没有检测到弹出窗口，静默安装'.format(device))

        elif d.device_info["brand"] == "DOOV":
            print('({}) 检测到康佳手机'.format(device))
            print('({}) 手机系统版本为{}'.format(devices_version(d)))
            cmd = '{} -s {} shell input tap 502 774'.format("adb", device)
            time.sleep(8)
            if d(text="权限提醒").exists:
                print('({}) 检测到弹出窗口，点击允许按钮'.format(device))
                time.sleep(2)
                print(cmd)
                subprocess.Popen(cmd, shell=True)
            else:
                print('({}) 没有检测到弹出窗口，静默安装'.format(device))

        else:
            return True
        # d.service("uiautomator").stop()
        # print("结束当前手机的uiautomator服务")
    except Exception as e:
        print(e)
        return False


def deal_with_python_version(data):
    if str(sys.version_info.major) == '3':
        if isinstance(data, list):
            return [d.decode('utf-8') for d in data]
        else:
            return data.decode('utf-8')
    else:
        return data


def output(p):
    if p.stdout:
        return deal_with_python_version(p.stdout.readlines())
    else:
        return deal_with_python_version(p.stderr.readlines())


def command_execute(cmd):
    try:
        if not cmd:
            return False
        command_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           executable="/bin/bash")
        return command_process
    except Exception as e:
        print(e)
        traceback.print_exc()


def get_package_version(packagename, device):
    print('({}) 获取 安装包 版本信息'.format(device))
    if check_package_installed(packagename, device):
        cmd = '{} -s {} shell dumpsys package {} | grep versionName'.format("adb",device, packagename)
        p = command_execute(cmd)
        r = output(p)
        if len(r) > 0:
            temp = r[0].split('=')
            if len(temp) > 0:
                version = temp[1].strip()
                print('({}) 版本是 [{}] '.format(device, version))
                return version
        return ''
    else:
        print('({}) {} 没有安装!'.format(device, packagename))
        return None


def get_installed_packages(device, show_table=False):
    try:
        cmd = '{} -s {} shell pm list packages'.format("adb", device)
        p = command_execute(cmd)
        package_list = output(p)
        if show_table:
            print('({}) 获取所有的已安装的包'.format(device))
            table_packages = prettytable.PrettyTable()
            table_packages.field_names = ["id", "package name"]
            for i, package in enumerate(package_list):
                row = [i, package]
                table_packages.add_row(row)
            print('({}) \n {}'.format(device, table_packages))
        return package_list
    except Exception as e:
        print(e)
        return e


def check_package_installed(packagename, device):
    for package in get_installed_packages(device):
        if packagename in package:
            return True

    return False


def uninstall_package(device, packagename):
    print('({}) 开始卸载 ：{}'.format(device, packagename))
    try:
        if check_package_installed(packagename, device):
            cmd = '{} -s {} uninstall {}'.format("adb",device, packagename)
            p = command_execute(cmd)
            result = output(p)
            for r in result:
                if 'Success' in r:
                    print('({}) 卸载 {} 成功'.format(device, packagename))
                    return True
            print('({}) 卸载 {} 失败 : '.format(device, packagename))
            return False
        else:
            print('({}) 设备没有安装 {}, 不需要卸载'.format(device, packagename))
            return True
    except Exception as e:
        print('({}) 卸载 {} 失败 : '.format(device, packagename))
        return e


#获取当前界面正在运行的APP
def get_current_application(device):
    return command_execute('{} -s {} shell dumpsys activity activities | findstr "Run"'.format("adb", device))


def get_current_activity(device):
    p = get_current_application(device)
    result = output(p)
    if len(result) > 0:
        names = result[0].split(' ')
        if len(names) > 1:
            activity_name = names[-1]
            if '/' in activity_name:
                activity = activity_name.split('/')
                return activity[1].strip() if len(activity) > 1 else activity
    return None


def whether_start_activity(packagename, d):
    pid = d.app_wait(packagename)  # 等待应用运行, return pid(int)
    if not pid:
        print("应用没有启动成功")
        return "success"
    else:
        print("应用启动成功，pid为 %d" % pid)
        return "file"


def start_activity(packagename, device, activity_name):
    try:
        activity_name = '{}/{}'.format(packagename, activity_name)
        print('({}) 启动 activity : {}'.format(device, activity_name))
        cmd = '{} -s {} shell am start -W -n {}'.format("adb", device, activity_name)
        p = command_execute(cmd)
        result = output(p)
        print(result)
        time.sleep(10)
        current_activity = get_current_activity(device)
        if current_activity == activity_name:
            print('({}) activity 已经启动成功'.format(device))
            return True
        return "file"
    except Exception as e:
        print(e)
        print(traceback.format_exc())


def analysis_app_info(d, packagename):
    appinfo = d.app_info(packagename)
    print(appinfo)


def apk_analysis(download_apk_name):
    try:
        print('开始分析包')
        package_info_re = re.compile(r"package: name='(.*)' versionCode='(.*)' versionName='(.*?)'.*", re.I)
        label_icon_re = re.compile(r"application: label='(.+)'.*icon='(.+)'", re.I)
        launchable_activity_re = re.compile(r"launchable-activity: name='(.+)'.*label.*", re.I)

        apk_info = {}


        command_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        infos = command_process.stdout.readlines()

        for info in infos:
            info = info.decode('utf-8')
            if info.startswith('package:'):
                temp = package_info_re.search(info)
                apk_info['package_name'] = temp.group(1)
                apk_info['version_code'] = temp.group(2) or 0
                apk_info['version_name'] = temp.group(3)
            elif info.startswith('application:'):
                temp = label_icon_re.search(info)
                apk_info['label'] = temp.group(1)
                apk_info['icon'] = temp.group(2)
            elif info.startswith('launchable-activity:'):
                temp = launchable_activity_re.search(info)
                apk_info['default_activity'] = temp.group(1)

        try:
            size = round(os.path.getsize(download_apk_name) / float(1024 * 1024), 2)
            apk_info['size'] = str(size)

        except Exception as e:
            print(e)
            print(traceback.format_exc())

        print(apk_info)

        if type == 1:
            pass
        elif type == 2:
            pass

        return apk_info
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return {}


def update_monkey(id=1, device_id=None, device_name=None, device_version=None, device_screen_size=None, begin_test_time=None,
                  end_test_time=None, install_time=None, package_name=None, package_version=None, whether_install=None,
                  whether_start=None, default_activity=None):
    tcloud_url = "http://192.168.31.214:8088"
    try:
        request_data_template = {
            "id": 1,
            "device_id": device_id,
            "device_name": device_name,
            "device_version": device_version,
            "device_screen_size": device_screen_size,
            "begin_test_time": begin_test_time,
            "end_test_time": end_test_time,
            "install_time": install_time,
            "package_name": package_name,
            "package_version": package_version,
            "whether_install": whether_install,
            "whether_start": whether_start,
            "default_activity": default_activity
        }
        request_data = {}

        for key in request_data_template.keys():
            value = request_data_template.get(key)
            if value is not None:
                request_data[key] = value

        request_url = '{}/v1/monkey/test_install/{}'.format(tcloud_url, device_id)
        print("输出这个request_url看看")
        print(request_data)
        print(request_url)

        response = requests.request(method='POST', url=request_url, json=request_data)

        if response.ok:
            print(response.text)
            print('({}) update monkey success'.format(device_name))
            return True
        return False
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return False


def quickinstall(device):

    packagename = apk_analysis(i)['package_name']
    activity_name = apk_analysis(i)['default_activity']
    device_id = 888

    cmd = '{} -s {} {} {}'.format("adb", device, "install", i)
    name = multiprocessing.current_process().name
    print(name)

    # 卸载原有apk
    d = u2.connect(device)


    # analysis_app_info(d, packagename)
    get_package_version(packagename, device)
    uninstall_package(device, packagename)
    try:
        check_screen_locked(device, d)
        print("({}) 开始推送包，请耐心等待...".format((device)))
        starting = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        st = time.time()
        command_execute(cmd)
        time.sleep(6)
        input_autoinstall(device, d)
        time.sleep(5)
        if check_package_installed(packagename, device):
            print('({}) 安装 {} 成功'.format(device, packagename))
            whether_install = "success"
            entire = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            en = time.time()
            install_time = en - st
            print('({}) 安装用时{}'.format(device, install_time))
            start_activity(packagename, device, activity_name)
            whether_start = whether_start_activity(packagename, d)
        else:
            print('({}) 安装 {} 失败'.format(device, packagename))
            whether_install = "file"
        device_id = 888
        update_monkey(id=1, device_id=device_id, device_name=device, device_version=devices_version(d),
                      device_screen_size=screen_size(d), begin_test_time=starting, end_test_time=entire,
                      install_time=str(install_time), package_name=packagename,
                      package_version=apk_analysis(i)['version_code'], whether_install=whether_install,
                      whether_start=whether_start, default_activity=activity_name)
    except:
        print("程序异常")



def qainstall(devices):
    starting = time.time()
    pool = Pool()  # 创建8个任务池
    pool.map(quickinstall, devices)
    entire = time.time()
    pool.close()
    pool.join()
    usetime ='本次安装总耗时为：{}'.format(entire - starting)
    print(usetime)  # 打印时间


if __name__ == "__main__":
    try:
        devices = getDevicesAll()
    except:
        print("获取设备出错")
    try:
        qainstall(devices)
    except Exception as e:
        print(e)
