# -*- coding: UTF-8 -*-
# ©Fei, DO NOT USE WITHOUT LICENSED
# Exploratory Data Analysis (EDC)

# require
import numpy
import pandas as pd
from pathlib import Path
from os import listdir
import codecs
import unicodedata
import re
from torch.utils.data import random_split

# main class


class Eda:
    def __init__(self, raw_path="Raw_data") -> None:
        self._dirs = listdir(raw_path)
        self._raw_path = raw_path
        self.df = self.fixdata()

    def fixdata(self):
        df_list = []
        for f in self._dirs:
            if "pairs" in f:
                try:
                    lines = open('%s\%s' % (self._raw_path, f),
                                 encoding='utf-8').read().strip().split('\n')
                except:
                    lines = open('%s\%s' % (self._raw_path, f),
                                 encoding='ISO-8859-1').read().strip().split('\n')
                col_names = self.__normalizeString(lines[0]).split("\t")
                col_len = len(col_names)
                df = pd.DataFrame()
                lines = lines[1:]
                for line in lines:
                    new_line = self.__normalizeString(line)
                    line_split = new_line.split("\t")
                    if len(line_split) != col_len:
                        continue
                    new_line_df = pd.DataFrame([line_split], columns=col_names)
                    df = pd.concat([df, new_line_df])
                df_list.append(df)
        combined_df = pd.concat(df_list)
        return combined_df

    def split(self):
        d2 = self.df
        train_set_size = int(len(d2) * 0.7)
        split_set_size = len(d2) - train_set_size

        train_set, split_set = random_split(
            d2, [train_set_size, split_set_size])

        test_set_size = int(len(split_set) * 0.5)
        val_set_size = len(split_set) - test_set_size

        val_set, test_set = random_split(
            split_set, [val_set_size, test_set_size])

        print("data set has been splited into: %s rows train_set, %s rows val_set, %s rows test_set" % (
            train_set_size, val_set_size, test_set_size))

        # save dataset
        datasets = {'train':train_set, 'val':val_set, "test":test_set}
        for set in datasets:
            file_name = "%s_cleaned.cbcsv" % (set)
            file_path = Path("Dataset\%s" % (file_name))
            d3 = d2.iloc[datasets[set].indices]
            try:
                d3.to_csv(file_path, index=False)
            except Exception as e:
                print("data save failed duo to: ", e)
            else:
                print("%s save succeed" % (file_name))

        

    def info(self):
        # dataset info
        self.df.info()

    def dataclean(self):
        # local var
        d1 = self.df

        # dataset info
        ori_rows = len(d1)

        # clean null
        d1 = d1.dropna()
        n_droped = ori_rows - len(d1)
        print("%d rows has been droped" % (n_droped))

        # save dataset
        file_name = "cleaned.cbcsv"
        file_path = Path("Dataset\%s" % (file_name))
        try:
            d1.to_csv(file_path, index=False)
        except Exception as e:
            print("data save failed duo to: ", e)
        else:
            print("data save succeed")

        # save to class
        self.df = d1

    def __unicodeToAscii(self, s):
        return ''.join(
            c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'
        )

    def __normalizeString(self, s):
        s = self.__unicodeToAscii(s.lower().strip())

        # Split .!? with words
        s = re.sub(r"([.!?])", r" \1", s)

        # Remove useless characters
        s = re.sub(r"[^a-zA-Z.!?\t]+", r" ", s)
        if s[0] == " ":
            s = s[1:]
        return s

# main function entry


def run():
    task = Eda()
    task.info()
    task.dataclean()
    task.split()


# OOP
if __name__ == '__main__':
    run()

pass