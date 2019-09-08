#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
import time, sys, os, json, random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions

settings = {}

default_bet_money_index = 17

def read_settings():
    if os.path.exists('setting.json'):
    # Read Setting file
        with open('setting.json') as json_file:
            settings = json.load(json_file)
    else:
        sys.exit('不能打开设置文件.')
    
    bet_serise = []
    betstandard = settings['standardbet']
    betloss = settings['lossbet']
    betwin = settings['winbet']

    bet_serise.extend(reversed(betloss))
    bet_serise.extend(betstandard)
    bet_serise.extend(betwin)   

    settings['bet_serise'] = bet_serise
    return settings

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("return [window.outerWidth - window.innerWidth + arguments[0], window.outerHeight - window.innerHeight + arguments[1]];", width, height)
    driver.set_window_size(*window_size)

#toggle commission checkbox
def toggle_commission(driver, flag):
    #print ("Toggling commission")
    while True:
        ret = driver.execute_script('\
            var _flag = arguments[0]; \
            console.log("Toggle commission. =>", _flag); \
            var _root = egret.sys.$TempStage.$children[0].$children[0].$children[0]; \
            var _toggleCtrl = undefined; \
            for (var _i=0; _i<_root.$children.length; _i++){ \
                if (_root.$children[_i].$children === null || _root.$children[_i].$children === undefined) continue; \
                if (_root.$children[_i].$children[0] === null || _root.$children[_i].$children[0] === undefined) continue; \
                if (_root.$children[_i].$children[0].$Component === null || _root.$children[_i].$children[0].$Component === undefined) continue;\
                if (_root.$children[_i].$children[0].$Component.length < 2) continue;\
                var _tempCompString = _root.$children[_i].$children[0].$Component[1]; \
                if (_tempCompString !== undefined && _tempCompString === "GameBacSkin.CommissionToggleSkin"){ \
                    _toggleCtrl = _root.$children[_i].$children[0]; \
                    break; \
                } \
            } \
            if (_toggleCtrl.selected !== _flag){ \
                var _posX = _toggleCtrl.$parent.x + 15; \
                var _posY = _toggleCtrl.$parent.y + 15; \
                console.log("Click pos for commission ctrl: ","(",_posX,":",_posY,")"); \
                egret.TouchEvent.dispatchTouchEvent(_toggleCtrl, egret.TouchEvent.TOUCH_BEGIN, !0, !0, _posX, _posY, !0);\
                egret.TouchEvent.dispatchTouchEvent(_toggleCtrl, egret.TouchEvent.TOUCH_END, !0, !0, _posX, _posY, !1);\
                egret.TouchEvent.dispatchTouchEvent(_toggleCtrl, egret.TouchEvent.TOUCH_TAP, !0, !0, _posX, _posY, !1);\
            }\
            return _toggleCtrl.selected; \
        ', flag)
        
        if ret == flag:
            #print ("Commission Set OK!")
            break
        else:
            print ("Still trying of selecting coin..", flag)
            time.sleep(1)

#select coin unit
def select_coin_unit(driver, unit):
    # select first 10 coin mark.
    # 1:10, 2:50, 3:100, 4:1K, 5:10K
    coin_data = {10:1,50:3,100:5,1000:7,10000:9}
    #print (unit, " coins unit selecting ...")

    while True:
        ret = driver.execute_script('var _coins = egret.sys.$TempStage.$children[0].$children[0].$children[0].$children[20];\
            var _index = parseInt(arguments[0]);\
            console.log("coins setting..."); \
            console.log(_index); \
            console.log(_coins.$children.length); \
            var _selectorPosX = _coins.$children[0].x; \
            console.log(Math.abs(_coins.$children[_index].x - _selectorPosX));\
            if (Math.abs(_coins.$children[_index].x - _selectorPosX) > 10) {\
                var _posX = _coins.$children[_index].x + 20; \
                var _posY = _coins.$children[_index].$parent.y + 20;\
                console.log(_posX);\
                console.log(_posY);\
                egret.TouchEvent.dispatchTouchEvent(_coins.$children[_index], egret.TouchEvent.TOUCH_BEGIN, !0, !0, _posX, _posY, !0);\
                egret.TouchEvent.dispatchTouchEvent(_coins.$children[_index], egret.TouchEvent.TOUCH_END, !0, !0, _posX, _posY, !1);\
                egret.TouchEvent.dispatchTouchEvent(_coins.$children[_index], egret.TouchEvent.TOUCH_TAP, !0, !0, _posX, _posY, !1);\
            };\
            if (Math.abs(_coins.$children[_index].x - _coins.$children[0].x) < 10) \
                return 1;\
            return 0;\
            ', coin_data[unit])        
        if ret:
            break
        else:
            print ("Still trying of selecting coin..", unit)
            time.sleep(1)

