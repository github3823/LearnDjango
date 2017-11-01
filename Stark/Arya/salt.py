
import os,sys

if __name__ == "__main__":
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stark.settings")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#环境变量，当前路径
    #print(BASE_DIR)
    sys.path.append(BASE_DIR)#加入环境变量
    from Arya.action_list import actions
    from Arya.backends.utils import ArgvManagement
    obj = ArgvManagement(sys.argv)