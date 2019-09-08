#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import json, os
import subprocess
from tkinter import messagebox

def read_settings():
    settings = {}
    # Read Setting file
    if not os.path.exists("setting.json"):
        settings = {
            "id": "",
            "pw":"",
            "region":"2",
            "bet how": "2",
            "reverse" : 0,
            "money": "1",
            "fixed":20,
            "table": "2",
            "fixedtbl":1,
            "limitbet" : 100,
            "limitmoney" : 100,
            "standardbet": [500], 
            "lossbet": [260, 130, 60, 30, 20, 20, 20, 20, 20, 20], 
            "winbet": [500, 700, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000],
            "game": "365826.com"
        }
        with open('setting.json', 'w') as outfile:
            json.dump(settings, outfile)
    with open('setting.json') as json_file:
        settings = json.load(json_file)

    return settings

def write_settings(settings):
    with open('setting.json', 'w') as json_file:
        json.dump(settings, json_file)

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        setting = read_settings()       
        
        self.id = tk.StringVar()
        self.id.set(setting["id"])
        self.pw = tk.StringVar()
        self.pw.set(setting["pw"])

        self.region = tk.StringVar()
        self.region.set(setting['region'])
        self.method = tk.StringVar()
        self.method.set(setting['bet how'])
        self.reverse = tk.IntVar()
        self.reverse.set(setting["reverse"])
        self.money = tk.StringVar()
        self.money.set(setting['money'])
        self.fixed = tk.IntVar()
        self.fixed.set(setting['fixed'])
        self.table = tk.StringVar()
        self.table.set(setting['table'])
        self.fixedtbl = tk.IntVar()
        self.fixedtbl.set(setting['fixedtbl'])
        self.limitbet = tk.StringVar()
        self.limitbet.set(setting["limitbet"])
        self.limitmoney = tk.StringVar()
        self.limitmoney.set(setting["limitmoney"])

        self.betloss = []
        self.betstandard = []
        self.betwin = []

        self.game_values = ["365826.com","21365z.com","36389.com"]
        self.box_value = tk.StringVar()
        self.box_value.set(setting["game"])
        self.createWidgets(setting)
        #<create the rest of your GUI here>

    def createWidgets(self, settings):        

        main = tk.Frame(self.parent, width=440)
        tk.Frame(main, height=20).pack(side=tk.TOP)

        row1 = tk.Frame(main)
        tk.Label(row1, width=5, text="账号").pack(side=tk.LEFT)
        tk.Entry(row1, textvariable=self.id).pack(side=tk.LEFT, fill=tk.X)
        tk.Label(row1, width=5, text="密码").pack(side=tk.LEFT)
        tk.Entry(row1, textvariable=self.pw).pack(side=tk.LEFT, fill=tk.X)
        row1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        tk.Frame(main, height=15).pack(side=tk.TOP)
        
        lf1 =tk.LabelFrame(main, text='百家乐', labelanchor="nw")        
        tk.Radiobutton(lf1, text='国际厅',value= "1", variable=self.region).pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        tk.Radiobutton(lf1, text='旗舰厅', value="2", variable=self.region).pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        chk_europe = tk.Radiobutton(lf1, text='欧洲厅', value="3", variable=self.region)
        chk_europe.pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        chk_europe.configure(state = tk.DISABLED)
        lf1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        tk.Frame(main, height=10).pack(side=tk.TOP)

        lf =tk.LabelFrame(main, text='下注方法', labelanchor="nw")        
        tk.Radiobutton(lf, text='锅', value="1", variable=self.method).pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        tk.Radiobutton(lf, text='过去', value="2", variable=self.method).pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        tk.Checkbutton(lf, text='相反', variable=self.reverse).pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        lf.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        tk.Frame(main, height=10).pack(side=tk.TOP)

        lf4 =tk.LabelFrame(main, text='下注金量', labelanchor="nw")        
        tk.Radiobutton(lf4, text='减少增长', value="1", variable=self.money, command=self.checkmoneyamount).pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        tk.Radiobutton(lf4, text='固定', value="2", variable=self.money, command=self.checkmoneyamount).pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        #tk.Checkbutton(lf4, text='相反', variable=self.reverse).pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        tk.Entry(lf4, textvariable=self.fixed).pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        lf4.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        tk.Frame(main, height=10).pack(side=tk.TOP)

        lf5 =tk.LabelFrame(main, text='表设置', labelanchor="nw")        
        tk.Radiobutton(lf5, text='随机', value="1", variable=self.table).pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        tk.Radiobutton(lf5, text='固定', value="2", variable=self.table).pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        #tk.Checkbutton(lf4, text='相反', variable=self.reverse).pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        tk.Entry(lf5, textvariable=self.fixedtbl).pack(side=tk.LEFT, fill=tk.X, padx=20, pady=10)
        lf5.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        tk.Frame(main, height=10).pack(side=tk.BOTTOM)

        row6 = tk.LabelFrame(main, text='限制', labelanchor="nw")     
        tk.Label(row6, width=5, text="下注数").pack(side=tk.LEFT, pady=10)
        tk.Entry(row6, textvariable=self.limitbet).pack(side=tk.LEFT, fill=tk.X, padx=10, pady=10)
        tk.Label(row6, width=5, text="存钱").pack(side=tk.LEFT, pady=10)
        tk.Entry(row6, textvariable=self.limitmoney).pack(side=tk.LEFT, fill=tk.X, padx=10, pady=10)
        row6.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)


        lf2 = tk.Frame(main)
        lf3 = tk.Frame(lf2)

        # Buttons
        tk.Button(lf2, padx=5, pady=2, text="取消", command = self.parent.destroy, width=15).pack(side=tk.RIGHT)
        tk.Frame(lf2, width=20).pack(side=tk.RIGHT)
        tk.Button(lf2, padx=5, pady=2, text="保存", command = self.save_setting,width=15).pack(side=tk.RIGHT)
        lf3.pack(sid=tk.TOP,fill=tk.X)
        lf2.pack(side=tk.BOTTOM, fill=tk.Y)
        main.pack(side=tk.LEFT, fill=tk.Y)

        tk.Frame(self.parent, height=26).pack(side=tk.TOP)
        fff = tk.Frame(self.parent)
        tk.Label(fff, width=5, text="服务器").pack(side=tk.LEFT)
        
        self.cb=ttk.Combobox(fff,values=self.game_values,width=15,textvariable=self.box_value)        
        #self.cb.current(0)
        self.cb.pack(side=tk.TOP)

        fff.pack(side=tk.TOP)
        tk.Frame(self.parent, height=18).pack(side=tk.TOP)

        extend = tk.LabelFrame(self.parent, text="减少/增长", labelanchor="n", width=100)
        item = tk.Frame(extend)
        tk.Label(item, width=5, text="失").pack(side=tk.LEFT, pady=5)
        entrystandard = tk.Entry(item, width=10, justify='center')
        entrystandard.delete("0","end")
        entrystandard.insert("0",settings["standardbet"][0])
        entrystandard.pack(side=tk.LEFT)
        if self.money.get() == "2":
            entrystandard.configure(state = tk.DISABLED)
        self.betstandard.append(entrystandard)

        tk.Label(item, width=5, text="赢").pack(side=tk.RIGHT, pady=5)
        item.pack(side=tk.TOP)
        
        for i in range(17):
            item1 = tk.Frame(extend)
            entryloss = tk.Entry(item1, width=10, justify='center')
            entrywin = tk.Entry(item1, width=10, justify='center')
            entryloss.delete("0","end")
            entryloss.insert("0",settings["lossbet"][i])
            entrywin.delete("0","end")
            entrywin.insert("0",settings["winbet"][i])
            entryloss.pack(side=tk.LEFT)
            entrywin.pack(side=tk.RIGHT)
            if self.money.get() == "2":
                entrywin.configure(state = tk.DISABLED)
                entryloss.configure(state = tk.DISABLED)
                
            item1.pack(side=tk.TOP)
            self.betloss.append(entryloss)
            self.betwin.append(entrywin)        
        
        extend.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    def checkmoneyamount(self):
        if self.money.get() == "2":
            for i in self.betloss:
                i.configure(state = tk.DISABLED)
            for i in self.betwin:
                i.configure(state = tk.DISABLED)
            for i in self.betstandard:
                i.configure(state = tk.DISABLED)
        else:
            for i in self.betloss:
                i.configure(state = tk.NORMAL)
            for i in self.betwin:
                i.configure(state = tk.NORMAL)
            for i in self.betstandard:
                i.configure(state = tk.NORMAL)

    def save_setting(self):        
        vali = []
        for i in range(2,5000):
            vali.append(i*10)

        if self.fixed.get() not in vali:
            messagebox.showwarning("警告","输入正确的数字 下注金量")
            return
        
        bet_for_loss = [x.get() for x in self.betloss]
        bet_for_win = [x.get() for x in self.betwin]
        setting = {
            "id": self.id.get(),
            "pw":self.pw.get(),
            "region":self.region.get(),
            "bet how": self.method.get(),
            "reverse" : self.reverse.get(),
            "money" : self.money.get(),
            "fixed" : self.fixed.get(),
            "table": self.table.get(),
            "fixedtbl" : self.fixedtbl.get(),
            "limitbet" : self.limitbet.get(),
            "limitmoney" : self.limitmoney.get(),
            "lossbet":bet_for_loss,
            "winbet":bet_for_win,
            "standardbet": [self.betstandard[0].get()],
            "game": self.box_value.get()
        }
        write_settings(setting)
    def start(self):
        #os.system('python autobetter.py')
        subprocess.Popen("python autobetter.py", shell=True)
    def printf(self, str):
        print (str)

if __name__ == "__main__":
    root = tk.Tk()
    ui = MainApplication(root).pack()
    root.geometry("550x500+400+10")
    root.resizable(False, False)
    root.title('设置')
    root.mainloop()
