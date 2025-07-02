import pandas as p

data_frame0 = p.read_csv("C:\\Users\\jackh\\Downloads\\xavier_hd2023.csv", encoding="latin1")
data_frame1 = p.read_csv("C:\\Users\\jackh\\Downloads\\xavier_flags2023.csv", encoding="latin1")
data_frame2 = p.read_csv("C:\\Users\\jackh\\Downloads\\xavier_ic2023.csv", encoding="latin1")
data_frame3 = p.read_csv("C:\\Users\\jackh\\Downloads\\xavier_ic_ay2023.csv", encoding="latin1")

merged_data_frame = p.concat([data_frame0, data_frame1, data_frame2, data_frame3], axis=1)

print(merged_data_frame)

# Save it to a new CSV 
merged_data_frame.to_csv("xu_institutional_characteristics2023.csv", index=False)