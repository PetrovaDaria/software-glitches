import multiprocessing

def worker(d, send_end):
    '''worker function'''
    d[1] = 1
    send_end.send([d, 1])

def join_dicts(d1, d2):
    new_d = {}
    new_d.update(d1)
    for k, v in d2.items():
        if k in new_d.keys():
            new_d[k] += v
        else:
            new_d[k] = v
    return new_d

def main():
    jobs = []
    pipe_list = []
    for i in range(5):
        recv_end, send_end = multiprocessing.Pipe(False)
        p = multiprocessing.Process(target=worker, args=({}, send_end))
        jobs.append(p)
        pipe_list.append(recv_end)
        p.start()

    for proc in jobs:
        proc.join()
    result_list = [x.recv() for x in pipe_list]
    print(result_list)
    # acc = {}
    # for i in range(len(result_list)):
    #     acc = join_dicts(acc, result_list[i])
    # print(acc)

if __name__ == '__main__':
    main()