import re
import subprocess
import sys
from argparse import ArgumentParser


class BeautifulTable(object):
    def __init__(self, headers, format_fns, total=False):
        """
        Parameters
        ----------
        headers: list
            List of headers for the table
        format_fns: list
            Formaters for the data
        total: bool
            Display the totals for the table
        """
        self.headers = headers
        self.format_fns = format_fns
        self.total = total

    @classmethod
    def _format_percent(cls, v):
        return "{:3.0f}%".format(v * 100)

    def _col_has_max(self, maxes, row_name, col):
        return maxes is not None \
               and row_name in maxes \
               and self.headers[col] in maxes[row_name] \
               and maxes[row_name][self.headers[col]] is not None

    def _format_col(self, col, quantity, max_val=None):
        fn = self.format_fns[col]
        if max_val is None:
            return [fn(quantity)]
        return [fn(quantity), fn(max_val), self._format_percent(quantity / max_val)]

    def _get_datapoint(self, data, row_name, col, maxes=None):
        return self._format_col(
            col=col, quantity=data[row_name][col],
            max_val=maxes[row_name][self.headers[col]] if self._col_has_max(maxes, row_name, col) else None
        )

    def _get_formatted_data_and_size(self, data, maxes=None):
        """Formats data and compute column widths
        Parameters
        ----------
        data: dict
            Mapping row name with row data as a list (must have an order consistent with headers)
        maxes: dict|None
            Dictionary mapping row name with data max as a dict mapping header with corresponding max value (None for
            not displaying the max). If a header is missing in the dict or mapping None, then the value for this column
            is not displayed.

        Returns
        -------
        names: list
            List of row names (sorted consistently with `rows`)
        rows: list
            Formatted data to display in all rows (sorted consistently with `names`). rows[i][k] is a list and contains
            the formatted data to display in cell (i, k) of the table. If a maximum should be displayed in this column,
            this list counts three string representing the formatted elements (value, max value, percentage). Otherwise,
            it contains 1 element.
        width_names: int
            Width of the name column (i.e. first column) of the table.
        widths: list
            Contains the widths of each column of the table.
            width[k][j]

        """
        n_columns = len(self.headers)
        widths = [None] * n_columns
        rows = []
        width_names = 0
        names = sorted(data.keys())
        for row_name in names:
            curr_row = []
            width_names = max(width_names, len(row_name))
            for k in range(n_columns):
                curr_col = self._get_datapoint(data, row_name, k, maxes=maxes)
                curr_row.append(curr_col)
                if widths[k] is None:
                    widths[k] = [len(s) for s in curr_col]
                else:
                    widths[k] = [max(w, len(c)) for w, c in zip(widths[k], curr_col)]
            rows.append(curr_row)

        if self.total:
            totals = [0] * n_columns
            total_maxes = [0] * n_columns
            for row_name in data.keys():
                for k in range(n_columns):
                    totals[k] += data[row_name][k]
                    if total_maxes[k] is None or not self._col_has_max(maxes, row_name, k):
                        total_maxes[k] = None
                        continue
                    total_maxes[k] += maxes[row_name][self.headers[k]]

            formatted = [
                self._format_col(k, t, max_val=None if maxes is None else m)
                for k, (t, m) in enumerate(zip(totals, total_maxes))
            ]
            rows.append(formatted)

            # update widths
            total_name = "total:"
            names.append(total_name)
            width_names = max(width_names, len(total_name))

            for k in range(n_columns):
                widths[k] = [max(w, len(c)) for w, c in zip(widths[k], formatted[k])]

        return names, rows, width_names, widths

    def display(self, data, maxes=None, out=sys.stdout):
        """
        Display given data in the table format
        data: dict
            Mapping row name with row data as a list (must have an order consistent with headers)
        maxes: dict|None
            Dictionary mapping row name with data max as a dict mapping header with corresponding max value (None for
            not displaying the max). If a header is missing in the dict or mapping None, then the value for this column
            is not displayed.
        out:
            output stream
        """
        names, rows, width_names, widths = self._get_formatted_data_and_size(data, maxes=maxes)
        # print headers
        header = [" " * width_names] + [h.center(sum(ws) + len(ws) - 1) for h, ws in zip(self.headers, widths)]
        print(" | ".join(header), file=out)
        for i, (name, row) in enumerate(zip(names, rows)):
            columns = [" ".join([
                c.rjust(w)
                for c, w in zip(subcols, ws)
            ]) for i, (subcols, ws) in enumerate(zip(row, widths))]
            r = [name.rjust(width_names)] + [c.rjust(len(self.headers[i])) for i, c in enumerate(columns)]
            if i == 0 or i == (len(names) - 1):
                print(" | ".join([
                    '-' * max(sum(ws) + len(ws) - 1, len(self.headers[k]) if k >= 0 else 0)
                    for k, ws in zip(range(-1, len(widths)), [[width_names]] + widths)
                ]), file=out)
            print(" | ".join(r), file=out)


