import pandas as p

def read_and_label(path, label):
    df = p.read_csv(path, encoding="latin1")

    #Convert label row (label in first column, rest blank)
    label_row = p.DataFrame([[label] + [None]*(len(df.columns)-1)], columns=df.columns)

    #Combine: label --> data
    df = p.concat([label_row, df], axis=0)

    return df.reset_index(drop=True)

data_frame0 = read_and_label("C:\\Users\\jackh\\Downloads\\c2016_a.csv", "c2016_a")
data_frame2 = read_and_label("C:\\Users\\jackh\\Downloads\\c2016_b.csv", "c2016_b")
data_frame3 = read_and_label("C:\\Users\\jackh\\Downloads\\c2016_c.csv", "c2016_c")
data_frame4 = read_and_label("C:\\Users\\jackh\\Downloads\\c2016dep.csv", "c2016dep")
data_frame5 = read_and_label("C:\\Users\\jackh\\Downloads\\flags2016.csv", "flags2016")



merged_data_frame = p.concat([data_frame0, data_frame2, data_frame3, data_frame4, data_frame5], axis=1)

print(merged_data_frame)

# Save it to a new CSV 
merged_data_frame.to_csv("Completions2016.csv", index=False)