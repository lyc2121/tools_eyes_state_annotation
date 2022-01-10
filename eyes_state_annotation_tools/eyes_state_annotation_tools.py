import tkinter
from tkinter import *
import cv2
import os
from PIL import Image, ImageTk
from tkinter import filedialog
import tkinter.font as tf

class get_veido_paly():
    def __init__(self):
        self.flag=0
        root=tkinter.Tk()
        self.page2=root
        self.movieLabel = Label(root)
        self.movieLabel.pack(padx=10, pady=10)
        self.frame=0
        self.open_close_eye_list=[]
        self.path_text=''

        root.title('视频播放器')
        root.geometry('1500x1000+0+0')

        self.start_button = tkinter.Button(self.page2, text='0-睁眼', width=30,height=4)
        self.start_button.place(x=430, y=850)
        self.start_button.bind("<Button-1>", self.start)

        self.stop_button = tkinter.Button(self.page2, text='1-闭眼', width=30,height=4)
        self.stop_button.place(x=730, y=850)
        self.stop_button.bind("<Button-1>", self.stop)

        self.save_button = tkinter.Button(self.page2, text='保存', width=30, height=4)
        self.save_button.place(x=1030, y=850)
        self.save_button.bind("<Button-1>", self.save)

        # self.save_button = tkinter.Button(self.page2, text='上一帧', width=30, height=4)
        # self.save_button.place(x=250, y=700)
        # self.save_button.bind("<Button-1>", self.get_up_frame)

        self.label_show=tkinter.Label(self.page2,text="当前帧数：",  width=30,height=4,		#text为显示的文本内容
                 bg='black',fg='white')
        self.label_show.place(x=630, y=750)

        ft = tf.Font(family='微软雅黑', size=100)

        self.text_frame = tkinter.Text(self.page2, width=30, height=4,  # text为显示的文本内容
                                        bg='white', fg='black')
        self.text_frame.place(x=880, y=760)

        self.text_frame.tag_add('tag','15.0')  # 申明一个tag,在a位置使用
        self.text_frame.tag_config('tag', foreground='red', font=ft)


        self.video_get(self.movieLabel)

    def set_label(self):
        self.text_frame.delete(0.0, tkinter.END)
        self.text_frame.insert('insert', "   "+str(self.frame))



    # 按钮的关联事件
    def start(self, event):
        self.open_close_eye_list.append(0)
        self.flag = 1
        self.frame = self.frame + 1
        self.set_label()
        # self.video_loop(self.cap)

    def stop(self, event):
        self.open_close_eye_list.append(1)
        self.flag = 1
        self.frame = self.frame + 1
        self.set_label()
        # self.video_loop(self.cap)
    def save(self,event):
        with open(self.path_text,'w') as f_out:
            for i in range(len(self.open_close_eye_list)):
                f_out.write(str(self.open_close_eye_list[i])+" ")
                if i>0 and i % 100==0:
                    f_out.write("\n")
        f_out.close()
        os._exit(0)
    def get_up_frame(self):
        self.flag=1
        self.frame=self.frame-2
        self.cap=self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame)
        self.video_loop(self.cap)
        # 获取视频
    def video_get(self, movieLabel):
        movie_path = filedialog.askopenfilename()  # 打开文件路径

        path_file=str(movie_path).strip().split("/")[:-1]
        path_video_name=str(movie_path).strip().split("/")[-1]
        path_pclose_name=str(path_video_name).replace('.mp4','.txt')


        for i in range(len(path_file)):
            if i==0:
                self.path_text = self.path_text  + path_file[i]
            else:
                self.path_text = self.path_text + "/" + path_file[i]

        self.path_text = self.path_text + "/" + path_pclose_name

        if os.path.exists(self.path_text):
            with open(self.path_text, 'r') as f_in:
                datas = f_in.readlines()
                print(datas)
                for data in datas:
                    items = data.strip('\n').strip().split(' ')
                    for item in items:
                        self.open_close_eye_list.append(item)
                f_in.close()
            self.frame=len(self.open_close_eye_list)
            self.set_label()

        self.cap = cv2.VideoCapture(movie_path)  # 获取视频
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame)
        self.wait_time = 1000 / self.cap.get(5)  # 视频频率
        self.video_loop(self.cap)

    # 视频播放
    def video_loop(self, cap):
        while 1:
            cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame)
            ret, frame = cap.read()  # 读取照片
            if ret:
                self.picture_show(frame)
                if self.flag == 1:
                    self.flag = 0

    def picture_show(self,frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        current_image = Image.fromarray(img).resize((1280, 720))  # 将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        self.movieLabel.imgtk = imgtk
        self.movieLabel.config(image=imgtk)
        self.movieLabel.update()



if __name__ == '__main__':
   a=get_veido_paly()