#
def get_selected_table_info(driver):
    ret = driver.execute_script(' \
        console.log("get_selected_table..."); \
        var _root = egret.sys.$TempStage.$children[0].$children[0].$children[0]; \
        var _tables = undefined; \
        var ret = {result: "Error"}; \
        console.log(_root.$children.length); \
        for (var _i=0; _i<_root.$children.length; _i++){ \
            if (_root.$children[_i].$Component === null || _root.$children[_i].$Component === undefined) continue; \
            var _tempCompString = _root.$children[_i].$Component[1]; \
            if (_tempCompString !== undefined && _tempCompString === "GameBacSkin.MultiTableSkin"){ \
                console.log("Found"); \
                _tables = _root.$children[_i].$children[0].$children[0].$children[0]; \
                var _selectedIndex = ""; \
                var _selectedName = ""; \
                var _selectedRemain = ""; \
                for (var _j=0; _j<_tables.$children.length; _j++){ \
                    var _tempSource = _tables.$children[_j].$children[0].$children[0].source; \
                    console.log("id:",_j, "  $displayFlags: ", _tempSource);\
                    if (_tempSource === undefined) continue; \
                    if (_tempSource === "table_tab_pressed") {\
                        _selectedIndex = _j; \
                        _selectedName = _tables.$children[_j].$children[0].$children[1].text;\
                        _selectedRemain = _tables.$children[_j].$children[0].$children[3].$children[2].text;\
                        break; \
                    } \
                }\
                ret = {result:"Success", index: _selectedIndex, name: _selectedName, state: _selectedRemain}; \
                console.log(ret); \
                break; \
            } \
        } \
        return ret;\
        ')
    return ret

def select_table(driver, index):
    driver.execute_script(' \
        console.log("get_selected_table...", arguments[0]); \
        var _root = egret.sys.$TempStage.$children[0].$children[0].$children[0]; \
        var _tables = undefined; \
        var _index = arguments[0];\
        console.log(_root.$children.length); \
        for (var _i=0; _i<_root.$children.length; _i++){ \
            if (_root.$children[_i].$Component === null || _root.$children[_i].$Component === undefined) continue; \
            var _tempCompString = _root.$children[_i].$Component[1]; \
            if (_tempCompString !== undefined && _tempCompString === "GameBacSkin.MultiTableSkin"){ \
                console.log("Found"); \
                _tables = _root.$children[_i].$children[0].$children[0].$children[0]; \
                var _tempSource = _tables.$children[_index].$children[0].$children[0].source; \
                if (_tempSource !== "table_tab_pressed") {\
                    var _tbl = _tables.$children[_index].$children[0];\
                    var _posX = _tbl.x + 20; \
                    var _posY = _tbl.y + 20; \
                    console.log("Click pos for select table: ","(",_posX,":",_posY,")"); \
                    egret.TouchEvent.dispatchTouchEvent(_tbl.$children[0], egret.TouchEvent.TOUCH_BEGIN, !0, !0, _posX, _posY, !0);\
                    egret.TouchEvent.dispatchTouchEvent(_tbl.$children[0], egret.TouchEvent.TOUCH_END, !0, !0, _posX, _posY, !1);\
                    egret.TouchEvent.dispatchTouchEvent(_tbl.$children[0], egret.TouchEvent.TOUCH_TAP, !0, !0, _posX, _posY, !1);\
                } \
                break; \
            } \
        } \
        ',index)

