# coding:utf-8
import requests
import json
import urllib3
import unittest
import re
import time
import HTMLTestRunner

urllib3.disable_warnings()

class Test(unittest.TestCase):

    def setUp(self):
        print("start")
    def tearDown(self):
        print("end")

    #设备
    def test02(self):
        host='http://bird.test.druidtech.net'
        hosts='https://bird.test.druidtech.net'
        mark='2121'
        firmwarename='v2.0.bin'
        pushmessageid='5a37919a020ef5cc5c82f795'

        r=requests.get(host+'/manager')
        #print("status",r.status_code)

        #login
        namepassword={"password":"7717f13af87abe0c149196267c7f828395be8c60423e4a059b25db912605a57f","username":"root"}
        npdata=json.dumps(namepassword)
        login=requests.post('https://bird.test.druidtech.net'+'/manager/api/v2/login',npdata,verify=False)
        #print("status",login.status_code)
        #print("login.text",login.text)
        print("loginheader",login.headers['X-Druid-Authentication'])

        #header
        header={
        "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)"}

        headerupdatedn={
        "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-limit":"50",
            "x-result-sort":"-updated_at"}

        #get company
        getcompany=requests.get(hosts+'/manager/api/v2/company/',headers=header,verify=False)
        self.assertEquals(200,getcompany.status_code)
        self.assertIn("company_name",getcompany.text)

        #get sn
        getsn=requests.get(hosts+'/manager/api/v2/manager/sn',headers=header,verify=False)
        self.assertEquals(200,getsn.status_code)
        self.assertIn("sn",getsn.text)

        #get myself
        getmyself=requests.get(hosts+'/manager/api/v2/user/myself',headers=header,verify=False)
        self.assertEquals(200,getmyself.status_code)
        self.assertIn("username",getmyself.text)

        #get druid_old查看登录映射
        getdruidold=requests.get(hosts+'/manager/api/v2/manager/druid_old',headers=header,verify=False)
        self.assertEquals(200,getdruidold.status_code)
        self.assertIn("env_id",getdruidold.text)


        #地图可视化
        #get statistics/all地图可视化获取所有设备点
        #getstatisticsall=requests.get(hosts+'/manager/api/v2/statistics/all',headers=header,verify=False)

        #/manager/api/v2/statistics/resamplev2获取设备精简点
        getstatisticsresamplev2=requests.get(hosts+'/manager/api/v2/statistics/resamplev2',headers=header,verify=False)
        self.assertEquals(200,getstatisticsresamplev2.status_code)
        self.assertIn("coordinates",getstatisticsresamplev2.text)

        #固件管理
        #get firmware
        getfirmware=requests.get(hosts+'/manager/api/v2/firmware/',headers=header,verify=False)
        self.assertEquals(200,getfirmware.status_code)
        self.assertIn("hardware_version",getfirmware.text)
        print("getfirmware",getfirmware.text)

        #上传.bin文件
        #readbin=open('C:\\Users\\liugc\\PycharmProjects\\birdmanagerAPI\\interface\\v2.0.bin','rb').read()
        readbin=open("/var/lib/jenkins/workspace/birdmanagerAPItest/interface/v2.0.bin","rb").read()
        updatebin=requests.post(hosts+'/manager/api/v2/firmware/name/'+firmwarename,readbin,headers=header,verify=False)
        self.assertEquals(201,updatebin.status_code)

        #删除.bin文件
        getfirmware1=requests.get(hosts+'/manager/api/v2/firmware/',headers=header,verify=False)
        print(len(eval(getfirmware1.text)))
        binname=eval(getfirmware1.text)[-1]['name']
        print("binname",binname)
        self.assertEquals("v2.0.bin",binname)
        binid=eval(getfirmware1.text)[-1]['id']
        deletefirmware=requests.delete(hosts+'/manager/api/v2/firmware/id/'+binid,headers=header,verify=False)
        self.assertEquals(204,deletefirmware.status_code)

        #导出数据
        #导出gps
        gpsinfo={"field":["uuid","updated_at","altitude","light","used_star","vertical","fix_time","mark","longitude","humidity","pressure","speed","battery_voltage","timestamp","latitude","temperature","dimension","horizontal","firmware_version"],"search":{"mark":[2121,2121]}}
        gpsdata=json.dumps(gpsinfo)
        exportgps=requests.post(hosts+'/manager/api/v2/manager/export/gps',gpsdata,headers=header,verify=False)
        self.assertEquals(200,exportgps.status_code)
        #导出行为数据
        behaviorinfo={"field":["uuid","updated_at","total_expend","firmware_version","sleep_time","activity_expend","mark","timestamp","sleep_expend","activity_time"],"search":{"mark":[2121,2121]}}
        behaviordata=json.dumps(behaviorinfo)
        exportbehavior=requests.post(hosts+'/manager/api/v2/manager/export/behavior',behaviordata,headers=header,verify=False)
        self.assertEquals(200,exportbehavior.status_code)
        #导出设备数据
        deviceinfo={"field":["uuid","hardware_version","company_name","sim_number","biological_type","mark","firmware_version","owner","battery_voltage","imsi","updated_at","device_type","mac","description"],"search":{"mark":[2121,2121]}}
        devicedata=json.dumps(deviceinfo)
        exportdevice=requests.post(hosts+'/manager/api/v2/manager/export/device',devicedata,headers=header,verify=False)
        self.assertEquals(200,exportdevice.status_code)

        #数据导入
        #SIM卡数据导入
        #simupdate=open("simtest.xlsx","rb")
        simupdate=open("/var/lib/jenkins/workspace/birdmanagerAPItest/interface/simtest.xlsx","rb")
        exportsimdata=simupdate.read()
        exportsim=requests.post(hosts+'/manager/api/v2/sim/excel',exportsimdata,headers=header,verify=False)
        self.assertEquals(201,exportsim.status_code)


        #编辑推送消息
        getpush=requests.get(hosts+'/manager/api/v2/push/',headers=header,verify=False)
        self.assertEquals(200,getpush.status_code)
        print("getpush ",getpush.text)
        #获取单个消息推送设置
        getapush=requests.get(hosts+'/manager/api/v2/push/id/'+pushmessageid,headers=header,verify=False)
        self.assertEquals(200,getapush.status_code)
        self.assertIn("活动很强",getapush.text)
        #生物高强度活动消息编辑  这个生物%d活动很强  zhe ge sheng wu %d huo dong hen qiang ！
        #设置发送管理员,不发送给用户
        sendmanagerinfo={"msg_cn":u"这是测试的输入，中文消息。abcd","msg_en":"This is the input of the test, the Chinese message. ABCD","admin_switch":True,"user_switch":False}
        sendmanagerdata=json.dumps(sendmanagerinfo)
        putsetting=requests.put(hosts+'/manager/api/v2/push/setting/'+pushmessageid,sendmanagerdata,headers=header,verify=False)
        self.assertEquals(201,putsetting.status_code)
        #设置不发送管理员,发送给用户(还原设置)
        senduserinfo={"msg_cn":u"这个生物%d活动很强","msg_en":"This creature has a strong %d activity","admin_switch":False,"user_switch":True}
        senduserdata=json.dumps(senduserinfo)
        sendusersetting=requests.put(hosts+'/manager/api/v2/push/setting/'+pushmessageid,senduserdata,headers=header,verify=False)
        self.assertEquals(201,sendusersetting.status_code)

        #SIM卡管理
        #get all sim info
        getsim=requests.get(hosts+'/manager/api/v2/sim/',headers=headerupdatedn,verify=False)
        self.assertEquals(200,getsim.status_code)
        print("sim0 ",getsim.text)
        self.assertIn("updated_at",getsim.text)

        #create sim
        siminfo={"description":"ceshishuju","imsi":"89011703278130900000","sim_number":"1234567890","iccid":"0987654321"}
        simdata=json.dumps(siminfo)
        createsim=requests.post(hosts+'/manager/api/v2/sim/',simdata,headers=header,verify=False)
        self.assertEquals(201,createsim.status_code)
        #
        #get all sim info
        getsim1=requests.get(hosts+'/manager/api/v2/sim/',headers=headerupdatedn,verify=False)
        self.assertEquals(200,getsim1.status_code)
        self.assertIn("updated_at",getsim1.text)

        #删除第一个sim卡
        simid=eval(getsim1.text)[0]['id']
        print("simid",simid)
        deletesim=requests.delete(hosts+'/manager/api/v2/sim/id/'+simid,headers=header,verify=False)
        self.assertEquals(204,deletesim.status_code)
        self.assertNotIn("1234567890",getsim.text)

        #回收设备
        #获取空闲设备第一个设备的id
        getidle=requests.get(hosts+'/manager/api/v2/device/idle/page/',headers=headerupdatedn,verify=False)
        self.assertEquals(200,getidle.status_code)
        deletedeviceid=eval(getidle.text)[0]['id']
        print("第一个空闲设备的id为：",deletedeviceid)
        #删除设备
        deletedevice=requests.delete(hosts+'/manager/api/v2/device/id/'+deletedeviceid,headers=header,verify=False)
        self.assertEquals(204,deletedevice.status_code)
        #获取设备回收站设备
        getdeleted=requests.get(hosts+'/manager/api/v2/device/deleted',headers=header,verify=False)
        self.assertEquals(200,getdeleted.status_code)
        #恢复设备
        recoverdevice=requests.put(hosts+'/manager/api/v2/device/recover/'+deletedeviceid,headers=header,verify=False)
        self.assertEquals(204,recoverdevice.status_code)


