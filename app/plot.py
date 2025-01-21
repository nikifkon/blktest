import subprocess


def plot(results, out_file):
    plot_script = ";".join(
        [
            "set xlabel 'iodepth'",
            "set ylabel 'Avg lat, us'",
            "set terminal png",
            "set output '{}'".format(out_file.name),
            "set style data histogram",
            "set style fill solid 0.5 border -1",
            "plot "
            + ", ".join(
                ["'-' using 2:xtic(1) title '{}'".format(test) for test in results]
            ),
        ]
    )
    stdin = "\n".join(
        [
            "\n".join(
                ["{} {}".format(iodepth, clat_ns // 1_000) for iodepth, clat_ns in data]
            )
            + "\ne"
            for data in results.values()
        ]
    )
    subprocess.run(["gnuplot", "-e", plot_script], input=stdin.encode() * 2)