def get_current_state(driver):
    ret = driver.execute_script(' \
        console.log("get_current_state..."); \
        var _root = egret.sys.$TempStage.$children[0].$children[0].$children[0]; \
        for (var _i=0; _i<_root.$children.length; _i++){ \
            if (_root.$children[_i].type === null || _root.$children[_i].type === undefined) continue; \
            if (_root.$children[_i].type === "dynamic")\
                return _root.$children[_i].text;\
        }\
        return "Error";\
        ')
    return ret

def get_remain_money(driver):
    ret = driver.execute_script(' \
        console.log("get_remain_money..."); \
        var _root = egret.sys.$TempStage.$children[0].$children[0].$children[0]; \
        for (var _i=0; _i<_root.$children.length; _i++){ \
            if (_root.$children[_i].width === 480 && _root.$children[_i].height === 60){ \
                return _root.$children[_i].$children[1].$children[1].$children[1].text;\
            } \
        }\
        return 0;\
        ')
    return ret.replace(",","")

#  Get My Betted Chip in Pot by characters.
def get_my_chip_in_pot(driver, char):
    ret = driver.execute_script(' \
        console.log("get_my_chip_in_pot...", arguments[0]); \
        var _root = egret.sys.$TempStage.$children[0].$children[0].$children[0]; \
        var _potBack = undefined; \
        var _char = arguments[0];\
        var ret = 0; \
        for (var _i=0; _i<_root.$children.length; _i++){ \
            if (_root.$children[_i].width === 480 && _root.$children[_i].height === 160){ \
                console.log("Found"); \
                _potBack = _root.$children[_i].$children[3]; \
                for (var _j =_potBack.$children.length-1; _j>0; _j--){ \
                    if (_potBack.$children[_j].$children[0].$children[0].$children[1] === undefined) continue; \
                    var _tempChar = _potBack.$children[_j].$children[0].$children[0].$children[1].text; \
                    console.log(_j,"=>",_tempChar);\
                    if (_tempChar === _char){\
                        var _chip = _potBack.$children[_j].$children[0].$children[1]; \
                        if (_chip.visible === true){\
                            ret = _chip.$children[0].$children[1].$children[1].text;\
                        } else {\
                            ret = 0;\
                        }\
                        break;\
                    }\
                }\
                console.log(ret); \
                break; \
            } \
        } \
        return ret;\
    ', char)
    return ret.replace(",","")

# click cancel button ! iterate from index 1 to 25 because index 0 element width&height is same with button holder
def pot_reset(driver):
    driver.execute_script(' \
        console.log("pot_reset..."); \
        var _root = egret.sys.$TempStage.$children[0].$children[0].$children[0]; \
        for (var _i=1; _i<_root.$children.length; _i++){ \
            if (_root.$children[_i].width === 480 && _root.$children[_i].height === 715){ \
                console.log("Found ", _i); \
                var _reset_btn = _root.$children[_i].$children[2];\
                var _posX = _reset_btn.x + 20; \
                var _posY = _reset_btn.y + 20; \
                console.log("Click pos for reset pot: ","(",_posX,":",_posY,")"); \
                egret.TouchEvent.dispatchTouchEvent(_reset_btn.$children[1], egret.TouchEvent.TOUCH_BEGIN, !0, !0, _posX, _posY, !0);\
                egret.TouchEvent.dispatchTouchEvent(_reset_btn.$children[1], egret.TouchEvent.TOUCH_END, !0, !0, _posX, _posY, !1);\
                egret.TouchEvent.dispatchTouchEvent(_reset_btn.$children[1], egret.TouchEvent.TOUCH_TAP, !0, !0, _posX, _posY, !1);\
                break;\
            }\
        }\
    ')

