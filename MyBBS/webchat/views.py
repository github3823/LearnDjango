from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from webchat import models
import queue,json,time,os


GLOBAL_MSG_QUEUES ={

}


@login_required
def dashboard(request):

    #print(dir(request.user.userprofile.friends.select_related))
    return render(request,'webchat/dashboard.html')


@login_required
def send_msg(request):
    print(request.POST)
    print(request.POST.get("msg"))
    # if request.POST.get()
    msg_data = request.POST.get("data")
    if msg_data:
        msg_data  = json.loads(msg_data)
        msg_data['timestamp'] = time.time()
        if msg_data['type'] == 'single':
            if not GLOBAL_MSG_QUEUES.get(int(msg_data['to'])):
                GLOBAL_MSG_QUEUES[int(msg_data['to'])] = queue.Queue()
            GLOBAL_MSG_QUEUES[int(msg_data['to'])].put(msg_data)
        else:#group
            group_obj = models.WebGroup.objects.get(id=msg_data['to'])
            for member in group_obj.members.select_related():
                if not GLOBAL_MSG_QUEUES.get(member.id):#如果字典里不存在这个用户的queue
                    GLOBAL_MSG_QUEUES[member.id] = queue.Queue()#就创建一个
                if member.id != request.user.userprofile.id:#判断是不是自己，且不给自己发送消息
                    GLOBAL_MSG_QUEUES[member.id].put(msg_data)#给其它人发消息



    print(GLOBAL_MSG_QUEUES)
    # if not GLOBAL_MSG_QUEUES.get()

    return HttpResponse('---msg recevied---')

def get_new_msgs(request):

    if request.user.userprofile.id not in GLOBAL_MSG_QUEUES:
        print("no queue for user [%s] " %request.user.userprofile.id, request.user)
        GLOBAL_MSG_QUEUES[request.user.userprofile.id] = queue.Queue()
    msg_count = GLOBAL_MSG_QUEUES[request.user.userprofile.id].qsize()
    q_obj = GLOBAL_MSG_QUEUES[request.user.userprofile.id]
    msg_list = []
    if msg_count >0:
        for msg in range(msg_count):
            msg_list.append(q_obj.get())
        print("new msgs:",msg_list)
    else:#没消息，要挂起
        print("no new msg for",request.user,request.user.userprofile.id)
        # print(GLOBAL_MSG_QUEUES)
        try:
            msg_list.append(q_obj.get(timeout=60))#如果60秒内获取到消息
        except queue.Empty:
            print("\033[41;1mno msg for [%s][%s],tiemout\033[0m" %(request.user.userprofile.id,request.user))
    return HttpResponse(json.dumps(msg_list))

def delete_cache_key(request):
    cache_key = request.GET.get("cache_key")
    cache.delete(cache_key)
    return HttpResponse("cache key [%s] got deleted " % cache_key)


def file_upload(request):
    print(request.POST,request.FILES)
    file_obj = request.FILES.get('file')
    user_file_dir = "templates/webchat/uploads/%s"  %request.user.userprofile.id
    if not os.path.isdir(user_file_dir):
        os.mkdir(user_file_dir)
    new_file_name = "%s/%s" %(user_file_dir,file_obj.name)
    recv_size = 0
    with open(new_file_name,'wb') as new_file_obj:
        for chunk in file_obj.chunks():
            new_file_obj.write(chunk)
            recv_size += len(chunk)
            cache.set(file_obj.name,recv_size)
    return HttpResponse('upload success')


def file_upload_progress(request):
    pass