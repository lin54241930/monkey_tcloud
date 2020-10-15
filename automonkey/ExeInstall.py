import os
import time
from multiprocessing import Pool
import multiprocessing
import uiautomator2 as u2
import subprocess


def conndevice(device):
    d = u2.connect(device)
    return d



def getDevicesAll():
    # 获取devices数量和名称
    devices = []
    try:
        for dName_ in os.popen("adb devices"):
            if "\t" in dName_:
                if dName_.find("emulator") < 0:
                    devices.append(dName_.split("\t")[0])
        devices.sort(cmp=None, key=None, reverse=False)
        print(devices)
    except:
        pass
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
        elif d.device_info["brand"] == 'HONOR' and float(devices_version) == 8:
            up_slide_unlock(device, d)
        elif d.device_info["brand"] == 'KONKA':
            up_slide_unlock(device, d)
        elif d.device_info["brand"] == 'motorola':
            up_slide_unlock(device, d)
        elif d.device_info["brand"] == 'Nokia':
            up_slide_unlock(device, d)
        elif d.device_info["brand"] == 'DOOV':
            up_slide_unlock(device, d)
        elif d.device_info["brand"] == 'OPPO' and float(devices_version) == 4.4:
            up_slide_unlock(device, d)
        elif d.device_info["brand"] == 'vivo':
            up_slide_unlock(device, d)
        elif d.device_info["brand"] == 'HUAWEI':
            coordinate_unlock(device, d)
        elif (d.device_info["brand"] == 'Xiaomi' or d.device_info["brand"] == 'xiaomi') and (float(devices_version) == 4.4 or float(devices_version) == 7.1):
            up_slide_unlock(device, d)
        elif d.device_info["brand"] == 'Meizu':
            up_slide_unlock(device, d)
        elif d.device_info["brand"] == 'SMARTISAN':
            up_slide_unlock(device, d)
        elif d.device_info["brand"] == 'LeEco':
            up_slide_unlock(device, d)
        elif d.device_info["brand"] == 'samsung':
            up_slide_unlock(device, d)
        else:
            check_ordinary(device, d)
    except Exception as e:
        print(e)
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


def input_autoinstall(device, d):
    try:
        devices_v = d.device_info["version"]
        devices_version = devices_v[0:3]
        display = d.device_info["display"]
        my_display = '{}*{}'.format(display["width"], display["height"])
        print('当前手机系统版本为 {}'.format(devices_version))
        print('检测手机厂商 {}'.format(d.device_info["brand"]))
        print('当前屏幕分辨率为 {}'.format(my_display))
        if d.device_info["brand"] == 'vivo':
            print('检测到vivo手机 {}'.format(device))
            if float(devices_version) < 8:
                d(resourceId="vivo:id/vivo_adb_install_ok_button").click()
            elif d(resourceId="android:id/button1").exists:
                print('开始输入密码 {}'.format(device))
                d.xpath(
                    '//*[@resource-id="com.bbk.account:id/dialog_pwd"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]').set_text(
                    "Pokercity2019")
                print('点击确认按钮 {}'.format(device))
                d(resourceId="android:id/button1").click()
                print('等待10s检测应用安全性 {}'.format(device))
                d(resourceId="com.sohu.inputmethod.sogou.vivo:id/imeview_keyboard").wait(timeout=10.0)
                print('点击安装按钮 {}'.format(device))
                d.click(0.497, 0.858)
                return True
            else:
                d.click(0.493, 0.885)
                time.sleep(2)
                d.click(0.493, 0.885)
        elif d.device_info["brand"] == 'OPPO' and float(devices_version) > 4.4:
            print('检测到OPPO手机 {}'.format(device))
            print('开始输入密码 {}'.format(device))
            time.sleep(2)
            d(resourceId="com.coloros.safecenter:id/et_login_passwd_edit").set_text("yibeizi20")
            print('点击确认按钮 {}'.format(device))
            d(resourceId="android:id/button1").click()
            print('等待8s检测应用安全性 {}'.format(device))
            time.sleep(8)
            if d(text="发现广告插件").exists:
                d.click(0.686, 0.929)
                time.sleep(2)
                d.click(0.482, 0.84)
                return True
            else:
                if float(devices_version) > 5 and float(devices_version) < 7:
                    d.click(0.718, 0.957)
                    return True
                elif float(devices_version) == 7.1:
                    d.click(0.495, 0.841)
                elif float(devices_version) > 8 and float(devices_version) < 11:
                    d.click(0.495, 0.954)
                    return True
                elif float(devices_version) < 5.3 and float(devices_version) >= 5:
                    d.click(0.498, 0.793)
                    return True
                else:
                    return True
        elif d.device_info["brand"] == "xiaomi":
            print('检测到小米手机{}'.format(device))
            print('手机系统版本为{}'.format(devices_version))
            if d(text="USB安装提示").exists:
                print('检测到弹出窗口，点击继续安装按钮')
                d.click(0.26, 0.953)
            else:
                print('没有检测到弹出窗口，静默安装')

        elif d.device_info["brand"] == "DOOV":
            print('检测到康佳手机{}'.format(device))
            print('手机系统版本为{}'.format(devices_version))
            cmd = '{} -s {} shell input tap 502 774'.format("adb", device)
            time.sleep(8)
            if d(text="权限提醒").exists:
                print('检测到弹出窗口，点击允许按钮')
                time.sleep(2)
                print(cmd)
                subprocess.Popen(cmd, shell=True)
            else:
                print('没有检测到弹出窗口，静默安装')

        else:
            return True
        # d.service("uiautomator").stop()
        # print("结束当前手机的uiautomator服务")
    except Exception as e:
        print(e)
        return False


def quickinstall(device):
    packagename = "com.alipay.hulu"
    i = "/Users/boke/Downloads/apk/SoloPi.apk"

    cmd = '{} -s {} {} {}'.format("adb", device, "install", i)
    print(cmd)
    name = multiprocessing.current_process().name
    print(name)

    # 卸载原有apk
    d = u2.connect(device)
    try:
        os.system('adb -s ' + device + ' uninstall %s' % packagename)
        print(device + " 卸载成功\n")
    except:
        print(device + " 卸载失败\n")
    check_screen_locked(device, d)
    subprocess.Popen(cmd, shell=True)
    time.sleep(6)
    input_autoinstall(device, d)



def qainstall(devices):
    starting = time.time()
    pool = Pool()  # 创建8个任务池
    pool.map(quickinstall, devices)
    entire = time.time()
    pool.close()
    pool.join()
    usetime ='本地安装总耗时为：{}'.format(entire - starting)
    print(usetime)  # 打印时间


if __name__ == "__main__":
    try:
        devices = getDevicesAll()
    except:
        print("获取设备出错")
    try:
        qainstall(devices)
    except:
        print("进程出错")
