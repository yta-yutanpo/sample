import random
import tkinter as tk
from collections import Counter
from PIL import Image, ImageDraw, ImageFont, ImageTk

# 画面の作成
root = tk.Tk()
root.title('ポーカーゲーム')
root.geometry('1500x1000')
root.configure(bg='white')

# フレームの用意
title_frame = tk.Frame(root, bg='white')
game_frame = tk.Frame(root, bg='white')

# タイトル画面を作成
title_frame.pack()
title_label = tk.Label(title_frame, text='ポーカーゲームへようこそ', bg='white')
title_label.pack()
button_start = tk.Button(title_frame, text='スタート', bg='lightblue', fg='black',
                         font=('Helvetica', 10, 'bold'), relief='raised', bd=10, command=lambda: switch_frame(game_frame))
button_start.pack()

def switch_frame(frame):
    title_frame.pack_forget()
    game_frame.pack()

# トランプの作成
card_number_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
spade = "\u2660"
heart = "\u2665"
diamond = "\u2666"
club = "\u2663"
card_suits = [spade, heart, diamond, club]
card_list = [(s, n) for s in card_suits for n in card_number_list]

# GUI用ラベル
label_cards = tk.Label(game_frame, text="", font=('Helvetica', 14), bg='white')
label_cards.pack()
# カード画像用フレームを追加
card_image_frame = tk.Frame(game_frame, bg='white', width=500, height=180)
card_image_frame.pack()
label_hand = tk.Label(game_frame, text="", font=('Helvetica', 10), bg='white')
label_hand.pack()
label_result = tk.Label(game_frame, text="", font=('Helvetica', 10), bg='white')
label_result.pack()




# スコアランク定義
score_rank = {
    'ロイヤルフラッシュ': 9,
    'ストレートフラッシュ': 8,
    'フォーカード': 7,
    'フルハウス': 6,
    'フラッシュ': 5,
    'ストレート': 4,
    'スリーカード': 3,
    'ツーペア': 2,
    'ワンペア': 1,
    '役なし': 0
}

card_order = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
              '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
card_order_alt = {'A': 14, **{k: v for k, v in card_order.items() if k != 'A'}}

def is_straight(numbers):
    return max(numbers) - min(numbers) == 4 and len(set(numbers)) == 5

def judge_hand(cards):
    nums = [card[1] for card in cards]
    suits = [card[0] for card in cards]
    counts = Counter(nums)
    counts_list = sorted(counts.values(), reverse=True)
    suits_counts = Counter(suits)

    num_vals = [card_order[n] for n in nums]
    num_vals_alt = [card_order_alt[n] for n in nums]

    royal = ['10', 'J', 'Q', 'K', 'A']
    is_flush = 5 in suits_counts.values()
    is_royal = all(card in nums for card in royal)
    is_straight_low = is_straight(sorted(num_vals))
    is_straight_high = is_straight(sorted(num_vals_alt))

    if is_flush and is_royal:
        return 'ロイヤルフラッシュ'
    elif is_flush and (is_straight_low or is_straight_high):
        return 'ストレートフラッシュ'
    elif counts_list == [4, 1]:
        return 'フォーカード'
    elif counts_list == [3, 2]:
        return 'フルハウス'
    elif is_flush:
        return 'フラッシュ'
    elif is_straight_low or is_straight_high:
        return 'ストレート'
    elif counts_list == [3, 1, 1]:
        return 'スリーカード'
    elif counts_list == [2, 2, 1]:
        return 'ツーペア'
    elif counts_list == [2, 1, 1, 1]:
        return 'ワンペア'
    else:
        return '役なし'


#カードの画像を作る関数
def create_card_image(cards):
    # 既存のカードラベルを削除
    #game_frame内のすべての部品を取得する
    for widget in card_image_frame.winfo_children():
        #is_card属性(True)を持つ部品を削除
        if hasattr(widget, "is_card"):
            widget.destroy()
    card_images = []
    # カードの画像を生成
    for idx, (suit, num) in enumerate(cards):
        # 白背景の画像を生成(80x120ピクセル)
        img = Image.new("RGB", (80, 120), (255, 255, 255))
        # 画像に描けるようにする
        draw = ImageDraw.Draw(img)
        #カードの枠線を描く
        draw.rectangle([(0, 0), (79, 119)], outline="black", width=2)
        #フォントの指定(記号や絵文字も表示できるように)(なければデフォルト)
        try:
            font = ImageFont.truetype("seguisym.ttf", 32)
        except:
            font = ImageFont.load_default()
        #カードのスートと数字を描く
        #ハート・ダイヤならば赤、クローバー・スペードならば黒
        if suit in [heart, diamond]:
            suit_color = (255, 0, 0)
        else:
            suit_color = (0, 0, 0)
        draw.text((10, 10), suit, fill=suit_color, font=font)
        draw.text((30, 60), str(num), fill=(0, 0, 0), font=font)
        #pillow画像をTkinter用に変換
        tk_img = ImageTk.PhotoImage(img)
        # 画像をカード画像フレームに追加
        card_images.append(tk_img)
        #カード画像にボタン機能をつける
        card_button = tk.Button(card_image_frame, image=tk_img, bg='white', fg='black',
                            font=('Helvetica', 10, 'bold'), bd=5)
        card_button.is_card = True  # カードラベルの目印(カードラベルならばTrue)
        #ラベル自身に画像を持たせて消えないようにする
        card_button.image = tk_img  # 参照保持
        #画像を横並びに配置
        card_button.place(x=10 + idx * 90, y=50)
        # 画像をクリックしたときの処理を設定(押したボタンが機能するようにLambdaを使うらしい)
        card_button.config(command=lambda btn=card_button: card_select(btn))
        card_button.card_index = idx  # ボタンにカードのインデックスを保存
    # 参照保持のためgame_frameに属性として保存(card_imagesが消えないようにするため)
    game_frame.card_images = card_images
        
