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
    def test05(self):
        host='http://bird.test.druidtech.net/'
        hosts='https://bird.test.druidtech.net/'
        mark='2026'
        mark1='2142'

        r=requests.get(host)
        #print("status",r.status_code)

        #login
        namepassword={"password":"7717f13af87abe0c149196267c7f828395be8c60423e4a059b25db912605a57f","username":"root"}
        npdata=json.dumps(namepassword)
        login=requests.post('https://bird.test.druidtech.net/manager'+'/api/v2/login',npdata,verify=False)
        #print("status",login.status_code)
        #print("login.text",login.text)
        #print("loginheader",login.headers['X-Druid-Authentication'])

        #header
        header={
        "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)"}

        headerup={"Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-sort":"updated_at"
             #"x-result-limit":limit
             }

        headerdn={"Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-sort":"-updated_at"
             #"x-result-limit":limit
             }


        headeridup={"Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-sort":"_id",
            "x-result-limit":"20"
             }
        headeriddn={"Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-limit":"20",
            "x-result-sort":"-_id"
             }
        headertimestampdn={"Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-sort":"timestamp",
            "x-result-limit":"20"
             }
        headertimestampup={"Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-sort":"-timestamp",
            "x-result-limit":"20"
             }

        #获取第一页gps数据

        getgps=requests.get(hosts+'/manager/api/v2/gps/page/',headers=headeriddn,verify=False)
        self.assertEquals(200,getgps.status_code)
        self.assertIn("device_id",getgps.text)
        #获取gps数据总数量
        getgpscount=requests.get(hosts+'/manager/api/v2/gps/count',headers=header,verify=False)
        print("GPS数据总数量为：",getgpscount.text)
        self.assertEquals(200,getgpscount.status_code)
        self.assertNotEquals(0,int(getgpscount.text))

        #获取第一页行为数据
        getbehavior=requests.get(hosts+'/manager/api/v2/behavior/page/',headers=headeriddn,verify=False)
        self.assertEquals(200,getbehavior.status_code)
        self.assertIn("device_id",getbehavior.text)
        #获取行为数据总数量
        getbehaviorcount=requests.get(hosts+'/manager/api/v2/behavior/count',headers=header,verify=False)
        print("行为数据总数量为：",getbehaviorcount.text)
        self.assertEquals(200,getbehaviorcount.status_code)
        self.assertNotEquals(0,int(getbehaviorcount.text))

        #获取第一页短信数据
        getsms=requests.get(hosts+'/manager/api/v2/gps/sms/page/',headers=headeriddn,verify=False)
        self.assertEquals(200,getsms.status_code)
        self.assertIn("device_id",getsms.text)
        #获取短信数据总数量
        getsmscount=requests.get(hosts+'/manager/api/v2/gps/sms/count',headers=header,verify=False)
        print("短信数据总数量为：",getsmscount.text)
        self.assertEquals(200,getsmscount.status_code)
        self.assertNotEquals(0,int(getsmscount.text))

        #获取第一页历史配置数据
        getsetting=requests.get(hosts+'/manager/api/v2/history/setting/page/',headers=headeriddn,verify=False)
        #self.assertEquals(200,getsetting.status_code)
        #self.assertIn("device_id",getsetting.text)
        #获取历史配置数据总数量
        getsettingcount=requests.get(hosts+'/manager/api/v2/history/setting/count',headers=header,verify=False)
        #print("历史配置数据总数量为：",getsettingcount.text)
        #self.assertEquals(200,getsettingcount.status_code)
        #self.assertNotEquals(0,int(getsettingcount.text))

        #获取第一页固件数据
        getfirm=requests.get(hosts+'/manager/api/v2/history/firmware/page/',headers=headeriddn,verify=False)
        self.assertEquals(200,getfirm.status_code)
        self.assertIn("device_id",getfirm.text)
        #获取固件数据总数量
        getfirmcount=requests.get(hosts+'/manager/api/v2/history/firmware/count',headers=header,verify=False)
        print("固件数据总数量为：",getfirmcount.text)
        self.assertEquals(200,getfirmcount.status_code)
        self.assertNotEquals(0,int(getfirmcount.text))

        #获取第一页网络状态数据
        getcel=requests.get(hosts+'/manager/api/v2/cellular/page/',headers=headeriddn,verify=False)
        self.assertEquals(200,getcel.status_code)
        self.assertIn("device_id",getcel.text)
        #获取网络状态数据总数量
        getcelcount=requests.get(hosts+'/manager/api/v2/cellular/count',headers=header,verify=False)
        print("网络状态数据总数量为：",getcelcount.text)
        self.assertEquals(200,getcelcount.status_code)
        self.assertNotEquals(0,int(getcelcount.text))

        ##获取第一页设备状态数据
        getstat=requests.get(hosts+'/manager/api/v2/status/page/',headers=headeriddn,verify=False)
        self.assertEquals(200,getstat.status_code)
        self.assertIn("device_id",getstat.text)
        #获取设备状态数据总数量
        getstatcount=requests.get(hosts+'/manager/api/v2/status/count',headers=header,verify=False)
        print("设备状态数据总数量为：",getstatcount.text)
        self.assertEquals(200,getstatcount.status_code)
        self.assertNotEquals(0,int(getstatcount.text))

        #get devices获取所有设备
        getdevices=requests.get(hosts+'/manager/api/v2/device/',headers=header,verify=False)
        print("devices ",getdevices.text)
        self.assertEquals(200,getdevices.status_code)
        self.assertIn("device_type",getdevices.text)


        ###############################################################################################################

        #单个设备数据查看

        #搜索设备卡号获取设备id
        searchbymark=requests.get(hosts+'/manager/api/v2/device/search/mark/'+mark,headers=header,verify=False)
        deviceid=eval(searchbymark.text)[0]['id']
        print("deviceid",deviceid)
        searchbymark1=requests.get(hosts+'/manager/api/v2/device/search/mark/'+mark1,headers=header,verify=False)
        deviceid1=eval(searchbymark1.text)[0]['id']
        print("deviceid1",deviceid1)

        #查看设备GPS数据
        getdivicegps=requests.get(hosts+'/manager/api/v2/gps/device/'+deviceid+'/page/',headers=headeriddn,verify=False)
        self.assertEquals(200,getdivicegps.status_code)
        self.assertIn("company_name",getdivicegps.text)
        #查看设备GPS数量
        getdevicegpscount=requests.get(hosts+'/manager/api/v2/gps/device/'+deviceid+'/count',headers=header,verify=False)
        self.assertEquals(200,getdevicegpscount.status_code)
        print("设备",mark,"GPS数据数量为：",getdevicegpscount.text,"个")

        #查看设备行为数据
        getdivicebehavior=requests.get(hosts+'/manager/api/v2/behavior/device/'+deviceid+'/page/',headers=headeriddn,verify=False)
        self.assertEquals(200,getdivicebehavior.status_code)
        self.assertIn("company_name",getdivicebehavior.text)
        #查看设备行为数据数量
        getdevicebehcount=requests.get(hosts+'/manager/api/v2/behavior/device/'+deviceid+'/count',headers=header,verify=False)
        self.assertEquals(200,getdevicebehcount.status_code)
        print("设备",mark,"行为数据数量为：",getdevicebehcount.text,"个")

        #查看设备短信数据
        getdivicesms=requests.get(hosts+'/manager/api/v2/gps/device/'+deviceid+'/sms/page/',headers=headeriddn,verify=False)
        self.assertEquals(200,getdivicesms.status_code)
        self.assertIn("company_name",getdivicesms.text)
        #查看设备短信数据数量
        getdevicesmscount=requests.get(hosts+'/manager/api/v2/behavior/device/'+deviceid+'/count',headers=header,verify=False)
        self.assertEquals(200,getdevicesmscount.status_code)
        print("设备",mark,"短信数据数量为：",getdevicesmscount.text,"个")

        #查看设备配置历史数据
        getdiviceset=requests.get(hosts+'/manager/api/v2/history/setting/device/'+deviceid+'/page/',headers=headeriddn,verify=False)
        self.assertEquals(200,getdiviceset.status_code)
        self.assertIn("updated_at",getdiviceset.text)
        #查看设备配置历史数据数量
        getdevicesetcount=requests.get(hosts+'/manager/api/v2/history/setting/device/'+deviceid+'/count',headers=header,verify=False)
        self.assertEquals(200,getdevicesetcount.status_code)
        print("设备",mark,"配置历史数据数量为：",getdevicesetcount.text,"个")

        #查看设备固件历史数据
        getdivicefirm=requests.get(hosts+'/manager/api/v2/history/firmware/device/'+deviceid+'/page/',headers=headeriddn,verify=False)
        self.assertEquals(200,getdivicefirm.status_code)
        self.assertIn("updated_at",getdivicefirm.text)
        #查看设备固件历史数据数量
        getdevicefirmcount=requests.get(hosts+'/manager/api/v2/history/firmware/device/'+deviceid+'/count',headers=header,verify=False)
        self.assertEquals(200,getdevicefirmcount.status_code)
        print("设备",mark,"固件历史数据数量为：",getdevicefirmcount.text,"个")

        #查看设备网络状态数据
        getdivicecell=requests.get(hosts+'/manager/api/v2/cellular/device/'+deviceid1+'/page/',headers=headeriddn,verify=False)
        self.assertEquals(200,getdivicecell.status_code)
        self.assertIn("mark",getdivicefirm.text)
        #查看设备网络状态数据数量
        getdevicecellcount=requests.get(hosts+'/manager/api/v2/cellular/device/'+deviceid1+'/count',headers=header,verify=False)
        self.assertEquals(200,getdevicecellcount.status_code)
        print("设备",mark1,"网络状态数据数量为：",getdevicecellcount.text,"个")

        #查看设备状态数据
        getdivicestatus=requests.get(hosts+'/manager/api/v2/status/device/'+deviceid+'/page/',headers=headeriddn,verify=False)
        self.assertEquals(200,getdivicestatus.status_code)
        self.assertIn("firmware_version",getdivicestatus.text)
        #查看设备状态数据数量
        getdevicestatuscount=requests.get(hosts+'/manager/api/v2/status/device/'+deviceid+'/count',headers=header,verify=False)
        self.assertEquals(200,getdevicestatuscount.status_code)
        print("设备",mark,"状态数据数量为：",getdevicestatuscount.text,"个")

