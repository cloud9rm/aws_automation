# aws_automation
AWs Windows 인스턴스에 대한 AD Join 자동화

AD JOIN 과정
:Windows 호스트 네임 변경 -> Reboot -> AD JOIN(도메인가입) -> Reboot

위의 과정을 자동화
```
[Ansible Controller 서버 세팅(Ubuntu 18.04 기준)]

sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install ansible
#apt-get으로만 앤서블을 설치할 경우 파이썬2에 설치됨. 따라서 pip3로 파이썬3에 Ansible을 설치해준다.
#pip3로만 앤서블을 설치할 경우 앤서블의 기본적인 환경 세팅이 누락되는 경우가 있음. 따라서 apt-get으로 먼저 설치해준 후, pip3로 한번 더 설치해준다.

sudo pip3 install ansible
sudo sed -i 's/python2/python3/' usr/bin/ansible
#shebang 변경. python2 -> python3
sudo apt-get install awscli
pip3 install pywinrm
#윈도우 인스턴스와 통신하기 위해서는 winrm 필요
```
[Ansible Remote 서버 세팅(Windows Server 2019 기준)]
```
$url = "https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
$file = "$env:temp\ConfigureRemotingForAnsible.ps1"
(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)
powershell.exe -ExecutionPolicy ByPass -File $file
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
# 대상 윈도우 인스턴스의 Winrm 서비스 
```
