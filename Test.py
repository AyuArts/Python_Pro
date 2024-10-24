import asyncio


async def my_sum(x, y):
    await asyncio.sleep(1)
    print(f"{x} / {y}")
    return x / y


async def gather_main():
    result = await asyncio.gather(
        my_sum(x=50, y=10),
        my_sum(x=60, y=10),
        my_sum(x=70, y=10),
        my_sum(x=80, y=10),
        my_sum(x=90, y=10),
    )
    print(f"Результат: {str(result)}")


async def print_numbers():
    for i in range(5):
        print(f"Number: {i}")
        await asyncio.sleep(1)


async def print_letters():
    for letter in 'ДЯКУЮ':
        print(f"Letter: {letter}")
        await asyncio.sleep(1)


async def main():
    for _ in range(1):
        print(f"Iteration {_ + 1}")
        await gather_main()
        print("деление завершено\n")
        await asyncio.gather(print_numbers(), print_letters())
        print(f"End of iteration {_ + 1}\n")


event_loop = asyncio.get_event_loop()

task_list = [
    event_loop.create_task(main())
]

tasks = asyncio.wait(task_list)
event_loop.run_until_complete(tasks)

event_loop.close()
