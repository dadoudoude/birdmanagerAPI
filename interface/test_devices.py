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
    def test03(self):
        host='http://bird.test.druidtech.net'
        hosts='https://bird.test.druidtech.net'
        mark='2121'
        mark1='2060'

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
        headerdatedn={
        "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-limit":"50",
            "x-result-sort":"-date"}

        #get devices获取设备列表
        getdevices=requests.get(hosts+'/manager/api/v2/device/',headers=headerupdatedn,verify=False)
        print(getdevices.status_code)
        print(getdevices.text)

        #获取设备数量
        getdevicecount=requests.get(hosts+'/manager/api/v2/device/count',headers=header,verify=False)
        self.assertEquals(200,getdevicecount.status_code)
        print("设备总数为",getdevicecount.text,"个")

        #获取用户信息
        getuser=requests.get(hosts+'/manager/api/v2/user/',headers=header,verify=False)
        self.assertEquals(200,getuser.status_code)
        self.assertIn("username",getuser.text)
        print("userinfo",getuser.text)

        #获取公司信息
        getcompany=requests.get(hosts+'/manager/api/v2/company/',headers=header,verify=False)
        self.assertEquals(200,getcompany.status_code)
        self.assertIn("company_name",getcompany.text)
        companyid1=eval(getcompany.text)[0]['id']
        companyid2=eval(getcompany.text)[1]['id']
        print("companyinfo",getcompany.text)
        print("companyid",companyid1,companyid2)

        #搜索设备卡号
        searchbymark=requests.get(hosts+'/manager/api/v2/device/search/mark/'+mark,headers=header,verify=False)
        deviceid=eval(searchbymark.text)[0]['id']
        print("deviceid",deviceid)
        searchbymark1=requests.get(hosts+'/manager/api/v2/device/search/mark/'+mark1,headers=header,verify=False)
        deviceid1=eval(searchbymark1.text)[0]['id']
        print("deviceid1",deviceid1)


        #获取单个设备信息
        getdevice=requests.get(hosts+'/manager/api/v2/device/id/'+deviceid,headers=header,verify=False)
        self.assertEquals(200,getdevice.status_code)
        self.assertIn("updated_at",getdevice.text)

        #获取所有设备历史数据
        getdeviceloaction=requests.get(hosts+'/manager/api/v2//statistics/device/resample/day/2018-05-15',headers=header,verify=False)
        self.assertEquals(200,getdeviceloaction.status_code)
        #print("location",getdeviceloaction.text)

        #查看设备轨迹
        getline3=requests.get(hosts+'/manager/api/v2/gps/device/'+deviceid+'/line?last=-3',headers=header,verify=False)
        self.assertEquals(200,getline3.status_code)
        #print("getline3",getline3.text)
        getline6=requests.get(hosts+'/manager/api/v2/gps/device/'+deviceid+'/line?last=-6',headers=header,verify=False)
        self.assertEquals(200,getline6.status_code)
        #print("line6",getline6.text)
        getline12=requests.get(hosts+'/manager/api/v2/gps/device/'+deviceid+'/line?last=-12',headers=header,verify=False)
        self.assertEquals(200,getline12.status_code)
        #print("line12",getline12.text)

        #范围搜索设备
        #圆形范围搜索设备
        cirl={"max":1415,"point":[104.0609764,30.5508162]}
        cirldata=json.dumps(cirl)
        searchbycirl=requests.post(hosts+'/manager/api/v2//ditu/',cirldata,headers=header,verify=False)
        self.assertEquals(200,searchbycirl.status_code)
        #print("2",searchbycirl.text)
        #多边形范围搜索设备
        pol={"polygon":[[[104.0516418,30.542556],[104.0714301,30.5420827],[104.0668877,30.5553152],[104.0501857,30.554382],[104.0516418,30.542556]]]}
        poldata=json.dumps(pol)
        searchbypol=requests.post(hosts+'/manager/api/v2//ditu/',poldata,headers=header,verify=False)
        self.assertEquals(200,searchbypol.status_code)
        #print("2",searchbypol.text)

        #查询短信数据
        getsms=requests.get(hosts+'/manager/api/v2/gps/device/'+deviceid+'/sms?last=-3',headers=header,verify=False)
        self.assertEquals(200,getsms.status_code)

        #设备配置
        getsetting=requests.get(hosts+'/manager/api/v2/setting/device/'+deviceid,headers=header,verify=False)
        self.assertEquals(200,getsetting.status_code)
        self.assertIn("updated_at",getsetting.text)
        #设置设备配置
        settinginfo={"gprs_type":0,"gprs_retries":1,"gprs_voltage_threshold":3.75,"gprs_freq":1200,"env_sampling_mode":1,"env_sampling_freq":1200,"env_voltage_threshold":3.75,"behavior_sampling_mode":1,"behavior_sampling_freq":600,"behavior_voltage_threshold":3.8,"gps_accuracy_threshold_v":15000,"gps_accuracy_threshold_h":15000,"gps_fix_timeout":2,"sms_mode":1,"sms_freq":86400,"sp_number":"+8614528001111","ota_voltage_threshold":3.8,"devices":["5a327777020ef5cc5c7485b1"]}
        settingdata=json.dumps(settinginfo)
        putsetting=requests.put(hosts+'/manager/api/v2/setting/many',settingdata,headers=header,verify=False)
        self.assertEquals(201,putsetting.status_code)

        #获取设备固件
        getset=requests.get(hosts+'/manager/api/v2/setting/device/'+deviceid,headers=header,verify=False)
        self.assertEquals(200,getset.status_code)
        #获取所有固件
        getsets=requests.get(hosts+'/manager/api/v2/firmware/',headers=header,verify=False)
        self.assertEquals(200,getsets.status_code)
        self.assertIn("firmware_version",getsets.text)
        #升级设备固件
        firminfo={"devices":[deviceid],"firmware_id":"5a75d0ac020ef5cc5c3ed948"}
        firmdata=json.dumps(firminfo)
        putfirm=requests.put(hosts+'/manager/api/v2/setting/firmware',firmdata,headers=header,verify=False)
        self.assertEquals(201,putfirm.status_code)


        #分配设备

        #获取空闲设备第一个设备的id
        getidle=requests.get(hosts+'/manager/api/v2/device/idle/page/',headers=headerupdatedn,verify=False)
        self.assertEquals(200,getidle.status_code)
        deletedeviceid=eval(getidle.text)[0]['id']
        print("第一个空闲设备的id为：",deletedeviceid)
        #分配空闲设备到公司
        fenpeiinfo={"company_id":companyid1,"id":[deletedeviceid]}
        fenpeidata=json.dumps(fenpeiinfo)
        putdevice=requests.put(hosts+'/manager/api/v2/device/company',fenpeidata,headers=header,verify=False)
        self.assertEquals(201,putdevice.status_code)
        #分配给游客
        #guestinfo={"id":[deletedeviceid]}
        #guestdata=json.dumps(guestinfo)
        #fenpeiguest=requests.post(hosts+' /manager/api/v2/user/id/5af9384de021490938a27619/add_device',guestdata,headers=header,verify=False)
        #print("fenpeiguest",fenpeiguest.status_code)
        # 从游客分配到公司
        #fenpeiinfo1={"company_id":companyid1,"id":[deletedeviceid]}
        #fenpeidata1=json.dumps(fenpeiinfo1)
        #putdevice1=requests.put(hosts+'/manager/api/v2/device/company',fenpeidata1,headers=header,verify=False)
        #print("putdevice1",putdevice1.status_code)
        # 从公司分配到公司
        fenpeiinfo2={"company_id":companyid2,"id":[deletedeviceid]}
        fenpeidata2=json.dumps(fenpeiinfo2)
        putdevice2=requests.put(hosts+'/manager/api/v2/device/company',fenpeidata2,headers=header,verify=False)
        self.assertEquals(201,putdevice2.status_code)
        #释放设备
        idledevice={"id":[deletedeviceid]}
        idledevicedata=json.dumps(idledevice)
        putdeviceidle=requests.put(hosts+'/manager/api/v2/device/idle',idledevicedata,headers=header,verify=False)
        self.assertEquals(201,putdeviceidle.status_code)
        ########


        #修改备注
        descinfo={"id":[deviceid],"description_root":"this is for test!"}
        descdata=json.dumps(descinfo)
        putdisc=requests.put(hosts+'/manager/api/v2/device/description',descdata,headers=header,verify=False)
        self.assertEquals(201,putdisc.status_code)

        #设置出厂时间
        stocttime={"id":[deviceid],"stock_time":"2018-05-01T09:00:47Z"}
        stoctdata=json.dumps(stocttime)
        putstoct=requests.put(hosts+'/manager/api/v2/device/stock',stoctdata,headers=header,verify=False)
        self.assertEquals(201,putstoct.status_code)

        #导出数据
        #导出设备数据  .csv/单个
        exportdeviceinfo={"id":[deviceid,deviceid1]}
        exportdevicedata=json.dumps(exportdeviceinfo)
        exportdevice=requests.post(hosts+'/manager/api/v2/device/csv/device',exportdevicedata,headers=header,verify=False)
        self.assertEquals(200,exportdevice.status_code)
        #导出环境数据  .csv/多个
        exportgps=requests.post(hosts+'/manager/api/v2/device/csv_multiple/env',exportdevicedata,headers=header,verify=False)
        self.assertEquals(200,exportgps.status_code)
        #导出环境数据  .kml/单个
        exportgpskml=requests.post(hosts+'/manager/api/v2/device/kml',exportdevicedata,headers=header,verify=False)
        self.assertEquals(200,exportgpskml.status_code)
        #导出行为数据  .csv/单个
        exportbehkml=requests.post(hosts+'/manager/api/v2/device/csv/behavior',exportdevicedata,headers=header,verify=False)
        self.assertEquals(200,exportbehkml.status_code)

        #管理调试
        #固件版本统计
        getfirmversion=requests.get(hosts+'/manager/api/v2/statistics/firmwareversion',headers=headerdatedn,verify=False)
        self.assertEquals(200,getfirmversion.status_code)
        self.assertIn("company_id",getfirmversion.text)
        #定位成功统计
        getgps=requests.get(hosts+'/manager/api/v2/statistics/gpscount',headers=headerdatedn,verify=False)
        self.assertEquals(200,getgps.status_code)
        self.assertIn("device_id",getgps.text)

