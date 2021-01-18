import copy
from datetime import date, datetime, timedelta
from typing import Optional, Tuple

from backend.cruds import activity as activity_crud
from backend.cruds import user as user_crud
from backend.schemas import activities as schemas
from sqlalchemy.orm import Session


def expand_activities_in_period(_activities, start_time: datetime, end_time: datetime):
    activities = []

    for activity in _activities:
        if activity_crud.is_periodic(activity):

            time_window = (activity.end_time - activity.start_time) % timedelta(days=1)

            time = activity.start_time
            while time < activity.end_time:
                a_start_time = time
                a_end_time = a_start_time + time_window

                if a_start_time >= end_time:
                    break

                if a_end_time > start_time:
                    _activity = copy.deepcopy(activity)

                    _activity.start_time = a_start_time
                    _activity.end_time = a_end_time

                    activities.append(_activity)
                time += activity.period
        else:
            activities.append(activity)

    return activities


def activity_to_plan_element(activity):
    start = int(activity.start_time.timestamp())
    end = int(activity.end_time.timestamp())
    len = int(activity.duration.total_seconds())
    cost = activity.stress_points

    return schemas.Plan(id=activity.id, start=start, end=end, len=len, cost=cost)


def cut_out_time(task: schemas.Plan, start_time: int, end_time: int) -> None:
    if task.start < start_time:
        task.start = min(start_time, task.end - task.len)

    if task.end > end_time:
        if task.end - task.len > end_time:  # task can be started later than today
            task.end = (
                end_time + task.len
            )  # if we can do this task then we need to start today
            task.important = False  # but it's not important


def plan_trace(plan):
    trace = []
    for id in plan:
        start = plan[id].start
        end = plan[id].end

        trace.append((id, start, True))
        trace.append((id, end, False))

    trace.sort(key=lambda point: (point[1], point[2]))

    return trace


def solve_collission(
    plans: dict, plan_name: str, collission: Tuple[int, int, int]
) -> bool:
    plan = plans[plan_name]

    task_a = plan[collission[0]]
    task_b = plan[collission[1]]

    if collission[2]:  # nesting
        if (
            task_a.end - task_a.start < task_b.end - task_b.start
        ):  # task A always bigger
            task_a, task_b = task_b, task_a

            solvable = False

            # try to put A before B
            if task_a.start + task_a.len <= task_b.end - task_b.len:
                solvable = True
                task_a.end = task_b.end - task_b.len
                task_b.start = max(task_a.start + task_a.len, task_b.start)

            # try to put B before A
            if task_b.start + task_b.len <= task_a.end - task_a.len:
                if solvable:  # if already solved
                    plans[
                        plan_name + f"_{task_a.id}:{task_b.id}"
                    ] = _plan = copy.deepcopy(plan)
                    _task_a = _plan[task_a.id]
                    _task_b = _plan[task_b.id]

                    _task_a.start = _task_b.start + _task_b.len
                    _task_b.end = min(_task_a.end - _task_a.len, _task_b.end)
                else:
                    solvable = True
                    task_a.start = task_b.start + task_b.len
                    task_b.end = min(task_a.end - task_a.len, task_b.end)

            return solvable

    else:  # intersection
        if task_b.start < task_a.start:  # task A always started earlier
            task_a, task_b = task_b, task_a

        border_mark = max(task_a.start + task_a.len, task_b.start)

        if task_b.end - border_mark < task_b.len:
            return False

        task_a.end = border_mark
        task_b.start = border_mark

    return True


def find_collissions(plan: dict) -> Optional[Tuple[int, int, int]]:
    """
    return collission in format
        (task_id1, task_id2, type)
        type:
            0 - intersection
            1 - nesting

    or None if collision not found
    """
    trace = plan_trace(plan)

    queue = []

    for point in trace:
        point_id = point[0]

        if point_id in queue:  # point is ending
            if len(queue) == 1:  # without collisions
                queue = []
            else:
                position = queue.index(point_id)

                if position > 0:
                    return (point_id, queue[position - 1], 1)  # collission - nesting

                return (point_id, queue[position + 1], 0)  # collission - intersection
        else:  # point is starting
            queue.append(point_id)

    return None


def calculate_stats(plan) -> Tuple[int, int]:
    """
    Return (max, amt)
    max - max stress level
    amt - amount of tasks
    """
    sorted_plan = list(plan.values())
    sorted_plan.sort(key=lambda task: task.start)

    max = 0
    current = 0
    amount_of_tasks = 0

    for task in sorted_plan:
        current += task.cost
        amount_of_tasks += 1

        if current > max:
            max = current

    return (max, amount_of_tasks)


def restress_plan(plans: dict, plan_name: str, max_stress: int) -> None:
    plan = plans[plan_name]

    sorted_plan = list(plan.values())
    sorted_plan.sort(key=lambda task: task.start)

    trace = []

    current = 0
    calc_max = 0
    unimportant_tasks = []

    for task in sorted_plan:
        current += task.cost

        if current > calc_max:
            calc_max = current

        trace.append((task.id, task.cost, current))

        if not task.important and task.cost > 0:
            unimportant_tasks.append(task.id)

    if calc_max < max_stress:
        return True

    # TODO: make function for variants enumeration
    for unimp_task in unimportant_tasks:
        current = 0
        for task in trace:
            if task.id == unimp_task:
                continue

            current += task.cost

            if current > max_stress:
                break
        else:
            del plan[unimp_task]
            return True

    return False


def make_plan(db: Session, user_id: int, plan_date: date):
    start_time = datetime.combine(plan_date, datetime.min.time())
    end_time = datetime.combine(plan_date + timedelta(days=1), datetime.min.time())

    activities = activity_crud.list(db, user_id, start_time, end_time)

    activities = expand_activities_in_period(activities, start_time, end_time)

    plan = {activity.id: activity_to_plan_element(activity) for activity in activities}

    # plan.sort(key=lambda task: task.end)

    # convert_time
    start_time = int(start_time.timestamp())
    end_time = int(end_time.timestamp())

    for id in plan:
        cut_out_time(plan[id], start_time, end_time)

    test_plans = {"": plan}
    plans = {}

    while test_plans:
        plan_name = next(iter(test_plans))
        plan = test_plans[plan_name]

        while collision := find_collissions(plan):
            if not solve_collission(test_plans, plan_name, collision):
                collision_a = collision[0]
                collision_b = collision[1]

                if not plan[collision_a].important:
                    del plan[collision_a]
                    continue

                if not plan[collision_b].important:
                    del plan[collision_b]
                    continue

                del test_plans[plan_name]

        # if plan without collisions save it
        plans[plan_name] = test_plans[plan_name]
        del test_plans[plan_name]

    if not plans:
        raise ValueError("Schedule have unresolvable collisions")

    max_stress = user_crud.get(db, user_id).max_stress_lvl

    # calculate stress
    stats = {}
    max_tasks = 0
    best_plan = None

    for plan_name in plans:
        stats[plan_name] = calculate_stats(plans[plan_name])
        if stats[plan_name][0] >= max_stress:
            if not restress_plan(plans, plan_name, max_stress):
                del plans[plan_name]
        elif stats[plan_name][1] > max_tasks:
            max_tasks = stats[plan_name][1]
            best_plan = plan_name

    if best_plan is None:
        raise ValueError("Schedule too stressed")

    return plans[best_plan]
