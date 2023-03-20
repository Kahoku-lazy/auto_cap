""" 计算查准率、 查全率 """
import os
import re

overwatch = [
    "Eliminated",
    "Revenge",
    "X_Player_Killed_Streak",
    "Team_Killed",
    "Ultimate_Skill_Ready",
    "Overtime",
    "Matching",
    "Matched",
    "Victory",
    "Defeat",
    "Reviving",
    "Discord",
    "Hacked",
    "Sleep",
    "Detected",
    "Pinned",
    "Stunned",
    "Change_Hero",
    "Prompts",
    "Trapped",
    "Stuck"
]

overwatch_count = [
    1149,
    61,
    342,
    281,
    531,
    490,
    903,
    786,
    302,
    282,
    101,
    117,
    103,
    100,
    86,
    100,
    100,
    120,
    100,
    102,
    100]

valorant = [
    "Eliminated",
    "ACE",
    "Spike_Carrier_Killed",
    "Presence_Detected",
    "Location_Revealed",
   "Spike_Initiating",
    "Spike_Planted",
    "Defusing",
    "In_Queue",
    "Match_Found",
    "Won",
    "Lost",
    "Victory",
    "Defeat",
    "CLUTCH",
    "Flawless",
    "BUY_PHASE",
    "MATCH_POINT",
    "RESPAWNIG_IN",
    "THRIFTY",
    "YOU_HAVE_THE_SPIKE",
    "CYPHER_UPLOADING",
    "Hold_4_To_Plant_Spike",
    "LAST_ROUND_BEFORE_SWAP",
    "TOXIN_LOW",
    "Play"
]

valorant_count =[
    2335,
    332,
    634,
    663,
    820,
    547,
    537,
    797,
    565,
    518,
    636,
    581,
    438,
    513,
    530,
    634,
    404,
    367,
    112,
    53,
    352,
    47,
    79,
    145,
    70,
    242
]


def input_data(file_path):
    
    amount = [0 for x in range(60)]
    for img in os.listdir(file_path):
        serial_number = img.split("-")[0].strip()
        amount[int(serial_number)] += 1

    return amount

def output_result(file_path):
    
    amount_tp = [0 for x in range(60)]
    amount_sum = [0 for x in range(60)]
    # result = []
    for dir in os.listdir(file_path):
        dir_path = os.path.join(file_path, dir)

        amount_sum[valorant.index(dir)] = len(os.listdir(dir_path))   # debug

        for img in os.listdir(dir_path):
            # img_path = os.path.join(dir_path, img)
             serial_number = img.split("-")[0].strip()

             if int(serial_number) == valorant.index(dir):
                 
                 amount_tp[int(serial_number)] += 1

    return amount_sum, amount_tp


def model_result(input_data, output_result):

    result_sum, reslut_tp = output_result 

    if len(input_data) == len(reslut_tp):
        for i in range(len(input_data)):
            if result_sum[i] > 0 and reslut_tp[i] > 0 and input_data[i] > 0:
                P = reslut_tp[i] / result_sum[i] 

                R2 = reslut_tp[i] / valorant_count[i]      # debug

                R = reslut_tp[i] / input_data[i]
                print(f"{i}: P:{P}\nR2:{R2}\nR:{R}\n")
            if R < 0.95:
                print(f"FAIL - {i}: P:{P}, R2:{R2}, R:{R}\n")
    else:
        print(f">>> ERROR\ninput_data:{len(input_data)}, result:{len(reslut_tp)}")

if __name__ == '__main__':

    # file_path = r"D:\Kahoku\HDMI_Project\Test_Data\test_pictures\Overwatch_pictures"
    file_path  = r"D:\Kahoku\HDMI_Project\Test_Data\test_pictures\Valorant_pictures"
    input_data = input_data(file_path)
    print(f"特征数量:{len(input_data)}, 输入数据: {input_data}\n")

    # result_path = r"D:\Kahoku\HDMI_Project\Overwatch_classes"
    result_path = r"D:\Kahoku\HDMI_Project\Valorant_classes"
    output_result = output_result(result_path)
    print(f"特征数量:{len(output_result)}, 输入数据: {output_result}\n")

    model_result(input_data, output_result)