# click cancel button ! iterate from index 1 to 25 because index 0 element width&height is same with button holder
def pot_apply(driver):
    driver.execute_script(' \
        console.log("pot_reset..."); \
        var _root = egret.sys.$TempStage.$children[0].$children[0].$children[0]; \
        for (var _i=1; _i<_root.$children.length; _i++){ \
            if (_root.$children[_i].width === 480 && _root.$children[_i].height === 715){ \
                console.log("Found ", _i); \
                var _reset_btn = _root.$children[_i].$children[0];\
                var _posX = _reset_btn.x + 20; \
                var _posY = _reset_btn.y + 20; \
                console.log("Click pos for reset pot: ","(",_posX,":",_posY,")"); \
                egret.TouchEvent.dispatchTouchEvent(_reset_btn.$children[1], egret.TouchEvent.TOUCH_BEGIN, !0, !0, _posX, _posY, !0);\
                egret.TouchEvent.dispatchTouchEvent(_reset_btn.$children[1], egret.TouchEvent.TOUCH_END, !0, !0, _posX, _posY, !1);\
                egret.TouchEvent.dispatchTouchEvent(_reset_btn.$children[1], egret.TouchEvent.TOUCH_TAP, !0, !0, _posX, _posY, !1);\
                break;\
            }\
        }\
    ')
#  Bet Prepared
def bet_to_pot(driver, char, money):
    print (char,"==>",money,"Coins")
    
    if float(get_remain_money(driver)) < float(money):
        print ("没有足够的资金")
        return False

    remain = int(money)
    wan = int(remain / 10000)
    remain = remain - wan * 10000
    qian = int(remain / 1000)
    remain = remain - qian * 1000
    bai = int(remain / 100)
    remain = remain - bai * 100
    wushi = int(remain / 50)
    remain = remain - wushi * 50
    shi = int(remain / 10)

    if wan > 0:
        select_coin_unit(driver, 10000)
        click_coin_for_bet(driver, char, wan)
    if qian > 0:
        select_coin_unit(driver, 1000)
        click_coin_for_bet(driver, char, qian)
    if bai > 0:
        select_coin_unit(driver, 100)
        click_coin_for_bet(driver, char, bai)
    if wushi > 0:
        select_coin_unit(driver, 50)
        click_coin_for_bet(driver, char, wushi)
    if shi > 0:
        select_coin_unit(driver, 10)
        click_coin_for_bet(driver, char, shi)
    
    return True

def click_coin_for_bet(driver, char, clicks):
  
    driver.execute_script(' \
        console.log("bet_prepare...", arguments[0],arguments[1]); \
        var _root = egret.sys.$TempStage.$children[0].$children[0].$children[0]; \
        var _potBack = undefined; \
        var _char = arguments[0];\
        var _clicks = arguments[1];\
        var ret = 0; \
        for (var _i=0; _i<_root.$children.length; _i++){ \
            if (_root.$children[_i].width === 480 && _root.$children[_i].height === 160){ \
                console.log("Found"); \
                _potBack = _root.$children[_i].$children[3]; \
                for (var _j =_potBack.$children.length-1; _j>0; _j--){ \
                    if (_potBack.$children[_j].$children[0].$children[0].$children[1] === undefined) continue; \
                    var _tempChar = _potBack.$children[_j].$children[0].$children[0].$children[1].text; \
                    console.log(_j,"=>",_tempChar);\
                    if (_tempChar === _char){\
                        var _panel = _potBack.$children[_j].$children[0]; \
                        var _posX = _panel.$parent.x + 20; \
                        var _posY = _panel.$parent.y + 20; \
                        console.log("Click pos for bet prepared: ","(",_posX,":",_posY,")"); \
                        for (var _k=0; _k<_clicks; _k++){\
                            egret.TouchEvent.dispatchTouchEvent(_panel, egret.TouchEvent.TOUCH_BEGIN, !0, !0, _posX, _posY, !0);\
                            egret.TouchEvent.dispatchTouchEvent(_panel, egret.TouchEvent.TOUCH_END, !0, !0, _posX, _posY, !1);\
                            egret.TouchEvent.dispatchTouchEvent(_panel, egret.TouchEvent.TOUCH_TAP, !0, !0, _posX, _posY, !1);\
                        }\
                        break;\
                    }\
                }\
                console.log(ret); \
                break; \
            } \
        } \
    ', char, clicks)
    #time.sleep(2) # For test

