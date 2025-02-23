import ReactApexChart from "react-apexcharts"
import {ITechnologyStatistics } from "../../types"

export default function TechnologiesPieChart({ technologies }: {technologies: ITechnologyStatistics[]}) {
          
    const series = technologies.map(technology => technology.total_changes)
    const options = {
      chart: {
        type: 'donut',
      },
      labels: technologies.map(technology => technology.technology),
      title: {
        text: 'Technology distribution'
      },
      responsive: [{
        breakpoint: 480,
        options: {
          legend: {
            position: 'bottom'
          },
        }
      }]
    }

    return (
      <div>
        <div className="chart">
            <ReactApexChart options={options} series={series} type="donut" height={500} width={500}/>
          </div>
        <div id="html-dist"></div>
      </div>
    );
  }