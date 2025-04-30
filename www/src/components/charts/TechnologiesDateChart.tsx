import ReactApexChart from "react-apexcharts"
import { ICommitStatistics } from "../../types"
import { ApexOptions } from "apexcharts";

export default function CommitsDateChart({ commits }: {commits: ICommitStatistics[]}) {

    const series = Array.from(prepareData(commits).entries()).map(([key, value]) => ({name: key, data: aggregateData(value)}))
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
            size: 10,
          },
          title: {
            text: 'Files changed in time',
          },
        }

    return (
      <div className="chart">
        <div>
            <ReactApexChart options={options} series={series} type="scatter" width={"100%"} height={"auto"}/>
          </div>
        <div id="html-dist"></div>
      </div>
    );
}

function prepareData(commits: ICommitStatistics[]) {
    const technologyGroup: Map<string, [number, number][]> = new Map()
    
    commits.forEach(commit => {
        commit.files.forEach(file => {
            if (technologyGroup.has(file.technology)) {
                technologyGroup.get(file.technology)!.push([Date.parse(commit.commit_date), 1])
            } else {
                technologyGroup.set(file.technology, [[Date.parse(commit.commit_date), 1]])
            }
        })
    })

    return technologyGroup
}

function aggregateData (data: [number, number][]): [number, number][] {
    const map = new Map<number, number>()
    
    data.forEach(([x, y]) => {
      map.set(x, (map.get(x) || 0) + y);
    });
   
    return Array.from(map.entries());
}