#  Get Money in Pot by colors.
def get_pot_info(driver):
    ret = driver.execute_script(' \
        console.log("get_pot_info..."); \
        var _root = egret.sys.$TempStage.$children[0].$children[0].$children[0]; \
        var _potBack = undefined; \
        var ret = {result: "Error"}; \
        console.log(_root.$children.length); \
        for (var _i=0; _i<_root.$children.length; _i++){ \
            if (_root.$children[_i].$Component === null || _root.$children[_i].$Component === undefined) continue; \
            var _tempCompString = _root.$children[_i].$Component[1]; \
            if (_tempCompString !== undefined && _tempCompString === "GameBacSkin.BetTableSkinP"){ \
                console.log("Found"); \
                _potBack = _root.$children[_i].$children[3]; \
                var _blue = ""; \
                var _green = ""; \
                var _red = ""; \
                for (var _j=0; _j<_potBack.$children.length; _j++){ \
                    if (_potBack.$children[_j].$children[0].$children[0].$children[1] === undefined) continue; \
                    var _tempChar = _potBack.$children[_j].$children[0].$children[0].$children[1].text; \
                    if (_tempChar === "闲") _blue = _potBack.$children[_j].$children[0].$children[0].$children[0].text;\
                    if (_tempChar === "和") _green = _potBack.$children[_j].$children[0].$children[0].$children[0].text;\
                    if (_tempChar === "庄") _red = _potBack.$children[_j].$children[0].$children[0].$children[0].text;\
                }\
                ret = {result:"Success", blue: _blue, green: _green, red: _red}; \
                console.log(ret); \
                break; \
            } \
        } \
        return ret;\
    ')
    return ret

def update_bet_money(current, after, before):
    print ("更新赌注....")
    s = read_settings()
    if after == before:
        return current
    
    ret = current
    if after > before:
        if current < default_bet_money_index:
            ret = default_bet_money_index
        else:
            ret += 1
    else:
        if current > default_bet_money_index:
            ret = default_bet_money_index
        else:
            ret -= 1

    if ret > len(s['bet_serise']) - 1:
        ret = len(s['bet_serise']) - 1
    elif ret < 0:
        ret = 0

    return ret

#  Get Money in Pot by colors.
def get_last_bet(driver):
    ret = driver.execute_script(' \
        var _root = egret.sys.$TempStage.$children[0].$children[0].$children[0]; \
        var ret = "和"; \
        for (var _i=0; _i<_root.$children.length; _i++){ \
            if (_root.$children[_i].$Component === null || _root.$children[_i].$Component === undefined) continue; \
            var _tempCompString = _root.$children[_i].$Component[1]; \
            if (_tempCompString !== undefined && _tempCompString === "GameBacSkin.CurrentRoadmapSkin"){ \
                if (_root.$children[_i].$children[1].$children[0].$children.length <= 1)\
                    return "和";\
                ret = _root.$children[_i].$children[1].$children[0].$children[0].$children[0].text; \
            } \
        } \
        return ret;\
    ')
    return ret

