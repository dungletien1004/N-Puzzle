from queue import PriorityQueue
from queue import Queue
from queue import LifoQueue
class State:
    def __init__(self,state,parent,action,depth,ksize):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.ksize = ksize
        self.goal = [0]
        for i in range(1,ksize*ksize):
            self.goal.append(i)
    def check(self):
        if self.state == self.goal:
            return True
        return False
    def available_moves(self,x,ksize): 
        moves = ['Left', 'Right', 'Up', 'Down']
        #ô trống không thể di chuyển sang trái
        if x % ksize == 0:
            moves.remove('Left')
        #ô trống không thể di chuyển sang phải
        if x % ksize == ksize-1:
            moves.remove('Right')
        #ô trống không thể di chuyển lên trên
        if x - ksize < 0:
            moves.remove('Up')
        #ô trống không thể di chuyển xuống dưới
        if x + ksize > ksize*ksize - 1:
            moves.remove('Down')
        return moves
    # hàm thêm nút con vao gốc
    def add_children(self,ksize):
        x = self.state.index(0)
        moves = self.available_moves(x,ksize)
        
        children = []
        for action in moves:
            temp = self.state.copy()
            #ô trống di chuyển sang trái
            if action == 'Left':
                temp[x], temp[x - 1] = temp[x - 1], temp[x]
             #ô trống di chuyển sang phải
            elif action == 'Right':
                temp[x], temp[x + 1] = temp[x + 1], temp[x]
            #ô trống di chuyển lên trên
            elif action == 'Up':
                temp[x], temp[x - ksize] = temp[x -ksize], temp[x]
            #ô trống di chuyển xuống dưới
            elif action == 'Down':
                temp[x], temp[x + ksize] = temp[x + ksize], temp[x]
            children.append(State(temp, self, action, self.depth + 1, ksize))
        return children
    #hàm trả về lời giải
    def solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]        
        solution.reverse()
        return solution 
def DFS(given_state,ksize):
    #khởi tạo nút gốc
    root = State(given_state, None, None, 0, ksize)
    if root.check():
        return root.solution()
    # tạo ngăn xếp stack
    frontier = LifoQueue()
    frontier.put(root)
    visited = []
    
    while not(frontier.empty()):
        current_node = frontier.get()
        max_depth = current_node.depth 
        visited.append(current_node.state)
        
        if max_depth == 50:
            continue #ngừng tìm kiếm
        #tạo các nút con
        children = current_node.add_children(ksize) 
        for child in children:
            #kiểm tra xem nút này đã duyệt hay chưa 
            if child.state not in visited:
                #kiểm tra đã đến mục tiêu hay chưa
                if child.check():
                    return child.solution(), len(visited)
                frontier.put(child)
    #trả về không tìm thấy lời giải và số nút đã duyệt
    return (("Không thể tìm thấy lời giải ở độ sâu bị giới hạn."), len(visited))

#hàm in puzzle theo dạng ma trận k*k
def print_puzzle(state,ksize):
    for i in range(0,ksize*ksize):
        if i % ksize == ksize-1:
            print(state[i],'\n')
        else:
            print(state[i],end =' ')
#hàm sinh puzzle ngẫu nhiên
import random
def puzzle_start(ksize):
    liststart = []
    for i in range(ksize*ksize):
        check = False
        while check != True:
            r = random.randint(0,ksize*ksize-1)        
            if r not in liststart:
                liststart.append(r)
                check = True
    return liststart

import time
if __name__ == "__main__":
    ksize = int(input("nhập k (n-puzzle với n = k*k - 1)  : "))
    puzzle = []
    print("1. Nhập Puzzle từ bàn phím")
    print("2 . Sinh Puzzle ngẫu nhiên")
    option = int(input('nhập lựa chọn : '))
    if option == 1:
        for id in range(0,ksize*ksize):
            r = int(input())
            puzzle.append(r)
    else:
        puzzle = puzzle_start(ksize)
    start = time.time()
    print(ksize*ksize - 1," Puzzle vừa tạo là :")
    print_puzzle(puzzle,ksize)
    dfs = DFS(puzzle,ksize)
    print(dfs)
    print('thời gian bỏ ra : %0.2fs' % (time.time()-start))
