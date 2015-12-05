import class_npc

def save(user,npc_group,npc_cnt):
    f = open('Data/save/save.txt','w')
    f.write(str(user.x)+'\n')
    f.write(str(user.y)+'\n')
    f.write(str(user.step_cnt)+'\n')
    f.write(str(user.hp)+'\n')
    f.write(str(user.maxhp)+'\n')
    f.write(str(user.gold)+'\n')
    f.write(str(user.dice_num)+'\n')
    f.write(str(user.suspicion)+'\n')
    f.write(str(user.last_tool)+'\n')
    f.write(str(user.last_type)+'\n')
    f.write(str(user.last_place)+'\n')
    f.write(str(user.tool_s)+'\n')
    f.write(str(user.type_s)+'\n')
    f.write(str(user.place_s)+'\n')

    f.write(str(npc_cnt)+"\n")
    for npc in npc_group:
        f.write(str(npc.type)+'\n')
        f.write(str(npc.x)+'\n')
        f.write(str(npc.y)+'\n')
        f.write(str(npc.waiting_time)+'\n')
        f.write(str(npc.dir)+'\n')
        f.write(str(npc.state)+'\n')
        f.write(str(npc.type_s)+'\n')
        f.write(str(npc.speech)+'\n')
        f.write(str(npc.place)+'\n')
    f.close()

def load(user,npc_group, bg):
    f = open('Data/save/save.txt','r')
    user.x = int(f.readline()) - 8
    user.y = int(f.readline()) - 8
    user.step_cnt = (int(f.readline()))
    user.hp = (int(f.readline()))
    user.maxhp = (int(f.readline()))
    user.gold = (int(f.readline()))
    user.dice_num = (int(f.readline()))
    user.suspicion = (int(f.readline()))
    user.last_tool = (int(f.readline()))
    user.last_type = (int(f.readline()))
    user.last_place = (str(f.readline()).split('\n')[0])
    user.tool_s= (str(f.readline()).split('\n')[0])
    user.type_s= (str(f.readline()).split('\n')[0])
    user.place_s= (str(f.readline()).split('\n')[0])

    npc_cnt = int(f.readline())
    for i in range(npc_cnt):
        temp_npc=class_npc.Npc(0,0,user,bg,npc_group,int(f.readline()))
        temp_npc.x = int(f.readline())
        temp_npc.y = int(f.readline())
        temp_npc.waiting_time = float(f.readline())
        temp_npc.dir = int(f.readline())
        temp_npc.state = int(f.readline())
        temp_npc.type_s = (str(f.readline()).split('\n')[0])
        temp_npc.speech = (str(f.readline()).split('\n')[0])
        temp_npc.place = (str(f.readline()).split('\n')[0])
        npc_group.append(temp_npc)
    f.close()

    return npc_cnt