def run(driver):
    print (" ")
    settings = read_settings()
    tblIndex = 0
    if (settings['table'] == "1"):
        tblIndex = random.randint(0,4)
    elif (settings['table'] == "2"):
        tblIndex = int(settings["fixedtbl"]) - 1

    select_table(driver, tblIndex)
    table_info = get_selected_table_info(driver)
    while table_info["result"] == "Error":
        print ("Getting Table Info Error.")
        time.sleep(1)
        table_info = get_selected_table_info(driver)

    print ("选中的表: ",table_info["name"], "   表状态:",table_info["state"])
    
    #
    limit = int(settings['limitbet'])
    bet_time = 2
    old_state = ""
    
    bet_money_index = default_bet_money_index # index of bet_serise

    limitmoney = False
    while limit > 0:
        save_money = float(read_settings()['limitmoney'])
        if float(get_remain_money(driver)) < save_money:
            if limitmoney == False:
                limitmoney = True
                print ("你不能因为缺钱而下注。 你的钱:", get_remain_money(driver), "  钱限制:",save_money)
            continue
        limitmoney = False

        cur_state = get_current_state(driver)
        if ( cur_state == "发牌中" or cur_state == "结算中"):
            if (old_state != cur_state):
                old_state = cur_state
                print (cur_state, "...")
            time.sleep(1)
            continue
        elif (cur_state == "洗牌中"):
            if (old_state != cur_state): # [Replace] Do change table.
                old_state = cur_state
                print (cur_state, "...")
            time.sleep(1) 
            continue
        # else:
        #     print ("在5秒之前开始.")
        
        seconds = int(cur_state)
        if seconds > 5:            
            time.sleep(0.5)
            continue
        
        # prepare betting
        toggle_commission(driver, True)
        select_coin_unit(driver, 10)
        old_seconds = 30
        while True:
            settings = read_settings()
            remain_seconds = int(get_current_state(driver))
            if remain_seconds == None:
                sys.exit("Parse Remain Seconds Error!")
            if old_seconds != remain_seconds:
                print ("打赌之前 ",remain_seconds,"秒...")
                old_seconds = remain_seconds

            if remain_seconds > bet_time:
                continue

            print (" ")
            print (" === 开始打赌 ===")
            pot_reset(driver)
            before_money = float(get_remain_money(driver))            
            
            if settings['bet how'] == "1":
                pot_info = get_pot_info(driver)

                if (pot_info["result"] == "Error"):
                    sys.exit("Parse Pot Info Error!")
                blue = float(str(pot_info['blue']).split("/")[0].replace(',',''))
                green = float(str(pot_info['green']).split("/")[0].replace(',',''))
                red = float(str(pot_info['red']).split("/")[0].replace(',',''))
                print ("闲 => ", blue, " ,   ","和 => ", green, " ,   ","庄 => ", red, " ,   ")
                
                ret = False
                if (blue >= red):
                    print ("闲 > 庄")
                    which = "闲"
                    if settings['reverse'] == 1:
                        which = "庄"

                    if settings['money'] == "1":
                        m = settings["bet_serise"][bet_money_index]
                    elif settings['money'] == "2":
                        m = settings["fixed"]

                    ret = bet_to_pot(driver, which, m)
                else:
                    print ("闲 < 庄")
                    which = "庄"
                    if settings['reverse'] == 1:
                        which = "闲"

                    if settings['money'] == "1":
                        m = settings["bet_serise"][bet_money_index]
                    elif settings['money'] == "2":
                        m = settings["fixed"]

                    ret = bet_to_pot(driver, which, m)

                if ret:
                    pot_apply(driver)
                else:
                    pot_reset(driver)

                time.sleep(2+1)
            elif settings['bet how'] == "2":
                which = get_last_bet(driver)
                print ("最近的 [",which,"]")

                if settings['reverse'] == 1: # Reverse
                    which = "庄" if which == "闲" else "闲"

                if which == "和":
                    which = "庄" if settings['reverse'] == 1 else "闲"
                
                if settings['money'] == "1":
                    m = settings["bet_serise"][bet_money_index]
                elif settings['money'] == "2":
                    m = settings["fixed"]

                ret = bet_to_pot(driver, which, m)

                if ret:
                    pot_apply(driver)
                else:
                    pot_reset(driver)

                time.sleep(2+1)

            while True:
                st = get_current_state(driver)
                if st != "发牌中" and st != "结算中":
                    break
                time.sleep(0.5)
            
            print (" === 打赌完成 ===")
            print (" ")
            time.sleep(2)
            after_money = float(get_remain_money(driver))
            print ("[结果]: 你的钱从 {} 改为 {}.  ".format(before_money, after_money))
            if before_money < after_money:
                print ("[:D] 胜利 ", after_money - before_money)
            elif before_money > after_money:
                print ("[:-(] 失去 ", after_money - before_money)
            else:
                print ("[:-|] 平局 ")
            #after_money += 20 # for test
            # if success
            if settings['money'] == "1" and before_money != after_money:
                bet_money_index = update_bet_money(bet_money_index, after_money, before_money)
            break

        limit -= 1

        #print (get_selected_table_info(driver), "==>", get_current_state(driver))
        #print (get_pot_info(driver))
        #print (get_remain_money(driver))
        #print (get_my_chip_in_pot(driver, "闲"), " : ", get_my_chip_in_pot(driver, "和"), " : ",get_my_chip_in_pot(driver, "庄"))
        time.sleep(3)


