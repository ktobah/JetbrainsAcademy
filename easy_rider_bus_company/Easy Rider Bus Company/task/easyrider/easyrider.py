# Write your awesome code here
import json
import re
import itertools
from datetime import datetime


def check_errors(ride_info: dict, errors_dic:dict):
    for key, val in ride_info.items():
        if key == "bus_id":
            if not isinstance(val, int):
                errors_dic[key] += 1
        elif key == "stop_id":
            if not isinstance(val, int):
                errors_dic[key] += 1
        elif key == "stop_name":
            if not re.match(r'^[A-Z].*(Road|Avenue|Boulevard|Street)$', val):
                errors_dic[key] += 1
        elif key == "next_stop":
            if not isinstance(val, int):
                errors_dic[key] += 1
        elif key == "stop_type":
            if val != "" and not re.match(r'^[SOF]$', val):
                errors_dic[key] += 1
        elif key == "a_time":
            if not re.match(r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$', str(val)):
                errors_dic[key] += 1


def print_error_result(errors_dic: dict):
    print(f"Format validation: {sum(errors_dic.values())} errors")
    for k, v in errors_dic.items():
        if k in ["stop_name", "stop_type", "a_time"]:
            print(f"{k}: {v}")


def print_bus_result(bus_dic: dict):
    print("Line names and number of stops:")
    for k, v in bus_dic.items():
        print(f"bus_id: : {k}, stops: {len(v)}")


def get_bus_info(ride_info, bus_info):
    if ride_info["bus_id"] not in bus_info:
        bus_info[ride_info["bus_id"]] = set()
        bus_info[ride_info["bus_id"]].add(ride_info["next_stop"])
    elif ride_info["next_stop"] not in bus_info[ride_info["bus_id"]]:
        bus_info[ride_info["bus_id"]].add(ride_info["next_stop"])


def get_stop_info(bus_data):
    bus_stop_info = {}
    stop_types = {"start": set(), "transfer": [], "final": set()}
    transfer_stops = {}
    for ride in bus_data:
        if ride["stop_type"] in ["F", "S"]:
            if ride["bus_id"] not in bus_stop_info:
                bus_stop_info[ride["bus_id"]] = {(ride["stop_id"], ride["stop_type"])}
                transfer_stops[ride["bus_id"]] = set()
            else:
                bus_stop_info[ride["bus_id"]].add((ride["stop_id"], ride["stop_type"]))
        if ride["bus_id"] not in bus_stop_info:
            transfer_stops[ride["bus_id"]] = set()
        transfer_stops[ride["bus_id"]].add(ride["stop_name"])
        if ride["stop_name"] not in itertools.chain(stop_types.values()):
            if ride["stop_type"] == "S":
                stop_types['start'].add(ride["stop_name"])
            elif ride["stop_type"] == "F":
                stop_types['final'].add(ride["stop_name"])
    for k, v in bus_stop_info.items():
        if len(v) != 2:
            return k, False

    # Get the common transfer stops
    for i, j in itertools.combinations(transfer_stops.values(), 2):
        k = i & j
        if k:
            k = list(k)
            stop_types['transfer'].extend(k)
    stop_types['transfer'] = set(stop_types['transfer'])
    return stop_types, True


def check_arrival_time(bus_data):
    stop_arrival_time = {}
    bus_arrival_error = {}

    for ride in bus_data:
        if ride["bus_id"] not in stop_arrival_time:
            stop_arrival_time[ride["bus_id"]] = {}
        if ride["stop_id"] not in stop_arrival_time[ride["bus_id"]]:
            stop_arrival_time[ride["bus_id"]][ride["stop_id"]] = datetime.strptime(ride["a_time"], '%H:%M')
        stop_arrival_time[ride["stop_id"]] = ride["stop_name"]
    for ride in bus_data:
        if ride["bus_id"] not in bus_arrival_error:
            if ride["stop_type"] == "F":
                continue
            if stop_arrival_time[ride["bus_id"]][ride["stop_id"]] >= stop_arrival_time[ride["bus_id"]][ride["next_stop"]]:
                bus_arrival_error[ride["bus_id"]] = stop_arrival_time[ride["next_stop"]]

    if not bus_arrival_error:
        return None, True
    else:
        return bus_arrival_error, False


def check_on_demand(bus_data):
    bus_stop_info = {}
    stop_types = {"start": set(), "transfer": [], "final": set(), "demand": set()}
    transfer_stops = {}
    for ride in bus_data:
        if ride["bus_id"] not in transfer_stops:
            transfer_stops[ride["bus_id"]] = set()
        transfer_stops[ride["bus_id"]].add(ride["stop_name"])
        if ride["stop_name"] not in itertools.chain(stop_types.values()):
            if ride["stop_type"] == "S":
                stop_types['start'].add(ride["stop_name"])
            elif ride["stop_type"] == "F":
                stop_types['final'].add(ride["stop_name"])
            elif ride["stop_type"] == "O":
                stop_types['demand'].add(ride["stop_name"])

    # Get the common transfer stops
    for i, j in itertools.combinations(transfer_stops.values(), 2):
        k = i & j
        if k:
            k = list(k)
            stop_types['transfer'].extend(k)
    stop_types['transfer'] = set(stop_types['transfer'])

    on_demand_final = set.union(stop_types['start'], stop_types['final'], stop_types['transfer'])
    on_demand_final = set.intersection(on_demand_final, stop_types['demand'])
    if on_demand_final:
        return on_demand_final, False
    else:
        return None, True


def main():
    bus_data = json.loads(input())

    # This is for on-demand stop checking
    on_demand_info, status = check_on_demand(bus_data)
    print('On demand stops test:')
    if status:
        print(f'OK')
    else:
        print(f'Wrong stop type: {sorted(on_demand_info)}')

    # This is for arrival time checking
    # arrival_info, status = check_arrival_time(bus_data)
    # print('Arrival time test:')
    # if status:
    #     print(f'OK')
    # else:
    #     for k, v in arrival_info.items():
    #         print(f'bus_id line {k}: wrong time on station {v}')

    # This is for bus stops checking
    # bus_stop_info = {}
    # bus, status = get_stop_info(bus_data, bus_stop_info)
    # if not status:
    #     print(f'There is no start or end stop for the line: {bus}.')
    # else:
    #     print(f'Start stops: {len(bus["start"])} {list(sorted(bus["start"]))}')
    #     print(f'Transfer stops: {len(bus["transfer"])} {list(sorted(bus["transfer"]))}')
    #     print(f'Finish stops: {len(bus["final"])} {list(sorted(bus["final"]))}')

    # This is for errors in data and bus line info
    # errors_dict = {"bus_id": 0, "stop_id": 0, "stop_name": 0, "next_stop": 0, "stop_type": 0, "a_time": 0}
    # bus_line_info = {}
    # for ride in bus_data:
    #     check_errors(ride, errors_dict)
    #     get_bus_info(ride, bus_line_info)
    # # print_error_result(errors_dict)
    # print_bus_result(bus_line_info)


if __name__ == "__main__":
    main()
