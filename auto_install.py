import os
import time
from multiprocessing import Pool
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
    try:
        if times >= 3:
            return False
        print('({}) <尝试{}次> 检查设备是否锁屏'.format(device, times))
        if d.info.get('screenOn') == True:
            print('({}) 设备是亮屏状态！'.format(device))
            d.press("power")
            print('({}) 关闭屏幕一次！'.format(device))
            time.sleep(2)
            d.unlock()
            print('({}) 执行一次解锁'.format(device))
            d.press("home")
            print('({}) 按一次home回到桌面'.format(device))
            return True
        else:
            print('({}) 设备是黑屏状态！'.format(device))
            d.unlock()
            print('({}) 直接执行解锁'.format(device))
            d.press("home")
            print('({}) 按一次home回到桌面'.format(device))
            return True
    except Exception as e:
        print(e)
        return check_screen_locked(times=times + 1)


def input_autoinstall(device, d):
    try:
        devices_v = d.device_info["version"]
        devices_version = devices_v[0:3]
        display = d.device_info["display"]
        my_display = '{}*{}'.format(display["width"], display["height"])
        print('当前手机系统版本为 {}'.format(devices_version))
        print('检测是否是vivo或者OPPO手机 {}'.format(device))
        print('当前屏幕分辨率为 {}'.format(my_display))
        if d.device_info["brand"] == 'vivo':
            print('检测到vivo手机 {}'.format(device))
            if float(devices_version) > 5 and float(devices_version) < 9:
                d(resourceId="vivo:id/vivo_adb_install_ok_button").click()
            else:
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
        elif d.device_info["brand"] == 'OPPO':
            print('检测到OPPO手机 {}'.format(device))
            print('开始输入密码 {}'.format(device))
            d(resourceId="com.coloros.safecenter:id/et_login_passwd_edit").set_text("Pokercity2019")
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
                elif float(devices_version) > 8 and float(devices_version) < 11:
                    d.click(0.495, 0.954)
                    return True
                elif float(devices_version) < 5.3 and float(devices_version) >= 5:
                    d.click(0.498, 0.793)
                    return True
                else:
                    return True
        else:
            return True
    except Exception as e:
        print(e)
        return False


def quickinstall(device):
    packagename = "com.saiyun.vtmjzz"
    i = "/Users/boke/Downloads/apk/mjzz_release_1.07_0727-appetizer.apk"

    cmd = '{} -s {} {} {}'.format("adb", device, "install", i)
    print(cmd)

    # 卸载原有apk
    d = u2.connect(device)
    try:
        os.system('adb -s ' + device + ' uninstall %s' % packagename)
        print(device + " 卸载成功\n")
    except:
        print(device + " 卸载失败\n")
    check_screen_locked(device, d)
    subprocess.Popen(cmd, shell=True)
    time.sleep(10)
    input_autoinstall(device, d)




def qainstall(devices):
    starting = time.time()
    pool = Pool()  # 创建8个任务池
    result = pool.map(quickinstall, devices)
    entire = time.time()
    pool.close()
    print(entire - starting)  # 打印时间


if __name__ == "__main__":
    try:
        devices = getDevicesAll()
    except:
        print("获取设备出错")
    try:
        qainstall(devices)
    except:
        print("进程出错")
