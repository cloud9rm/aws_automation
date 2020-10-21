import os
import subprocess
import yaml
<<<<<<< HEAD
import sys
import getpass
from time import sleep
=======
>>>>>>> b9456e5342c33987983110ceb7df2e01843aec16

class Ec2Auto:
    def __init__(self):
        print("Ec2Auto Created")

    def read_ini(self):
        self.target_ip_list =[]
        flag=0
        with open("/etc/ansible/hosts","r") as file:
            for line in file:
                if line == "\n":
                    flag = 0 
                if flag == 1:
                    print(line)
                    self.target_ip_list.append(line[:-1])
                if line == "[Ec2Auto]\n":
                    print("[Ec2Auto] contact")
                    flag = 1    
        print("target_ip_list :" + str(self.target_ip_list))

    def awscli_iam_getuser(self):
    
        while(True):
            print("check awscli version")
            exit_code=subprocess.call('aws --version',shell=True)
            if exit_code != 0:
                print("awscli hasn't be installed. First, Install awscli")
                print("Bye")
                break
<<<<<<< HEAD
            print('check aws iam get-user')
=======
            print('CHECK aws iam get-user')
>>>>>>> b9456e5342c33987983110ceb7df2e01843aec16
            exit_code=subprocess.call('aws iam get-user',shell=True)
            if exit_code == 0:
                print('aws iam get-user SUCCESS')
                break
<<<<<<< HEAD
            
            
            print('aws iam get-user FAILED')
            '''
            print("isdir ~/.aws")
            if os.path.isdir('~/.aws') == True:
                print("isdir ~/.aws True")
                print("isfile config & credentials")
                if os.path.isfile('~/.aws/config') and os.path.isfile('~/.aws/credentials') == True:
                    print("isfile ~/.aws/config & ~/.aws/credentials True")
                else:
                    print("isfile ~/.aws/config & ~/.aws/credentials False")
                    print("aws configure")
                    os.system('aws configure')
                    print("aws configure done")
            
            else:
                print("isdir ~/.aws False")
                print("mkdir ~/.aws")
                os.mkdir('~/.aws')
            '''
=======
            print('aws iam get-user FAILED')
>>>>>>> b9456e5342c33987983110ceb7df2e01843aec16
            print("aws configure")
            os.system('aws configure')
            print("aws configure done")

    def awscli_ec2_instance_name_tag(self):
        print("aws ec2 describe-instances")
        self.ip_nametag_mapping_list=[]
        for target_ip in self.target_ip_list:
            awscli_query=f"aws ec2 describe-instances --filters Name=private-ip-address,Values={target_ip} \
                            --query 'Reservations[*].Instances[*].Tags[*].{{Value:Value}}' --output text"
            byte_name_tag = subprocess.check_output(awscli_query, shell=True)
            str_name_tag = byte_name_tag[:-1].decode()
            dict = {
                    'private_ip' : target_ip,
                    'name_tag' : str_name_tag
                    }
            self.ip_nametag_mapping_list.append(dict)
        self.ip_nametag_mapping_list_beans={'target_host' : self.ip_nametag_mapping_list}
<<<<<<< HEAD
        # print(self.ip_nametag_mapping_list)
=======
        print(self.ip_nametag_mapping_list)
>>>>>>> b9456e5342c33987983110ceb7df2e01843aec16
        print(self.ip_nametag_mapping_list_beans)

    def dump_yaml_from_dict(self):
        print("dump yaml file describing target host")
        with open('ip_nametag_mapping_list.yml','w') as f:
            yaml.dump(self.ip_nametag_mapping_list_beans,f)
        with open('ip_nametag_mapping_list.yml','r') as t:
            print(t.read())

