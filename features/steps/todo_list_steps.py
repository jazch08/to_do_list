from behave import given, when, then
from todo_list import TodoListManager

todo_manager = TodoListManager()


@given("the To-Do list is empty")
def step_todo_list_is_empty(context):
    todo_manager.clear_tasks()


@when('the user adds a task "{task}"')
def step_user_adds_task(context, task):
    todo_manager.add_task(task)


@then('the to-do list should contain "{task}"')
def step_todo_list_should_contain(context, task):
    assert task in todo_manager.list_task()


@given("the to-do list contains tasks")
def step_todo_list_contains_tasks(context):
    todo_manager.clear_tasks()
    for row in context.table:
        todo_manager.add_task(row["Task"])


@given("the to-do list contains tasks with various statuses")
def step_todo_list_contains_tasks_with_various_statuses(context):
    todo_manager.clear_tasks()
    assert context.table is not None, "No task table found in the scenario."
    for row in context.table:
        todo_manager.add_task(row["Task"])
        if row["Status"] == "Completed":
            todo_manager.mark_as_completed(row["Task"])


@when("the user lists all tasks")
def step_user_lists_all_tasks(context):
    context.listed_tasks = todo_manager.list_task()


@then("the output should contain")
def step_output_should_contain(context):
    expected_output = " ".join(context.text.strip().split())  # Normaliza los espacios
    actual_output = " ".join(
        ("Tasks:\n" + "\n".join(f"- {task}" for task in todo_manager.list_task()))
        .strip()
        .split()
    )
    assert (
        expected_output == actual_output
    ), f"Expected:\n{expected_output}\nBut got:\n{actual_output}"


@when('the user marks task "{task}" as completed')
def step_user_marks_task_as_completed(context, task):
    todo_manager.mark_as_completed(task)


@then('the to-do list should show task "{task}" as')
def step_todo_list_should_show_task_as(context, task):
    tasks = todo_manager.task
    task_status = next((t["status"] for t in tasks if t["Title"] == task), None)
    assert (
        task_status == "Completed"
    ), f"Expected task '{task}' to be 'Completed', but was '{task_status}'"


@when("the user clears the to-do list")
def step_user_clears_todo_list(context):
    todo_manager.clear_tasks()


@then("the to-do list should be empty")
def step_todo_list_should_be_empty(context):
    assert len(todo_manager.task) == 0


@when('the user edits task "{old_task}" to "{new_task}" with status "{status}"')
def step_user_edits_task(context, old_task, new_task, status):
    todo_manager.edit_task(old_task, new_task, status)


@then('the to-do list should display task "{task}" with the updated status')
def step_todo_list_should_display_updated_task(context, task):
    tasks = todo_manager.task
    updated_task = next((t for t in tasks if t["Title"] == task), None)
    assert updated_task is not None, f"Task '{task}' was not found"
    assert (
        updated_task["status"] == "Completed"
    ), f"Expected task '{task}' to be 'Completed', but was '{updated_task['status']}'"


@when('the user filters tasks by status "{status}"')
def step_user_filters_tasks_by_status(context, status):
    context.filtered_tasks = todo_manager.filter_by_status(status)


@then("the output should contain only pending tasks")
def step_output_should_contain_only_pending_tasks(context):
    # Verifica si la tabla existe
    if context.table is None:
        raise AssertionError("No task table found in the scenario.")

    expected_tasks = [
        row["Task"] for row in context.table if row["Status"] == "Pending"
    ]
    actual_tasks = todo_manager.filter_by_status("Pending")

    # Verificación de las tareas pendientes
    assert set(expected_tasks) == set(
        actual_tasks
    ), f"Expected: {expected_tasks}, but got: {actual_tasks}"
