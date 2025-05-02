import ReactApexChart from "react-apexcharts"
import {ITechnologyStatistics } from "../../types"
import { ApexOptions } from "apexcharts"

export default function TechnologiesBarChart({ technologies }: {technologies: ITechnologyStatistics[]}) {
          
    const series = [{data: technologies.map(technology => technology.total_changes)}]
    const options: ApexOptions = {
      chart: {
        type: 'bar',
      },
      plotOptions: {
        bar: {
          distributed: true,
        }
      },
      xaxis: {
        categories: technologies.map(technology => technology.technology),
      },
      labels: technologies.map(technology => technology.technology),
      legend: {
        markers: {
          shape: 'circle'
        },
      },
      tooltip: {
        enabled: false
      },
    }

    return (
      <div className="chart">
        <div>
            <b>Total file changes by technology</b>
            <ReactApexChart options={options} series={series} type="bar" height={"auto"} width={"100%"}/>
        </div>
        <div id="html-dist"></div>
      </div>
    );
  }