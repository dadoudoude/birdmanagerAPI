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
    def test04(self):
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

        headerupdatedn={"Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-sort":"-update_at",
            "x-result-limit":"500",
            "x-result-offset":"0"}

        #新增公司
        companyinfo={"company_name":"测试公司","address":u"四川省成都市高新区天府三街199号","phone":"13512345678"}
        companydata=json.dumps(companyinfo)
        createcompany=requests.post(hosts+'/manager/api/v2/company/',companydata,headers=header,verify=False)
        self.assertEquals(201,createcompany.status_code)

        #获取公司列表
        getcompany=requests.get(hosts+'/manager/api/v2/company/',headers=headerupdatedn,verify=False)
        self.assertEquals(200,getcompany.status_code)
        self.assertIn("company_name",getcompany.text)
        companyid=eval(getcompany.text)[-1]['id']
        print("companyid: ",companyid)
        #获取单个公司信息
        getcompanyinfo=requests.get(hosts+'/manager/api/v2/company/id/'+companyid,headers=header,verify=False)
        self.assertEquals(200,getcompanyinfo.status_code)
        self.assertIn("company_name",getcompanyinfo.text)

        #修改公司信息
        resetinfo={"address":u"云南省昆明市长城街123333","phone":"13333333333"}
        resetdata=json.dumps(resetinfo)
        reset=requests.put(hosts+'/manager/api/v2/company/id/'+companyid,resetdata,headers=header,verify=False)
        self.assertEquals(200,reset.status_code)

        #创建admin帐号
        admininfo={"username":"testadmin","password":"b51dd0742b89810ce080542a3e745bb15a86b5197147885dc70164344cc08afe","email":"123456@test.com","company_id":companyid,"address":u"四川省成都市","phone":"135123456789","role":"admin"}
        admindata=json.dumps(admininfo)
        createadmin=requests.post(hosts+'/manager/api/v2/user/',admindata,headers=header,verify=False)
        self.assertEquals(201,createadmin.status_code)

        #获取当前新的用户列表
        getuser=requests.get(hosts+'/manager/api/v2/user/',headers=headerupdatedn,verify=False)
        self.assertEquals(200,getuser.status_code)
        self.assertIn("username",getuser.text)
        #分片提取admin username跟userid
        newusername=getuser.text[-348:-339]
        print("newusername",newusername)
        newuserid=getuser.text[-386:-362]
        print("newuserid",newuserid)

        #修改admin用户信息
        adminuserinfo={"address":u"四川省高新区","email":"13333333333@qq.com","phone":"13333333333"}
        adminuserdata=json.dumps(adminuserinfo)
        resetadmin=requests.put(hosts+'/manager/api/v2/user/id/'+newuserid+'/info',adminuserdata,headers=header,verify=False)
        self.assertEquals(204,resetadmin.status_code)

        #修改admin帐号密码
        adpwinfo={"old_password":"7717f13af87abe0c149196267c7f828395be8c60423e4a059b25db912605a57f","password":"c41ff8d27a7ef0beef8271a878a8e51af8c45f301fb655781ab21e5f3a20ed12"}
        adpwdata=json.dumps(adpwinfo)
        resetadpw=requests.put(hosts+'/manager/api/v2/user/id/'+newuserid+'/password',adpwdata,headers=header,verify=False)
        self.assertEquals(204,resetadpw.status_code)

        #删除admin帐号
        deleteadmin=requests.delete(hosts+'/manager/api/v2/user/id/'+newuserid,headers=header,verify=False)
        self.assertEquals(204,deleteadmin.status_code)

        #创建manager帐号 权限最高
        managerinfo={"username":"testmanager","password":"33839428c07edad5f5dba154939ad696f00fd43c238dc600e4dd67111a148f38","email":"123456@manager.com","address":u"四川省成都市高新区","phone":"135123456789","role":"manager","permissions":{"sim_auth":3,"device_auth":3,"platform_auth":3,"user_auth":3,"data_auth":3,"firmware_auth":3,"setting_auth":3,"company_auth":3,"export_auth":1,"search_auth":1}}
        managerdata=json.dumps(managerinfo)
        crmanager=requests.post(hosts+'/manager/api/v2/user/',managerdata,headers=header,verify=False)
        self.assertEquals(201,crmanager.status_code)

        #再次获取当前用户列表
        getuser1=requests.get(hosts+'/manager/api/v2/user/',headers=headerupdatedn,verify=False)
        self.assertEquals(200,getuser1.status_code)
        #分片提取manager username跟userid
        newusername1=getuser1.text[-535:-524]
        print("newusername1",newusername1)
        newuserid1=getuser1.text[-573:-549]
        print("newuserid1",newuserid1)

        #编辑manager帐号信息
        newmanagerinfo={"email":"23333@manager.com","address":u"四川省成都市天府三街","phone":"13333333333333","permissions":{"sim_auth":0,"device_auth":0,"platform_auth":0,"user_auth":0,"data_auth":0,"firmware_auth":0,"setting_auth":0,"company_auth":0,"export_auth":0,"search_auth":0}}
        newmanagerdata=json.dumps(newmanagerinfo)
        resetmanager=requests.put(hosts+'/manager/api/v2/user/id/'+newuserid1+'/info',newmanagerdata,headers=header,verify=False)
        self.assertEquals(204,resetmanager.status_code)

        #修改manager帐号密码
        managerpwinfo={"old_password":"7717f13af87abe0c149196267c7f828395be8c60423e4a059b25db912605a57f","password":"c41ff8d27a7ef0beef8271a878a8e51af8c45f301fb655781ab21e5f3a20ed12"}
        managerpwdata=json.dumps(managerpwinfo)
        resetmanpw=requests.put(hosts+'/manager/api/v2/user/id/'+newuserid1+'/password',managerpwdata,headers=header,verify=False)
        self.assertEquals(204,resetmanpw.status_code)

        #删除manager帐号
        deletemanager=requests.delete(hosts+'/manager/api/v2/user/id/'+newuserid1,headers=header,verify=False)
        self.assertEquals(204,deletemanager.status_code)

        #删除公司
        deletecompany=requests.delete(hosts+'/manager/api/v2/company/id/'+companyid,headers=header,verify=False)
        self.assertEquals(204,deletecompany.status_code)