def wait_load_game(driver):
    tryCount = 15 # Wait to load Game for 15 seconds
    while tryCount > 0:
        try:
            driver.find_element_by_xpath('//*[@id="StageDelegateDiv"]')
        except:
            time.sleep(1)
            tryCount -= 1
            continue
        else:
            return True
    return False

#["365826.com","21365z.com","36389.com"]
def login(driver, game):

    if game == "365826.com":
        username_i = driver.find_element_by_xpath('//*[@id="username"]')
        password_i = driver.find_element_by_xpath('//*[@id="password"]')
        loginBtn_b = driver.find_element_by_xpath('//*[@id="loginBtn"]')
    elif game == "21365z.com":
        time.sleep(3)
        username_i = driver.find_element_by_xpath('//*[contains(@id,"_username")]')
        password_i = driver.find_element_by_xpath('//*[contains(@id,"_password")]')
        loginBtn_b = driver.find_element_by_xpath('//*[text()="登录"]')
    elif game == "36389.com":
        username_i = driver.find_element_by_xpath('//*[@id="username"]')
        password_i = driver.find_element_by_xpath('//*[@id="password"]')
        loginBtn_b = driver.find_element_by_xpath('//*[@id="sliderBlock_reg2"]')
    
    if username_i and password_i:
        print ("登录中...")
        username_i.click()        
        username_i.send_keys(read_settings()['id'])
        password_i.click()
        password_i.send_keys(read_settings()['pw'])
        loginBtn_b.click()
        
        time.sleep(5)
        cnt = 10
        goto_game = None

        if game == "365826.com":
            while cnt:
                cnt -= 1
                try:
                    goto_game = driver.find_element_by_xpath('//*[contains(@onclick, "GotoGame?GameType=AG&uid=")]')
                except:
                    goto_game = None
                    time.sleep(0.5)
                else:
                    print ("登录成功!")
                    break            
            
            if goto_game:
                print ("进入游戏中...")
                time.sleep(5)
                goto_game.click()
                time.sleep(5)
            else:
                print ("登录失败!")

        elif game == "21365z.com":
            # Close confirm message box 2 times
            while True:
                try:
                    confirm = driver.find_element_by_xpath('//*[text()="确定"]')
                except:
                    break
                else:
                    confirm.click()
                    time.sleep(2)

            time.sleep(2)
            try:
                close = driver.find_element_by_xpath('//*[@aria-label="Close"]')
            except:
                pass
            else:
                close.click()
                time.sleep(1)

            # select game icon
            while cnt:
                cnt -= 1
                try:
                    goto_game = driver.find_elements_by_xpath('//*[contains(@data-item, "AG国际馆")]/parent::div[1]')
                except:
                    goto_game = None
                    time.sleep(0.5)
                else:
                    print ("登录成功!")
                    break            
            
            if goto_game:
                print ("进入游戏中...")
                try:
                    goto_game[0].click()
                except:
                    try:
                        confirm = driver.find_element_by_xpath('//*[text()="确定"]')
                    except:
                        pass
                    else:
                        goto_game[0].click()
                #driver.get("https://gci.hongaming.com/magingame/NewPlaza31/?pid=D53&stamp=1567416366238")
                time.sleep(5)
            else:
                print ("登录失败!")

        elif game == "36389.com":
            print ("验证")
            while "36389.com/m/index" not in driver.current_url:
                time.sleep(3)
            
            time.sleep(5)
            # try:
            #     confirm = driver.find_element_by_class_name('//*[@class="box-btns"]')
            # except:
            #     pass
            # else:
            #     confirm.click()
            #     time.sleep(1)

             # select game icon
            while cnt:
                cnt -= 1
                try:
                    goto_game = driver.find_element_by_xpath('//*[@href="/m/voide/inFace?type=ag"]/parent::div[1]')
                except:
                    goto_game = None
                    time.sleep(0.5)
                else:
                    print ("登录成功!")
                    break            
            
            if goto_game:
                print ("进入游戏中...")
                time.sleep(1)
                #goto_game.click()
                #touchactions = TouchActions(driver)
                #touchactions.tap(goto_game)
                driver.get("http://36389.com/m/voide/inFace?type=ag")
                time.sleep(5)
            else:
                print ("登录失败!")


