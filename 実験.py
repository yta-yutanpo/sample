import random
import tkinter as tk
from collections import Counter

# 画面の作成
root = tk.Tk()
root.title('ポーカーゲーム')
root.geometry('300x250')
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
card_suits = ['S', 'D', 'H', 'C']
card_list = [(s, n) for s in card_suits for n in card_number_list]

# GUI用ラベル
label_cards = tk.Label(game_frame, text="", font=('Helvetica', 14), bg='white')
label_cards.pack()
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

def card_hand_out():
    deck = card_list[:]
    random.shuffle(deck)
    player_card = deck[:5]
    cpu_card = deck[5:10]

    player_hand = judge_hand(player_card)
    cpu_hand = judge_hand(cpu_card)

    card_text = '  '.join([f'{suit}{num}' for suit, num in player_card])
    label_cards.config(text=f'あなたの手札：\n{card_text}')
    label_hand.config(text=f'あなたの役 : {player_hand}')

    # 勝敗表示
    player_score = score_rank[player_hand]
    cpu_score = score_rank[cpu_hand]

    if player_score > cpu_score:
        result = "あなたの勝ち！"
    elif player_score < cpu_score:
        result = "CPUの勝ち！"
    else:
        result = "引き分け！"

    label_result.config(text=f'CPUの役 : {cpu_hand}\n結果 : {result}')

# ボタンなどのUI
button_hand_out = tk.Button(game_frame, text='5枚引く', bg='lightblue', fg='black',
                            font=('Helvetica', 10, 'bold'), relief='raised', bd=10, command=card_hand_out)
button_hand_out.pack()

button_back = tk.Button(game_frame, text='タイトルに戻る', bg='lightblue', fg='black',
                        font=('Helvetica', 10, 'bold'), relief='raised', bd=10, command=lambda: switch_frame(title_frame))
button_back.pack()

root.mainloop()
