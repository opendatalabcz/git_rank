import ReactApexChart from "react-apexcharts"
import { ICommitStatistics } from "../../types"
import { ApexOptions } from "apexcharts"

export default function LintScoreDateChart({ commits }: {commits: ICommitStatistics[]}) {

    const add_lint = commits.filter(commit => commit.average_add_lint_score != null).map(
      commit => (
        {
          x: commit.commit_date,
          y: commit.average_add_lint_score?.toFixed(2)
        })).sort((a, b) => {
          const dateA = new Date(a.x).getTime();
          const dateB = new Date(b.x).getTime();
          return dateA - dateB;
        })
    const change_lint = commits.filter(commit => commit.average_change_lint_score != null).map(
      commit => (
        {
          x: commit.commit_date,
          y: commit.average_change_lint_score?.toFixed(2)
        })).sort((a, b) => {
          const dateA = new Date(a.x).getTime();
          const dateB = new Date(b.x).getTime();
          return dateA - dateB;
        })

    const series = [
        {name: "ADDED", data: add_lint},
        {name: "CHANGED", data: change_lint}
    ]
    const options: ApexOptions = {
          chart: {
            zoom: {
              enabled: true,
              type: 'xy',
            }
          },
          xaxis: {
            type: 'datetime',
            labels: {
              datetimeUTC: false,
            }
          },
          markers: {
            size: 5,
          },
          stroke: {
            curve: 'smooth',
          },
        }

    return (
      <div className="chart">
        <div>
            <b>Average lint scores in time</b>
            <ReactApexChart options={options} series={series} type="line" width={"100%"} height={"auto"}/>
        </div>
        <div id="html-dist"></div>
      </div>
    );
}