<<<<<<< HEAD
    def write_vault_passwd(self):
        self.vault_passwd = getpass.getpass('PLEASE ENTER VAULT PASSWORD\n')
        with open('.passwd','w') as file:
            file.write(self.vault_passwd)

    def get_domain_info(self):
        print("Insert Domain name : ", end='')
        self.domain_name = input()
        print("Insert Domain user : ", end='')
        self.domain_user = input()
        self.domain_passwd = getpass.getpass('Insert Domain password : ')


    def ansible_ping_check(self):
        # check ansible localhost
        print("check ansible ping localhost")
        exit_code=subprocess.call('ansible localhost -m ping',shell=True)
        if exit_code == 0:
            print("ansible working well")
        print("check ansible ping all")
        proc=subprocess.Popen(['ansible all --vault-password-file=.passwd -m win_ping'],shell=True,stdin=subprocess.PIPE)
        # proc.communicate(self.vault_passwd.encode())
        # proc.stdin.close()
        # proc.wait()
        # proc.stdin.write(self.vault_passwd.encode())
        # proc.stdin.flush()
        # proc.kill()
        proc.wait()
        print("-----------------------")
        while True:
        # return code == 0 is success return
            if proc.returncode == 0:
                break
            sleep(1)
            print("wait...this means win_ping toward ansible-target do not work.")
        # print("return code :"+str(proc.returncode))
        # proc.communicate(self.vault_passwd.encode())

    def ansible_change_hostname_and_reboot(self):
        # execute ansible-playbook for changing hostname and rebooting
        print("ansible-playbook change_hostname.yml")
        for item in self.ip_nametag_mapping_list:
            private_ip = item['private_ip']
            name_tag = item['name_tag']
            # os.system(f'ansible-playbook --ask-vault-pass change_hostname.yml -e "private_ip={private_ip} name_tag={name_tag}"')
            proc=subprocess.Popen([f'ansible-playbook --vault-password-file=.passwd change_hostname.yml -e "private_ip={private_ip} name_tag={name_tag}"'],shell=True,stdin=subprocess.PIPE)
            proc.wait()
            # print(proc.returncode)
            if proc.returncode == 0:
                print(private_ip+" "+"ansible change hostname and reboot done")

    def ansible_domain_join(self):
        print("ansible domain join")
        # self.get_domain_info()
        for item in self.ip_nametag_mapping_list:
            private_ip = item['private_ip']
            # os.system(f'ansible-playbook --ask-vault-pass domain_join.yml -e "private_ip={private_ip} domain_name={domain_name} \
                    # domain_user={domain_user} domain_passwd={domain_passwd}"')
            proc=subprocess.Popen([f'ansible-playbook --vault-password-file=.passwd domain_join.yml -e "private_ip={private_ip} domain_name={self.domain_name} \
                     domain_user={self.domain_user} domain_passwd={self.domain_passwd}"'],shell=True, stdin=subprocess.PIPE)

    def ansible_domain_unjoin(self):
        # execute ansible-playbook for unjoining domain and rebooting
        print("ansible domain unjoin")
        # self.get_domain_info()
        for item in self.ip_nametag_mapping_list:
            private_ip = item['private_ip']
            # os.system(f'ansible-playbook --ask-vault-pass domain_unjoin.yml -e "private_ip={private_ip} \
                    # domain_user={self.domain_user} domain_passwd={self.domain_passwd}"')
            proc=subprocess.Popen([f'ansible-playbook --vault-password-file=.passwd domain_unjoin.yml -e "private_ip={private_ip} \
                    domain_user={self.domain_user} domain_passwd={self.domain_passwd}"'],shell=True, stdin=subprocess.PIPE)

    def delete_vault_passwd(self):
        os.system('sudo rm .passwd')
=======
    def ansible_ping_check(self):
        # check ansible localhost
        exit_code=subprocess.call('ansible localhost -m ping',shell=True)
        print(exit_code)

        # check ansible remote target
        exit_code=subprocess.call('ansible all -m win_ping',shell=True)
        print(exit_code)


    def ansible_change_hostname_and_reboot(self):
        # execute ansible-playbook for changing hostname and rebooting
        for item in self.ip_nametag_mapping_list:
            private_ip = item['private_ip']
            name_tag = item['name_tag']
            os.system(f'ansible-playbook change_hostname.yml -e "private_ip={private_ip} name_tag={name_tag}"')

    def ansible_domain_join(self):
        # execute ansible-playbook for joining domain and rebooting
        print("Insert Domain name : ", end='')
        domain_name = input()
        print("Insert Domain user : ", end='')
        domain_user = input()
        print("Insert Domain password : ",end='')
        domain_passwd = input()
        for item in self.ip_nametag_mapping_list:
            private_ip = item['private_ip']
            os.system(f'ansible-playbook domain_join.yml -e "private_ip={private_ip} domain_name={domain_name} \
                    domain_user={domain_user} domain_passwd={domain_passwd}"')

    def ansible_domain_unjoin(self):
        # execute ansible-playbook for unjoining domain and rebooting
        print("Insert Domain user : ", end='')
        domain_user = input()
        print("Insert Domain password : ",end='')
        domain_passwd = input()
        for item in self.ip_nametag_mapping_list:
            private_ip = item['private_ip']
            os.system(f'ansible-playbook domain_unjoin.yml -e "private_ip={private_ip} \
                    domain_user={domain_user} domain_passwd={domain_passwd}"')
>>>>>>> b9456e5342c33987983110ceb7df2e01843aec16

if __name__ == '__main__':
    Ec2Auto = Ec2Auto()
    Ec2Auto.read_ini()
<<<<<<< HEAD

    Ec2Auto.awscli_iam_getuser()
    Ec2Auto.awscli_ec2_instance_name_tag()
    Ec2Auto.write_vault_passwd()
    Ec2Auto.ansible_ping_check()
    Ec2Auto.get_domain_info()
    # Ec2Auto.ansible_domain_unjoin()
    Ec2Auto.ansible_change_hostname_and_reboot()
    Ec2Auto.ansible_domain_join()
    # Ec2Auto.delete_vault_passwd()
=======
    Ec2Auto.awscli_iam_getuser()
    Ec2Auto.awscli_ec2_instance_name_tag()


    Ec2Auto.ansible_ping_check()
    Ec2Auto.ansible_domain_unjoin()
    Ec2Auto.ansible_change_hostname_and_reboot()
    Ec2Auto.dump_yaml_from_dict()

    # Ec2Auto.ansible_domain_join()
>>>>>>> b9456e5342c33987983110ceb7df2e01843aec16
