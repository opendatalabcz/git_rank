import ReactApexChart from "react-apexcharts"
import { ICommitStatistics } from "../../types"

export default function LintScoreDateChart({ commits }: {commits: ICommitStatistics[]}) {

    const add_lint = commits.map(commit => ({x: commit.commit_date, y: commit.average_add_lint_score}))
    const change_lint = commits.map(commit => ({x: commit.commit_date, y: commit.average_change_lint_score}))

    const series = [
        {name: "ADDED", data: add_lint},
        {name: "CHANGED", data: change_lint}
    ]
    const options = {
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
            size: 10,
          },
          title: {
            text: 'Average lint scores in time',
          },
        }

    return (
      <div>
        <div className="chart">
            <ReactApexChart options={options} series={series} type="line" width={700} height={500}/>
          </div>
        <div id="html-dist"></div>
      </div>
    );
}