class Job(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.attributes = list(kwargs.keys())

    def __repr__(self):
        return "Job({})".format(','.join(["{}={}".format(attr, getattr(self, attr)) for attr in self.attributes]))


def sq():
    return ["squeue", "-O", 'jobid:.15,partition:.15,name:.100,username:.18,state:.12,tres-per-node'
                            ':.16,numtasks:.10,minmemory:.15,timeused:.16,timelimit:.16,reasonlist:'
                            '.22,prioritylong:.22,submittime:.24,nice:.5']


def si():
    return ["sinfo", "-o", "%30N %10c %10m  %10G", "-e"]


def max_resources_per_node():
    """Extract max resources per node"""
    cmd = subprocess.run(si(), stdout=subprocess.PIPE)
    outputs = re.split("[\r\n]+", cmd.stdout.decode('utf-8').strip())[1:]
    outputs = [re.split(r'\s+', l) for l in outputs]

    node_dict = dict()
    for nodes in outputs:
        match = re.match(r'^([a-z\-]+)\[([0-9]+)-([0-9]+)\]$', nodes[0])
        data = {"gpus": int(nodes[3].split(":")[1]), "cpus": int(nodes[1]), "mem": int(nodes[2]) * 1000}
        if match is None:
            node_dict[nodes[0]] = data
        else:
            prefix = match.group(1)
            start = int(match.group(2))
            end = int(match.group(3))
            for i in range(start, end + 1):
                name = "{}{}".format(prefix, str(i).rjust(2, '0'))
                node_dict[name] = data

    return node_dict


def queued_jobs():
    """Extract queued jobs"""
    cmd = subprocess.run(sq(), stdout=subprocess.PIPE)
    outputs = re.split("[\r\n]+", cmd.stdout.decode('utf-8').strip())
    headers, jobs = outputs[0], outputs[1:]
    headers = [s.lower() for s in re.split("\s+", headers.strip())]
    jobs = [re.split("\s+", l.strip()) for l in jobs]
    return [Job(**{h: l for h, l, in zip(headers, job)}) for job in jobs]


def count_by(jobs, by, keep):
    unique_dict = dict()
    for job in jobs:
        if not keep(job):
            continue
        key = getattr(job, by)
        unique_dict[key] = unique_dict.get(key, 0) + 1
    return unique_dict


def sum_by(jobs, by, attrs, keep):
    aggr_dict = dict()
    for job in jobs:
        if not keep(job):
            continue
        key = getattr(job, by)
        by_list = aggr_dict.get(key, [0] * len(attrs))
        for i, attr in enumerate(attrs):
            by_list[i] += attr(job)
        aggr_dict[key] = by_list
    return aggr_dict


def print_dict(d):
    for k, v in d.items():
        print("-", k, ":", v)


def parse_memory(m):
    match = re.match(r"^([0-9]+)([GKMT])$", m)
    if match is None:
        raise ValueError('Invalid memory string: {}'.format(m))
    mem = int(match.group(1))
    unit = match.group(2)
    if unit == "T":
        return mem * 1000000000
    elif unit == "G":
        return mem * 1000000
    elif unit == "M":
        return mem * 1000
    elif unit == "K":
        return mem


def format_memory(m):
    c = 0
    while m > 10000:
        m //= 1000
        c += 1
    return "{}{}".format(m, ["K", "M", "G", "T"][c])


def main(argv):
    argparser = ArgumentParser()
    argparser.add_argument("-u", "--per_user", dest="per_user", action="store_true",
                           help="to display resources per user")
    argparser.add_argument("-q", "--queued", dest="queued", action="store_true",
                           help="to display requested resources in the queue (per user)")
    argparser.set_defaults(queued=False, per_user=False)
    params, _ = argparser.parse_known_args(argv)

    jobs = queued_jobs()
    is_running = lambda j: j.state == "RUNNING"
    is_queued = lambda j: not is_running(j)
    memory_attr = lambda j: parse_memory(j.min_memory)
    tasks_attr = lambda j: int(j.tasks)
    gpus_attr = lambda j: int(j.tres_per_node.split(":")[1]) if j.tres_per_node != "N/A" else 0
    count_attr = lambda j: 1

    print()
    print("Resources per node")
    table = BeautifulTable(
        headers=["jobs", "mem", "cpus", "gpus"],
        format_fns=[str, format_memory, str, str],
        total=True
    )
    table.display(
        data=sum_by(jobs, "nodelist(reason)", [count_attr, memory_attr, tasks_attr, gpus_attr], is_running),
        maxes=max_resources_per_node()
    )
    print()

    if params.per_user:
        print("Resources per user (running jobs)")
        table = BeautifulTable(
            headers=["jobs", "mem", "cpus", "gpus"],
            format_fns=[str, format_memory, str, str],
            total=True
        )
        table.display(data=sum_by(jobs, "user", [count_attr, memory_attr, tasks_attr, gpus_attr], is_running))
        print()

    if params.queued:
        print("Resources per user (queued jobs)")
        table = BeautifulTable(
            headers=["jobs", "mem", "cpus", "gpus"],
            format_fns=[str, format_memory, str, str],
            total=True
        )
        table.display(data=sum_by(jobs, "user", [count_attr, memory_attr, tasks_attr, gpus_attr], is_queued))
        print()


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
