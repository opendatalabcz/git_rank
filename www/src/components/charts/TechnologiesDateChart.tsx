import ReactApexChart from "react-apexcharts"
import { ICommitStatistics } from "../../types"

export default function CommitsDateChart({ commits }: {commits: ICommitStatistics[]}) {

    const series = Array.from(prepareData(commits).entries()).map(([key, value]) => ({name: key, data: aggregateData(value)}))
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
            text: 'Technology changes in time',
          },
        }

    return (
      <div>
        <div className="chart">
            <ReactApexChart options={options} series={series} type="scatter" width={700} height={500}/>
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