#######################################
###             Main                ###
#######################################
game = read_settings()["game"]
#["365826.com","21365z.com","36389.com"]
urls = {
    "365826.com" : "https://365826.com/Mobile/Login",
    "21365z.com" : "https://m.21365z.com/#module/member/action/login",
    "36389.com" : "http://36389.com/m/login/login"
}
# Initialize web driver
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C153 Safari/604.1")

driver = webdriver.Firefox(profile)
set_viewport_size(driver, 360, 640)

driver.get(urls[game])

login(driver, game)

if game == "365826.com":
    driver.switch_to.window(driver.window_handles[1])
elif game == "21365z.com":
    driver.switch_to.window(driver.window_handles[1])

#print (driver.current_url)
if wait_load_game(driver) == False:
    #driver.quit()
    sys.exit("Load Game Failed.")

# Game Loaded !!
time.sleep(15)
print ("mobile version...")
#
driver.execute_script('''
    document.addEventListener("mousedown", function(t){
        e = document.createEvent('UIEvent');
        e.initUIEvent("touchstart", true, true);
        console.log(t.clientX, ":",t.clientY);
        e.changedTouches = [{ pageX: t.clientX, pageY: t.clientY, clientX: t.clientX, clientY: t.clientY}];
        t.target.dispatchEvent(e);
    });

    document.addEventListener("mouseup", function(t){
        e = document.createEvent('UIEvent');
        e.initUIEvent("touchend", true, true);
        e.changedTouches = [{ pageX: t.clientX, pageY: t.clientY, clientX: t.clientX, clientY: t.clientY}];
        t.target.dispatchEvent(e);
    });
''')


# Entering Room
# entry_pos = driver.execute_script('var _entryIcon = egret.sys.$TempStage.$screen.stage.$children[0].$children[0].$children[0].$children[0].$children[0].$children[1].$children[1].$children[0].$children[26];\
#     return {x: _entryIcon.x, y: _entryIcon.y, w:_entryIcon.width, h:_entryIcon.height};')
# print (entry_pos)

region = "AGQ"
if read_settings()["region"] == "1":
    region = "DSP"
elif read_settings()["region"] == "3":
    region = "EMA"

driver.execute_script('var _entryIcons = egret.sys.$TempStage.$children[0].$children[0].$children[0].$children[0].$children[0].$children[1].$children[1].$children[0].$children;\
    console.log("===",_entryIcons.length);\
    for (var i=(_entryIcons.length-1);i>0;i--){ \
        if (_entryIcons[i]._data.platform == arguments[0]) {\
            egret.TouchEvent.dispatchTouchEvent(_entryIcons[i], egret.TouchEvent.TOUCH_BEGIN, !0, !0, 50, 50, !0);\
            egret.TouchEvent.dispatchTouchEvent(_entryIcons[i], egret.TouchEvent.TOUCH_END, !0, !0, 50, 50, !1);\
            break;\
        }\
    }\
    ', region)
time.sleep(5)
run(driver)