seleceted_indices = set() # 選択されたカードのインデックスを保持するセット

#カードを選択したときに上に上がる処理
def card_select(card_button):
    # 現在の位置を取得
    x = card_button.winfo_x()
    y = card_button.winfo_y()
    #ボタンにcard_index属性がなければ何もしない(Noneを返す)
    #安全装置としての認識らしい(事故防止)
    idx = getattr(card_button, "card_index", None)
    if idx is None:
        return
    # すでに上がっていれば下げる、そうでなければ上げる(ボタンにis_selected属性を追加している)
    # getattr(オブジェクト, "属性名", デフォルト値)で属性が存在しない場合にデフォルト値を返す
    # ここでは"is_selected"属性がFalseならばデフォルトのFalseを返す
    if getattr(card_button, "is_selected", False):
        card_button.place(x=x, y=y+20)
        card_button.is_selected = False
        selected_indices.discard(idx) 
    else:
        card_button.place(x=x, y=y-20)
        card_button.is_selected = True
        selected_indices.add(idx) 
    if selected_indices:
        #選択したカードの引き直しボタン
        button_redraw = tk.Button(game_frame, text='選択したカードを引き直す', bg='lightblue', fg='black',
                          font=('Helvetica', 10, 'bold'), relief='raised', bd=10, command=redraw_selected_cards)

    
#カードを引いた時の処理
def card_hand_out():
    global player_card, cpu_card, selected_indices, cpu_hand, player_hand, cpu_hand
    deck = card_list[:]
    random.shuffle(deck)
    player_card = deck[:5]
    cpu_card = deck[5:10]
    selected_indices = set()

    player_hand = judge_hand(player_card)
    cpu_hand = judge_hand(cpu_card)

    card_text = '  '.join([f'{suit}{num}' for suit, num in player_card])
    label_cards.config(text=f'あなたの手札：')
    create_card_image(player_card)
    label_hand.config(text=f'あなたの役 : {player_hand}')
    judge_winner(player_hand, cpu_hand)

    button_redraw.pack() #引き直しボタンを設置
    button_hand_out.pack_forget() #5枚引くボタンを消す

result = ""  # 勝敗結果を保持する変数

#勝敗を判定する関数
def judge_winner(player_hand, cpu_hand):
    global result
    player_score = score_rank[player_hand]
    cpu_score = score_rank[cpu_hand]

    if player_score > cpu_score:
        result = "あなたの勝ち！"
    elif player_score < cpu_score:
        result = "CPUの勝ち！"
    else:
        result = "引き分け！"

#選択したカードを引き直すための関数
def redraw_selected_cards():
    global player_card, selected_indices
    if not selected_indices:
        return  # 選択されたカードがない場合は何もしない
    #山札から、すでに配られたカードを除外する(残りの山札がdeck)
    used_cards = set(player_card + cpu_card)
    deck = [card for card in card_list if card not in used_cards]
    random.shuffle(deck)
    new_cards = []
    for idx in selected_indices:
        new_card = deck.pop()
        player_card[idx] = new_card
    #選択状態をリセット
    selected_indices.clear()
    create_card_image(player_card)
    player_hand = judge_hand(player_card)
    label_hand.config(text=f'あなたの役 : {player_hand}')
    judge_winner(player_hand, cpu_hand)

#結果を表示する関数
def show_result():
    label_result.config(text=f'CPUの役 : {cpu_hand}\n結果 : {result}')

# ボタンなどのUI
#カードを5枚配るボタン
button_hand_out = tk.Button(game_frame, text='5枚引く', bg='lightblue', fg='black',
                            font=('Helvetica', 10, 'bold'), relief='raised', bd=10, command=card_hand_out)
button_hand_out.pack()


#勝負するボタン
button_battle = tk.Button(game_frame, text='勝負する', bg='lightblue', fg='black',
                          font=('Helvetica', 10, 'bold'), relief='raised', bd=10, command=show_result)
button_battle.pack()

# タイトルに戻るボタン
def back_to_title():
    game_frame.pack_forget()
    title_frame.pack()

button_back = tk.Button(game_frame, text='タイトルに戻る', bg='lightblue', fg='black',
                        font=('Helvetica', 10, 'bold'), relief='raised', bd=10, command=back_to_title)
button_back.pack(side='bottom')

root.mainloop()


#今後の改善の流れ　
# １．結果は引き直しをした後に表示するようにする(専用のボタンを用意する)←完了
# ２．引き直しの回数制限を設ける(３回)
# ３．CPUの思考ルーチンを作成する(引き直しの判断)
# ４．賭けの概念を導入する(所持金、ベット、勝敗による増減)