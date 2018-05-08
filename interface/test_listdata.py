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
    def test01(self):
        host='http://bird.test.druidtech.net/manager'
        hosts='https://bird.test.druidtech.net/manager'
        mark1='2003'
        mark2='2106'

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



        #get devices count获取当前用户设备数量
        getdevicescount=requests.get(hosts+'/api/v2/device/count',headers=header,verify=False)
        print("当前账户拥有设备数量：",getdevicescount.text,"个")
        self.assertEquals(200,getdevicescount.status_code)

        #根据降序对设备排序
        getdevices1=requests.get(hosts+'/api/v2/device/page/',headers=headerup,verify=False)
        print(getdevices1.text)
        print(eval(getdevices1.text)[0]['updated_at'])
        print(eval(getdevices1.text)[-1]['updated_at'])
        bool1=eval(getdevices1.text)[0]['updated_at']<eval(getdevices1.text)[-1]['updated_at']
        print(bool1)
        self.assertEquals(True,bool1)

        #根据升序对设备排序
        getdevices2=requests.get(hosts+'/api/v2/device/page/',headers=headerdn,verify=False)
        print(getdevices2.text)
        print(eval(getdevices2.text)[0]['updated_at'])
        print(eval(getdevices2.text)[-1]['updated_at'])
        bool2=eval(getdevices2.text)[0]['updated_at']>eval(getdevices2.text)[-1]['updated_at']
        self.assertEquals(True,bool2)



        #Search Device By mark
        getdevicebymark=requests.get(hosts+'/api/v2/device/search/mark/'+mark1,headers=header,verify=False)
        deviceid=eval(getdevicebymark.text)[0]['id']
        print("deviceid",mark1,deviceid)
        #Search Device By mark
        getdevicebymark1=requests.get(hosts+'/api/v2/device/search/mark/'+mark2,headers=header,verify=False)
        deviceidbeh=eval(getdevicebymark1.text)[0]['id']
        print("deviceidbeh",mark2,deviceidbeh)


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


        #get device gps获取设备的GPS数据的数量
        getgpscount=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/count',headers=header,verify=False)
        print("这个设备的GPS数量为：",getgpscount.text)
        self.assertEquals(200,getgpscount.status_code)

        #_id升序排列所有GPS数据
        getgpsidup=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/page/',headers=headeridup,verify=False)
        print(getgpsidup.status_code)
        print(getgpsidup.text)
        print(eval(getgpsidup.text)[0]['updated_at'])
        print(eval(getgpsidup.text)[-1]['updated_at'])
        bool3=eval(getgpsidup.text)[0]['updated_at']<eval(getgpsidup.text)[-1]['updated_at']
        self.assertEquals(True,bool3)


        #_id降序排列所有GPS数据
        getgpsiddn=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/page/',headers=headeriddn,verify=False)
        print("gpsdn",getgpsiddn.status_code)
        print("gpsdn",getgpsiddn.text)
        print(eval(getgpsiddn.text)[0]['updated_at'])
        print(eval(getgpsiddn.text)[-1]['updated_at'])
        bool4=eval(getgpsiddn.text)[0]['updated_at']>eval(getgpsiddn.text)[-1]['updated_at']
        self.assertEquals(True,bool4)
        gpsparam=eval(getgpsiddn.text)[-1]['updated_at']
        deviceid1=eval(getgpsiddn.text)[0]['id']
        print("gpsparam",gpsparam)

        #timestampup
        getgpstsup=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/page/',headers=headertimestampup,verify=False)
        print("gpstsup",getgpstsup.status_code)
        print("gpstsup",getgpstsup.text)
        print(eval(getgpstsup.text)[0]['updated_at'])
        print(eval(getgpstsup.text)[-1]['updated_at'])
        bool5=eval(getgpstsup.text)[0]['updated_at']>eval(getgpstsup.text)[-1]['updated_at']
        self.assertEquals(True,bool5)

        #timestampdn
        getgpstsdn=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/page/',headers=headertimestampdn,verify=False)
        print("gpstsdn",getgpstsdn.status_code)
        print("gpstsdn",getgpstsdn.text)
        print(eval(getgpstsdn.text)[0]['updated_at'])
        print(eval(getgpstsdn.text)[-1]['updated_at'])
        bool6=eval(getgpstsdn.text)[0]['updated_at']<eval(getgpstsdn.text)[-1]['updated_at']
        self.assertEquals(True,bool6)



        #get device behavior获取设备的behavior数据的数量
        getbehaviorcount=requests.get(hosts+'/api/v2/behavior/device/'+deviceidbeh+'/count',headers=header,verify=False)
        print("设备",mark2,"的behavior数量为：",getbehaviorcount.text)
        self.assertEquals(200,getbehaviorcount.status_code)

        #_id升序排列所有behavior数据
        getbehavioridup=requests.get(hosts+'/api/v2/behavior/device/'+deviceidbeh,headers=headeridup,verify=False)
        print(getbehavioridup.status_code)
        print(getbehavioridup.text)
        print(eval(getbehavioridup.text)[0]['updated_at'])
        print(eval(getbehavioridup.text)[-1]['updated_at'])
        bool7=eval(getbehavioridup.text)[0]['updated_at']<eval(getbehavioridup.text)[-1]['updated_at']
        self.assertEquals(True,bool7)


        #_id降序排列所有behavior数据
        getbehavioriddn=requests.get(hosts+'/api/v2/behavior/device/'+deviceidbeh,headers=headeriddn,verify=False)
        print("behaviordn",getbehavioriddn.status_code)
        print("behaviordn",getbehavioriddn.text)
        print(eval(getbehavioriddn.text)[0]['updated_at'])
        print(eval(getbehavioriddn.text)[-1]['updated_at'])
        bool8=eval(getbehavioriddn.text)[0]['updated_at']>eval(getbehavioriddn.text)[-1]['updated_at']
        self.assertEquals(True,bool8)
        behaviorparam=eval(getbehavioriddn.text)[0]['updated_at']
        behdeviceid=eval(getbehavioriddn.text)[0]['id']

        #timestampup
        getbehaviortsup=requests.get(hosts+'/api/v2/behavior/device/'+deviceidbeh,headers=headertimestampdn,verify=False)
        print("behaviortsup",getbehaviortsup.status_code)
        print("behaviortsup",getbehaviortsup.text)
        print(eval(getbehaviortsup.text)[0]['updated_at'])
        print(eval(getbehaviortsup.text)[-1]['updated_at'])
        bool9=eval(getbehaviortsup.text)[0]['updated_at']<eval(getbehaviortsup.text)[-1]['updated_at']
        self.assertEquals(True,bool9)

        #timestampdn
        getbehaviortsdn=requests.get(hosts+'/api/v2/behavior/device/'+deviceidbeh,headers=headertimestampdn,verify=False)
        print("behaviortsdn",getbehaviortsdn.status_code)
        print("behaviortsdn",getbehaviortsdn.text)
        print(eval(getbehaviortsdn.text)[0]['updated_at'])
        print(eval(getbehaviortsdn.text)[-1]['updated_at'])
        bool10=eval(getbehaviortsdn.text)[0]['updated_at']<eval(getbehaviortsdn.text)[-1]['updated_at']
        self.assertEquals(True,bool10)



        #et device sms获取设备的短信数据的数量
        getsmscount=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/sms/count',headers=header,verify=False)
        print("这个设备的短信数据数量为：",getsmscount.text)
        self.assertEquals(200,getsmscount.status_code)

        #_id升序排列所有sms数据
        getsmsidup=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/sms/page/',headers=headeridup,verify=False)
        print(getsmsidup.status_code)
        print(getsmsidup.text)
        print(eval(getsmsidup.text)[0]['updated_at'])
        print(eval(getsmsidup.text)[-1]['updated_at'])
        bool11=eval(getsmsidup.text)[0]['updated_at']<eval(getsmsidup.text)[-1]['updated_at']
        self.assertEquals(True,bool11)


        #_id降序排列所有sms数据
        getsmsiddn=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/sms/page/',headers=headeriddn,verify=False)
        print("getsmsiddn",getsmsiddn.status_code)
        print("getsmsiddn",getsmsiddn.text)
        print(hosts+'/api/v2/behavior/device/'+deviceid)
        print(eval(getsmsiddn.text)[0]['updated_at'])
        print(eval(getsmsiddn.text)[-1]['updated_at'])
        bool12=eval(getsmsiddn.text)[0]['updated_at']>eval(getsmsiddn.text)[-1]['updated_at']
        self.assertEquals(True,bool12)
        smsparam=eval(getsmsiddn.text)[-1]['updated_at']
        smsdeviceid=eval(getsmsiddn.text)[0]['id']

        #timestampup
        getsmssup=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/sms/page/',headers=headertimestampup,verify=False)
        print("getsmssup",getsmssup.status_code)
        print("getsmssup",getbehaviortsup.text)
        print(eval(getsmssup.text)[0]['updated_at'])
        print(eval(getsmssup.text)[-1]['updated_at'])
        bool13=eval(getsmssup.text)[0]['updated_at']>eval(getsmssup.text)[-1]['updated_at']
        self.assertEquals(True,bool13)

        #timestampdn
        getsmstsdn=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/sms/page/',headers=headertimestampdn,verify=False)
        print("getsmstsdn",getsmstsdn.status_code)
        print("getsmstsdn",getsmstsdn.text)
        print(eval(getsmstsdn.text)[0]['updated_at'])
        print(eval(getsmstsdn.text)[-1]['updated_at'])
        bool14=eval(getsmstsdn.text)[0]['updated_at']<eval(getsmstsdn.text)[-1]['updated_at']
        self.assertEquals(True,bool14)

        #device根据时间戳筛选设备
        timeparam1=eval(getdevices2.text)[0]['updated_at']
        getdevwithparam=requests.get(hosts+'/api/v2/device/page/'+timeparam1,headers=header,verify=False)
        self.assertEquals(200,getdevwithparam.status_code)
        self.assertIn("device_type",getdevwithparam.text)

        #gps根据时间戳筛选设备
        getdevwithparam2=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/page/'+gpsparam,headers=headertimestampdn,verify=False)
        self.assertEquals(200,getdevwithparam2.status_code)
        self.assertIn("company_name",getdevwithparam2.text)
        #gps根据device_id筛选设备
        getdevwithparam2=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/page/'+deviceid1,headers=headeriddn,verify=False)
        self.assertEquals(200,getdevwithparam2.status_code)
        self.assertIn("company_name",getdevwithparam2.text)

        #behavior根据时间戳筛选设备
        getdevwithparam1=requests.get(hosts+'/api/v2/behavior/device/'+deviceidbeh+'/page/'+behaviorparam,headers=headertimestampup,verify=False)
        self.assertEquals(200,getdevwithparam1.status_code)
        self.assertIn("company_name",getdevwithparam1.text)
        #behavior根据device_id筛选设备
        getdevwithparam1=requests.get(hosts+'/api/v2/behavior/device/'+deviceidbeh+'/page/'+behdeviceid,headers=headeriddn,verify=False)
        self.assertEquals(200,getdevwithparam1.status_code)
        self.assertIn("company_name",getdevwithparam1.text)


        #sms根据时间戳筛选设备
        getdevwithparam3=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/sms/page/'+smsparam,headers=headertimestampdn,verify=False)
        self.assertEquals(200,getdevwithparam3.status_code)
        self.assertIn("company_name",getdevwithparam3.text)
        #sms根据id筛选设备
        getdevwithparam3=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/sms/page/'+smsdeviceid,headers=headeriddn,verify=False)
        self.assertEquals(200,getdevwithparam3.status_code)
        self.assertIn("company_name",getdevwithparam3.text)
