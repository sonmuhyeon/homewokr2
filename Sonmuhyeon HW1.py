def add_data(friend):
    friend_list.append(friend)
    flistLen=len(friend_list)

    if flistLen>=2:
        if friend_list[flistLen-1][1]>=friend_list[flistLen-2][1]:
            temp=friend_list[flistLen-2]
            friend_list[flistLen-2]=friend_list[flistLen-1]
            friend_list[flistLen-1]=temp

   

def delete_data(position):
    if friend_list2[position] != None:
         del friend_list[position]
         print(friend_list)
         friend_list2[position]=None
    else:
        print("삭제할 데이터가 존재하지 않습니다.")


friend_list=[]
friend_list2=friend_list

if __name__ == "__main__":
    
    while(True):
        select = int((input("선택하세요(1:추가,2:삭제,3:종료)-->")))

        if select == 1:
            friend=eval(input("추가할 데이터-->"))
            add_data(friend) 
            print(friend_list)

        elif select == 2:
            position=int(input("삭제할 순서-->"))-1
            delete_data(position)

        elif select == 3:
            break