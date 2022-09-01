import multiprocessing

result = []

def worker(arg):
    global result

    if arg == 12:
        result.append(1)
    else:
        result.append(0)

if __name__ == "__main__":
    
    arguments = [1, 2, 3]

    p = multiprocessing.Process(
        target=worker,
        args=arguments
    )
    
    p.start()
    p.join()
    print(result)












