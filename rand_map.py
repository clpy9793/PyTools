#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-22 11:03:42
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
import json
import random
import hashlib
from collections import namedtuple

GridType = namedtuple('GridType', ['empty', 'master', 'sub_city', 'barrier'])
grid_type = GridType(0, 1, 2, 3)


def get_input():
    if sys.version.startswith('3'):
        return input()
    else:
        return raw_input()


class Map(object):
    def __init__(self, grids=24, teams=None, barrier_rate=None, sub_city_rate=None):
        if  grids % 3 != 0:
            pass

        if teams is None:
            teams = [3, 3]
        if barrier_rate is None:
            barrier_rate = random.choice([i * 0.01 for i in range(10, 23)])
        if sub_city_rate is None:
            sub_city_rate = random.choice([i * 0.01 for i in range(2, 6)])

        self.grids = grids
        self.teams = sorted(teams, reverse=True)  # 团队数与队员数
        n = len(self.teams)
        self.master = [set([]) for _ in range(n)]  # 团队主城所在坐标点
        self.barrier_rate = barrier_rate
        self.sub_city_rate = sub_city_rate

        self.empty_roads = set([])
        self.barriers = set([])
        self.sub_cities = set([])
        self.all = set([])
        self.generate()


    def generate(self):
        # 生成空地图
        self.make_empty_map()
        # 生成主城
        if len(self.teams) == 2:
            self.make_master_city()
        elif len(self.teams) == 3:
            self.make_master_city_v2()
        elif len(self.teams) == 4:
            self.make_master_city_v3()
        elif len(self.teams) == 5:
            self.make_master_city_v4()
        elif len(self.teams) >= 6:
            self.make_master_city_v5()
        # 生成通路
        self.make_chain()
        # 生成障碍
        self.make_barrier()
        # 生成副城池
        self.make_sub_city()
        # 拼接地图
        self.make_map()

        # self.toFile()

    def newToFile(self, path=None):
        list_ = []
        md = hashlib.md5()
        res = json.dumps(self.map)
        md.update(res)
        file_name = md.hexdigest() + '.json'
        if path is not None:
            file_name = os.path.join(path, file_name)
        for i in self.map:
            list_.extend(i)
        with open(file_name, 'w') as f:
            json.dump(list_, f)

    def toFile(self, path=None):
        md = hashlib.md5()
        res = json.dumps(self.map)
        md.update(res)
        file_name = md.hexdigest() + '.json'
        with open(file_name, 'w') as f:
            json.dump(self.map, f)

    def make_map(self):
        set_ = set([])
        for i in self.master:
            set_ = set_.union(i)
        print set_

        for team in self.master:
            for x, y in team:
                self.map[x][y] = grid_type.master

        # road
        for x, y in self.empty_roads:
            if (x, y) in set_:
                continue
            self.map[x][y] = grid_type.empty

        # barrier
        for x, y in self.barriers:
            if (x, y) in set_:
                continue
            self.map[x][y] = grid_type.barrier

        # sub_city
        for x, y in self.sub_cities:
            if (x, y) in set_:
                continue
            self.map[x][y] = grid_type.sub_city
            # for i in self.map:
            # print i


    def make_barrier(self):
        paths = [(x, y) for x in xrange(self.grids) for y in xrange(self.grids) if (x, y) not in self.all]
        random.shuffle(paths)
        nums = int(self.barrier_rate * (self.grids ** 2))
        assert nums <= len(paths)
        barriers = random.sample(paths, nums)
        for x, y in barriers:
            self.barriers.add((x, y))
            self.all.add((x, y))


    def make_sub_city(self):
        paths = [(x, y) for x in xrange(self.grids) for y in xrange(self.grids) if (x, y) not in self.all]
        paths.extend(list(self.empty_roads))
        paths = list(set(paths))
        random.shuffle(paths)
        nums = int(self.sub_city_rate * (self.grids ** 2))
        # ToDo
        assert nums <= len(paths)
        sub_cities = random.sample(paths, nums)
        for x, y in sub_cities:
            self.sub_cities.add((x, y))
            self.all.add((x, y))


    def make_chain(self):
        team_path = []
        for team in self.master:
            master_list = list(team)
            start = master_list[0]
            team_path.append(start)
            for end in master_list[1:]:
                self.make_empty_road(start, end)
        for i in range(len(team_path) - 1):
            self.make_empty_road(team_path[i], team_path[i + 1])

    def make_empty_road(self, start, end):
        # ToDo
        min_ = 0
        max_ = self.grids - 1
        x, y = start
        end_x, end_y = end
        move_x = -1 if x > end_x else 1
        while x != end_x:
            x += move_x
            self.empty_roads.add((x, y))
            self.all.add((x, y))
            # Todo
            move_y = random.choice([1, -1])
            if (move_y == -1 and y > min_) or (move_y == 1 and y < max_):
                y += move_y
                self.empty_roads.add((x, y))
                self.all.add((x, y))

        move_y = -1 if y > end_y else 1
        while y != end_y:
            y += move_y
            self.empty_roads.add((x, y))
            self.all.add((x, y))


    def make_empty_map(self):
        self.map = [[0 for j in xrange(self.grids)] for i in xrange(self.grids)]
        # return [[0 for j in xrange(self.grids)] for i in xrange(self.grids)]

    def make_master_city(self):
        '''2v2'''
        # ToDo
        self.func([(0, 0), (0, 1), (1, 0)], 1)
        self.func([(2, 1), (2, 2), (1, 2)], 2)



    def make_master_city_v2(self):
        '''2v2v2'''
        # ToDo
        self.func([(0, 0)], 1)
        self.func([(0, 2)], 2)
        self.func([(2, 2)], 3)


    def make_master_city_v3(self):
        '''1v1v1v1'''
        # ToDo
        self.func([(0, 0)], 1)
        self.func([(2, 0)], 2)
        self.func([(0, 2)], 3)
        self.func([(2, 2)], 4)


    def make_master_city_v4(self):
        '''1v1v1v1v1'''
        # ToDo
        self.func([(0, 0)], 1)
        self.func([(2, 0)], 2)
        self.func([(0, 2)], 3)
        self.func([(2, 2)], 4)
        self.func([(1, 1)], 5)

    def make_master_city_v5(self):
        '''1v1v1v1v1'''
        # ToDo
        size = len(self.teams)
        for i in range(size):
            self.func([(x, y) for x in range(3) for y in range(3)], i + 1)


    def func(self, choice_list, n):
        grid_size = self.grids / 3
        sum_ = 0
        while 1:
            place = random.choice(choice_list)
            x = place[0]
            y = place[1]
            start_x = grid_size * x
            end_x = grid_size * (1 + x)
            start_y = grid_size * y
            end_y = grid_size * (1 + y)
            x, y = random.choice([(x, y) for x in range(start_x, end_x) for y in range(start_y, end_y)])
            if (x, y) in self.master[n - 1] or (x, y) in self.all:
                continue
            else:
                print '------------------'
                print place
                print (x,y)
                print '------------------'
                self.master[n - 1].add((x, y))
                self.all.add((x, y))
                sum_ += 1
                if sum_ >= self.teams[n - 1]:
                    break



def main():
    from itertools import combinations_with_replacement

    # grids = [18, 21, 24]
    # for grid in grids:
    #     for n in range(2, 6):
    #         teams = [i for i in list(combinations_with_replacement([1, 2, 3, 4, 5], n)) if sum(i) <= 6]
    #         for team in teams:
    #             Map(grids=grid, teams=team)
    grids = 24
    teams = [[3,3],[2,2,2]]
    TWO_TEAM_PATH = 'two'
    THREE_TEAM_PATH = 'three'
    if not os.path.isdir(TWO_TEAM_PATH):
        os.mkdir(TWO_TEAM_PATH)
    if not os.path.isdir(THREE_TEAM_PATH):
        os.mkdir(THREE_TEAM_PATH)
    for team in teams:
        for i in xrange(1000):
            m = Map(grids=grids, teams=team)
            length = len(team)
            prefix = None
            if length == 2:
                prefix = TWO_TEAM_PATH
            elif length == 3:
                prefix = THREE_TEAM_PATH
            m.newToFile(prefix)


if __name__ == '__main__':
    main()