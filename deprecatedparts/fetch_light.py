# # -*- coding: UTF-8 -*-
# # -----------------------
# # 请手动把温度看成光照值
# # -----------------------

# from connect_db import db  # model about connect db
# import MySQLdb
# import json
# import time
# from operator import itemgetter
# from datetime import datetime

# TABLE = 'luminous_intensity'  # 查询的表
# ITEM = 'value, time'  # 查询的值
# FILTER = ''            # 过滤器

# current_time = datetime.now()

# # 框架


# # 通过更改过滤条件选择查询时间范围

# def bolcktime(argItem, argTable, argFilter):
#     # *********************^_^|here****不要忘记语句连接之间的空格
#     sql = 'SELECT {0} FROM {1} '.format(argItem, argTable) + argFilter
#     # print sql  # 测试sql语句
#     try:
#         db.execute_db(sql)
#         # db.conn.commit() # 如果没有设置自动提交事务 autocommit(True)
#         # 手动提交事务
#     except MySQLdb.Error as e:
#         raise e
#     else:
#         data = db.cur.fetchall()
#         # js中时间戳为毫秒数，需* 1000
#         data = [[row[0], time.mktime(row[1].timetuple()) * 1000]
#                 for row in data]
#         for row in data:
#             row.reverse()  # 反转时间和温度值
#     return json.dumps(data)
#     # json只能存储数组和对象格式，即list和dict


# # 显示时间曲线表
# # 默认显示最新15条数据

# def view_light_data():

#     FILTER = 'ORDER BY time  DESC LIMIT 20'  # 选取最近时间20条数据
#     data = bolcktime(ITEM, TABLE, FILTER)
#     data = json.loads(data)
#     data = sorted(data, key=itemgetter(0))
#     return json.dumps(data)

# # 所有温度


# def get_alllight():
#     FILTER = 'ORDER BY TIME'
#     data = bolcktime(ITEM, TABLE, FILTER)
#     data = json.loads(data)
#     data = sorted(data, key=itemgetter(0))
#     return json.dumps(data)

# # 实时最新数据
# # 选取最新一条数据


# def get_latestlight():

#     FILTER = 'ORDER BY time DESC LIMIT 1'
#     sql = 'SELECT {0} FROM {1} '.format(ITEM, TABLE) + FILTER
#     try:
#         db.execute_db(sql)
#         # db.conn.commit() # 如果没有设置自动提交事务 autocommit(True)
#         # 手动提交事务
#     except MySQLdb.Error as e:
#         raise e
#     else:
#         row = db.cur.fetchone()  # fetchone()!!!才能把实时数据显示到前端图表
#         if row:
#             # js中时间戳为毫秒数，需* 1000
#             # 查询出的时间戳转换为json格式
#             # datetime.datime() -> 时间元组 -> float类型时间值
#             data = [row[0], time.mktime(row[1].timetuple()) * 1000]
#             data.reverse()  # 反转时间和温度值
#         else:
#             data = [0, time.mktime(current_time.timetuple()) * 1000]
#             data.reverse()  # 反转时间和温度值
#     return json.dumps(data)


# # 前一天的数据
# # 按平均选取24条数据，不足则选取全部
# def get_lastdaylight():

#     FILTER = 'WHERE DATE(time) = DATE_SUB(CURDATE(), INTERVAL 1 day)'
#     data = bolcktime(ITEM, TABLE, FILTER)
#     data = json.loads(data)
#     count = len(data)
#     if count > 24:
#         step = count / 24
#         data = data[0:count - count % 24:step]
#     data = json.dumps(data)

#     return data


# # 框架


# # 避免查询每天最高温最低温时代码重复写

# def dayOfWeek(week_min, week_max, day_of_week, filter_end):
#     # sql: 格式化时间戳返回星期几(0=sun, 1=mon, 6=sat)
#     # **不要忘记语句连接之间的空格**************^_^|here****
#     filter_start = "WHERE DATE_FORMAT(time, '%w') = "
#     # day_of_week = ''  # 查询星期几

#     FILTER = filter_start + day_of_week + filter_end

#     data_json = bolcktime(ITEM, TABLE, FILTER)
#     data_list = json.loads(data_json)  # json转列表
#     if data_list:
#         # 按温度排序
#         data_list = sorted(data_list, key=itemgetter(1))
#         week_min.append(data_list[0])  # 分别存放最高温最低温
#         week_max.append(data_list[-1])
#         # 重新按时间排序
#         week_min = sorted(week_min)
#         week_max = sorted(week_max)
#     else:
#         pass
#     return week_min, week_max


# # 上周的数据

# def get_lastweeklight():
#     week_min = []
#     week_max = []
#     # sql: 格式化时间戳返回一年中当前周数|当前周数- 1，即上周
#     # *********^_^|here****不要忘记语句连接之间的空格
#     filter_end = " and DATE_FORMAT(time, '%u') = (WEEKOFYEAR(CURDATE()) -1 )"
#     # 选取上一周内每天的最高温和最低温
#     day_of_week = '1'  # Monday
#     week_min, week_max = dayOfWeek(week_min, week_max,
#                                    day_of_week, filter_end)

#     day_of_week = '2'  # Tuesday
#     week_min, week_max = dayOfWeek(week_min, week_max,
#                                    day_of_week, filter_end)

#     day_of_week = '3'  # Wendesday
#     week_min, week_max = dayOfWeek(week_min, week_max,
#                                    day_of_week, filter_end)

#     day_of_week = '4'  # Thursday
#     week_min, week_max = dayOfWeek(week_min, week_max,
#                                    day_of_week, filter_end)

#     day_of_week = '5'  # Friday
#     week_min, week_max = dayOfWeek(week_min, week_max,
#                                    day_of_week, filter_end)

#     day_of_week = '6'  # Saturday
#     week_min, week_max = dayOfWeek(week_min, week_max,
#                                    day_of_week, filter_end)

#     day_of_week = '0'  # Sunday
#     week_min, week_max = dayOfWeek(week_min, week_max,
#                                    day_of_week, filter_end)
#     # 有一整周的数据则正常发送到前端
#     if len(week_min) == 7 and len(week_max) == 7:
#         # 列表转json
#         data = json.dumps([week_min, week_max])
#         return data
#     else:
#         return json.dumps(None)  # 数据不完整则直接返回空


# # 测试

# if __name__ == '__main__':
#     pass
