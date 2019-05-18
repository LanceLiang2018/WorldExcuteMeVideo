import time
import math


class Lrc:
    class Line:
        def __init__(self, label: str=None, ctime: float=0.0, string: str=''):
            self.time = ctime
            self.string = string
            self.label = label

        def __str__(self):
            if self.label is not None:
                return '[%s]%s' % (self.label, self.string)
            return '[%s]%s' % (Lrc.int2str(self.time), self.string)

    class Data:
        def __init__(self):
            self.lines = []

        def sort(self):
            self.lines.sort(key=lambda x: x.time)

        def __str__(self):
            result = ''
            for line in self.lines:
                result = result + str(line) + '\n'
            return result

    def __init__(self, split_char: str=' - '):
        self.split_char = split_char

    # 解析字符串时间 -> 秒数
    # 遇到异常抛出
    @staticmethod
    def str2int(s: str):
        if len(s.split(':')) < 2:
            raise ValueError
        minn = s.split(':')[0]
        sec = s.split(':')[1]
        try:
            res = 60 * int(minn) + float(sec)
        except:
            raise ValueError
        return res

    # 秒数 -> 字符串时间
    @staticmethod
    def int2str(n: float):
        n = float(n)
        minn = int(n // 60)
        sec = math.floor(n - minn * 60)
        other = n - minn * 60 - sec
        res = "%02d:%02d.%s" % (minn, sec, str("%02d0" % int(other * 100)))
        return res

    @staticmethod
    def parse_line(line: str):
        if not line.startswith('['):
            raise ValueError
        if ']' not in line:
            raise ValueError
        # 我猜应该不会出现[xxx][yyyy]这样的歌词了...
        second = line.split('[')[-1].split(']')[0]
        string = line.split('[')[-1].split(']')[-1]
        # 尝试转换，转换失败就留着原来的格式。
        try:
            second = Lrc.str2int(second)
        except ValueError:
            return Lrc.Line(label=second, string=string)
        return Lrc.Line(ctime=second, string=string)

    @staticmethod
    def parse_lrc(lrc: str):
        # 看来还是会有错误的写法...
        lines = lrc.split('\n')
        # 删去空行。
        for i in lines:
            if len(i) == 0:
                lines.remove(i)

        data = Lrc.Data()
        for line in lines:
            try:
                data.lines.append(Lrc.parse_line(line))
            except ValueError:
                data.lines.append(Lrc.Line(ctime=0.0, string=line))

        # 排序
        data.sort()

        return data

    # 合并多个lrc。主要是翻译。
    # 在排列前面的会显示在前面。
    @staticmethod
    def blend(lrcs_str: list, reverse=False):
        if reverse:
            lrcs_str.reverse()
        lrcs = []
        for lrc_str in lrcs_str:
            lrcs.append(Lrc.parse_lrc(lrc_str))
        data = Lrc.Data()
        for lrc in lrcs:
            data.lines.extend(lrc.lines)
        data.sort()
        return data

    # 按行合并。
    # 用于mp3显示不了同一时间的歌词和翻译时的处理。
    def blend_lines(self, lrc_str: str):
        lrc = Lrc.parse_lrc(lrc_str)
        data = Lrc.Data()
        index = 0
        while index < len(lrc.lines):
            i = 1
            while i + index < len(lrc.lines) and lrc.lines[index].time == lrc.lines[index + i].time and lrc.lines[index].label is None:
                i += 1
            # print(list(map(lambda x: str(x), lrc.lines[index:index+i])))
            got_lines = lrc.lines[index:index+i]
            if len(got_lines) > 1 or (len(got_lines) == 1 and got_lines[0].label is None):
                form_line = ''
                for got in got_lines:
                    form_line = form_line + got.string + self.split_char
                form_line = form_line[:-len(self.split_char)]
                data.lines.append(Lrc.Line(ctime=got_lines[0].time, string=form_line))
            if len(got_lines) == 1 and got_lines[0].label is not None:
                data.lines.append(got_lines[0])
            index += i
        data.sort()
        return data


class Lyric:
    def __init__(self):
        self.file_en = 'Lyric/world.execute(me);_en.lrc'
        self.file_cn = 'Lyric/world.execute(me);_translated.lrc'
        with open(self.file_en) as f:
            self.data = Lrc.parse_lrc(f.read())
        with open(self.file_cn) as f:
            self.data_cn = Lrc.parse_lrc(f.read())
        # print(self.data)
        self.time_start = 0
        self.pointer = 0

    def start(self):
        self.time_start = time.time()

    def has_new(self):
        if self.time_start == 0:
            return False
        if self.pointer >= len(self.data.lines):
            return False
        now = time.time() - self.time_start
        if now >= self.data.lines[self.pointer].time:
            return True
        return False

    def top(self):
        return self.data.lines[self.pointer].string

    def next(self):
        top = self.top()
        self.pointer += 1
        return top
