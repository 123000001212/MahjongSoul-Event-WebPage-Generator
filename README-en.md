# Generate Mahjong Soul Event‘s Statistics Page by Mahjong Soul Review Supporter

## 1. Setups

Recommended environment：

- Python 3.8.8
- pandas==1.2.4

## 2. How to use

### 2.1 Fetch the match data by Mahjong Soul Review Supporter

First [install the Mahjong Soul Review Supporter plug-in](https://www.bilibili.com/read/cv17873540) in Chrome or Edge browser. (It is recommended to use the Edge browser because Chrome needs to install the tamper monkey plug-in first).

Start Mahjong Soul in your browser. Enter game review interface and run the plug-in, copy all contents in the Result Output block to ./data-example.xlsx (select A2 cell and press Ctrl+V to paste).

Save the table to ./data, name the file as "Year.Month.Day-Number.xlsx" (i.e. 2023.02.07-1.xlsx).

Each game corresponds to a xlsx file.

- TODO：try [mahjong_soul_api](https://github.com/MahjongRepository/mahjong_soul_api) to fetch match data automatically.

### 2.2 Set game configures

#### 2.2.1 Team member information

Open ./player.xlsx, fill in “id、name、team_id、team_name” four columns information from 0 according to the id (Note that 'AI' must be added in the last line in order to process the match data of the AI player).

#### 2.2.2 Game rules information

Open ./config.py by Notepad, modify rules here (The modification here must be consistent with the information in player.xlsx.

Open ./game_rule.txt by Notepad, Enter the text version of the competition rules (Note that the file must be saved as utf-8 format).

### 2.3 Run python script

Open the command line window under this folder and run the command:

```
python ./cal.py
```

### 2.4 Outputs

- Table output：./output.xlsx
- Web page output：./index.html

